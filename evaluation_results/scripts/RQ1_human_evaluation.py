#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
from pathlib import Path
import re

import matplotlib

matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parent.parent
RESULT_FILES = [
    ROOT / "results" / "RQ1" / "effectiveness_humanEvaluation" / "results" / "group1" / "aggregated.md",
    ROOT / "results" / "RQ1" / "effectiveness_humanEvaluation" / "results" / "group2" / "aggregated.md",
]
OUTPUT_BASE = ROOT / "results" / "RQ1" / "effectiveness_humanEvaluation" / "RQ1_human_evaluation"

COLOR_A = "#69A1C4"
COLOR_B = "#FFE264"
COLOR_C = "#F4978E"
COLOR_NOT_EVALUATED = "#666565"

FIG_WIDTH = 10
FIG_HEIGHT = 5.1

FONT_SIZE_BASE = 16
FONT_SIZE_TITLE = 20
FONT_SIZE_LEGEND = 15
FONT_SIZE_PCT = 20
FONT_SIZE_FOOTNOTE = 17

OUTPUT_FORMATS = ["png", "pdf"]
OUTPUT_DPI = 300

NO_LEVEL_CENTER_DEGREES = 225


def adjusted_percentages(sizes: list[int], total: int, decimals: int = 1) -> list[float]:
    if total <= 0:
        return [0.0 for _ in sizes]

    scale = 10**decimals
    exact_units = [size / total * 100 * scale for size in sizes]
    floor_units = [int(np.floor(value)) for value in exact_units]
    target_units = 100 * scale
    remainder_units = target_units - sum(floor_units)

    order = sorted(
        range(len(sizes)),
        key=lambda index: (exact_units[index] - floor_units[index], sizes[index]),
        reverse=True,
    )
    for index in order[:remainder_units]:
        floor_units[index] += 1

    return [value / scale for value in floor_units]


def parse_aggregated(path: Path) -> dict[str, Counter]:
    text = path.read_text(encoding="utf-8")
    sections = re.split(r"^## (.+)$", text, flags=re.MULTILINE)
    result: dict[str, Counter] = {}

    for index in range(1, len(sections) - 1, 2):
        method = sections[index].strip()
        body = sections[index + 1]
        ratings = Counter()

        for line in body.splitlines():
            line = line.strip()
            if not line.startswith("|") or line.startswith("|---"):
                continue
            parts = [part.strip() for part in line.strip("|").split("|")]
            if len(parts) < 2 or "`" not in parts[0]:
                continue
            rating = parts[1]
            if rating in {"A", "B", "C", "X"}:
                ratings[rating] += 1

        if ratings:
            result[method] = ratings

    return result


def collect_ratings() -> dict[str, Counter]:
    totals: dict[str, Counter] = {}
    for path in RESULT_FILES:
        for method, ratings in parse_aggregated(path).items():
            totals.setdefault(method, Counter()).update(ratings)
    return totals


def start_angle_with_no_level(sizes: list[int]) -> float:
    evaluated_count = sum(sizes[:-1])
    total_count = sum(sizes)
    no_level_count = sizes[-1]
    return (
        NO_LEVEL_CENTER_DEGREES
        - (evaluated_count / total_count) * 360
        - (no_level_count / total_count) * 180
    )


