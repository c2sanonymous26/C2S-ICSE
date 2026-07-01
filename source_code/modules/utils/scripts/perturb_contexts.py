from __future__ import annotations

import argparse
import hashlib
import json
import logging
import uuid
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = REPO_ROOT / "inputs" / "taxi" / "data"
TYPE_ALPHA = {
    "instant": 10.0,
    "bias": 5.0,
    "drift": 5.0,
}
SEGMENT_MIN_LENGTH = 2
SEGMENT_MAX_LENGTH = 3
MAX_SEGMENT_ATTEMPTS = 10000
MIN_DIFFERENCE_RATIO = 0.1
LOCATION_MIN_DIFFERENCE_RATIO = 0.05
DEFAULT_FIELD_RANGES: dict[str, tuple[float, float]] = {
    "longitude": (-180.0, 180.0),
    "latitude": (-90.0, 90.0),
    "speed": (0.0, 250.0),
    "direction": (0.0, 360.0),
}
MinDifferences = dict[str, float]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply typed perturbations to taxi context data.")
    parser.add_argument(
        "--data-file-name",
        required=True,
        help="Source data file name without .csv, e.g. 5000.",
    )
    parser.add_argument(
        "--perturbation-probability",
        type=float,
        required=True,
        help="Expected probability of perturbing contexts, between 0 and 1.",
    )
    parser.add_argument(
        "--random-seed",
        type=str,
        help="Optional seed. When set, the output id is this seed and generation is reproducible.",
    )
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    if args.perturbation_probability < 0 or args.perturbation_probability > 1:
        raise ValueError("--perturbation-probability must be between 0 and 1")


def build_rng(seed: str | None) -> np.random.Generator:
    if seed is None:
        return np.random.default_rng()

    digest = hashlib.sha256(seed.encode("utf-8")).digest()
    seed_int = int.from_bytes(digest[:8], byteorder="big", signed=False)
    return np.random.default_rng(seed_int)


def get_significance_threshold(field: str, min_differences: MinDifferences) -> float:
    return min_differences[field]


def build_min_differences() -> MinDifferences:
    min_differences: MinDifferences = {}
    for field, (range_min, range_max) in DEFAULT_FIELD_RANGES.items():
        if field in {"longitude", "latitude"}:
            min_difference = (range_max - range_min) * LOCATION_MIN_DIFFERENCE_RATIO
        else:
            min_difference = (range_max - range_min) * MIN_DIFFERENCE_RATIO
        min_differences[field] = min_difference
    return min_differences


def format_value(field: str, value: Any) -> str | int:
    if field == "timestamp":
        return f"{float(value):.3f}"
    if field in {"longitude", "latitude"}:
        return f"{float(value):.6f}"
    if field in {"speed", "direction"}:
        return f"{float(value):.1f}"
    if field in {"id", "grpid"}:
        return int(value)
    return str(value)


def format_delta(value: float) -> str:
    return str(float(value))


def generate_random_value(
    field: str,
    original_value: float,
    min_differences: MinDifferences,
    rng: np.random.Generator,
) -> float:
    range_min, range_max = DEFAULT_FIELD_RANGES[field]
    threshold = get_significance_threshold(field, min_differences)

    for _ in range(100):
        new_value = float(rng.uniform(range_min, range_max))
        if abs(new_value - original_value) > threshold:
            return new_value

    if original_value + threshold + 0.01 <= range_max:
        return original_value + threshold + 0.01
    if original_value - threshold - 0.01 >= range_min:
        return original_value - threshold - 0.01

    raise ValueError(f"Failed to generate a significant random value for {field}={original_value}")


def is_value_in_range(field: str, value: float) -> bool:
    range_min, range_max = DEFAULT_FIELD_RANGES[field]
    return range_min <= value <= range_max


def generate_bias_values(
    original_values: list[float],
    field: str,
    min_differences: MinDifferences,
    rng: np.random.Generator,
) -> list[float] | None:
    for _ in range(100):
        new_values = [
            generate_random_value(field, original_value, min_differences, rng)
            for original_value in original_values
        ]
        if all(
            abs(new_value - original_value) > min_differences[field]
            for original_value, new_value in zip(original_values, new_values, strict=True)
        ):
            return new_values

    return None


def generate_drift_values(
    original_values: list[float],
    field: str,
    min_differences: MinDifferences,
    rng: np.random.Generator,
) -> list[float] | None:
    min_difference = min_differences[field]
    range_min, range_max = DEFAULT_FIELD_RANGES[field]

    for _ in range(100):
        sign = float(rng.choice([-1.0, 1.0]))
        offsets: list[float] = []
        possible = True
        for original_value in original_values:
            max_offset = range_max - original_value if sign > 0 else original_value - range_min
            if max_offset <= min_difference:
                possible = False
                break
            offsets.append(float(rng.uniform(min_difference, max_offset)))
        if not possible:
            continue

        offsets.sort()
        new_values = [
            original_value + sign * offset
            for original_value, offset in zip(original_values, offsets, strict=True)
        ]
        if all(is_value_in_range(field, value) for value in new_values):
            return new_values

    return None


