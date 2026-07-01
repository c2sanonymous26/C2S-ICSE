from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parent.parent.parent.parent
INSTANTIATION_BASE = REPO_ROOT / "outputs" / "instantiation"
CONSTRAINTS_BASE = REPO_ROOT / "constraints"
METHOD_DIR_NAME = "C2S"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract constraints from a single instantiation directory."
    )
    parser.add_argument("--scenario", "-s", required=True, help="Scenario name, e.g. taxi")
    parser.add_argument(
        "--run-dir",
        "-r",
        required=True,
        help="Instantiation directory name or path",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        required=True,
        help="Output directory name under constraints/, e.g. taxi_1",
    )
    parser.add_argument(
        "--renumber",
        action="store_true",
        help=(
            "Assign extracted constraints consecutive ids starting from 1. "
            "By default, output ids preserve source template ids to match release constraints."
        ),
    )
    return parser.parse_args()


def resolve_target_dir(scenario: str, dir_arg: str) -> Path:
    raw = Path(dir_arg)
    if raw.exists():
        return raw.resolve()

    candidate = (INSTANTIATION_BASE / dir_arg).resolve()
    if candidate.exists():
        return candidate

    candidate = (INSTANTIATION_BASE / scenario / dir_arg).resolve()
    if candidate.exists():
        return candidate

    raise FileNotFoundError(f"Target instantiation directory does not exist: {dir_arg}")


def extract_template_index(template_dir: Path) -> int:
    match = re.search(r"template_(\d+)", template_dir.name)
    if not match:
        raise ValueError(f"Invalid template directory name: {template_dir.name}")
    return int(match.group(1))


def iter_template_dirs(target_dir: Path) -> list[Path]:
    dirs: list[Path] = []
    for mode_dir in sorted(
        item
        for item in target_dir.iterdir()
        if item.is_dir() and not item.name.startswith(".") and not item.name.startswith("_")
    ):
        for template_dir in sorted(
            (item for item in mode_dir.iterdir() if item.is_dir() and item.name.startswith("template_")),
            key=extract_template_index,
        ):
            dirs.append(template_dir)
    return sorted(dirs, key=extract_template_index)


def extract_config_from_dir_name(dir_name: str) -> str | None:
    suffix = dir_name.rsplit("_", 1)[-1]
    if re.fullmatch(r"[01]{4}", suffix):
        return suffix
    return None


def resolve_method_dir_name(source_dir: Path, output_dir_name: str) -> tuple[str, str | None]:
    config = extract_config_from_dir_name(source_dir.name)
    if config is None:
        return METHOD_DIR_NAME, None

    if config == "1111" and not output_dir_name.startswith("taxi_RQ3_"):
        return METHOD_DIR_NAME, config
    return f"{METHOD_DIR_NAME}_{config}", config


def get_relative_path(path: Path, base: Path) -> str:
    return str(path.relative_to(base))


def check_template_instantiation(template_dir: Path) -> tuple[bool, int]:
    inst_dir = template_dir / "instantiations"
    if not inst_dir.exists():
        return False, 0
    xml_files = list(inst_dir.glob("constraint_i*.xml"))
    return len(xml_files) > 0, len(xml_files)


def extract_constraint_status(log_file: Path) -> str:
    content = log_file.read_text(encoding="utf-8")

    is_solving = "Solving process starts" in content
    is_validating = "Validating process starts" in content
    if is_solving == is_validating:
        raise ValueError(f"Invalid instantiation log: {log_file}")

    if is_solving:
        if re.search(r"Solving process timeout in\s+([\d\.e\-\+]+)\s+seconds", content):
            return "solve_timeout"
        valid_models_match = re.search(r"has\s+(\d+)\s+valid models", content)
        if valid_models_match is None:
            raise ValueError(f"Missing valid model summary in log: {log_file}")
        return "solve_no_solution" if int(valid_models_match.group(1)) == 0 else "solve_success"

    if re.search(r"Validating process timeout in\s+([\d\.e\-\+]+)\s+seconds", content):
        return "validate_timeout"
    if re.search(r"is invalid", content):
        return "validate_invalid"
    if re.search(r"is valid", content):
        return "validate_success"
    raise ValueError(f"Missing validation summary in log: {log_file}")


