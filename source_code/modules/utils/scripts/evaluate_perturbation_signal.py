from __future__ import annotations

import argparse
import csv
import json
import logging
import re
import sys
from pathlib import Path
from typing import Any

from sklearn.metrics import average_precision_score


SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parent.parent.parent.parent
INPUT_DIR = REPO_ROOT / "inputs"
SIGNAL_DIR = REPO_ROOT / "evaluation" / "perturbation_signal"


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(message)s",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate perturbation-signal usefulness for the current C2S directory structure."
    )
    parser.add_argument("--scenario", "-s", required=True, help="Scenario name, e.g. taxi")
    parser.add_argument(
        "--constraint-dir",
        required=True,
        help="Constraint directory that directly contains xml/ and py/, e.g. constraints/taxi_1/C2S",
    )
    parser.add_argument(
        "--check-dir",
        required=True,
        help="Check output directory, e.g. outputs/check/taxi_1/C2S",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--perturbation-data-name",
        help="Single perturbation data in the format <prob>/<id>, e.g. 5000_pp_0.1/0cfb5cac",
    )
    group.add_argument(
        "--perturbation-data-prob",
        help="Batch mode perturbation-probability directory, e.g. 5000_pp_0.1",
    )
    return parser.parse_args()


def resolve_repo_path(path_str: str) -> Path:
    raw = Path(path_str)
    if raw.exists():
        return raw.resolve()
    candidate = (REPO_ROOT / path_str).resolve()
    if candidate.exists():
        return candidate
    raise FileNotFoundError(f"Path does not exist: {path_str}")


def parse_perturbation_data_name(perturbation_data_name: str) -> tuple[str, str]:
    if "/" not in perturbation_data_name or perturbation_data_name.count("/") != 1:
        raise ValueError(
            f"Invalid perturbation_data_name format: {perturbation_data_name}. Expected format: <prob>/<id>"
        )
    perturbation_prob, perturbation_id = perturbation_data_name.split("/", 1)
    return perturbation_prob, perturbation_id


def output_root(constraint_dir: Path) -> Path:
    constraint_group = constraint_dir.parent.name
    constraint_name = constraint_dir.name
    return SIGNAL_DIR / constraint_group / constraint_name