def make_record(
    row: pd.Series,
    perturbation_type: str,
    field: str,
    original_value: float,
    new_value: float,
) -> dict[str, Any]:
    return {
        "id": int(row["id"]),
        "type": perturbation_type,
        "field": field,
        "original_value": format_value(field, original_value),
        "new_value": format_value(field, new_value),
        "delta": format_delta(new_value - original_value),
        "meta": {
            "carid": str(row["carid"]),
            "grpid": str(int(row["grpid"])),
        },
    }


def split_targets(total_count: int, rng: np.random.Generator) -> dict[str, int]:
    if total_count <= 0:
        return {"instant": 0, "bias": 0, "drift": 0}

    type_names = list(TYPE_ALPHA)
    ratios = rng.dirichlet([TYPE_ALPHA[name] for name in type_names])
    raw_targets = rng.multinomial(total_count, ratios)
    targets = dict(zip(type_names, (int(value) for value in raw_targets), strict=True))

    for perturbation_type in ("bias", "drift"):
        if targets[perturbation_type] == 1:
            targets["instant"] += 1
            targets[perturbation_type] = 0

    return targets


def build_trajectories(df: pd.DataFrame) -> list[list[int]]:
    trajectories: list[list[int]] = []
    for _, group in df.groupby("carid", sort=False):
        sorted_group = group.sort_values(["grpid", "timestamp", "id"])
        if len(sorted_group) >= SEGMENT_MIN_LENGTH:
            trajectories.append(sorted_group.index.tolist())
    return trajectories


def choose_segment(
    trajectories: list[list[int]],
    occupied_rows: set[int],
    max_length: int,
    rng: np.random.Generator,
) -> list[int] | None:
    if max_length < SEGMENT_MIN_LENGTH:
        return None

    for _ in range(MAX_SEGMENT_ATTEMPTS):
        trajectory = trajectories[int(rng.integers(0, len(trajectories)))]
        length_upper = min(SEGMENT_MAX_LENGTH, max_length, len(trajectory))
        if length_upper < SEGMENT_MIN_LENGTH:
            continue

        segment_length = int(rng.integers(SEGMENT_MIN_LENGTH, length_upper + 1))
        start_upper = len(trajectory) - segment_length
        start = int(rng.integers(0, start_upper + 1))
        segment = trajectory[start : start + segment_length]
        if not any(row_index in occupied_rows for row_index in segment):
            return segment

    return None


def perturb_segment(
    df_new: pd.DataFrame,
    segment: list[int],
    perturbation_type: str,
    min_differences: MinDifferences,
    rng: np.random.Generator,
) -> list[dict[str, Any]] | None:
    fields = list(DEFAULT_FIELD_RANGES)
    rng.shuffle(fields)

    for field in fields:
        original_values = [float(df_new.at[row_index, field]) for row_index in segment]
        if perturbation_type == "bias":
            new_values = generate_bias_values(original_values, field, min_differences, rng)
        elif perturbation_type == "drift":
            new_values = generate_drift_values(original_values, field, min_differences, rng)
        else:
            raise ValueError(f"Unsupported segment perturbation type: {perturbation_type}")

        if new_values is None:
            continue

        records: list[dict[str, Any]] = []
        for row_index, original_value, new_value in zip(segment, original_values, new_values, strict=True):
            row = df_new.loc[row_index]
            df_new.at[row_index, field] = new_value
            records.append(make_record(row, perturbation_type, field, original_value, new_value))
        return records

    return None


