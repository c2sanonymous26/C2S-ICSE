#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from statistics import mean, stdev
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from sklearn.metrics import average_precision_score


PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_DATA_DIR = PROJECT_ROOT / "inputs" / "taxi" / "data"
OUTPUT_CHECK_DIR = PROJECT_ROOT / "outputs" / "check"
CONSTRAINTS_DIR = PROJECT_ROOT / "constraints"
EVALUATION_DIR = PROJECT_ROOT / "results" / "RQ2"

SCENARIO = "taxi"
EXPERIMENTS = [f"{SCENARIO}_RQ1&2_{index}" for index in range(1, 6)]
METHODS = ["C2S", "AR+"]
PERTURBATION_PROBS = ["5000_pp_0.01", "5000_pp_0.05", "5000_pp_0.1"]

COLOR_C2S = "#69A1C4"
COLOR_ARPLUS = "#F07167"
RANGE_COLOR = "#6B6B6B"
HATCH_C2S = "\\\\"
HATCH_ARPLUS = "///"

FIG_WIDTH = 10
FIG_HEIGHT = 4
FONT_SIZE_BASE = 16
FONT_SIZE_LABEL = 16
FONT_SIZE_LEGEND = 12
FONT_SIZE_VALUE = 18
BAR_WIDTH = 0.3
X_MAX = 1.0
VALUE_LABEL_OFFSET = 0.005
RANGE_LINE_OFFSET = 0.055
RANGE_LINE_WIDTH = 1.4
RANGE_CAP_HALF_HEIGHT = 0.045
MEAN_MARKER_SIZE = 34
OUTPUT_FORMATS = ["png", "pdf"]
OUTPUT_DPI = 300

OUTPUT_FIGURE_BASE = EVALUATION_DIR / "RQ2_perturbation_signal"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate the RQ2 perturbation-signal figure from results/RQ2. "
            "Use --regenerate-results to regenerate all per-sample and average results first. "
            "This script directly uses the perturbed-context check results without removing "
            "violations already present in the clean 5000 dataset."
        )
    )
    parser.add_argument(
        "--regenerate-results",
        action="store_true",
        help="Regenerate all results under results/RQ2 before plotting.",
    )
    return parser.parse_args()


def load_json(path: Path) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def read_incs_file(path: Path) -> list[tuple[str, dict[str, int]]]:
    rows: list[tuple[str, dict[str, int]]] = []
    if not path.exists():
        raise FileNotFoundError(f"Missing incs file: {path}")

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


def group_incs_by_constraint(
    perturbation_incs: list[tuple[str, dict[str, int]]],
) -> dict[str, list[dict[str, int]]]:
    grouped: dict[str, list[dict[str, int]]] = {}
    for constraint_name, assignment in perturbation_incs:
        grouped.setdefault(constraint_name, []).append(assignment)
    return grouped


def extract_suspicious_id_freq(assignments: list[dict[str, int]]) -> dict[int, int]:
    freq: dict[int, int] = {}
    for assignment in assignments:
        for data_id in assignment.values():
            freq[data_id] = freq.get(data_id, 0) + 1
    return freq


