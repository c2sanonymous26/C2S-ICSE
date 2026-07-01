#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parent.parent
EVALUATION_BASE = PROJECT_ROOT / "results" / "RQ3" / "constraintQuantity"
CONSTRAINTS_BASE = PROJECT_ROOT / "constraints"

CONFIG_ORDER = [
    "C2S_0000",
    "C2S_1000",
    "C2S_0100",
    "C2S_0010",
    "C2S_0001",
    "C2S_1111",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Summarize ICSE RQ3 quantity results."
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
        default=EVALUATION_BASE / "RQ3_number.json",
        help="Output JSON path, default: results/RQ3/constraintQuantity/RQ3_number.json",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_constraint_name(name: str) -> str:
    if name.startswith("template_"):
        return "constraint_" + name.split("_", 1)[1]
    return name


def constraint_name_from_mapping_item(item: dict[str, Any]) -> str | None:
    source_template_id = item.get("source_template_id")
    if source_template_id is not None:
        return f"constraint_{int(source_template_id)}"

    original_name = item.get("original_name")
    if original_name:
        return normalize_constraint_name(str(original_name))

    constraint_id = item.get("constraint_id")
    if constraint_id is not None:
        return f"constraint_{int(constraint_id)}"

    return None


def load_successful_constraints(experiment_index: str, method: str) -> set[str]:
    mapping = load_json(CONSTRAINTS_BASE / f"taxi_RQ3_{experiment_index}" / method / "mapping.json")
    successful: set[str] = set()
    for item in mapping.get("constraints", []):
        if item.get("status") in {"solve_success", "validate_success"}:
            constraint_name = constraint_name_from_mapping_item(item)
            if constraint_name:
                successful.add(constraint_name)
    return successful


def get_unique_constraints(experiment_index: str, method: str) -> set[str]:
    successful = load_successful_constraints(experiment_index, method)
    duplicates = load_json(EVALUATION_BASE / experiment_index / f"duplicates_{method}.json")

    constraints_in_classes: set[str] = set()
    representatives: set[str] = set()

    for eq_class in duplicates.get("equivalence_classes", []):
        constraints = eq_class.get("constraints", [])
        if not constraints:
            continue
        constraints_in_classes.update(constraints)
        for constraint_name in constraints:
            if constraint_name in successful:
                representatives.add(constraint_name)
                break

    return (successful - constraints_in_classes) | representatives


def get_unit_valid_constraints(experiment_index: str, method: str) -> set[str]:
    successful = load_successful_constraints(experiment_index, method)
    validity = load_json(EVALUATION_BASE / experiment_index / f"semantic_check_{method}.json")
    passed = {
        item["constraint_name"]
        for item in validity.get("details", [])
        if item.get("overall_passed", False)
    }
    return successful & passed


def get_total_count(experiment_index: str, method: str) -> int:
    mapping = load_json(CONSTRAINTS_BASE / f"taxi_RQ3_{experiment_index}" / method / "mapping.json")
    metadata = mapping.get("metadata", {})
    return int(metadata.get("total_extracted_constraints", 0))


def build_method_summary(experiment_index: str, method: str) -> dict[str, int]:
    unique_constraints = get_unique_constraints(experiment_index, method)
    unit_valid_constraints = get_unit_valid_constraints(experiment_index, method)
    return {
        "total_constraints": get_total_count(experiment_index, method),
        "unique_constraints": len(unique_constraints),
        "unit_valid_constraints": len(unit_valid_constraints),
        "qualified_constraints": len(unique_constraints & unit_valid_constraints),
    }


def build_experiment_summary(experiment_index: str) -> dict[str, Any]:
    summary: dict[str, Any] = {"experiment": experiment_index}
    for method in CONFIG_ORDER:
        summary[method] = build_method_summary(experiment_index, method)
    return summary


def build_average_summary(experiments: list[dict[str, Any]]) -> dict[str, Any]:
    fields = [
        "total_constraints",
        "unique_constraints",
        "unit_valid_constraints",
        "qualified_constraints",
    ]
    summary: dict[str, Any] = {"experiment": "average"}
    count = len(experiments)

    for method in CONFIG_ORDER:
        summary[method] = {}
        for field in fields:
            avg = sum(item[method][field] for item in experiments) / count if count else 0.0
            summary[method][field] = round(avg, 2)

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
    table_rows: list[tuple[str, str, str, str, str, str]] = []
    for item in rows:
        for method in CONFIG_ORDER:
            row = item[method]
            table_rows.append(
                (
                    str(item["experiment"]),
                    method,
                    str(row["total_constraints"]),
                    str(row["unique_constraints"]),
                    str(row["unit_valid_constraints"]),
                    str(row["qualified_constraints"]),
                )
            )

    headers = (
        "experiment",
        "method",
        "total_constraints",
        "unique_constraints",
        "unit_valid_constraints",
        "qualified_constraints",
    )
    widths = [
        max(len(headers[i]), max(len(row[i]) for row in table_rows))
        for i in range(len(headers))
    ]

    def format_row(values: tuple[str, ...]) -> str:
        return "  ".join(value.ljust(widths[i]) for i, value in enumerate(values))

    print(format_row(headers))
    for row in table_rows:
        print(format_row(row))


def main() -> None:
    print("Generating RQ3 quantity results...")
    args = parse_args()
    output = build_output(args.experiments)
    write_json(args.output, output)
    print_table(output)
    print(f"\nWritten files:\n  {args.output}")
    print("\nDone.")


if __name__ == "__main__":
    main()
