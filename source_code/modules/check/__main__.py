import argparse
import csv
import logging
import re
import shutil
import time
from pathlib import Path
from typing import Any

import tomli

from ..utils import (
    INPUT_DIR,
    CONTEXT_DEFINITIONS_FILE_NAME,
    CTreeNode,
    get_data_size,
    log_info,
    parse_constraint,
    set_log_file_handler,
)
from . import CHECK_OUTPUT_DIR, INCS_FILE_NAME, INDENT, LOGGER_NAME, CheckResult
from .check import check

PROJECT_ROOT = INPUT_DIR.parent


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", "-s", required=True, type=str, help="Scenario name")
    parser.add_argument(
        "--constraint-dir",
        required=True,
        type=str,
        help="Constraint directory that directly contains xml/ and py/",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--perturbation-prob",
        type=str,
        help="Relative perturbation-probability directory under inputs/{scenario}/data, e.g. 5000_pp_0.1",
    )
    group.add_argument(
        "--perturbation-file",
        type=str,
        help="Relative path to a perturbed.csv file under inputs/{scenario}/data, e.g. 5000_pp_0.1/0b6a00b5/perturbed.csv",
    )
    return parser.parse_args()


def _to_project_relative(path: Path) -> str:
    resolved_path = path.resolve()
    try:
        return str(resolved_path.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(path)


def _get_constraint_and_bfunc_files(constraint_dir: Path):
    xml_dir = constraint_dir / "xml"
    py_dir = constraint_dir / "py"
    if not xml_dir.exists() or not py_dir.exists():
        raise FileNotFoundError(f"Constraint dir {constraint_dir} must contain xml/ and py/")

    xml_files = sorted(xml_dir.glob("*.xml"))
    py_files = sorted(py_dir.glob("*.py"))
    if not xml_files:
        raise FileNotFoundError(f"No XML files found in {xml_dir}")
    if not py_files:
        raise FileNotFoundError(f"No Python files found in {py_dir}")

    xml_pattern = re.compile(r"constraint_(\d+)\.xml")
    py_pattern = re.compile(r"bfuncs_(\d+)\.py")

    invalid_xml = [path.name for path in xml_files if not xml_pattern.fullmatch(path.name)]
    invalid_py = [path.name for path in py_files if not py_pattern.fullmatch(path.name)]
    if invalid_xml or invalid_py:
        error_lines = ["Constraint files do not follow the required naming format."]
        if invalid_xml:
            error_lines.append(f"Invalid XML files: {invalid_xml}")
        if invalid_py:
            error_lines.append(f"Invalid Python files: {invalid_py}")
        error_lines.append("Expected XML format: constraint_<id>.xml")
        error_lines.append("Expected Python format: bfuncs_<id>.py")
        raise ValueError("\n".join(error_lines))

    xml_mapping = {int(xml_pattern.fullmatch(path.name).group(1)): path for path in xml_files}
    py_mapping = {int(py_pattern.fullmatch(path.name).group(1)): path for path in py_files}

    xml_ids = set(xml_mapping.keys())
    py_ids = set(py_mapping.keys())
    if xml_ids != py_ids:
        missing_xml = sorted(py_ids - xml_ids)
        missing_py = sorted(xml_ids - py_ids)

        error_lines = ["XML files and Python files do not match one-to-one."]
        if missing_xml:
            error_lines.append(
                f"Missing XML files: {[f'constraint_{constraint_id}.xml' for constraint_id in missing_xml]}"
            )
        if missing_py:
            error_lines.append(
                f"Missing Python files: {[f'bfuncs_{constraint_id}.py' for constraint_id in missing_py]}"
            )
        raise ValueError("\n".join(error_lines))

    return [
        (constraint_id, xml_mapping[constraint_id], py_mapping[constraint_id])
        for constraint_id in sorted(xml_ids)
    ]


def _load_field_type_map(config_file_path: Path) -> dict[str, Any]:
    type_map = {}

    if not config_file_path.exists() or not config_file_path.is_file():
        raise FileNotFoundError(f"Dataset file {config_file_path} not found")

    with open(config_file_path, "rb") as f:
        try:
            fields = tomli.load(f)["context_definitions"]["fields"]
            for field_name, field_info in fields.items():
                field_type = field_info.get("type")
                if field_type == "int":
                    type_map[field_name] = int
                elif field_type == "float":
                    type_map[field_name] = float
                elif field_type == "str":
                    type_map[field_name] = str
                else:
                    raise ValueError(f"Unsupported field type: {field_type}")
        except (KeyError, ValueError) as e:
            raise ValueError(f"Load field type map error: {str(e)}")

    return type_map


def _get_data_files(scenario: str, perturbation_prob: str | None, perturbation_file: str | None) -> tuple[Path, list[Path]]:
    data_root = INPUT_DIR / scenario / "data"
    if not data_root.exists():
        raise FileNotFoundError(f"Data root {data_root} not found")

    if perturbation_prob is not None:
        prob_dir = data_root / perturbation_prob
        if not prob_dir.exists() or not prob_dir.is_dir():
            raise FileNotFoundError(f"Perturbation-probability directory {prob_dir} not found")

        data_files = sorted(prob_dir.rglob("perturbed.csv"))
        if not data_files:
            raise FileNotFoundError(f"No perturbed.csv files found under {prob_dir}")
        return data_root, data_files

    assert perturbation_file is not None
    data_file_path = data_root / perturbation_file
    if not data_file_path.exists() or not data_file_path.is_file():
        raise FileNotFoundError(f"Data file {data_file_path} not found")
    if data_file_path.name != "perturbed.csv":
        raise ValueError(
            "Only perturbed.csv is supported. Clean data files such as 5000.csv "
            "are not supported."
        )
    return data_root, [data_file_path]


def _set_output_dir(constraint_dir: Path, data_root: Path, data_file_path: Path) -> Path:
    rel_path = data_file_path.relative_to(data_root)
    if rel_path.name != "perturbed.csv":
        raise ValueError(
            f"Only perturbed.csv is supported, but got {rel_path.name} from {data_file_path}"
        )
    if len(rel_path.parts) < 3:
        raise ValueError(
            "Expected data file layout inputs/{scenario}/data/{perturbation_prob}/{run_id}/perturbed.csv"
        )

    prob_path = Path(*rel_path.parts[:-2])
    run_id = rel_path.parts[-2]
    data_flag = prob_path / f"{run_id}_perturbed"

    constraint_group = constraint_dir.parent.name
    output_dir = CHECK_OUTPUT_DIR / constraint_group / constraint_dir.name / data_flag
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=False)
    return output_dir