def calculate_auprc(
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


def calculate_sample_std(values: list[float]) -> float:
    if len(values) <= 1:
        return 0.0
    return float(stdev(values))


def build_single_result(
    experiment_name: str,
    method_name: str,
    perturbation_prob: str,
    perturbation_id: str,
) -> dict[str, Any]:
    check_base = OUTPUT_CHECK_DIR / experiment_name / method_name
    constraints_py_dir = CONSTRAINTS_DIR / experiment_name / method_name / "py"
    data_dir = INPUT_DATA_DIR / perturbation_prob / perturbation_id

    perturbation_incs_file = check_base / perturbation_prob / f"{perturbation_id}_perturbed" / "incs.csv"
    perturbed_json = data_dir / "perturbed.json"
    perturbed_csv = data_dir / "perturbed.csv"

    if not perturbation_incs_file.exists():
        raise FileNotFoundError(f"Missing perturbation incs file: {perturbation_incs_file}")
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
            raise ValueError(f"Unsupported constraint name in current layout: {constraint_name}")
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
        auprc_value = calculate_auprc(actual_perturbation_ids, suspicious_id_freq_dict, all_data_ids)

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
        "AUPRC": calculate_auprc(overall_actual_perturbation_ids, freq_sum_scores, all_data_ids),
        "actual_perturbation_count": len(overall_actual_perturbation_ids),
        "suspicious_count": len(freq_sum_scores),
    }

    perturbation_data_name = f"{perturbation_prob}/{perturbation_id}"
    return {
        "metadata": {
            "scenario": SCENARIO,
            "constraint_dir": str((CONSTRAINTS_DIR / experiment_name / method_name).relative_to(PROJECT_ROOT)),
            "check_dir": str(check_base.relative_to(PROJECT_ROOT)),
            "perturbation_data_name": perturbation_data_name,
            "pure_perturbation_incs_count": len(perturbation_incs),
            "uses_perturbed_data_incs_directly": True,
        },
        "overall_results": overall_results,
        "per_constraint_results": per_constraint_results,
    }


def round_result(result: dict[str, Any]) -> dict[str, Any]:
    def transform(obj: Any) -> Any:
        if isinstance(obj, dict):
            return {
                k: transform(v)
                for k, v in obj.items()
                if k not in {"actual_perturbation_ids", "suspicious_id_freq_dict"}
            }
        if isinstance(obj, list):
            return [transform(item) for item in obj]
        if isinstance(obj, float):
            return float(f"{obj:.6f}")
        return obj

    return transform(result)


def build_average_result(
    experiment_name: str,
    method_name: str,
    perturbation_prob: str,
    all_results: list[dict[str, Any]],
) -> dict[str, Any]:
    total_samples = len(all_results)
    if total_samples == 0:
        raise ValueError("No results provided for averaging")

    constraint_names = sorted(
        {
            constraint_name
            for result in all_results
            for constraint_name in result["per_constraint_results"].keys()
        }
    )

    positive_ratios = []
    for result in all_results:
        perturbation_prob, perturbation_id = result["metadata"]["perturbation_data_name"].split("/", 1)
        perturbed_csv = INPUT_DATA_DIR / perturbation_prob / perturbation_id / "perturbed.csv"
        total_rows = len(load_all_data_ids(perturbed_csv))
        actual_perturbation_count = result["overall_results"]["actual_perturbation_count"]
        positive_ratios.append(actual_perturbation_count / total_rows if total_rows else 0.0)
    baseline_auprc = mean(positive_ratios) if positive_ratios else 0.0

    per_constraint_averages: dict[str, Any] = {}
    for constraint_name in constraint_names:
        incs_values: list[float] = []
        auprc_values: list[float] = []
        actual_perturbation_counts: list[float] = []
        suspicious_counts: list[float] = []
        occurrence_count = 0

        for result in all_results:
            constraint_result = result["per_constraint_results"].get(constraint_name)
            if constraint_result is None:
                incs_values.append(0.0)
                auprc_values.append(baseline_auprc)
                actual_perturbation_counts.append(0.0)
                suspicious_counts.append(0.0)
                continue

            occurrence_count += 1
            incs_values.append(float(constraint_result["incs"]))
            auprc_values.append(float(constraint_result["AUPRC"]))
            actual_perturbation_counts.append(float(constraint_result["actual_perturbation_count"]))
            suspicious_counts.append(float(constraint_result["suspicious_count"]))

        per_constraint_averages[constraint_name] = {
            "incs": {"mean": mean(incs_values), "std": calculate_sample_std(incs_values)},
            "AUPRC": {"mean": mean(auprc_values), "std": calculate_sample_std(auprc_values)},
            "actual_perturbation_count": {
                "mean": mean(actual_perturbation_counts),
                "std": calculate_sample_std(actual_perturbation_counts),
            },
            "suspicious_count": {
                "mean": mean(suspicious_counts),
                "std": calculate_sample_std(suspicious_counts),
            },
            "occurrence/total_samples": f"{occurrence_count}/{total_samples}",
        }

    involved_constraint_counts = [float(item["overall_results"]["involved_constraint_count"]) for item in all_results]
    incs_values = [float(item["overall_results"]["incs"]) for item in all_results]
    auprc_values = [float(item["overall_results"]["AUPRC"]) for item in all_results]
    actual_perturbation_counts = [float(item["overall_results"]["actual_perturbation_count"]) for item in all_results]
    suspicious_counts = [float(item["overall_results"]["suspicious_count"]) for item in all_results]

    overall_average_results = {
        "total_samples": total_samples,
        "involved_constraint_count": {
            "mean": mean(involved_constraint_counts),
            "std": calculate_sample_std(involved_constraint_counts),
        },
        "incs": {"mean": mean(incs_values), "std": calculate_sample_std(incs_values)},
        "AUPRC": {"mean": mean(auprc_values), "std": calculate_sample_std(auprc_values)},
        "actual_perturbation_count": {
            "mean": mean(actual_perturbation_counts),
            "std": calculate_sample_std(actual_perturbation_counts),
        },
        "suspicious_count": {
            "mean": mean(suspicious_counts),
            "std": calculate_sample_std(suspicious_counts),
        },
    }

    return {
        "metadata": {
            "scenario": SCENARIO,
            "constraint_dir": str((CONSTRAINTS_DIR / experiment_name / method_name).relative_to(PROJECT_ROOT)),
            "check_dir": str((OUTPUT_CHECK_DIR / experiment_name / method_name).relative_to(PROJECT_ROOT)),
            "perturbation_data_prob": perturbation_prob,
        },
        "overall_average_results": round_result(overall_average_results),
        "per_constraint_averages": round_result(per_constraint_averages),
    }