def load_all_data_ids(perturbed_csv: Path) -> set[int]:
    all_data_ids: set[int] = set()
    with open(perturbed_csv, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            all_data_ids.add(int(row["id"]))
    return all_data_ids


def load_perturbation_info(perturbed_json: Path) -> list[dict[str, Any]]:
    with open(perturbed_json, "r", encoding="utf-8") as f:
        return json.load(f)


def read_incs_file(incs_file: Path) -> list[tuple[str, dict[str, int]]]:
    if not incs_file.exists():
        return []

    incs_data: list[tuple[str, dict[str, int]]] = []
    pattern = r"\(([^,]+),(\d+)\)"

    with open(incs_file, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 2:
                continue
            constraint_name = row[0].strip()
            assignment_str = row[1].strip()
            assignment_dict: dict[str, int] = {}
            for var_name, value_str in re.findall(pattern, assignment_str):
                assignment_dict[var_name.strip()] = int(value_str.strip())
            if constraint_name and assignment_dict:
                incs_data.append((constraint_name, assignment_dict))
    return incs_data


def group_incs_by_constraint(
    pure_perturbation_incs: list[tuple[str, dict[str, int]]]
) -> dict[str, list[dict[str, int]]]:
    incs_by_constraint: dict[str, list[dict[str, int]]] = {}
    for constraint_name, assignment in pure_perturbation_incs:
        incs_by_constraint.setdefault(constraint_name, []).append(assignment)
    return incs_by_constraint


def extract_constraint_fields(constraint_name: str, constraint_dir: Path) -> set[str]:
    match = re.fullmatch(r"constraint_(\d+)", constraint_name)
    if not match:
        raise ValueError(f"Invalid constraint name format: {constraint_name}")

    constraint_id = match.group(1)
    bfunc_file = constraint_dir / "py" / f"bfuncs_{constraint_id}.py"
    if not bfunc_file.exists():
        raise FileNotFoundError(f"Missing bfunc file for {constraint_name}: {bfunc_file}")

    content = bfunc_file.read_text(encoding="utf-8")
    pattern = r"var_bindings\s*\[\s*['\"]v\d+['\"]\s*\]\s*\[\s*['\"]([^'\"]+)['\"]\s*\]"
    return set(re.findall(pattern, content))


def extract_actual_perturbation_ids(
    perturbation_info_data: list[dict[str, Any]],
    constraint_fields: set[str] | None = None,
) -> set[int]:
    actual_perturbation_ids: set[int] = set()
    for perturbation in perturbation_info_data:
        if constraint_fields is not None and perturbation["field"] not in constraint_fields:
            continue
        actual_perturbation_ids.add(int(perturbation["id"]))
    return actual_perturbation_ids


def extract_suspicious_ids_frequency(assignments: list[dict[str, int]]) -> dict[int, int]:
    suspicious_id_freq_dict: dict[int, int] = {}
    for assignment in assignments:
        for _, data_id in assignment.items():
            suspicious_id_freq_dict[data_id] = suspicious_id_freq_dict.get(data_id, 0) + 1
    return suspicious_id_freq_dict


def calculate_ap(actual_perturbation_ids: set[int], score_map: dict[int, float], all_data_ids: set[int]) -> float:
    ordered_ids = sorted(all_data_ids)
    y_true = [1 if data_id in actual_perturbation_ids else 0 for data_id in ordered_ids]
    y_scores = [score_map.get(data_id, 0.0) for data_id in ordered_ids]
    try:
        return float(average_precision_score(y_true, y_scores))
    except ValueError:
        return 0.0


def analyze_per_constraint(
    pure_perturbation_incs: list[tuple[str, dict[str, int]]],
    perturbation_info_data: list[dict[str, Any]],
    all_data_ids: set[int],
    constraint_dir: Path,
) -> dict[str, dict[str, Any]]:
    incs_by_constraint = group_incs_by_constraint(pure_perturbation_incs)
    constraint_results: dict[str, dict[str, Any]] = {}

    for constraint_name, assignments in sorted(incs_by_constraint.items()):
        constraint_fields = extract_constraint_fields(constraint_name, constraint_dir)
        actual_perturbation_ids = extract_actual_perturbation_ids(perturbation_info_data, constraint_fields)
        freq_dict = extract_suspicious_ids_frequency(assignments)
        ap_score = calculate_ap(actual_perturbation_ids, freq_dict, all_data_ids)

        constraint_results[constraint_name] = {
            "incs": len(assignments),
            "AUPRC": ap_score,
            "actual_perturbation_count": len(actual_perturbation_ids),
            "suspicious_count": len(freq_dict),
            "suspicious_id_freq_dict": freq_dict,
        }
    return constraint_results


def merge_by_freq_sum(per_constraint_results: dict[str, dict[str, Any]]) -> dict[int, float]:
    freq_map: dict[int, float] = {}
    for result in per_constraint_results.values():
        for data_id, cnt in result["suspicious_id_freq_dict"].items():
            freq_map[data_id] = freq_map.get(data_id, 0.0) + float(cnt)
    return freq_map


def analyze_overall(
    per_constraint_results: dict[str, dict[str, Any]],
    perturbation_info_data: list[dict[str, Any]],
    all_data_ids: set[int],
) -> dict[str, Any]:
    actual_perturbation_ids = extract_actual_perturbation_ids(perturbation_info_data, None)
    freq_sum_map = merge_by_freq_sum(per_constraint_results)
    total_pure_perturbation_incs = sum(result["incs"] for result in per_constraint_results.values())

    return {
        "involved_constraint_count": len(per_constraint_results),
        "incs": total_pure_perturbation_incs,
        "AUPRC": calculate_ap(actual_perturbation_ids, freq_sum_map, all_data_ids),
        "actual_perturbation_count": len(actual_perturbation_ids),
        "suspicious_count": len(freq_sum_map),
    }


def format_single_result(result: dict[str, Any]) -> dict[str, Any]:
    def _format(obj: Any) -> Any:
        if isinstance(obj, dict):
            new_obj = {}
            for k, v in obj.items():
                if k in {"actual_perturbation_ids", "suspicious_id_freq_dict"}:
                    continue
                elif isinstance(v, float):
                    new_obj[k] = float(f"{v:.6f}")
                else:
                    new_obj[k] = _format(v)
            return new_obj
        if isinstance(obj, list):
            return [_format(x) for x in obj]
        return obj

    return _format(result)


def sample_std(values: list[float], mean: float) -> float:
    if len(values) <= 1:
        return 0.0
    squared_diff_sum = sum((x - mean) ** 2 for x in values)
    return (squared_diff_sum / (len(values) - 1)) ** 0.5


def calculate_per_constraint_averages(
    all_results: list[dict[str, Any]],
    all_data_ids_by_sample: list[set[int]],
    perturbation_info_by_sample: list[list[dict[str, Any]]],
) -> dict[str, dict[str, Any]]:
    total_samples = len(all_results)
    all_constraints = set()
    for result in all_results:
        all_constraints.update(result["per_constraint_results"].keys())

    baseline_ap_values = []
    for all_ids, perturbation_info_data in zip(all_data_ids_by_sample, perturbation_info_by_sample):
        positive_ratio = len(extract_actual_perturbation_ids(perturbation_info_data)) / len(all_ids)
        baseline_ap_values.append(positive_ratio)
    baseline_ap = sum(baseline_ap_values) / len(baseline_ap_values) if baseline_ap_values else 0.0

    constraint_averages: dict[str, dict[str, Any]] = {}
    for constraint_name in sorted(all_constraints):
        incs_values: list[float] = []
        ap_values: list[float] = []
        actual_perturbation_count_values: list[float] = []
        suspicious_count_values: list[float] = []
        occurrence_count = 0

        for result in all_results:
            per_constraint = result["per_constraint_results"]
            if constraint_name in per_constraint:
                item = per_constraint[constraint_name]
                incs_values.append(float(item["incs"]))
                ap_values.append(float(item["AUPRC"]))
                actual_perturbation_count_values.append(float(item["actual_perturbation_count"]))
                suspicious_count_values.append(float(item["suspicious_count"]))
                occurrence_count += 1
            else:
                incs_values.append(0.0)
                ap_values.append(baseline_ap)
                actual_perturbation_count_values.append(0.0)
                suspicious_count_values.append(0.0)

        avg_incs = sum(incs_values) / total_samples
        avg_ap = sum(ap_values) / total_samples
        avg_actual_perturbation_count = sum(actual_perturbation_count_values) / total_samples
        avg_suspicious_count = sum(suspicious_count_values) / total_samples

        constraint_averages[constraint_name] = {
            "incs": {"mean": avg_incs, "std": sample_std(incs_values, avg_incs)},
            "AUPRC": {"mean": avg_ap, "std": sample_std(ap_values, avg_ap)},
            "actual_perturbation_count": {
                "mean": avg_actual_perturbation_count,
                "std": sample_std(actual_perturbation_count_values, avg_actual_perturbation_count),
            },
            "suspicious_count": {
                "mean": avg_suspicious_count,
                "std": sample_std(suspicious_count_values, avg_suspicious_count),
            },
            "occurrence/total_samples": f"{occurrence_count}/{total_samples}",
        }
    return constraint_averages


def calculate_overall_average(all_results: list[dict[str, Any]]) -> dict[str, Any]:
    total_samples = len(all_results)
    involved_constraint_counts = []
    incs_values = []
    auprc_values = []
    actual_perturbation_count_values = []
    suspicious_count_values = []

    for result in all_results:
        overall = result["overall_results"]
        involved_constraint_counts.append(float(overall["involved_constraint_count"]))
        incs_values.append(float(overall["incs"]))
        auprc_values.append(float(overall["AUPRC"]))
        actual_perturbation_count_values.append(float(overall["actual_perturbation_count"]))
        suspicious_count_values.append(float(overall["suspicious_count"]))

    def _mean(values: list[float]) -> float:
        return sum(values) / total_samples

    avg_involved_constraint_count = _mean(involved_constraint_counts)
    avg_incs = _mean(incs_values)
    avg_auprc = _mean(auprc_values)
    avg_actual_perturbation_count = _mean(actual_perturbation_count_values)
    avg_suspicious_count = _mean(suspicious_count_values)

    return {
        "total_samples": total_samples,
        "involved_constraint_count": {
            "mean": avg_involved_constraint_count,
            "std": sample_std(involved_constraint_counts, avg_involved_constraint_count),
        },
        "incs": {"mean": avg_incs, "std": sample_std(incs_values, avg_incs)},
        "AUPRC": {
            "mean": avg_auprc,
            "std": sample_std(auprc_values, avg_auprc),
        },
        "actual_perturbation_count": {
            "mean": avg_actual_perturbation_count,
            "std": sample_std(actual_perturbation_count_values, avg_actual_perturbation_count),
        },
        "suspicious_count": {
            "mean": avg_suspicious_count,
            "std": sample_std(suspicious_count_values, avg_suspicious_count),
        },
    }


def format_average_result(result: dict[str, Any]) -> dict[str, Any]:
    def _format(obj: Any) -> Any:
        if isinstance(obj, dict):
            new_obj = {}
            for k, v in obj.items():
                if isinstance(v, float):
                    new_obj[k] = float(f"{v:.6f}")
                else:
                    new_obj[k] = _format(v)
            return new_obj
        if isinstance(obj, list):
            return [_format(x) for x in obj]
        return obj

    return _format(result)


def evaluate_single(
    scenario: str,
    constraint_dir: Path,
    check_dir: Path,
    perturbation_data_name: str,
) -> tuple[dict[str, Any], set[int], list[dict[str, Any]]]:
    perturbation_prob, perturbation_id = parse_perturbation_data_name(perturbation_data_name)
    perturbation_data_dir = INPUT_DIR / scenario / "data" / perturbation_prob / perturbation_id
    perturbed_csv = perturbation_data_dir / "perturbed.csv"
    perturbed_json = perturbation_data_dir / "perturbed.json"
    if not perturbed_csv.exists() or not perturbed_json.exists():
        raise FileNotFoundError(f"Missing perturbation data files under {perturbation_data_dir}")

    perturbation_check_dir = check_dir / perturbation_prob / f"{perturbation_id}_perturbed"
    perturbation_incs_file = perturbation_check_dir / "incs.csv"
    if not perturbation_incs_file.exists():
        raise FileNotFoundError(f"Missing check result file: {perturbation_incs_file}")

    perturbation_incs = read_incs_file(perturbation_incs_file)
    pure_perturbation_incs = perturbation_incs

    all_data_ids = load_all_data_ids(perturbed_csv)
    perturbation_info_data = load_perturbation_info(perturbed_json)
    per_constraint_results = analyze_per_constraint(
        pure_perturbation_incs,
        perturbation_info_data,
        all_data_ids,
        constraint_dir,
    )
    overall_results = analyze_overall(per_constraint_results, perturbation_info_data, all_data_ids)

    result = {
        "metadata": {
            "scenario": scenario,
            "constraint_dir": str(constraint_dir.relative_to(REPO_ROOT)),
            "check_dir": str(check_dir.relative_to(REPO_ROOT)),
            "perturbation_data_name": perturbation_data_name,
            "pure_perturbation_incs_count": len(pure_perturbation_incs),
            "uses_perturbation_data_incs_directly": True,
        },
        "overall_results": overall_results,
        "per_constraint_results": per_constraint_results,
    }
    return result, all_data_ids, perturbation_info_data


def write_json(path: Path, obj: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)


def process_single_mode(args: argparse.Namespace, constraint_dir: Path, check_dir: Path) -> None:
    result, _, _ = evaluate_single(
        args.scenario,
        constraint_dir,
        check_dir,
        args.perturbation_data_name,
    )
    perturbation_prob, perturbation_id = parse_perturbation_data_name(args.perturbation_data_name)
    output_file = output_root(constraint_dir) / perturbation_prob / perturbation_id / "results.json"
    write_json(output_file, format_single_result(result))
    logging.info(f"Wrote single-sample results to {output_file.relative_to(REPO_ROOT)}")
    overall = result["overall_results"]
    logging.info(f"Overall AUPRC = {overall['AUPRC']:.6f}")


def process_batch_mode(args: argparse.Namespace, constraint_dir: Path, check_dir: Path) -> None:
    prob_dir = INPUT_DIR / args.scenario / "data" / args.perturbation_data_prob
    if not prob_dir.exists():
        raise FileNotFoundError(f"Perturbation-data probability directory not found: {prob_dir}")

    perturbation_ids = sorted(item.name for item in prob_dir.iterdir() if item.is_dir())
    if not perturbation_ids:
        raise FileNotFoundError(f"No perturbation ids found under {prob_dir}")

    all_results: list[dict[str, Any]] = []
    all_data_ids_by_sample: list[set[int]] = []
    perturbation_info_by_sample: list[list[dict[str, Any]]] = []

    for perturbation_id in perturbation_ids:
        perturbation_data_name = f"{args.perturbation_data_prob}/{perturbation_id}"
        result, all_data_ids, perturbation_info_data = evaluate_single(
            args.scenario,
            constraint_dir,
            check_dir,
            perturbation_data_name,
        )
        output_file = output_root(constraint_dir) / args.perturbation_data_prob / perturbation_id / "results.json"
        write_json(output_file, format_single_result(result))
        all_results.append(result)
        all_data_ids_by_sample.append(all_data_ids)
        perturbation_info_by_sample.append(perturbation_info_data)
        logging.info(f"Wrote sample results to {output_file.relative_to(REPO_ROOT)}")

    average_result = {
        "metadata": {
            "scenario": args.scenario,
            "constraint_dir": str(constraint_dir.relative_to(REPO_ROOT)),
            "check_dir": str(check_dir.relative_to(REPO_ROOT)),
            "perturbation_data_prob": args.perturbation_data_prob,
        },
        "overall_average_results": calculate_overall_average(all_results),
        "per_constraint_averages": calculate_per_constraint_averages(
            all_results,
            all_data_ids_by_sample,
            perturbation_info_by_sample,
        ),
    }
    average_output = output_root(constraint_dir) / args.perturbation_data_prob / "average" / "results.json"
    write_json(average_output, format_average_result(average_result))
    logging.info(f"Wrote average results to {average_output.relative_to(REPO_ROOT)}")

    overall = average_result["overall_average_results"]
    logging.info("Average overall AUPRC = %.6f", overall["AUPRC"]["mean"])


def main() -> int:
    try:
        args = parse_args()
        constraint_dir = resolve_repo_path(args.constraint_dir)
        check_dir = resolve_repo_path(args.check_dir)

        if args.perturbation_data_name:
            process_single_mode(args, constraint_dir, check_dir)
        else:
            process_batch_mode(args, constraint_dir, check_dir)
        return 0
    except Exception as exc:
        logging.error(str(exc))
        return 1


if __name__ == "__main__":
    sys.exit(main())