def perturb_segments(
    df_new: pd.DataFrame,
    trajectories: list[list[int]],
    occupied_rows: set[int],
    perturbation_type: str,
    target_count: int,
    min_differences: MinDifferences,
    rng: np.random.Generator,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    remaining = target_count

    while remaining >= SEGMENT_MIN_LENGTH:
        segment = choose_segment(trajectories, occupied_rows, remaining, rng)
        if segment is None:
            break

        segment_records = perturb_segment(df_new, segment, perturbation_type, min_differences, rng)
        if segment_records is None:
            continue

        records.extend(segment_records)
        occupied_rows.update(segment)
        remaining -= len(segment)

    return records


def perturb_instants(
    df_new: pd.DataFrame,
    occupied_rows: set[int],
    target_count: int,
    min_differences: MinDifferences,
    rng: np.random.Generator,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    available_rows = [row_index for row_index in df_new.index.tolist() if row_index not in occupied_rows]
    rng.shuffle(available_rows)
    fields = list(DEFAULT_FIELD_RANGES)

    for row_index in available_rows:
        if len(records) >= target_count:
            break

        field = str(rng.choice(fields))
        original_value = float(df_new.at[row_index, field])
        new_value = generate_random_value(field, original_value, min_differences, rng)
        row = df_new.loc[row_index]

        df_new.at[row_index, field] = new_value
        occupied_rows.add(row_index)
        records.append(make_record(row, "instant", field, original_value, new_value))

    return records


def apply_typed_perturbations(
    df: pd.DataFrame,
    perturbation_probability: float,
    rng: np.random.Generator,
) -> tuple[pd.DataFrame, list[dict[str, Any]], dict[str, int]]:
    df_new = df.copy()
    total_target = int(rng.binomial(len(df_new), perturbation_probability))
    targets = split_targets(total_target, rng)
    min_differences = build_min_differences()

    trajectories = build_trajectories(df_new)
    occupied_rows: set[int] = set()
    records: list[dict[str, Any]] = []

    drift_records = perturb_segments(
        df_new,
        trajectories,
        occupied_rows,
        "drift",
        targets["drift"],
        min_differences,
        rng,
    )
    records.extend(drift_records)

    bias_records = perturb_segments(
        df_new,
        trajectories,
        occupied_rows,
        "bias",
        targets["bias"],
        min_differences,
        rng,
    )
    records.extend(bias_records)

    remaining_target = total_target - len(records)
    instant_target = max(targets["instant"], remaining_target)
    instant_records = perturb_instants(df_new, occupied_rows, instant_target, min_differences, rng)
    records.extend(instant_records)

    records.sort(key=lambda record: record["id"])
    return df_new, records, targets


def post_process_dataset(df: pd.DataFrame) -> pd.DataFrame:
    assert "carid" in df.columns, "carid column does not exist in the DataFrame"
    assert "grpid" in df.columns, "grpid column does not exist in the DataFrame"

    df_updated = df.copy()
    car_ids = sorted(df["carid"].unique())
    car_grpid_starts = {
        car_id: df[df["carid"] == car_id]["grpid"].min()
        for car_id in car_ids
    }

    for car_id in car_ids:
        car_indices = sorted(df[df["carid"] == car_id].index.tolist())
        grpid_start = car_grpid_starts[car_id]
        for offset, row_index in enumerate(car_indices):
            df_updated.at[row_index, "grpid"] = grpid_start + offset

    return df_updated


def save_taxi_csv(df: pd.DataFrame, output_file: Path) -> None:
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("id,grpid,carid,timestamp,longitude,latitude,speed,direction\n")
        for _, row in df.iterrows():
            f.write(
                f"{int(row['id'])},{int(row['grpid'])},{row['carid']},"
                f"{row['timestamp']:.3f},{row['longitude']:.6f},{row['latitude']:.6f},"
                f"{row['speed']:.1f},{row['direction']:.1f}\n"
            )


def create_output_dir(data_file_name: str, perturbation_probability: float, random_seed: str | None) -> Path:
    first_level_dir = DATA_DIR / f"{data_file_name}_pp_{perturbation_probability}"
    first_level_dir.mkdir(parents=True, exist_ok=True)
    if random_seed is not None:
        output_dir = first_level_dir / random_seed
        output_dir.mkdir(exist_ok=False)
        return output_dir

    while True:
        output_id = str(uuid.uuid4())[:8]
        output_dir = first_level_dir / output_id
        try:
            output_dir.mkdir(exist_ok=False)
            return output_dir
        except FileExistsError:
            continue


def main() -> None:
    args = parse_args()
    validate_args(args)

    rng = build_rng(args.random_seed)
    if args.random_seed is not None:
        logging.info("Using random seed: %s", args.random_seed)

    data_file = DATA_DIR / f"{args.data_file_name}.csv"
    if not data_file.exists():
        raise FileNotFoundError(f"Source data file not found: {data_file}")

    logging.info("Reading source data: %s", data_file)
    df = pd.read_csv(data_file)
    logging.info("Source data record count: %s", len(df))

    missing_fields = [field for field in DEFAULT_FIELD_RANGES if field not in df.columns]
    if missing_fields:
        raise ValueError(f"Source data is missing required fields: {missing_fields}")

    output_dir = create_output_dir(args.data_file_name, args.perturbation_probability, args.random_seed)
    logging.info("Output directory: %s", output_dir)

    perturbed_df, perturbation_records, targets = apply_typed_perturbations(df, args.perturbation_probability, rng)
    perturbed_df = post_process_dataset(perturbed_df)

    save_taxi_csv(perturbed_df, output_dir / "perturbed.csv")
    with open(output_dir / "perturbed.json", "w", encoding="utf-8") as f:
        json.dump(perturbation_records, f, indent=2)

    actual_counts = Counter(record["type"] for record in perturbation_records)
    logging.info("Target typed perturbation counts: %s", targets)
    logging.info("Actual typed perturbation counts: %s", dict(actual_counts))
    logging.info("Applied %s perturbations", len(perturbation_records))
    logging.info("Saved perturbed data to: %s", output_dir)


if __name__ == "__main__":
    main()
