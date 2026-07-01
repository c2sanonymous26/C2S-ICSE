from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from sentence_transformers import SentenceTransformer, util


SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parent.parent.parent.parent
INVENTOR_DIR = REPO_ROOT / "outputs" / "invention" / "inventor"
EVALUATION_DIR = REPO_ROOT / "evaluation" / "duplicate_check"


@dataclass(frozen=True)
class ConstraintRecord:
    constraint_id: int
    source_template_id: int
    template_json_path: Path
    template_data: dict[str, Any]


class UnionFind:
    def __init__(self) -> None:
        self.parent: dict[str, str] = {}
        self.rank: dict[str, int] = {}

    def find(self, x: str) -> str:
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: str, y: str) -> None:
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

    def get_equivalence_classes(self) -> list[set[str]]:
        groups: dict[str, set[str]] = {}
        for node in self.parent:
            root = self.find(node)
            groups.setdefault(root, set()).add(node)
        return [group for group in groups.values() if len(group) > 1]


class SimilarityChecker:
    def __init__(self, semantic_threshold: float = 0.98) -> None:
        print("Loading similarity model...")
        self.model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
        print("Similarity model loaded")
        self.semantic_threshold = semantic_threshold

    def calculate_semantics_similarity(self, semantics1: str, semantics2: str) -> float:
        if not semantics1 or not semantics2:
            return 0.0

        common_prefix = os.path.commonprefix([semantics1, semantics2])
        diff1 = semantics1[len(common_prefix) :]
        diff2 = semantics2[len(common_prefix) :]

        overall_sim = util.cos_sim(
            self.model.encode(semantics1),
            self.model.encode(semantics2),
        ).item()

        if diff1 and diff2:
            diff_sim = util.cos_sim(
                self.model.encode(diff1),
                self.model.encode(diff2),
            ).item()
        else:
            diff_sim = 1.0 if not diff1 and not diff2 else 0.0

        ave_overall_len = (len(semantics1) + len(semantics2)) / 2
        ave_diff_len = (len(diff1) + len(diff2)) / 2
        if ave_overall_len == 0:
            return 1.0

        return (
            len(common_prefix) / ave_overall_len * overall_sim
            + ave_diff_len / ave_overall_len * diff_sim
        )

    def calculate_structure_similarity(self, structure1: str, structure2: str) -> float:
        if not structure1 or not structure2:
            return 0.0
        if structure1 == structure2:
            return 1.0
        return util.cos_sim(
            self.model.encode(structure1),
            self.model.encode(structure2),
        ).item()

    @staticmethod
    def calculate_count_similarity(count1: int, count2: int) -> float:
        if count1 == 0 and count2 == 0:
            return 1.0
        max_count = max(count1, count2)
        min_count = min(count1, count2)
        if max_count == 0:
            return 1.0
        return min_count / max_count

    def calculate_implementation_similarity(self, bfuncs1: list[dict[str, Any]], bfuncs2: list[dict[str, Any]]) -> float:
        if not bfuncs1 or not bfuncs2:
            return 0.0

        implementations1 = [bfunc.get("implementation", "") for bfunc in bfuncs1 if bfunc.get("implementation", "").strip()]
        implementations2 = [bfunc.get("implementation", "") for bfunc in bfuncs2 if bfunc.get("implementation", "").strip()]
        if not implementations1 or not implementations2:
            return 0.0

        sims: list[float] = []
        for impl1 in implementations1:
            for impl2 in implementations2:
                sims.append(
                    util.cos_sim(self.model.encode(impl1), self.model.encode(impl2)).item()
                )
        return sum(sims) / len(sims) if sims else 0.0

    @staticmethod
    def is_bfuncs_identical(bfuncs1: list[dict[str, Any]], bfuncs2: list[dict[str, Any]]) -> bool:
        if len(bfuncs1) != len(bfuncs2):
            return False
        sorted_bfuncs1 = sorted(bfuncs1, key=lambda x: x.get("id", ""))
        sorted_bfuncs2 = sorted(bfuncs2, key=lambda x: x.get("id", ""))
        for bf1, bf2 in zip(sorted_bfuncs1, sorted_bfuncs2):
            if bf1.get("implementation", "") != bf2.get("implementation", ""):
                return False
        return True

    def calculate_comprehensive_similarity(
        self,
        constraint_data1: dict[str, Any],
        constraint_data2: dict[str, Any],
    ) -> dict[str, Any]:
        semantics1 = constraint_data1.get("semantics", "")
        semantics2 = constraint_data2.get("semantics", "")
        structure1 = constraint_data1.get("structure", "")
        structure2 = constraint_data2.get("structure", "")
        bfuncs1 = constraint_data1.get("bfuncs", [])
        bfuncs2 = constraint_data2.get("bfuncs", [])

        structure_identical = structure1.strip() == structure2.strip() and structure1.strip() != ""
        bfuncs_identical = self.is_bfuncs_identical(bfuncs1, bfuncs2)

        if structure_identical and bfuncs_identical:
            comprehensive_sim = 1.0
            similarity_reason = "Identical structure and bfuncs"
        else:
            comprehensive_sim = self.calculate_semantics_similarity(semantics1, semantics2)
            similarity_reason = f"Based on semantic similarity (semantics: {comprehensive_sim:.4f})"

        return {
            "semantics_similarity": self.calculate_semantics_similarity(semantics1, semantics2),
            "structure_similarity": self.calculate_structure_similarity(structure1, structure2),
            "count_similarity": self.calculate_count_similarity(len(bfuncs1), len(bfuncs2)),
            "implementation_similarity": self.calculate_implementation_similarity(bfuncs1, bfuncs2),
            "comprehensive_similarity": comprehensive_sim,
            "structure_identical": structure_identical,
            "bfuncs_identical": bfuncs_identical,
            "similarity_reason": similarity_reason,
        }

    def is_equivalent(self, result: dict[str, Any]) -> bool:
        if (
            result.get("comprehensive_similarity") == 1.0
            and result.get("structure_identical")
            and result.get("bfuncs_identical")
        ):
            return True
        return result.get("semantics_similarity", 0.0) > self.semantic_threshold


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run duplicate checking for extracted constraints under the current directory structure."
    )
    parser.add_argument("--scenario", "-s", required=True, help="Scenario name, e.g. taxi")
    parser.add_argument(
        "--constraint-dir",
        required=True,
        help="Constraint directory that directly contains xml/, py/, and mapping.json",
    )
    parser.add_argument(
        "--semantic-threshold",
        type=float,
        default=0.98,
        help="Semantic similarity threshold for duplicate grouping (default: 0.98)",
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


def output_root(constraint_dir: Path) -> Path:
    return EVALUATION_DIR / constraint_dir.parent.name / constraint_dir.name


def load_mapping(constraint_dir: Path) -> dict[str, Any]:
    mapping_file = constraint_dir / "mapping.json"
    if not mapping_file.exists():
        raise FileNotFoundError(f"Missing mapping.json: {mapping_file}")
    return json.loads(mapping_file.read_text(encoding="utf-8"))


def source_dir_name_from_mapping(mapping: dict[str, Any]) -> str:
    metadata = mapping.get("metadata", {})
    source_dir = metadata.get("source_dir")
    if source_dir is not None:
        return Path(str(source_dir)).name

    source_dirs = metadata.get("source_dirs")
    if isinstance(source_dirs, list) and len(source_dirs) == 1:
        return Path(str(source_dirs[0])).name

    raise ValueError("Missing source_dir in mapping metadata")


def template_id_from_path(path: Path) -> int | None:
    candidate = path.parent.name if path.name == "template.json" else path.name
    match = re.fullmatch(r"template_(\d+)", candidate)
    if match:
        return int(match.group(1))
    return None


def source_template_id_from_item(item: dict[str, Any]) -> int | None:
    source_template_id = item.get("source_template_id")
    if source_template_id is not None:
        return int(source_template_id)

    original_name = item.get("original_name", "")
    match = re.fullmatch(r"template_(\d+)", str(original_name))
    if match:
        return int(match.group(1))

    for path_key in ("template_path", "original_path"):
        path_value = item.get(path_key)
        if path_value:
            template_id = template_id_from_path(Path(str(path_value)))
            if template_id is not None:
                return template_id

    return None


def inventor_run_name_from_mapping(mapping: dict[str, Any], constraint_dir: Path) -> str:
    metadata = mapping.get("metadata", {})
    source_dirs = []
    if metadata.get("source_dir") is not None:
        source_dirs.append(str(metadata["source_dir"]))
    if isinstance(metadata.get("source_dirs"), list):
        source_dirs.extend(str(item) for item in metadata["source_dirs"] if item)

    for source_dir in source_dirs:
        parts = Path(source_dir).parts
        if "instantiation" in parts:
            index = parts.index("instantiation")
            if index + 1 < len(parts):
                return parts[index + 1]
        if "inventor" in parts:
            index = parts.index("inventor")
            if index + 2 < len(parts):
                return parts[index + 2]
        if source_dir:
            return Path(source_dir).name

    return constraint_dir.parent.name


def resolved_template_json_path(path_value: str) -> Path | None:
    raw_path = Path(path_value)
    candidate = raw_path if raw_path.is_absolute() else REPO_ROOT / raw_path
    if candidate.name != "template.json":
        candidate = candidate / "template.json"
    if candidate.exists():
        return candidate
    return None


def template_json_path_from_item(
    scenario: str,
    inventor_run_name: str,
    method_name: str,
    mapping: dict[str, Any],
    item: dict[str, Any],
) -> tuple[Path, int]:
    for path_key in ("template_path", "original_path"):
        path_value = item.get(path_key)
        if path_value:
            source_template_id = source_template_id_from_item(item)
            if source_template_id is None:
                raise ValueError("Could not infer source template id from mapping path")

            direct_path = resolved_template_json_path(str(path_value))
            if direct_path is not None:
                return direct_path, source_template_id

            inferred_path = infer_template_json_path(
                scenario,
                inventor_run_name,
                method_name,
                source_template_id,
            )
            if inferred_path is not None:
                return inferred_path, source_template_id

    source_template_id = source_template_id_from_item(item)
    if source_template_id is None:
        raise ValueError("Incomplete extracted constraint entry in mapping.json")

    inferred_path = infer_template_json_path(scenario, inventor_run_name, method_name, source_template_id)
    if inferred_path is not None:
        return inferred_path, source_template_id

    return (
        INVENTOR_DIR
        / scenario
        / inventor_run_name
        / f"template_{source_template_id}"
        / "template.json",
        source_template_id,
    )


def infer_template_json_path(scenario: str, inventor_run_name: str, method_name: str, template_id: int) -> Path | None:
    inventor_run_dir = INVENTOR_DIR / scenario / inventor_run_name
    if not inventor_run_dir.exists():
        return None

    direct_path = inventor_run_dir / f"template_{template_id}" / "template.json"
    if direct_path.exists():
        return direct_path

    match = re.fullmatch(r".*_(\d{4})", method_name)
    if not match:
        return None

    suffix = match.group(1)
    candidates = sorted(
        path / f"template_{template_id}" / "template.json"
        for path in inventor_run_dir.iterdir()
        if path.is_dir()
        and not path.name.startswith("_")
        and path.name.endswith(f"_{suffix}")
        and (path / f"template_{template_id}" / "template.json").exists()
    )
    if len(candidates) == 1:
        return candidates[0]
    return None


def load_constraint_records(scenario: str, constraint_dir: Path) -> list[ConstraintRecord]:
    mapping = load_mapping(constraint_dir)
    inventor_run_name = inventor_run_name_from_mapping(mapping, constraint_dir)
    method_name = constraint_dir.name
    records: list[ConstraintRecord] = []
    for item in mapping.get("constraints", []):
        source_template_id = source_template_id_from_item(item)
        constraint_id = item.get("constraint_id")
        if constraint_id is None:
            constraint_id = source_template_id
        if constraint_id is None or source_template_id is None:
            raise ValueError("Incomplete extracted constraint entry in mapping.json")

        template_json_path, source_template_id = template_json_path_from_item(
            scenario,
            inventor_run_name,
            method_name,
            mapping,
            item,
        )
        if not template_json_path.exists():
            raise FileNotFoundError(f"Missing source template.json: {template_json_path}")

        template_data = json.loads(template_json_path.read_text(encoding="utf-8"))
        records.append(
            ConstraintRecord(
                constraint_id=int(constraint_id),
                source_template_id=int(source_template_id),
                template_json_path=template_json_path,
                template_data=template_data,
            )
        )

    records.sort(key=lambda item: item.constraint_id)
    return records


def calculate_all_similarities(records: list[ConstraintRecord], checker: SimilarityChecker) -> list[dict[str, Any]]:
    total_pairs = len(records) * (len(records) - 1) // 2
    current_pair = 0
    results: list[dict[str, Any]] = []
    print(f"Found {len(records)} constraints, start computing similarities...")

    for i in range(len(records)):
        for j in range(i + 1, len(records)):
            current_pair += 1
            left = records[i]
            right = records[j]
            print(
                f"Progress: {current_pair}/{total_pairs} - "
                f"constraint_{left.constraint_id} vs constraint_{right.constraint_id}"
            )
            similarity_result = checker.calculate_comprehensive_similarity(
                left.template_data,
                right.template_data,
            )
            results.append(
                {
                    "constraint1": {
                        "constraint_id": left.constraint_id,
                        "template_json": str(left.template_json_path.relative_to(REPO_ROOT)),
                    },
                    "constraint2": {
                        "constraint_id": right.constraint_id,
                        "template_json": str(right.template_json_path.relative_to(REPO_ROOT)),
                    },
                    **similarity_result,
                }
            )
    return results


def build_equivalence_classes(
    results: list[dict[str, Any]],
    checker: SimilarityChecker,
) -> tuple[list[set[str]], list[dict[str, Any]], dict[str, dict[str, Any]]]:
    uf = UnionFind()
    remaining_results: list[dict[str, Any]] = []
    equivalence_relations: dict[str, dict[str, Any]] = {}

    for result in results:
        left = str(result["constraint1"]["constraint_id"])
        right = str(result["constraint2"]["constraint_id"])
        if checker.is_equivalent(result):
            uf.union(left, right)
            equivalence_relations[f"{left}_{right}"] = result
        else:
            remaining_results.append(result)

    return uf.get_equivalence_classes(), remaining_results, equivalence_relations


def generate_equivalence_explanations(
    equivalence_class: set[str],
    equivalence_relations: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    explanations: list[dict[str, Any]] = []
    constraints_list = sorted(equivalence_class, key=int)
    for i in range(len(constraints_list)):
        for j in range(i + 1, len(constraints_list)):
            c1 = constraints_list[i]
            c2 = constraints_list[j]
            relation = equivalence_relations.get(f"{c1}_{c2}") or equivalence_relations.get(f"{c2}_{c1}")
            if relation:
                explanations.append(
                    {
                        "constraint1": f"constraint_{relation['constraint1']['constraint_id']}",
                        "constraint2": f"constraint_{relation['constraint2']['constraint_id']}",
                        "reason": relation["similarity_reason"],
                        "comprehensive_similarity": relation["comprehensive_similarity"],
                        "semantics_similarity": relation["semantics_similarity"],
                        "structure_identical": relation["structure_identical"],
                        "bfuncs_identical": relation["bfuncs_identical"],
                    }
                )
    return explanations


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def save_similarity_results(
    scenario: str,
    constraint_dir: Path,
    results: list[dict[str, Any]],
    checker: SimilarityChecker,
) -> None:
    out_dir = output_root(constraint_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    classes, remaining_results, relations = build_equivalence_classes(results, checker)
    sorted_classes = sorted(classes, key=lambda group: (-len(group), sorted(group)[0]))
    duplicates_payload = {
        "semantic_threshold": checker.semantic_threshold,
        "total_equivalence_classes": len(sorted_classes),
        "total_constraints_in_classes": sum(len(group) for group in sorted_classes),
        "largest_class_size": max((len(group) for group in sorted_classes), default=0),
        "equivalence_classes": [
            {
                "class_id": idx,
                "size": len(group),
                "constraints": [f"constraint_{item}" for item in sorted(group, key=int)],
                "explanations": generate_equivalence_explanations(group, relations),
            }
            for idx, group in enumerate(sorted_classes, start=1)
        ],
    }
    remain_payload = {
        "pairwise_results": sorted(
            remaining_results,
            key=lambda item: item["comprehensive_similarity"],
            reverse=True,
        ),
    }
    write_json(out_dir / "duplicates.json", duplicates_payload)
    write_json(out_dir / "remain.json", remain_payload)
    print(f"Wrote {out_dir / 'duplicates.json'}")
    print(f"Wrote {out_dir / 'remain.json'}")


def main() -> int:
    try:
        args = parse_args()
        constraint_dir = resolve_repo_path(args.constraint_dir)
        checker = SimilarityChecker(semantic_threshold=args.semantic_threshold)
        records = load_constraint_records(args.scenario, constraint_dir)
        if len(records) < 2:
            raise ValueError("At least two constraints are required for duplicate checking")
        results = calculate_all_similarities(records, checker)
        save_similarity_results(
            args.scenario,
            constraint_dir,
            results,
            checker,
        )
        return 0
    except KeyboardInterrupt:
        print("\nDuplicate checking interrupted")
        return 1
    except Exception as exc:
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