def extract_time_from_log(log_file: Path) -> tuple[float, dict[str, Any]]:
    content = log_file.read_text(encoding="utf-8")

    total_time = 0.0
    details: dict[str, Any] = {
        "preparation_time": 0.0,
        "computing_basic_ranges_time": 0.0,
        "solving_details": None,
        "validating_details": None,
    }

    prep_section_match = re.search(
        r"\*+\s*Preparation starts\s*\*+(.*?)\*+\s*Preparation completes\s*\*+",
        content,
        re.DOTALL,
    )
    if prep_section_match is None:
        raise ValueError(f"Preparation section not found in log: {log_file}")
    prep_section = prep_section_match.group(1)

    prep_times = []
    for pattern in (
        r"Decomposed template in\s+([\d\.e\-\+]+)\s+seconds",
        r"Constructed ctx data in\s+([\d\.e\-\+]+)\s+seconds",
        r"Loaded data field types in\s+([\d\.e\-\+]+)\s+seconds",
    ):
        match = re.search(pattern, prep_section)
        if match is None:
            raise ValueError(f"Missing preparation timing in log: {log_file}")
        prep_times.append(float(match.group(1)))
    details["preparation_time"] = sum(prep_times)
    total_time += details["preparation_time"]

    computing_section_match = re.search(
        r"\*+\s*Symbol basic ranges computing starts\s*\*+(.*?)\*+\s*Symbol basic ranges computing completes\s*\*+",
        content,
        re.DOTALL,
    )
    if computing_section_match:
        extra = re.findall(r"in\s+([\d\.e\-\+]+)\s+seconds", computing_section_match.group(1))
        details["computing_basic_ranges_time"] = sum(float(x) for x in extra)
        total_time += details["computing_basic_ranges_time"]

    solving_section_match = re.search(
        r"\*+\s*Solving process starts\s*\*+(.*?)\*+\s*Solving process completes\s*\*+",
        content,
        re.DOTALL,
    )
    if solving_section_match:
        solving_timeout_match = re.search(r"Solving process timeout in\s+([\d\.e\-\+]+)\s+seconds", content)
        section = solving_section_match.group(1)
        solving_details: dict[str, Any] = {
            "is_timeout": solving_timeout_match is not None,
            "parsed_template_time": 0.0,
            "constructed_main_constraint_time": 0.0,
            "constructed_ve_constraints_time": 0.0,
            "constructed_symbol_domain_constraints_time": 0.0,
            "solved_times": [],
            "evaluated_times": [],
            "solved_avg_time": 0.0,
            "evaluated_avg_time": 0.0,
            "total_time": 0.0,
        }
        if solving_timeout_match:
            solving_details["timeout_time"] = float(solving_timeout_match.group(1))

        for key, pattern in (
            ("parsed_template_time", r"Parsed template in\s+([\d\.e\-\+]+)\s+seconds"),
            ("constructed_main_constraint_time", r"Constructed main constraint in\s+([\d\.e\-\+]+)\s+seconds"),
            ("constructed_ve_constraints_time", r"Constructed VE constraints in\s+([\d\.e\-\+]+)\s+seconds"),
            (
                "constructed_symbol_domain_constraints_time",
                r"Constructed symbol domain constraints in\s+([\d\.e\-\+]+)\s+seconds",
            ),
        ):
            match = re.search(pattern, section)
            if match:
                solving_details[key] = float(match.group(1))

        solving_details["solved_times"] = [
            float(x) for x in re.findall(r"solved in\s+([\d\.e\-\+]+)\s+seconds", section, re.IGNORECASE)
        ]
        solving_details["evaluated_times"] = [
            float(x) for x in re.findall(r"evaluated in\s+([\d\.e\-\+]+)\s+seconds", section, re.IGNORECASE)
        ]

        if solving_details["solved_times"]:
            solving_details["solved_avg_time"] = sum(solving_details["solved_times"]) / len(
                solving_details["solved_times"]
            )
        if solving_details["evaluated_times"]:
            solving_details["evaluated_avg_time"] = sum(solving_details["evaluated_times"]) / len(
                solving_details["evaluated_times"]
            )

        if solving_timeout_match:
            solving_details["total_time"] = solving_details["timeout_time"]
        else:
            section_without_known = section
            for pattern in (
                r"Parsed template in\s+[\d\.e\-\+]+\s+seconds",
                r"Constructed main constraint in\s+[\d\.e\-\+]+\s+seconds",
                r"Constructed VE constraints in\s+[\d\.e\-\+]+\s+seconds",
                r"Constructed symbol domain constraints in\s+[\d\.e\-\+]+\s+seconds",
                r"solved in\s+[\d\.e\-\+]+\s+seconds",
                r"evaluated in\s+[\d\.e\-\+]+\s+seconds",
            ):
                section_without_known = re.sub(pattern, "", section_without_known, flags=re.IGNORECASE)
            other_times = [float(x) for x in re.findall(r"in\s+([\d\.e\-\+]+)\s+seconds", section_without_known)]
            solving_details["total_time"] = (
                solving_details["parsed_template_time"]
                + solving_details["constructed_main_constraint_time"]
                + solving_details["constructed_ve_constraints_time"]
                + solving_details["constructed_symbol_domain_constraints_time"]
                + sum(solving_details["solved_times"])
                + sum(solving_details["evaluated_times"])
                + sum(other_times)
            )

        details["solving_details"] = solving_details
        total_time += solving_details["total_time"]

    validating_section_match = re.search(
        r"\*+\s*Validating process starts\s*\*+(.*?)\*+\s*Validating process completes\s*\*+",
        content,
        re.DOTALL,
    )
    if validating_section_match:
        validating_timeout_match = re.search(r"Validating process timeout in\s+([\d\.e\-\+]+)\s+seconds", content)
        section = validating_section_match.group(1)
        validating_details: dict[str, Any] = {
            "is_timeout": validating_timeout_match is not None,
            "parsed_template_time": 0.0,
            "individual_times": [],
            "total_time": 0.0,
        }
        if validating_timeout_match:
            validating_details["timeout_time"] = float(validating_timeout_match.group(1))

        parsed_match = re.search(r"Parsed template in\s+([\d\.e\-\+]+)\s+seconds", section)
        if parsed_match:
            validating_details["parsed_template_time"] = float(parsed_match.group(1))

        section_without_parsed = re.sub(r"Parsed template in\s+[\d\.e\-\+]+\s+seconds", "", section)
        section_without_parsed = re.sub(
            r"Validating process timeout in\s+[\d\.e\-\+]+\s+seconds",
            "",
            section_without_parsed,
        )
        validating_details["individual_times"] = [
            float(x) for x in re.findall(r"in\s+([\d\.e\-\+]+)\s+seconds", section_without_parsed, re.IGNORECASE)
        ]

        if validating_timeout_match:
            validating_details["total_time"] = validating_details["timeout_time"]
        else:
            validating_details["total_time"] = (
                validating_details["parsed_template_time"] + sum(validating_details["individual_times"])
            )
        details["validating_details"] = validating_details
        total_time += validating_details["total_time"]

    return total_time, details


