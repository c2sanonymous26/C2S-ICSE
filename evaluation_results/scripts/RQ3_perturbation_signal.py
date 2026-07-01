#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from statistics import mean, stdev
from typing import Any

from sklearn.metrics import average_precision_score


PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_DATA_DIRS = [
    PROJECT_ROOT / "inputs" / "taxi" / "data",
    ]
OUTPUT_CHECK_DIR = PROJECT_ROOT / "outputs" / "check"
CONSTRAINTS_DIR = PROJECT_ROOT / "constraints"
EVALUATION_DIR = PROJECT_ROOT / "results" / "RQ3" / "environmentalCorrespondence"

EXPERIMENTS = [f"taxi_RQ3_{index}" for index in range(1, 6)]
CONFIGS = [
    "C2S_0000",
    "C2S_1000",
    "C2S_0100",
    "C2S_0010",
    "C2S_0001",
    "C2S_1111",
]
PERTURBATION_PROB = "5000_pp_0.1"


def load_json(path: Path) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sample_std(values: list[float]) -> float:
    if len(values) <= 1:
        return 0.0
    return float(stdev(values))


def read_incs_file(path: Path) -> list[tuple[str, dict[str, int]]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing incs file: {path}")

    rows: list[tuple[str, dict[str, int]]] = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            constraint_name = row[0].strip()
            assignment_text = row[1].strip() if len(row) > 1 else ""
            assignment: dict[str, int] = {}
            for var_name, value in re.findall(r"\(([^,]+),(\d+)\)", assignment_text):
                assignment[var_name.strip()] = int(value)
            if constraint_name and assignment:
                rows.append((constraint_name, assignment))
    return rows


def group_incs_by_constraint(
    incs: list[tuple[str, dict[str, int]]],
) -> dict[str, list[dict[str, int]]]:
    grouped: dict[str, list[dict[str, int]]] = {}
    for constraint_name, assignment in incs:
        grouped.setdefault(constraint_name, []).append(assignment)
    return grouped


def extract_suspicious_id_freq(assignments: list[dict[str, int]]) -> dict[int, int]:
    freq: dict[int, int] = {}
    for assignment in assignments:
        for data_id in assignment.values():
            freq[data_id] = freq.get(data_id, 0) + 1
    return freq


def load_all_data_ids(perturbed_csv: Path) -> set[int]:
    ids: set[int] = set()
    with open(perturbed_csv, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if row:
                ids.add(int(row[0]))
    return ids


def extract_constraint_fields(bfunc_file: Path) -> set[str]:
    text = bfunc_file.read_text(encoding="utf-8")
    return set(
        re.findall(
            r"var_bindings\s*\[\s*['\"]v\d+['\"]\s*\]\s*\[\s*['\"]([^'\"]+)['\"]\s*\]",
            text,
        )
    )


def resolve_perturbation_data_dir(perturbation_prob: str, perturbation_id: str) -> Path:
    for input_data_dir in INPUT_DATA_DIRS:
        candidate = input_data_dir / perturbation_prob / perturbation_id
        if candidate.exists():
            return candidate
    searched = [str(input_data_dir / perturbation_prob / perturbation_id) for input_data_dir in INPUT_DATA_DIRS]
    raise FileNotFoundError(f"Missing perturbation data directory. Searched: {searched}")


def calculate_average_precision(
    actual_perturbation_ids: set[int],
    score_map: dict[int, float],
    all_data_ids: set[int],
) -> float:
    ordered_ids = sorted(all_data_ids)
    y_true = [1 if data_id in actual_perturbation_ids else 0 for data_id in ordered_ids]
    y_scores = [score_map.get(data_id, 0.0) for data_id in ordered_ids]
    try:
        return float(average_precision_score(y_true, y_scores))
    except ValueError:
        return 0.0


def merge_by_freq_sum(per_constraint_results: dict[str, dict[str, Any]]) -> dict[int, float]:
    merged: dict[int, float] = {}
    for result in per_constraint_results.values():
        for data_id, count in result["suspicious_id_freq_dict"].items():
            merged[data_id] = merged.get(data_id, 0.0) + float(count)
    return merged


def round_result(result: dict[str, Any]) -> dict[str, Any]:
    def transform(obj: Any) -> Any:
        if isinstance(obj, dict):
            return {
                key: transform(value)
                for key, value in obj.items()
                if key not in {"actual_perturbation_ids", "suspicious_id_freq_dict"}
            }
        if isinstance(obj, list):
            return [transform(item) for item in obj]
        if isinstance(obj, float):
            return float(f"{obj:.6f}")
        return obj

    return transform(result)


def build_single_result(experiment_name: str, config_name: str, perturbation_id: str) -> dict[str, Any]:
    check_base = OUTPUT_CHECK_DIR / experiment_name / config_name
    constraints_py_dir = CONSTRAINTS_DIR / experiment_name / config_name / "py"
    data_dir = resolve_perturbation_data_dir(PERTURBATION_PROB, perturbation_id)

    perturbation_incs_file = check_base / PERTURBATION_PROB / f"{perturbation_id}_perturbed" / "incs.csv"
    perturbed_json = data_dir / "perturbed.json"
    perturbed_csv = data_dir / "perturbed.csv"

    if not perturbed_json.exists():
        raise FileNotFoundError(f"Missing perturbation metadata file: {perturbed_json}")
    if not perturbed_csv.exists():
        raise FileNotFoundError(f"Missing perturbation data file: {perturbed_csv}")

    perturbation_incs = read_incs_file(perturbation_incs_file)
    perturbation_records = load_json(perturbed_json)
    all_data_ids = load_all_data_ids(perturbed_csv)
    incs_by_constraint = group_incs_by_constraint(perturbation_incs)

    per_constraint_results: dict[str, dict[str, Any]] = {}
    for constraint_name, assignments in sorted(incs_by_constraint.items()):
        match = re.fullmatch(r"constraint_(\d+)", constraint_name)
        if not match:
            raise ValueError(f"Unsupported constraint name: {constraint_name}")
        constraint_id = match.group(1)
        bfunc_file = constraints_py_dir / f"bfuncs_{constraint_id}.py"
        if not bfunc_file.exists():
            raise FileNotFoundError(f"Missing bfunc file: {bfunc_file}")

        constraint_fields = extract_constraint_fields(bfunc_file)
        actual_perturbation_ids = {
            int(record["id"])
            for record in perturbation_records
            if record.get("field") in constraint_fields
        }
        suspicious_id_freq_dict = extract_suspicious_id_freq(assignments)
        auprc_value = calculate_average_precision(actual_perturbation_ids, suspicious_id_freq_dict, all_data_ids)

        per_constraint_results[constraint_name] = {
            "incs": len(assignments),
            "AUPRC": auprc_value,
            "actual_perturbation_ids": sorted(actual_perturbation_ids),
            "actual_perturbation_count": len(actual_perturbation_ids),
            "suspicious_count": len(suspicious_id_freq_dict),
            "suspicious_id_freq_dict": suspicious_id_freq_dict,
        }

    overall_actual_perturbation_ids = {int(record["id"]) for record in perturbation_records}
    freq_sum_scores = merge_by_freq_sum(per_constraint_results)

    overall_results = {
        "involved_constraint_count": len(per_constraint_results),
        "incs": sum(result["incs"] for result in per_constraint_results.values()),
        "AUPRC": calculate_average_precision(overall_actual_perturbation_ids, freq_sum_scores, all_data_ids),
        "actual_perturbation_count": len(overall_actual_perturbation_ids),
        "suspicious_count": len(freq_sum_scores),
    }

    return {
        "perturbation_data_name": f"{PERTURBATION_PROB}/{perturbation_id}",
        "overall_results": overall_results,
        "per_constraint_results": per_constraint_results,
    }


def build_average_result(all_results: list[dict[str, Any]]) -> dict[str, Any]:
    total_samples = len(all_results)
    overall_results = [result["overall_results"] for result in all_results]

    overall_average_results = {
        "total_samples": total_samples,
        "involved_constraint_count": {
            "mean": mean(float(item["involved_constraint_count"]) for item in overall_results),
            "std": sample_std([float(item["involved_constraint_count"]) for item in overall_results]),
        },
        "incs": {
            "mean": mean(float(item["incs"]) for item in overall_results),
            "std": sample_std([float(item["incs"]) for item in overall_results]),
        },
        "AUPRC": {
            "mean": mean(float(item["AUPRC"]) for item in overall_results),
            "std": sample_std([float(item["AUPRC"]) for item in overall_results]),
        },
        "actual_perturbation_count": {
            "mean": mean(float(item["actual_perturbation_count"]) for item in overall_results),
            "std": sample_std([float(item["actual_perturbation_count"]) for item in overall_results]),
        },
        "suspicious_count": {
            "mean": mean(float(item["suspicious_count"]) for item in overall_results),
            "std": sample_std([float(item["suspicious_count"]) for item in overall_results]),
        },
    }

    per_constraint_values: dict[str, list[dict[str, Any]]] = {}
    for result in all_results:
        for constraint_name, constraint_result in result["per_constraint_results"].items():
            per_constraint_values.setdefault(constraint_name, []).append(constraint_result)

    per_constraint_averages: dict[str, dict[str, Any]] = {}
    for constraint_name in sorted(per_constraint_values):
        values = per_constraint_values[constraint_name]
        per_constraint_averages[constraint_name] = {
            "incs": {
                "mean": mean(float(item["incs"]) for item in values),
                "std": sample_std([float(item["incs"]) for item in values]),
            },
            "AUPRC": {
                "mean": mean(float(item["AUPRC"]) for item in values),
                "std": sample_std([float(item["AUPRC"]) for item in values]),
            },
            "actual_perturbation_count": {
                "mean": mean(float(item["actual_perturbation_count"]) for item in values),
                "std": sample_std([float(item["actual_perturbation_count"]) for item in values]),
            },
            "suspicious_count": {
                "mean": mean(float(item["suspicious_count"]) for item in values),
                "std": sample_std([float(item["suspicious_count"]) for item in values]),
            },
            "occurrence/total_samples": f"{len(values)}/{total_samples}",
        }

    return {
        "overall_average_results": overall_average_results,
        "per_constraint_averages": per_constraint_averages,
    }


def run_all(selected_experiments: list[str], selected_configs: list[str]) -> None:
    for experiment_name in selected_experiments:
        for config_name in selected_configs:
            perturbation_prob_dir = OUTPUT_CHECK_DIR / experiment_name / config_name / PERTURBATION_PROB
            if not perturbation_prob_dir.exists():
                raise FileNotFoundError(f"Missing check result directory: {perturbation_prob_dir}")
            perturbation_ids = sorted(
                path.name.removesuffix("_perturbed")
                for path in perturbation_prob_dir.iterdir()
                if path.is_dir() and path.name.endswith("_perturbed")
            )

            all_results: list[dict[str, Any]] = []
            for perturbation_id in perturbation_ids:
                result = round_result(build_single_result(experiment_name, config_name, perturbation_id))
                output_file = (
                    EVALUATION_DIR
                    / experiment_name
                    / config_name
                    / PERTURBATION_PROB
                    / perturbation_id
                    / "results.json"
                )
                write_json(output_file, result)
                all_results.append(result)

            average_result = round_result(build_average_result(all_results))
            average_output_file = (
                EVALUATION_DIR
                / experiment_name
                / config_name
                / PERTURBATION_PROB
                / "average"
                / "results.json"
            )
            write_json(average_output_file, average_result)


def build_summary_for(selected_experiments: list[str], selected_configs: list[str]) -> dict[str, Any]:
    experiments_payload: list[dict[str, Any]] = []
    for experiment in selected_experiments:
        item: dict[str, Any] = {"experiment": experiment}
        for config in selected_configs:
            average_file = EVALUATION_DIR / experiment / config / PERTURBATION_PROB / "average" / "results.json"
            item[config] = load_json(average_file)["overall_average_results"]
        experiments_payload.append(item)

    average_payload: dict[str, Any] = {}
    metric_names = [
        "involved_constraint_count",
        "incs",
        "AUPRC",
        "actual_perturbation_count",
        "suspicious_count",
    ]
    for config in selected_configs:
        config_values = [item[config] for item in experiments_payload]
        average_payload[config] = {
            "total_samples": int(round(mean(float(v["total_samples"]) for v in config_values))),
        }
        for metric in metric_names:
            mean_values = [float(v[metric]["mean"]) for v in config_values]
            average_payload[config][metric] = {
                "mean": mean(mean_values),
                "std": sample_std(mean_values),
            }

    return {
        "average": average_payload,
        "experiments": experiments_payload,
    }


def print_summary_table(summary: dict[str, Any], configs: list[str]) -> None:
    rows: list[tuple[str, str, str, str]] = []
    for config in configs:
        rows.append(
            (
                "average",
                config,
                f"{float(summary['average'][config]['AUPRC']['mean']):.3f}",
                str(int(summary["average"][config]["total_samples"])),
            )
        )

    for experiment in summary["experiments"]:
        for config in configs:
            rows.append(
                (
                    experiment["experiment"],
                    config,
                    f"{float(experiment[config]['AUPRC']['mean']):.3f}",
                    str(int(experiment[config]["total_samples"])),
                )
            )

    headers = ("experiment", "config", "mean_auprc", "total_samples")
    widths = [max(len(headers[i]), max(len(row[i]) for row in rows)) for i in range(len(headers))]

    def format_row(values: tuple[str, str, str, str]) -> str:
        return "  ".join(value.ljust(widths[i]) for i, value in enumerate(values))

    print(format_row(headers))
    for row in rows:
        print(format_row(row))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate the RQ3 perturbation-signal summary from results/RQ3/environmentalCorrespondence results. "
            "Use --regenerate-results to regenerate all per-sample and average results first."
        )
    )
    parser.add_argument("--experiments", nargs="*", default=EXPERIMENTS)
    parser.add_argument("--configs", nargs="*", default=CONFIGS)
    parser.add_argument(
        "--regenerate-results",
        action="store_true",
        help="Regenerate all results/RQ3/environmentalCorrespondence results before summarizing.",
    )
    return parser.parse_args()


def main() -> None:
    print("Generating RQ3 perturbation-signal summary...")
    args = parse_args()
    written_files: list[Path] = []

    if args.regenerate_results:
        print("Regenerating RQ3 perturbation-signal results...")
        run_all(args.experiments, args.configs)
    else:
        print("Generating RQ3 perturbation-signal summary from existing results...")

    summary = build_summary_for(args.experiments, args.configs)
    if args.experiments == EXPERIMENTS and args.configs == CONFIGS:
        summary_path = EVALUATION_DIR / "RQ3_perturbation_signal.json"
        write_json(summary_path, summary)
        written_files.append(summary_path)

    print_summary_table(summary, args.configs)
    print("\nWritten files:")
    for path in written_files:
        print(f"  {path}")
    print("\nDone.")


if __name__ == "__main__":
    main()