def collect_perturbation_ids(experiment_name: str, method_name: str, perturbation_prob: str) -> list[str]:
    perturbation_prob_dir = OUTPUT_CHECK_DIR / experiment_name / method_name / perturbation_prob
    if not perturbation_prob_dir.exists():
        raise FileNotFoundError(f"Missing check perturbation-probability directory: {perturbation_prob_dir}")
    return sorted(
        item.name.removesuffix("_perturbed")
        for item in perturbation_prob_dir.iterdir()
        if item.is_dir() and item.name.endswith("_perturbed")
    )


def regenerate_all_results() -> list[Path]:
    written_files: list[Path] = []
    print("Generating RQ2 perturbation-signal results...")

    for experiment_name in EXPERIMENTS:
        for method_name in METHODS:
            for perturbation_prob in PERTURBATION_PROBS:
                perturbation_ids = collect_perturbation_ids(experiment_name, method_name, perturbation_prob)
                sample_results: list[dict[str, Any]] = []
                for perturbation_id in perturbation_ids:
                    result = build_single_result(
                        experiment_name=experiment_name,
                        method_name=method_name,
                        perturbation_prob=perturbation_prob,
                        perturbation_id=perturbation_id,
                    )
                    sample_results.append(result)

                    sample_output = (
                        EVALUATION_DIR
                        / experiment_name
                        / method_name
                        / perturbation_prob
                        / perturbation_id
                        / "results.json"
                    )
                    write_json(sample_output, round_result(result))
                    written_files.append(sample_output)

                average_output = (
                    EVALUATION_DIR
                    / experiment_name
                    / method_name
                    / perturbation_prob
                    / "average"
                    / "results.json"
                )
                write_json(
                    average_output,
                    build_average_result(
                        experiment_name=experiment_name,
                        method_name=method_name,
                        perturbation_prob=perturbation_prob,
                        all_results=sample_results,
                    ),
                )
                written_files.append(average_output)

                print(
                    f"{experiment_name}  {method_name:<3}  {perturbation_prob:<12}  "
                    f"samples={len(sample_results)}"
                )

    return written_files


