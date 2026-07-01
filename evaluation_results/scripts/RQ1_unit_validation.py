#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch


ROOT = Path(__file__).resolve().parent.parent
HUMAN_EVALUATION_FILES = [
    ROOT / "results" / "RQ1" / "effectiveness_humanEvaluation" / "results" / "group1" / "aggregated.md",
    ROOT / "results" / "RQ1" / "effectiveness_humanEvaluation" / "results" / "group2" / "aggregated.md",
]
UNIT_VALIDATION_BASE = ROOT / "results" / "RQ1" / "effectiveness_unitValidation"
OUTPUT_BASE = UNIT_VALIDATION_BASE / "RQ1_unit_validation"

METHOD_LABELS = {
    "Method 1": "C2S",
    "Method 2": "AR+",
}
METHOD_ORDER = ["AR+", "C2S"]
LEVELS = ["A", "B", "C"]
LEVEL_LABELS = {
    "A": "Level A",
    "B": "Level B",
    "C": "Level C",
}

COLOR_A = "#69A1C4"
COLOR_B = "#FFE264"
COLOR_C = "#F4978E"
HATCH_TOTAL = "////"
LEVEL_COLORS = {
    "A": COLOR_A,
    "B": COLOR_B,
    "C": COLOR_C,
}
LEVEL_EDGES = {
    "A": "#3E6F8E",
    "B": "#B79B00",
    "C": "#C95046",
}

FIG_WIDTH = 7.2
FIG_HEIGHT = 2.6
FONT_SIZE_BASE = 16
FONT_SIZE_LABEL = 15
FONT_SIZE_LEGEND = 12
FONT_SIZE_VALUE = 17
BAR_WIDTH = 0.20
BAR_OFFSET = 0.22
VALUE_OFFSET = 1.0
OUTPUT_FORMATS = ["png", "pdf"]
OUTPUT_DPI = 300


def parse_ratings(path: Path) -> dict[str, dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    sections = re.split(r"^## (.+)$", text, flags=re.MULTILINE)
    ratings: dict[str, dict[str, str]] = {method: {} for method in METHOD_ORDER}

    for index in range(1, len(sections) - 1, 2):
        method = METHOD_LABELS.get(sections[index].strip())
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

            constraint_match = re.search(r"`([^`]+)`", parts[0])
            rating = parts[1]
            if constraint_match and rating in LEVELS:
                ratings[method][constraint_match.group(1)] = rating

    return ratings


def collect_ratings() -> dict[str, dict[str, str]]:
    ratings: dict[str, dict[str, str]] = {method: {} for method in METHOD_ORDER}
    for path in HUMAN_EVALUATION_FILES:
        file_ratings = parse_ratings(path)
        for method in METHOD_ORDER:
            ratings[method].update(file_ratings[method])
    return ratings


def load_unit_valid_constraints(method: str) -> set[str]:
    passed: set[str] = set()
    method_dir = UNIT_VALIDATION_BASE / method

    for path in sorted(method_dir.glob("taxi_RQ1&2_*.json")):
        run_match = re.search(r"taxi_RQ1&2_(\d+)$", path.stem)
        if not run_match:
            continue
        run_id = run_match.group(1)

        data = json.loads(path.read_text(encoding="utf-8"))
        for item in data.get("details", []):
            if item.get("overall_passed", False):
                passed.add(f"{run_id}_{item['constraint_name']}")

    return passed


def build_data() -> dict[str, Any]:
    ratings = collect_ratings()
    output: dict[str, Any] = {}

    for method in METHOD_ORDER:
        unit_valid = load_unit_valid_constraints(method)
        total_by_level: Counter[str] = Counter()
        unit_valid_by_level: Counter[str] = Counter()

        for constraint_id, level in ratings[method].items():
            total_by_level[level] += 1
            if constraint_id in unit_valid:
                unit_valid_by_level[level] += 1

        output[method] = {
            "by_level": {
                LEVEL_LABELS[level]: {
                    "total_constraints": total_by_level[level],
                    "unit_valid_constraints": unit_valid_by_level[level],
                }
                for level in LEVELS
            },
            "summary": {
                "total_constraints": sum(total_by_level.values()),
                "unit_valid_constraints": sum(unit_valid_by_level.values()),
            },
        }

    return output


def add_value_labels(ax: plt.Axes, bars: Any, values: list[int], color: str = "black") -> None:
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + VALUE_OFFSET,
            f"{value}",
            ha="center",
            va="bottom",
            fontsize=FONT_SIZE_VALUE,
            fontweight="bold",
            color=color,
            zorder=10,
        )