def extract_constraint_structure(template_dir: Path) -> dict[str, Any]:
    xml_file = template_dir / ".intermediate" / "template_decomposed.xml"
    bfunc_file = template_dir / ".intermediate" / "bfuncs_decomposed.py"

    result = {
        "height": 0,
        "quantifier_count": 0,
        "quantifier_nesting_layers": 0,
        "symbol_count": 0,
        "has_multiple_solutions": False,
    }

    if not xml_file.exists() or not bfunc_file.exists():
        return result

    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        def calculate_height(element: ET.Element, current_height: int = 0) -> int:
            max_child_height = current_height
            for child in element:
                max_child_height = max(max_child_height, calculate_height(child, current_height + 1))
            return max_child_height

        def count_quantifiers_and_nesting(element: ET.Element, current_nesting: int = 0) -> tuple[int, int]:
            quantifier_count = 0
            max_nesting_layers = current_nesting
            tag_name = element.tag.lower()
            if "forall" in tag_name or "exists" in tag_name:
                quantifier_count += 1
                current_nesting += 1
                max_nesting_layers = max(max_nesting_layers, current_nesting)
            for child in element:
                child_count, child_nesting = count_quantifiers_and_nesting(child, current_nesting)
                quantifier_count += child_count
                max_nesting_layers = max(max_nesting_layers, child_nesting)
            return quantifier_count, max_nesting_layers

        result["height"] = calculate_height(root)
        quantifier_count, max_nesting_layers = count_quantifiers_and_nesting(root)
        result["quantifier_count"] = quantifier_count
        result["quantifier_nesting_layers"] = max_nesting_layers

        bfunc_content = bfunc_file.read_text(encoding="utf-8")
        bfunc_to_symbols: dict[str, list[str]] = {}
        all_symbols: set[str] = set()
        bfunc_pattern = r"def\s+(bfunc_\w+)\s*\([^)]*\)\s*->\s*[^:]*:(.*?)(?=def\s+bfunc_|\Z)"
        for match in re.finditer(bfunc_pattern, bfunc_content, re.DOTALL):
            bfunc_name = match.group(1)
            symbols_in_func = set(re.findall(r"_[NS]_THRESHOLD_\d+", match.group(2)))
            if symbols_in_func:
                bfunc_to_symbols[bfunc_name] = list(symbols_in_func)
                all_symbols.update(symbols_in_func)
        result["symbol_count"] = len(all_symbols)

        def subtree_has_symbols(element: ET.Element) -> bool:
            if element.tag == "bfunc":
                bfunc_id = element.attrib.get("id")
                return f"bfunc_{bfunc_id}" in bfunc_to_symbols
            return any(subtree_has_symbols(child) for child in element)

        def analyze_multiple_solutions(element: ET.Element, goal_truth: bool = True) -> bool:
            tag_name = element.tag.lower()
            if tag_name == "bfunc":
                return False
            if tag_name == "forall":
                return analyze_multiple_solutions(element[0], goal_truth) or (
                    (not goal_truth) and subtree_has_symbols(element[0])
                )
            if tag_name == "exists":
                return analyze_multiple_solutions(element[0], goal_truth) or (
                    goal_truth and subtree_has_symbols(element[0])
                )
            if tag_name == "and":
                left_child, right_child = element[0], element[1]
                current_has_multi = (not goal_truth and subtree_has_symbols(left_child) and subtree_has_symbols(right_child))
                return (
                    analyze_multiple_solutions(left_child, goal_truth)
                    or analyze_multiple_solutions(right_child, goal_truth)
                    or current_has_multi
                )
            if tag_name == "or":
                left_child, right_child = element[0], element[1]
                current_has_multi = goal_truth and subtree_has_symbols(left_child) and subtree_has_symbols(right_child)
                return (
                    analyze_multiple_solutions(left_child, goal_truth)
                    or analyze_multiple_solutions(right_child, goal_truth)
                    or current_has_multi
                )
            if tag_name == "implies":
                left_child, right_child = element[0], element[1]
                current_has_multi = goal_truth and subtree_has_symbols(left_child) and subtree_has_symbols(right_child)
                return (
                    analyze_multiple_solutions(left_child, not goal_truth)
                    or analyze_multiple_solutions(right_child, goal_truth)
                    or current_has_multi
                )
            if tag_name == "not":
                return analyze_multiple_solutions(element[0], not goal_truth)
            return any(analyze_multiple_solutions(child, goal_truth) for child in element)

        result["has_multiple_solutions"] = analyze_multiple_solutions(root, True)
        return result
    except Exception:
        return result


