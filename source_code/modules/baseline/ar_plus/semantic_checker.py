from __future__ import annotations

from dataclasses import dataclass
from numbers import Integral
from typing import Any


FIELD_TYPES = {
    "timestamp": "time",
    "longitude": "coordinate",
    "latitude": "coordinate",
    "speed": "speed",
    "direction": "angle",
}

DERIVED_TYPE = "derived"


@dataclass(frozen=True)
class SemanticCheckResult:
    valid: bool
    semantic_type: str | None
    reason: str


class SemanticChecker:
    """Lightweight AR-style semantic preference checker for taxi assertions."""

    def __init__(self, feature_names: list[str]):
        self.feature_names = feature_names

    def check_program(self, program: Any, target_col: str) -> SemanticCheckResult:
        target_type = self._field_type(target_col)
        if target_type is None:
            return SemanticCheckResult(False, None, f"unknown target field: {target_col}")

        semantic_type, next_index, reason = self._infer_node(program.program, 0)
        if semantic_type is None:
            return SemanticCheckResult(False, None, reason)
        if next_index != len(program.program):
            return SemanticCheckResult(False, semantic_type, "program has unused nodes")
        if semantic_type in {target_type, "scalar", DERIVED_TYPE}:
            return SemanticCheckResult(True, semantic_type, "semantic type is acceptable")
        return SemanticCheckResult(
            False,
            semantic_type,
            f"RHS semantic type {semantic_type} does not match target type {target_type}",
        )

    def _infer_node(self, nodes: list[Any], index: int) -> tuple[str | None, int, str]:
        if index >= len(nodes):
            return None, index, "unexpected end of program"

        node = nodes[index]
        if isinstance(node, Integral):
            if int(node) >= len(self.feature_names):
                return None, index + 1, f"feature index out of range: {node}"
            field_name = self.feature_names[int(node)]
            semantic_type = self._field_type(field_name)
            if semantic_type is None:
                return None, index + 1, f"unknown feature field: {field_name}"
            return semantic_type, index + 1, "field"

        if not hasattr(node, "arity"):
            return "scalar", index + 1, "constant"

        child_types: list[str] = []
        next_index = index + 1
        for _ in range(node.arity):
            child_type, next_index, reason = self._infer_node(nodes, next_index)
            if child_type is None:
                return None, next_index, reason
            child_types.append(child_type)

        semantic_type = self._apply_function(node.name, child_types)
        if semantic_type is None:
            return None, next_index, f"invalid semantic operation: {node.name}({', '.join(child_types)})"
        return semantic_type, next_index, "function"

    def _field_type(self, field_name: str) -> str | None:
        base_name = self._strip_pair_suffix(field_name)
        return FIELD_TYPES.get(base_name)

    @staticmethod
    def _strip_pair_suffix(field_name: str) -> str:
        if field_name.endswith("_1") or field_name.endswith("_2"):
            return field_name[:-2]
        return field_name

    @staticmethod
    def _apply_function(function_name: str, child_types: list[str]) -> str | None:
        if function_name in {"add", "sub"}:
            return SemanticChecker._combine_add_sub(child_types)
        if function_name == "mul":
            return SemanticChecker._combine_mul(child_types)
        if function_name == "div":
            return SemanticChecker._combine_div(child_types)
        if function_name in {"abs", "neg"}:
            return child_types[0]
        if function_name == "sqrt":
            return "scalar" if child_types[0] == "scalar" else DERIVED_TYPE
        if function_name == "log":
            return "scalar" if child_types[0] == "scalar" else None
        if function_name in {"sin", "cos", "tan"}:
            return "scalar" if child_types[0] in {"angle", "scalar"} else None
        if function_name in {"min", "max"}:
            return SemanticChecker._combine_min_max(child_types)
        return None

    @staticmethod
    def _combine_add_sub(child_types: list[str]) -> str | None:
        left, right = child_types
        if left == right:
            return left
        if left == "scalar":
            return right
        if right == "scalar":
            return left
        return None

    @staticmethod
    def _combine_mul(child_types: list[str]) -> str | None:
        left, right = child_types
        if left == right == "scalar":
            return "scalar"
        if left == "scalar":
            return right
        if right == "scalar":
            return left
        return DERIVED_TYPE

    @staticmethod
    def _combine_div(child_types: list[str]) -> str | None:
        left, right = child_types
        if right == "scalar":
            return left
        if left == right:
            return "scalar"
        return DERIVED_TYPE

    @staticmethod
    def _combine_min_max(child_types: list[str]) -> str | None:
        left, right = child_types
        if left == right:
            return left
        if left == "scalar":
            return right
        if right == "scalar":
            return left
        return None