def plot_unit_validation(data: dict[str, Any]) -> list[Path]:
    plt.rcParams["font.size"] = FONT_SIZE_BASE
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["Times New Roman", "Times", "DejaVu Serif"]

    x = np.arange(len(METHOD_ORDER))
    offsets = np.array([-BAR_OFFSET, 0.0, BAR_OFFSET])

    fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))

    max_value = 0
    for level, offset in zip(LEVELS, offsets):
        totals = [
            data[method]["by_level"][LEVEL_LABELS[level]]["total_constraints"]
            for method in METHOD_ORDER
        ]
        unit_values = [
            data[method]["by_level"][LEVEL_LABELS[level]]["unit_valid_constraints"]
            for method in METHOD_ORDER
        ]
        max_value = max(max_value, *totals)
        total_bars = ax.bar(
            x + offset,
            totals,
            width=BAR_WIDTH,
            color="white",
            hatch=HATCH_TOTAL,
            edgecolor=LEVEL_EDGES[level],
            linewidth=1.7,
            zorder=2,
        )
        unit_bars = ax.bar(
            x + offset,
            unit_values,
            width=BAR_WIDTH,
            color=LEVEL_COLORS[level],
            edgecolor=LEVEL_EDGES[level],
            linewidth=1.4,
            label=LEVEL_LABELS[level],
            zorder=3,
        )
        ax.bar(
            x + offset,
            totals,
            width=BAR_WIDTH,
            color="none",
            edgecolor=LEVEL_EDGES[level],
            linewidth=1.7,
            zorder=4,
        )
        add_value_labels(ax, total_bars, totals, "black")

        different_unit_values = [
            unit_value if unit_value != total else -1
            for unit_value, total in zip(unit_values, totals)
        ]
        for bar, unit_value in zip(unit_bars, different_unit_values):
            if unit_value < 0:
                continue
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + VALUE_OFFSET,
                f"{unit_value}",
                ha="center",
                va="bottom",
                fontsize=FONT_SIZE_VALUE,
                fontweight="bold",
                color="black",
                zorder=11,
            )

    ax.set_xticks(x)
    ax.set_xticklabels(
        ["AR+", r"$\mathrm{C^2S}$"],
        fontsize=FONT_SIZE_LABEL,
        fontweight="bold",
    )
    ax.set_ylabel("# Constraints", fontsize=FONT_SIZE_LABEL, fontweight="bold")
    ax.set_ylim(0, max_value + 55)
    ax.grid(True, axis="y", alpha=0.18, linestyle="--", color="black", zorder=0)
    ax.set_axisbelow(True)

    total_handles: list[Patch] = []
    unit_handles: list[Patch] = []
    for level in LEVELS:
        total_handles.append(
            Patch(
                facecolor="white",
                edgecolor=LEVEL_EDGES[level],
                hatch=HATCH_TOTAL,
                linewidth=1.7,
                label=f"Level {level} Total",
            )
        )
        unit_handles.append(
            Patch(
                facecolor=LEVEL_COLORS[level],
                edgecolor=LEVEL_EDGES[level],
                linewidth=1.4,
                label=f"Level {level} Unit-valid",
            )
        )
    legend_handles = total_handles + unit_handles

    ax.legend(
        handles=legend_handles,
        loc="upper right",
        ncol=2,
        prop={"size": FONT_SIZE_LEGEND, "weight": "bold"},
        framealpha=0.9,
        borderpad=0.3,
        labelspacing=0.25,
        columnspacing=0.8,
        handletextpad=0.5,
    )

    plt.tight_layout(rect=[0, 0, 1, 1])

    written: list[Path] = []
    OUTPUT_BASE.parent.mkdir(parents=True, exist_ok=True)
    for fmt in OUTPUT_FORMATS:
        output_file = OUTPUT_BASE.with_suffix(f".{fmt}")
        plt.savefig(output_file, dpi=OUTPUT_DPI, bbox_inches="tight", format=fmt)
        written.append(output_file)

    plt.close()
    return written


def main() -> None:
    data = build_data()
    written = plot_unit_validation(data)

    print(json.dumps(data, indent=2))
    print("\nWritten files:")
    for path in written:
        print(f"  {path}")


if __name__ == "__main__":
    main()