def format_time_breakdown(time_details: dict[str, Any] | None) -> dict[str, Any] | None:
    if not time_details:
        return None

    breakdown: dict[str, Any] = {
        "preparation_time_seconds": round(time_details["preparation_time"], 3),
    }
    if time_details.get("computing_basic_ranges_time", 0) > 0:
        breakdown["computing_basic_ranges_time_seconds"] = round(time_details["computing_basic_ranges_time"], 3)

    if time_details["solving_details"]:
        s = time_details["solving_details"]
        breakdown["solving"] = {
            "is_timeout": s["is_timeout"],
            "parsed_template_time_seconds": round(s["parsed_template_time"], 3),
            "constructed_main_constraint_time_seconds": round(s["constructed_main_constraint_time"], 3),
            "constructed_ve_constraints_time_seconds": round(s["constructed_ve_constraints_time"], 3),
            "constructed_symbol_domain_constraints_time_seconds": round(
                s["constructed_symbol_domain_constraints_time"], 3
            ),
            "solved_avg_time_seconds": round(s["solved_avg_time"], 3),
            "solved_count": len(s["solved_times"]),
            "evaluated_avg_time_seconds": round(s["evaluated_avg_time"], 3),
            "evaluated_count": len(s["evaluated_times"]),
            "total_time_seconds": round(s["total_time"], 3),
        }
        if s["is_timeout"]:
            breakdown["solving"]["timeout_time_seconds"] = round(s["timeout_time"], 3)

    if time_details["validating_details"]:
        v = time_details["validating_details"]
        breakdown["validating"] = {
            "is_timeout": v["is_timeout"],
            "parsed_template_time_seconds": round(v["parsed_template_time"], 3),
            "individual_times_count": len(v["individual_times"]),
            "total_time_seconds": round(v["total_time"], 3),
        }
        if v["is_timeout"]:
            breakdown["validating"]["timeout_time_seconds"] = round(v["timeout_time"], 3)
        else:
            breakdown["validating"]["individual_times_sum_seconds"] = round(sum(v["individual_times"]), 3)

    return breakdown