def load_plot_data() -> dict[str, dict[str, list[float]]]:
    plot_data: dict[str, dict[str, list[float]]] = {method: {} for method in METHODS}
    for method_name in METHODS:
        for perturbation_prob in PERTURBATION_PROBS:
            values: list[float] = []
            for experiment_name in EXPERIMENTS:
                path = (
                    EVALUATION_DIR
                    / experiment_name
                    / method_name
                    / perturbation_prob
                    / "average"
                    / "results.json"
                )
                if not path.exists():
                    raise FileNotFoundError(
                        f"Missing required file: {path}\n"
                        "Please rerun with --regenerate-results."
                    )
                payload = load_json(path)
                values.append(float(payload["overall_average_results"]["AUPRC"]["mean"]))
            plot_data[method_name][perturbation_prob] = values
    return plot_data


def draw_range_indicator(ax: plt.Axes, mean_value: float, min_value: float, max_value: float, y_pos: float) -> None:
    ax.hlines(y_pos, min_value, max_value, colors=RANGE_COLOR, linewidth=RANGE_LINE_WIDTH, zorder=4)
    ax.vlines(
        [min_value, max_value],
        y_pos - RANGE_CAP_HALF_HEIGHT,
        y_pos + RANGE_CAP_HALF_HEIGHT,
        colors=RANGE_COLOR,
        linewidth=RANGE_LINE_WIDTH,
        zorder=4,
    )
    ax.scatter(
        [mean_value],
        [y_pos],
        s=MEAN_MARKER_SIZE,
        facecolors="white",
        edgecolors=RANGE_COLOR,
        linewidths=1.2,
        zorder=5,
    )