def draw_pie(
    ax: plt.Axes,
    counter: Counter,
    title: str,
) -> None:
    rating_order = ["A", "B", "C"]
    sizes = [counter.get(rating, 0) for rating in rating_order]
    colors = [COLOR_A, COLOR_B, COLOR_C]

    no_level_count = counter.get("X", 0)
    if no_level_count > 0:
        sizes.append(no_level_count)
        colors.append(COLOR_NOT_EVALUATED)
        startangle = start_angle_with_no_level(sizes)
    else:
        startangle = 35

    total_constraints = sum(sizes)
    display_pcts = adjusted_percentages(sizes, total_constraints)

    wedges, _ = ax.pie(
        sizes,
        labels=None,
        colors=colors,
        startangle=startangle,
        wedgeprops={"edgecolor": "white", "linewidth": 1.0},
        radius=1.0,
    )

    inside_threshold = 0.05

    for wedge, size, color, pct in zip(wedges, sizes, colors, display_pcts):
        angle = (wedge.theta1 + wedge.theta2) / 2
        angle_rad = np.deg2rad(angle)

        if color == COLOR_NOT_EVALUATED:
            ax.text(
                1.14 * np.cos(angle_rad),
                1.14 * np.sin(angle_rad),
                f"{size} ({pct:.1f}%)*",
                ha="left" if np.cos(angle_rad) >= 0 else "right",
                va="center",
                fontsize=FONT_SIZE_PCT,
                fontweight="bold",
                color="black",
            )
            continue

        if size / total_constraints >= inside_threshold:
            ax.text(
                0.62 * np.cos(angle_rad),
                0.62 * np.sin(angle_rad),
                f"{size}\n({pct:.1f}%)",
                ha="center",
                va="center",
                fontsize=FONT_SIZE_PCT,
                fontweight="bold",
                color="black",
            )
        else:
            ax.text(
                1.08 * np.cos(angle_rad),
                1.08 * np.sin(angle_rad),
                f"{size} ({pct:.1f}%)",
                ha="left" if np.cos(angle_rad) >= 0 else "right",
                va="center",
                fontsize=FONT_SIZE_PCT,
                fontweight="bold",
                color="black",
            )

    ax.set_xlim(-1.8, 1.8)
    ax.set_ylim(-1.18, 1.18)
    ax.set_title(
        f"{title}  (# constraints = {total_constraints})",
        fontsize=FONT_SIZE_TITLE,
        fontweight="bold",
        pad=4,
    )


def plot_effectiveness() -> tuple[dict[str, Counter], list[Path]]:
    plt.rcParams["font.size"] = FONT_SIZE_BASE
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["Times New Roman", "Times", "DejaVu Serif"]

    totals = collect_ratings()
    c2s = totals.get("Method 1", Counter())
    ar_plus = totals.get("Method 2", Counter())

    fig, axes = plt.subplots(1, 2, figsize=(FIG_WIDTH, FIG_HEIGHT))
    fig.subplots_adjust(wspace=-0.1, bottom=0.18, left=0.02, right=0.90, top=0.88)

    draw_pie(
        axes[0],
        c2s,
        r"$\mathrm{C^2S}$",
    )
    draw_pie(
        axes[1],
        ar_plus,
        r"$\mathrm{AR+}$",
    )

    left_pos = axes[0].get_position()
    note_x = left_pos.x0
    note_y = left_pos.y0 - 0.01
    note = "* One constraint was not assigned a final level because no consensus was reached."
    note_text = fig.text(
        note_x,
        note_y,
        note,
        ha="left",
        va="top",
        fontsize=FONT_SIZE_FOOTNOTE,
        fontweight="bold",
        transform=fig.transFigure,
    )

    legend_handles = [
        mpatches.Patch(color=COLOR_A, label="Level A"),
        mpatches.Patch(color=COLOR_B, label="Level B"),
        mpatches.Patch(color=COLOR_C, label="Level C"),
        mpatches.Patch(color=COLOR_NOT_EVALUATED, label="No Level"),
    ]
    fig.legend(
        handles=legend_handles,
        loc="center left",
        ncol=1,
        prop={"size": FONT_SIZE_LEGEND, "weight": "bold"},
        framealpha=0.9,
        bbox_to_anchor=(0.82, 0.52),
        bbox_transform=fig.transFigure,
    )

    OUTPUT_BASE.parent.mkdir(parents=True, exist_ok=True)
    written_files: list[Path] = []
    for fmt in OUTPUT_FORMATS:
        output_path = OUTPUT_BASE.with_suffix(f".{fmt}")
        plt.savefig(output_path, dpi=OUTPUT_DPI, format=fmt, bbox_inches="tight", pad_inches=0.03)
        written_files.append(output_path)
    plt.close()

    _ = note_text
    return totals, written_files


def print_summary(totals: dict[str, Counter]) -> None:
    for method in ["Method 1", "Method 2"]:
        counter = totals.get(method, Counter())
        effective = counter.get("A", 0) + counter.get("B", 0) + counter.get("C", 0)
        total = effective + counter.get("X", 0)
        print(f"{method}\t{dict(counter)}\teffective={effective}\ttotal={total}")


def main() -> None:
    totals, written_files = plot_effectiveness()
    print_summary(totals)
    print("\nWritten files:")
    for path in written_files:
        print(f"  {path}")


if __name__ == "__main__":
    main()
