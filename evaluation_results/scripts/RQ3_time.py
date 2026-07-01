#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parent.parent
EVALUATION_BASE = PROJECT_ROOT / "results" / "RQ3" / "synthesisTime"
CONSTRAINTS_BASE = PROJECT_ROOT / "constraints"
INVENTOR_BASE = PROJECT_ROOT / "outputs" / "invention" / "inventor"
CONVERTER_BASE = PROJECT_ROOT / "outputs" / "invention" / "converter"

CONFIG_ORDER = [
    "C2S_0000",
    "C2S_1000",
    "C2S_0100",
    "C2S_0010",
    "C2S_0001",
    "C2S_1111",
]

SECONDS_PER_HOUR = 3600.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Summarize ICSE RQ3 time metrics for all C2S configurations."
    )
    parser.add_argument(
        "--experiments",
        nargs="*",
        default=["1", "2", "3", "4", "5"],
        help="Experiment indices to summarize, default: 1 2 3 4 5",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=EVALUATION_BASE / "RQ3_time.json",
        help="Output JSON path, default: results/RQ3/synthesisTime/RQ3_time.json",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_config_dir(base_dir: Path, experiment_index: str, method: str) -> Path:
    experiment_dir = base_dir / f"taxi_RQ3_{experiment_index}"
    if not experiment_dir.exists():
        raise FileNotFoundError(f"Missing directory: {experiment_dir}")

    suffix = method.split("_", 1)[1]
    matches = sorted(
        path
        for path in experiment_dir.iterdir()
        if path.is_dir() and not path.name.startswith("_") and path.name.endswith(f"_{suffix}")
    )
    if len(matches) != 1:
        raise ValueError(
            f"Expected exactly one config directory for suffix {suffix} under {experiment_dir}, "
            f"found {[p.name for p in matches]}"
        )
    return matches[0]


def sum_statistics_total_time(config_dir: Path) -> float:
    total_time = 0.0
    for template_dir in sorted(
        path for path in config_dir.iterdir() if path.is_dir() and path.name.startswith("template_")
    ):
        stats_file = template_dir / "statistics.json"
        if not stats_file.exists():
            continue
        stats = load_json(stats_file)
        total_time += float(stats.get("total_time", 0.0))
    return total_time


def get_c2s_generation_time_seconds(experiment_index: str, method: str) -> float:
    inventor_config_dir = get_config_dir(INVENTOR_BASE, experiment_index, method)
    converter_config_dir = get_config_dir(CONVERTER_BASE, experiment_index, method)
    return sum_statistics_total_time(inventor_config_dir) + sum_statistics_total_time(converter_config_dir)


def get_c2s_instantiation_time_seconds(experiment_index: str, method: str) -> float:
    mapping = load_json(CONSTRAINTS_BASE / f"taxi_RQ3_{experiment_index}" / method / "mapping.json")
    return float(mapping.get("metadata", {}).get("total_time_seconds", 0.0))


def get_c2s_total_time_seconds(experiment_index: str, method: str) -> float:
    return get_c2s_generation_time_seconds(experiment_index, method) + get_c2s_instantiation_time_seconds(
        experiment_index,
        method,
    )


def round_hours(seconds: float) -> float:
    return round(seconds / SECONDS_PER_HOUR, 2)


def build_method_summary(total_time_seconds: float) -> dict[str, Any]:
    return {"total_time_hours": round_hours(total_time_seconds)}


def build_experiment_summary(experiment_index: str) -> dict[str, Any]:
    summary: dict[str, Any] = {"experiment": experiment_index}
    for method in CONFIG_ORDER:
        summary[method] = build_method_summary(get_c2s_total_time_seconds(experiment_index, method))
    return summary


def build_average_summary(experiments: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {"experiment": "average"}
    count = len(experiments)

    for method in CONFIG_ORDER:
        avg_total_time_hours = (
            sum(item[method]["total_time_hours"] for item in experiments) / count if count else 0.0
        )
        summary[method] = {"total_time_hours": round(avg_total_time_hours, 2)}

    return summary


def build_output(experiment_indices: list[str]) -> dict[str, Any]:
    experiments = [build_experiment_summary(idx) for idx in experiment_indices]
    return {
        "average": build_average_summary(experiments),
        "experiments": experiments,
    }


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def print_table(data: dict[str, Any]) -> None:
    rows = [data["average"], *data["experiments"]]
    table_rows: list[tuple[str, str, str]] = []
    for item in rows:
        for method in CONFIG_ORDER:
            row = item[method]
            table_rows.append(
                (
                    str(item["experiment"]),
                    method,
                    str(row["total_time_hours"]),
                )
            )

    headers = ("experiment", "method", "total_time_hours")
    widths = [
        max(len(headers[i]), max(len(row[i]) for row in table_rows))
        for i in range(len(headers))
    ]

    def format_row(values: tuple[str, str, str]) -> str:
        return "  ".join(value.ljust(widths[i]) for i, value in enumerate(values))

    print(format_row(headers))
    for row in table_rows:
        print(format_row(row))


def main() -> None:
    print("Generating RQ3 time results...")
    args = parse_args()
    output = build_output(args.experiments)
    write_json(args.output, output)
    print_table(output)
    print(f"\nWritten files:\n  {args.output}")
    print("\nDone.")


if __name__ == "__main__":
    main()