def collect_constraint_info(target_dir: Path, template_dir: Path) -> dict[str, Any]:
    log_file = template_dir / "instantiation.log"
    if not log_file.exists():
        raise FileNotFoundError(f"Missing instantiation.log: {template_dir}")

    is_instantiated, instantiation_count = check_template_instantiation(template_dir)
    total_time, time_details = extract_time_from_log(log_file)
    status = extract_constraint_status(log_file)
    structure = extract_constraint_structure(template_dir)

    return {
        "source_template_id": extract_template_index(template_dir),
        "template_path": get_relative_path(template_dir, REPO_ROOT),
        "is_instantiated": is_instantiated,
        "instantiation_count": instantiation_count,
        "total_time": total_time,
        "time_details": time_details,
        "status": status,
        "structure": structure,
        "xml_path": template_dir / "constraint.xml",
        "py_path": template_dir / "bfuncs.py",
    }


def copy_extracted_files(
    output_dir: Path,
    constraint_infos: list[dict[str, Any]],
    renumber: bool,
) -> dict[int, dict[str, Any]]:
    extracted: dict[int, dict[str, Any]] = {}
    xml_dir = output_dir / "xml"
    py_dir = output_dir / "py"
    xml_dir.mkdir(parents=True, exist_ok=True)
    py_dir.mkdir(parents=True, exist_ok=True)

    next_constraint_id = 1
    used_constraint_ids: set[int] = set()
    for info in constraint_infos:
        xml_path = info["xml_path"]
        py_path = info["py_path"]
        if not xml_path.exists() or not py_path.exists():
            continue

        constraint_id = next_constraint_id if renumber else int(info["source_template_id"])
        if constraint_id in used_constraint_ids:
            raise ValueError(f"Duplicate constraint id {constraint_id}")
        used_constraint_ids.add(constraint_id)

        new_xml_name = f"constraint_{constraint_id}.xml"
        new_py_name = f"bfuncs_{constraint_id}.py"
        shutil.copy2(xml_path, xml_dir / new_xml_name)
        shutil.copy2(py_path, py_dir / new_py_name)

        extracted[id(info)] = {
            "constraint_id": constraint_id,
            "new_xml": new_xml_name,
            "new_py": new_py_name,
            "original_xml": get_relative_path(xml_path, REPO_ROOT),
            "original_py": get_relative_path(py_path, REPO_ROOT),
        }
        next_constraint_id += 1

    return extracted