def plot_summary(plot_data: dict[str, dict[str, list[float]]]) -> list[Path]:
    plt.rcParams["font.size"] = FONT_SIZE_BASE
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["Times New Roman", "Times", "DejaVu Serif"]

    perturbation_prob_labels = ["1%", "5%", "10%"]
    perturbation_prob_keys = ["5000_pp_0.01", "5000_pp_0.05", "5000_pp_0.1"]
    y = np.arange(len(perturbation_prob_keys))
    offset = BAR_WIDTH / 2

    c2s_means = [mean(plot_data["C2S"][perturbation_prob]) for perturbation_prob in perturbation_prob_keys]
    ar_means = [mean(plot_data["AR+"][perturbation_prob]) for perturbation_prob in perturbation_prob_keys]
    c2s_mins = [min(plot_data["C2S"][perturbation_prob]) for perturbation_prob in perturbation_prob_keys]
    c2s_maxs = [max(plot_data["C2S"][perturbation_prob]) for perturbation_prob in perturbation_prob_keys]
    ar_mins = [min(plot_data["AR+"][perturbation_prob]) for perturbation_prob in perturbation_prob_keys]
    ar_maxs = [max(plot_data["AR+"][perturbation_prob]) for perturbation_prob in perturbation_prob_keys]

    fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))

    bars_c2s = ax.barh(
        y + offset,
        c2s_means,
        height=BAR_WIDTH,
        color=COLOR_C2S,
        hatch=HATCH_C2S,
        edgecolor="white",
        linewidth=0.8,
        label=r"$\mathrm{C^2S}$",
        zorder=3,
    )
    bars_ar = ax.barh(
        y - offset,
        ar_means,
        height=BAR_WIDTH,
        color=COLOR_ARPLUS,
        hatch=HATCH_ARPLUS,
        edgecolor="white",
        linewidth=0.8,
        label=r"$\mathrm{AR+}$",
        zorder=3,
    )

    for bar, mean_value, min_value, max_value in zip(bars_c2s, c2s_means, c2s_mins, c2s_maxs):
        draw_range_indicator(ax, mean_value, min_value, max_value, bar.get_y() + bar.get_height() + RANGE_LINE_OFFSET)
    for bar, mean_value, min_value, max_value in zip(bars_ar, ar_means, ar_mins, ar_maxs):
        draw_range_indicator(ax, mean_value, min_value, max_value, bar.get_y() - RANGE_LINE_OFFSET)

    for bar in list(bars_c2s) + list(bars_ar):
        width = bar.get_width()
        ax.text(
            width + VALUE_LABEL_OFFSET,
            bar.get_y() + bar.get_height() / 2,
            f"{width:.3f}",
            ha="left",
            va="center",
            fontsize=FONT_SIZE_VALUE,
            color="black",
            fontweight="bold",
        )

    ax.set_yticks(y)
    ax.set_yticklabels(perturbation_prob_labels, fontsize=FONT_SIZE_BASE, fontweight="bold")
    ax.set_ylabel(r"$P_{p}$ (Perturbation Probability)", fontsize=FONT_SIZE_LABEL, fontweight="bold")
    ax.set_xlabel("PSS (Perturbation Signaling Score)", fontsize=FONT_SIZE_LABEL, fontweight="bold")
    ax.set_xlim([0, X_MAX])
    ax.grid(True, axis="x", alpha=0.15, linestyle="--", color="black", zorder=0)
    ax.set_axisbelow(True)

    legend_handles = [
        mpatches.Patch(facecolor=COLOR_C2S, hatch=HATCH_C2S, edgecolor="white", label=r"$\mathrm{C^2S}$ Avg."),
        mpatches.Patch(facecolor=COLOR_ARPLUS, hatch=HATCH_ARPLUS, edgecolor="white", label=r"$\mathrm{AR+}$ Avg."),
        mlines.Line2D(
            [],
            [],
            color=RANGE_COLOR,
            linewidth=RANGE_LINE_WIDTH,
            marker="o",
            markersize=5,
            markerfacecolor="white",
            markeredgecolor=RANGE_COLOR,
            label="Range across 5 runs",
        ),
    ]
    ax.legend(handles=legend_handles, loc="lower right", prop={"size": FONT_SIZE_LEGEND, "weight": "bold"}, framealpha=0.9)

    plt.tight_layout()

    written_files: list[Path] = []
    for fmt in OUTPUT_FORMATS:
        output_file = OUTPUT_FIGURE_BASE.with_suffix(f".{fmt}")
        plt.savefig(output_file, dpi=OUTPUT_DPI, bbox_inches="tight", format=fmt)
        written_files.append(output_file)
    plt.close()
    return written_files


def print_plot_table(plot_data: dict[str, dict[str, list[float]]]) -> None:
    rows: list[tuple[str, str, str, str, str]] = []
    for perturbation_prob in PERTURBATION_PROBS:
        label = perturbation_prob.replace("5000_pp_", "")
        for method_name in METHODS:
            values = plot_data[method_name][perturbation_prob]
            rows.append(
                (
                    label,
                    method_name,
                    f"{mean(values):.3f}",
                    f"{min(values):.3f}",
                    f"{max(values):.3f}",
                )
            )

    headers = ("perturbation_prob", "method", "mean_auprc", "min_auprc", "max_auprc")
    widths = [max(len(headers[i]), max(len(row[i]) for row in rows)) for i in range(len(headers))]

    def format_row(values: tuple[str, str, str, str, str]) -> str:
        return "  ".join(value.ljust(widths[i]) for i, value in enumerate(values))

    print(format_row(headers))
    for row in rows:
        print(format_row(row))


def print_written_files(paths: list[Path]) -> None:
    print("\nWritten files:")
    for path in paths:
        print(f"  {path}")


def main() -> None:
    args = parse_args()
    written_files: list[Path] = []

    if args.regenerate_results:
        written_files.extend(regenerate_all_results())
    else:
        print("Generating RQ2 perturbation-signal figure from existing results...")

    plot_data = load_plot_data()
    print()
    print_plot_table(plot_data)
    written_files.extend(plot_summary(plot_data))
    print_written_files(written_files)
    print("\nDone.")


if __name__ == "__main__":
    main()