def _set_check_data(ctree_root: CTreeNode, check_ctx2data: dict[str, Path]) -> dict[str, int]:
    check_data_num_dict = {}

    queue = [ctree_root]
    while queue:
        node = queue.pop(0)
        if node[0] in ("forall", "exists"):
            ctx = node[2]["in"]
            check_data_num = get_data_size(check_ctx2data[ctx])
            check_data_num_dict[ctx] = check_data_num
            node[2]["check_data_info"] = (check_ctx2data[ctx], check_data_num)

        if node[3] is not None:
            for child in node[3]:
                queue.append(child)

    return check_data_num_dict


def _dump_check_result(constraint_id: int, check_result: CheckResult, output_dir: Path) -> int:
    incs_file_path = output_dir / INCS_FILE_NAME
    if not incs_file_path.exists():
        incs_file_path.touch()

    if check_result is None:
        return -1

    truth, links = check_result
    inc_num = 0
    if not truth:
        with open(incs_file_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for link in links:
                inc_num += 1
                link_str = "{" + ", ".join([f"({var},{row_id})" for var, row_id in link]) + "}"
                writer.writerow([f"constraint_{constraint_id}", link_str])
    return inc_num


def _generate_summary_report(
    output_dir: Path,
    constraint_dir: Path,
    constraint_files: list[tuple[int, Path, Path]],
    data_file_path: Path,
    check_time: float,
):
    incs_file_path = output_dir / INCS_FILE_NAME
    if not incs_file_path.exists():
        incs_file_path.touch()

    summary_file = output_dir / "summary.txt"

    constraint_stats = {}
    total_incs = 0
    if incs_file_path.exists() and incs_file_path.stat().st_size > 0:
        with open(incs_file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2:
                    constraint_name = row[0]
                    if constraint_name not in constraint_stats:
                        constraint_stats[constraint_name] = 0
                    constraint_stats[constraint_name] += 1
                    total_incs += 1

    with open(summary_file, "w", encoding="utf-8") as f:
        f.write("=== Check Results Summary ===\n\n")
        f.write(f"Data File: {_to_project_relative(data_file_path)}\n")
        f.write(f"Constraint Directory: {_to_project_relative(constraint_dir)}\n")
        f.write(f"Total Constraints Checked: {len(constraint_files)}\n")
        f.write(f"Total Inconsistencies Found: {total_incs}\n")
        f.write(f"Check Time: {check_time:.2f} seconds\n\n")

        if constraint_stats:
            f.write("=== Inconsistencies by Constraint ===\n")
            for constraint_name, count in sorted(constraint_stats.items()):
                f.write(f"{constraint_name}: {count}\n")
        else:
            f.write("No inconsistencies found - all constraints satisfied!\n")

    return total_incs


def _run_single_check(
    scenario: str,
    constraint_dir: Path,
    constraint_files: list[tuple[int, Path, Path]],
    field_type_map: dict[str, Any],
    data_root: Path,
    data_file_path: Path,
):
    output_dir = _set_output_dir(constraint_dir, data_root, data_file_path)
    set_log_file_handler(LOGGER_NAME, output_dir / "check.log", logging.DEBUG)
    relative_constraint_dir = _to_project_relative(constraint_dir)
    relative_data_file_path = _to_project_relative(data_file_path)
    relative_output_dir = _to_project_relative(output_dir)

    log_info(
        LOGGER_NAME,
        f"{relative_constraint_dir} check starts",
        center=True,
        symbol="=",
    )

    check_ctx2data = {"ctx1": data_file_path}
    relative_check_ctx2data = {
        ctx: Path(_to_project_relative(path))
        for ctx, path in check_ctx2data.items()
    }
    log_info(LOGGER_NAME, f"- data_file_path: {relative_data_file_path}")
    log_info(LOGGER_NAME, f"- output_dir: {relative_output_dir}")
    log_info(LOGGER_NAME, f"- check_ctx2data: {relative_check_ctx2data}")

    begin_time = time.time()
    for constraint_id, constraint_file, bfunc_file in constraint_files:
        log_info(LOGGER_NAME, f"Check constraint_{constraint_id}:")

        start_time = time.time()
        ctree_root = parse_constraint(constraint_file, bfunc_file, True)
        log_info(
            LOGGER_NAME,
            f'{" " * INDENT}- parsed constraint in {time.time() - start_time} seconds',
        )

        start_time = time.time()
        check_data_num_dict = _set_check_data(ctree_root, check_ctx2data)
        log_info(
            LOGGER_NAME,
            f'{" " * INDENT}- set check data in {time.time() - start_time} seconds',
        )
        log_info(
            LOGGER_NAME,
            f'{" " * (2 * INDENT)}- check data num info: {check_data_num_dict}',
        )

        start_time = time.time()
        try:
            check_result = check(ctree_root, bfunc_file, field_type_map)
        except Exception:
            check_result = None
        log_info(
            LOGGER_NAME,
            f'{" " * INDENT}- checked constraint in {time.time() - start_time} seconds',
        )
        inc_num = _dump_check_result(constraint_id, check_result, output_dir)
        log_info(LOGGER_NAME, f'{" " * (2 * INDENT)}- inc num: {inc_num}')

    check_time = time.time() - begin_time
    log_info(LOGGER_NAME, f"Checked {len(constraint_files)} constraints in {check_time:.2f} seconds")

    total_incs = _generate_summary_report(
        output_dir,
        constraint_dir,
        constraint_files,
        data_file_path,
        check_time,
    )
    log_info(LOGGER_NAME, f"Total inconsistencies found: {total_incs}")
    log_info(LOGGER_NAME, f"Results saved to: {relative_output_dir}")
    log_info(
        LOGGER_NAME,
        f"{relative_constraint_dir} check completes",
        center=True,
        symbol="=",
    )


def run(args):
    constraint_dir = Path(args.constraint_dir)
    constraint_files = _get_constraint_and_bfunc_files(constraint_dir)
    field_type_map = _load_field_type_map(INPUT_DIR / args.scenario / CONTEXT_DEFINITIONS_FILE_NAME)
    data_root, data_files = _get_data_files(args.scenario, args.perturbation_prob, args.perturbation_file)

    for data_file_path in data_files:
        _run_single_check(
            scenario=args.scenario,
            constraint_dir=constraint_dir,
            constraint_files=constraint_files,
            field_type_map=field_type_map,
            data_root=data_root,
            data_file_path=data_file_path,
        )


if __name__ == "__main__":
    args = parse_args()
    run(args)