def build_mapping(
    scenario: str,
    source_dir: Path,
    output_dir: Path,
    method_dir_name: str,
    config: str | None,
    constraint_infos: list[dict[str, Any]],
    extracted_files: dict[int, dict[str, Any]],
    renumber: bool,
) -> dict[str, Any]:
    total_templates = len(constraint_infos)
    total_time = sum(info["total_time"] for info in constraint_infos)
    avg_time = total_time / total_templates if total_templates else 0.0
    total_extracted_constraints = len(extracted_files)

    status_counts: dict[str, int] = {}
    status_time_totals: dict[str, float] = {}
    for info in constraint_infos:
        status = info["status"]
        status_counts[status] = status_counts.get(status, 0) + 1
        status_time_totals[status] = status_time_totals.get(status, 0.0) + info["total_time"]

    detailed_status_breakdown = {}
    for status, count in sorted(status_counts.items()):
        total_status_time = status_time_totals[status]
        detailed_status_breakdown[status] = {
            "count": count,
            "percentage": round((count / total_templates) * 100, 2) if total_templates else 0.0,
            "total_time_seconds": round(total_status_time, 2),
            "avg_time_seconds": round(total_status_time / count, 2) if count else 0.0,
        }

    mapping: dict[str, Any] = {
        "metadata": {
            "scenario": scenario,
            "source_dir": get_relative_path(source_dir, REPO_ROOT),
            "output_dir": get_relative_path(output_dir, REPO_ROOT),
            "method_dir_name": method_dir_name,
            "config": config,
            "total_templates": total_templates,
            "total_extracted_constraints": total_extracted_constraints,
            "total_time_seconds": round(total_time, 2),
            "avg_time_seconds": round(avg_time, 2),
            "naming_scheme": {
                "xml": "constraint_{constraint_id}.xml",
                "py": "bfuncs_{constraint_id}.py",
                "id_source": "consecutive" if renumber else "source_template_id",
            },
            "detailed_status_breakdown": detailed_status_breakdown,
        },
        "constraints": [],
    }

    sorted_infos = sorted(
        constraint_infos,
        key=lambda item: (
            extracted_files[id(item)]["constraint_id"]
            if id(item) in extracted_files
            else int(item["source_template_id"])
        ),
    )

    for info in sorted_infos:
        extracted = extracted_files.get(id(info))
        entry: dict[str, Any] = {
            "constraint_id": extracted["constraint_id"] if extracted else None,
            "source_template_id": info["source_template_id"],
            "template_path": info["template_path"],
            "status": info["status"],
            "instantiation_count": info["instantiation_count"],
            "total_time_seconds": round(info["total_time"], 2),
            "time_breakdown": format_time_breakdown(info["time_details"]),
            "structure_features": info["structure"],
            "extracted": extracted is not None,
        }
        if extracted:
            entry["files"] = {
                "xml": extracted["new_xml"],
                "py": extracted["new_py"],
            }
            entry["original_files"] = {
                "xml": extracted["original_xml"],
                "py": extracted["original_py"],
            }
        mapping["constraints"].append(entry)

    return mapping


def extract_from_dirs(
    scenario: str,
    source_dir: Path,
    output_dir_name: str,
    renumber: bool,
) -> tuple[Path, int, int]:
    method_dir_name, config = resolve_method_dir_name(source_dir, output_dir_name)
    output_dir = CONSTRAINTS_BASE / output_dir_name / method_dir_name
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    constraint_infos: list[dict[str, Any]] = []
    template_dirs = iter_template_dirs(source_dir)
    if not template_dirs:
        raise FileNotFoundError(f"No template_* directories found under {source_dir}")
    for template_dir in template_dirs:
        constraint_infos.append(collect_constraint_info(source_dir, template_dir))

    extracted_files = copy_extracted_files(output_dir, constraint_infos, renumber)
    mapping = build_mapping(
        scenario,
        source_dir,
        output_dir,
        method_dir_name,
        config,
        constraint_infos,
        extracted_files,
        renumber,
    )
    with open(output_dir / "mapping.json", "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)

    return output_dir, len(constraint_infos), len(extracted_files)


def main() -> int:
    try:
        args = parse_args()
        source_dir = resolve_target_dir(args.scenario, args.run_dir)
        output_dir, total_templates, extracted_constraints = extract_from_dirs(
            args.scenario,
            source_dir,
            args.output_dir,
            args.renumber,
        )

        print(f"Scenario: {args.scenario}")
        print(f"Source dir: {source_dir}")
        print(f"Output dir: {output_dir}")
        print(f"Total templates: {total_templates}")
        print(f"Extracted constraints: {extracted_constraints}")
        return 0
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
