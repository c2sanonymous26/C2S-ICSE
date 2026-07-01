#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parent.parent
HUMAN_EVALUATION_FILES = [
    PROJECT_ROOT / "results" / "RQ1" / "effectiveness_humanEvaluation" / "results" / "group1" / "aggregated.md",
    PROJECT_ROOT / "results" / "RQ1" / "effectiveness_humanEvaluation" / "results" / "group2" / "aggregated.md",
]
OUTPUT_PATH = PROJECT_ROOT / "results" / "RQ1" / "efficiency_synthesisTime" / "RQ1_time.json"
CONSTRAINTS_BASE = PROJECT_ROOT / "constraints"
INVENTOR_BASE = PROJECT_ROOT / "outputs" / "invention" / "inventor"
CONVERTER_BASE = PROJECT_ROOT / "outputs" / "invention" / "converter"

METHOD_NAMES = {
    "Method 1": "C2S",
    "Method 2": "AR+",
}
EXPERIMENTS = ["1", "2", "3", "4", "5"]
SECONDS_PER_HOUR = 3600.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate the ICSE RQ1 synthesis-efficiency table data."
    )
    parser.add_argument(
        "--experiments",
        nargs="*",
        default=EXPERIMENTS,
        help="Experiment indices to summarize, default: 1 2 3 4 5",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_PATH,
        help="Output JSON path, default: results/RQ1/efficiency_synthesisTime/RQ1_time.json",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_human_evaluation(path: Path) -> dict[str, dict[str, Counter]]:
    text = path.read_text(encoding="utf-8")
    sections = re.split(r"^## (.+)$", text, flags=re.MULTILINE)
    result: dict[str, dict[str, Counter]] = {}

    for index in range(1, len(sections) - 1, 2):
        method_label = sections[index].strip()
        method = METHOD_NAMES.get(method_label)
        if method is None:
            continue

        body = sections[index + 1]
        for line in body.splitlines():
            line = line.strip()
            if not line.startswith("|") or line.startswith("|---"):
                continue

            parts = [part.strip() for part in line.strip("|").split("|")]
            if len(parts) < 2 or "`" not in parts[0]:
                continue

            constraint_name = parts[0].strip("`")
            rating = parts[1]
            match = re.fullmatch(r"(\d+)_constraint_\d+", constraint_name)
            if not match or rating not in {"A", "B", "C", "X"}:
                continue

            experiment_index = match.group(1)
            result.setdefault(experiment_index, {}).setdefault(method, Counter())[rating] += 1

    return result


def collect_human_evaluation_counts() -> dict[str, dict[str, Counter]]:
    totals: dict[str, dict[str, Counter]] = {}
    for path in HUMAN_EVALUATION_FILES:
        file_counts = parse_human_evaluation(path)
        for experiment_index, methods in file_counts.items():
            for method, counter in methods.items():
                totals.setdefault(experiment_index, {}).setdefault(method, Counter()).update(counter)
    return totals


def get_level_a_or_b_count(counts: dict[str, dict[str, Counter]], experiment_index: str, method: str) -> int:
    counter = counts.get(experiment_index, {}).get(method, Counter())
    return int(counter.get("A", 0) + counter.get("B", 0))


def get_ar_total_time_seconds(experiment_index: str) -> float:
    report = load_json(CONSTRAINTS_BASE / f"taxi_RQ1&2_{experiment_index}" / "AR+" / "analysis_report.json")
    return float(report.get("all_runs_time_stats", {}).get("total_time_from_logs", 0.0))


def get_single_run_dir(base_dir: Path, experiment_index: str) -> Path:
    experiment_dir = base_dir / f"taxi_RQ1&2_{experiment_index}"
    if not experiment_dir.exists():
        raise FileNotFoundError(f"Missing directory: {experiment_dir}")

    run_dirs = sorted(path for path in experiment_dir.iterdir() if path.is_dir())
    if len(run_dirs) != 1:
        raise ValueError(
            f"Expected exactly one run directory under {experiment_dir}, found {[path.name for path in run_dirs]}"
        )
    return run_dirs[0]


def sum_statistics_total_time(run_dir: Path) -> float:
    total_time = 0.0
    for template_dir in sorted(path for path in run_dir.iterdir() if path.is_dir() and path.name.startswith("template_")):
        stats_file = template_dir / "statistics.json"
        if not stats_file.exists():
            continue
        stats = load_json(stats_file)
        total_time += float(stats.get("total_time", 0.0))
    return total_time


def get_c2s_generation_time_seconds(experiment_index: str) -> float:
    inventor_run_dir = get_single_run_dir(INVENTOR_BASE, experiment_index)
    converter_run_dir = get_single_run_dir(CONVERTER_BASE, experiment_index)
    return sum_statistics_total_time(inventor_run_dir) + sum_statistics_total_time(converter_run_dir)


def get_c2s_instantiation_time_seconds(experiment_index: str) -> float:
    mapping = load_json(CONSTRAINTS_BASE / f"taxi_RQ1&2_{experiment_index}" / "C2S" / "mapping.json")
    return float(mapping.get("metadata", {}).get("total_time_seconds", 0.0))


def get_total_time_seconds(experiment_index: str, method: str) -> float:
    if method == "AR+":
        return get_ar_total_time_seconds(experiment_index)
    if method == "C2S":
        return get_c2s_generation_time_seconds(experiment_index) + get_c2s_instantiation_time_seconds(experiment_index)
    raise ValueError(f"Unsupported method: {method}")


def round_hours(seconds: float) -> float:
    return round(seconds / SECONDS_PER_HOUR, 2)


def build_method_summary(total_time_seconds: float, level_a_or_b_constraints: int) -> dict[str, Any]:
    total_time_hours = round_hours(total_time_seconds)
    if level_a_or_b_constraints <= 0:
        time_cost_per_level_a_or_b_constraint_hours = 0.0
    else:
        time_cost_per_level_a_or_b_constraint_hours = round(
            total_time_hours / level_a_or_b_constraints,
            2,
        )

    return {
        "total_time_hours": total_time_hours,
        "level_a_or_b_constraints": level_a_or_b_constraints,
        "time_cost_per_level_a_or_b_constraint_hours": time_cost_per_level_a_or_b_constraint_hours,
    }


def build_experiment_summary(
    experiment_index: str,
    human_evaluation_counts: dict[str, dict[str, Counter]],
) -> dict[str, Any]:
    summary: dict[str, Any] = {"experiment": experiment_index}
    for method in ["AR+", "C2S"]:
        level_a_or_b_constraints = get_level_a_or_b_count(human_evaluation_counts, experiment_index, method)
        total_time_seconds = get_total_time_seconds(experiment_index, method)
        summary[method] = build_method_summary(total_time_seconds, level_a_or_b_constraints)
    return summary


def build_average_summary(experiments: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {"experiment": "average"}
    count = len(experiments)

    for method in ["AR+", "C2S"]:
        total_time_hours_sum = sum(item[method]["total_time_hours"] for item in experiments)
        total_level_a_or_b_constraints = sum(item[method]["level_a_or_b_constraints"] for item in experiments)

        if total_level_a_or_b_constraints <= 0:
            time_cost_per_level_a_or_b_constraint_hours = 0.0
        else:
            time_cost_per_level_a_or_b_constraint_hours = round(
                total_time_hours_sum / total_level_a_or_b_constraints,
                2,
            )

        summary[method] = {
            "time_cost_per_run_hours": round(total_time_hours_sum / count, 2) if count else 0.0,
            "level_a_or_b_constraints": total_level_a_or_b_constraints,
            "time_cost_per_level_a_or_b_constraint_hours": time_cost_per_level_a_or_b_constraint_hours,
        }

    return summary


def build_output(experiment_indices: list[str]) -> dict[str, Any]:
    human_evaluation_counts = collect_human_evaluation_counts()
    experiments = [
        build_experiment_summary(experiment_index, human_evaluation_counts)
        for experiment_index in experiment_indices
    ]
    return {
        "average": build_average_summary(experiments),
        "experiments": experiments,
    }


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def print_table(data: dict[str, Any]) -> None:
    rows: list[tuple[str, str, str, str]] = []
    for method in ["AR+", "C2S"]:
        row = data["average"][method]
        rows.append(
            (
                method,
                f"{row['time_cost_per_run_hours']:.2f}",
                str(row["level_a_or_b_constraints"]),
                f"{row['time_cost_per_level_a_or_b_constraint_hours']:.2f}",
            )
        )

    headers = (
        "approach",
        "time_cost_per_run_hours",
        "level_a_or_b_constraints",
        "time_cost_per_level_a_or_b_constraint_hours",
    )
    widths = [max(len(headers[i]), max(len(row[i]) for row in rows)) for i in range(len(headers))]

    def format_row(values: tuple[str, str, str, str]) -> str:
        return "  ".join(value.ljust(widths[i]) for i, value in enumerate(values))

    print(format_row(headers))
    for row in rows:
        print(format_row(row))


def main() -> None:
    print("Generating RQ1 time table...")
    args = parse_args()
    data = build_output(args.experiments)
    write_json(args.output, data)
    print_table(data)
    print(f"\nWritten files:\n  {args.output}")
    print("\nDone.")


if __name__ == "__main__":
    main()
