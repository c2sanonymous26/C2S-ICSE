#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from lark import Lark, Tree
from pint import Quantity, UnitRegistry

try:
    import tomllib as tomli
except ModuleNotFoundError:  # pragma: no cover
    import tomli


SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parent.parent.parent.parent
CONSTRAINTS_DIR = REPO_ROOT / "constraints"
INPUTS_DIR = REPO_ROOT / "inputs"
OUTPUT_DIR = REPO_ROOT / "evaluation" / "unit_validation"


AR_PLUS_GRAMMAR = r"""
    ?start: expr

    ?expr: term
         | expr "+" term   -> add
         | expr "-" term   -> sub

    ?term: factor
         | term "*" factor -> mul
         | term "/" factor -> div

    ?factor: power
           | "+" factor    -> pos
           | "-" factor    -> neg_op

    ?power: atom
          | atom "**" factor -> pow

    ?atom: NUMBER           -> number
         | func_call
         | field            -> field_ref
         | "(" expr ")"     -> paren

    func_call: FUNC_NAME "(" expr ("," expr)* ")"

    field: FIELD_NAME "_" INDEX | FIELD_NAME

    FUNC_NAME.2: "abs" | "sqrt" | "log" | "exp" | "sin" | "cos" | "tan"
               | "min" | "max" | "neg" | "add" | "sub" | "mul" | "div"
    FIELD_NAME.1: /(?!(abs|sqrt|log|exp|sin|cos|tan|min|max|neg|add|sub|mul|div)\b)[a-zA-Z][a-zA-Z0-9]*/
    INDEX: /[0-9]+/

    %import common.NUMBER
    %import common.WS
    %ignore WS
"""


@dataclass(frozen=True)
class UnitExpr:
    quantity: Quantity | None = None
    unknown: bool = False

    @property
    def units(self) -> str:
        if self.unknown:
            return "unknown"
        return str(self.quantity.units)


class ARPlusExpressionUnitChecker:
    def __init__(self, field_units: dict[str, dict[str, str]]):
        self.parser = Lark(AR_PLUS_GRAMMAR, parser="lalr")
        self.field_units = field_units
        self.ureg = UnitRegistry()

    def _dict_to_pint_unit(self, unit_dict: dict[str, str]) -> str:
        if not unit_dict:
            return ""

        unit_name_map = {
            "km": "kilometer",
            "h": "hour",
            "s": "second",
            "second": "second",
            "m": "meter",
            "degree": "degree",
            "radian": "radian",
        }

        numerator: list[str] = []
        denominator: list[str] = []

        for unit, power_str in unit_dict.items():
            power = int(power_str)
            pint_unit = unit_name_map.get(unit, unit)

            if power > 0:
                numerator.append(pint_unit if power == 1 else f"{pint_unit}**{power}")
            elif power < 0:
                denominator.append(pint_unit if power == -1 else f"{pint_unit}**{-power}")

        if numerator and denominator:
            return f"({' * '.join(numerator)}) / ({' * '.join(denominator)})"
        if numerator:
            return " * ".join(numerator)
        if denominator:
            return f"1 / ({' * '.join(denominator)})"
        return ""

    def _dimensionless(self) -> UnitExpr:
        return UnitExpr(self.ureg.Quantity(1.0, ""))

    def _unknown(self) -> UnitExpr:
        return UnitExpr(None, unknown=True)

    def _quantity(self, unit_str: str) -> UnitExpr:
        quantity = self.ureg.Quantity(1.0, unit_str) if unit_str else self.ureg.Quantity(1.0, "")
        return UnitExpr(quantity)

    def _as_scale(self, value: UnitExpr) -> Quantity:
        if value.unknown:
            return self.ureg.Quantity(1.0, "")
        return value.quantity

    def _compatible(self, left: UnitExpr, right: UnitExpr) -> bool:
        if left.unknown or right.unknown:
            return True
        return left.quantity.is_compatible_with(right.quantity)

    def _merge_same_unit(self, func_name: str, left: UnitExpr, right: UnitExpr) -> tuple[bool, str | None, UnitExpr | None]:
        if left.unknown and right.unknown:
            return True, None, self._unknown()
        if left.unknown:
            return True, None, right
        if right.unknown:
            return True, None, left
        if not left.quantity.is_compatible_with(right.quantity):
            return False, f"Function {func_name} requires unit-compatible arguments: {left.units} vs {right.units}", None
        return True, None, left

    def check_expression(self, expr_str: str) -> tuple[bool, str | None, UnitExpr | None]:
        try:
            tree = self.parser.parse(expr_str)
            return self._analyze_expr(tree)
        except Exception as exc:
            return False, f"Parse error: {exc}", None

    def _analyze_expr(self, node: Tree) -> tuple[bool, str | None, UnitExpr | None]:
        if node.data == "add":
            return self._analyze_add(node)
        if node.data == "sub":
            return self._analyze_sub(node)
        if node.data == "mul":
            return self._analyze_mul(node)
        if node.data == "div":
            return self._analyze_div(node)
        if node.data == "neg_op":
            success, error, result = self._analyze_expr(node.children[0])
            if not success:
                return success, error, None
            if result.unknown:
                return True, None, result
            return True, None, UnitExpr(-result.quantity)
        if node.data == "pos":
            return self._analyze_expr(node.children[0])
        if node.data == "paren":
            return self._analyze_expr(node.children[0])
        if node.data == "number":
            return True, None, self._unknown()
        if node.data == "field_ref":
            return self._analyze_field(node.children[0])
        if node.data == "func_call":
            return self._analyze_func(node)
        return False, f"Unknown parse node type: {node.data}", None

    def _analyze_add(self, node: Tree) -> tuple[bool, str | None, UnitExpr | None]:
        success, error, left = self._analyze_expr(node.children[0])
        if not success:
            return success, error, None
        success, error, right = self._analyze_expr(node.children[1])
        if not success:
            return success, error, None
        return self._merge_same_unit("add", left, right)

    def _analyze_sub(self, node: Tree) -> tuple[bool, str | None, UnitExpr | None]:
        success, error, left = self._analyze_expr(node.children[0])
        if not success:
            return success, error, None
        success, error, right = self._analyze_expr(node.children[1])
        if not success:
            return success, error, None
        return self._merge_same_unit("sub", left, right)

    def _analyze_mul(self, node: Tree) -> tuple[bool, str | None, UnitExpr | None]:
        success, error, left = self._analyze_expr(node.children[0])
        if not success:
            return success, error, None
        success, error, right = self._analyze_expr(node.children[1])
        if not success:
            return success, error, None
        return True, None, UnitExpr(self._as_scale(left) * self._as_scale(right))

    def _analyze_div(self, node: Tree) -> tuple[bool, str | None, UnitExpr | None]:
        success, error, left = self._analyze_expr(node.children[0])
        if not success:
            return success, error, None
        success, error, right = self._analyze_expr(node.children[1])
        if not success:
            return success, error, None
        return True, None, UnitExpr(self._as_scale(left) / self._as_scale(right))

    def _analyze_field(self, field_node: Tree) -> tuple[bool, str | None, UnitExpr | None]:
        field_name_token = field_node.children[0]
        field_base = field_name_token.value if hasattr(field_name_token, "value") else str(field_name_token)

        if field_base not in self.field_units:
            return False, f"Unknown field: {field_base}", None

        unit_str = self._dict_to_pint_unit(self.field_units[field_base])
        return True, None, self._quantity(unit_str)

    def _analyze_func(self, func_node: Tree) -> tuple[bool, str | None, UnitExpr | None]:
        func_name = func_node.children[0].value
        params = []
        for i in range(1, len(func_node.children)):
            success, error, param = self._analyze_expr(func_node.children[i])
            if not success:
                return success, error, None
            params.append(param)

        if func_name in ["sin", "cos", "tan"]:
            return self._check_trig_func(func_name, params)
        if func_name in ["log", "exp"]:
            return self._check_log_func(func_name, params)
        if func_name == "sqrt":
            return self._check_sqrt_func(params)
        if func_name in ["min", "max"]:
            return self._check_minmax_func(func_name, params)
        if func_name == "abs":
            return self._check_abs_func(params)
        if func_name == "neg":
            if params[0].unknown:
                return True, None, params[0]
            return True, None, UnitExpr(-params[0].quantity)
        if func_name == "add":
            return self._check_add_func(params)
        if func_name == "sub":
            return self._check_sub_func(params)
        if func_name == "mul":
            return self._check_mul_func(params)
        if func_name == "div":
            return self._check_div_func(params)
        return False, f"Unknown function: {func_name}", None

    def _check_trig_func(self, func_name: str, params: list[UnitExpr]) -> tuple[bool, str | None, UnitExpr | None]:
        if len(params) != 1:
            return False, f"Function {func_name} requires 1 argument", None
        param = params[0]
        if param.unknown:
            return True, None, self._dimensionless()
        if param.quantity.units != self.ureg.radian:
            return False, f"Function {func_name} strictly requires a radian unit, but got {param.units}", None
        return True, None, self._dimensionless()

    def _check_log_func(self, func_name: str, params: list[UnitExpr]) -> tuple[bool, str | None, UnitExpr | None]:
        if len(params) != 1:
            return False, f"Function {func_name} requires 1 argument", None
        param = params[0]
        if param.unknown:
            return True, None, self._dimensionless()
        if param.quantity.dimensionality or str(param.quantity.units) != "dimensionless":
            return False, f"Function {func_name} requires a dimensionless parameter without units, but got {param.units}", None
        return True, None, self._dimensionless()

    def _check_sqrt_func(self, params: list[UnitExpr]) -> tuple[bool, str | None, UnitExpr | None]:
        if len(params) != 1:
            return False, "Function sqrt requires 1 argument", None
        if params[0].unknown:
            return True, None, self._unknown()
        return True, None, UnitExpr(params[0].quantity ** 0.5)

    def _check_minmax_func(self, func_name: str, params: list[UnitExpr]) -> tuple[bool, str | None, UnitExpr | None]:
        if len(params) != 2:
            return False, f"Function {func_name} requires 2 arguments", None
        return self._merge_same_unit(func_name, params[0], params[1])

    def _check_abs_func(self, params: list[UnitExpr]) -> tuple[bool, str | None, UnitExpr | None]:
        if len(params) != 1:
            return False, "Function abs requires 1 argument", None
        return True, None, params[0]

    def _check_add_func(self, params: list[UnitExpr]) -> tuple[bool, str | None, UnitExpr | None]:
        if len(params) != 2:
            return False, "Function add requires 2 arguments", None
        return self._merge_same_unit("add", params[0], params[1])

    def _check_sub_func(self, params: list[UnitExpr]) -> tuple[bool, str | None, UnitExpr | None]:
        if len(params) != 2:
            return False, "Function sub requires 2 arguments", None
        return self._merge_same_unit("sub", params[0], params[1])

    def _check_mul_func(self, params: list[UnitExpr]) -> tuple[bool, str | None, UnitExpr | None]:
        if len(params) != 2:
            return False, "Function mul requires 2 arguments", None
        return True, None, UnitExpr(self._as_scale(params[0]) * self._as_scale(params[1]))

    def _check_div_func(self, params: list[UnitExpr]) -> tuple[bool, str | None, UnitExpr | None]:
        if len(params) != 2:
            return False, "Function div requires 2 arguments", None
        return True, None, UnitExpr(self._as_scale(params[0]) / self._as_scale(params[1]))

    def check_comparison(self, target_col: str, cmp: str, assertion: str) -> tuple[bool, str | None]:
        match = re.match(r"([a-zA-Z][a-zA-Z0-9]*)(?:_(\d+))?$", target_col)
        if not match:
            return False, f"Failed to parse target_col: {target_col}"

        field_base = match.group(1)
        if field_base not in self.field_units:
            return False, f"Unknown field: {field_base}"

        unit_str = self._dict_to_pint_unit(self.field_units[field_base])
        target_quantity = self.ureg.Quantity(1.0, unit_str) if unit_str else self.ureg.Quantity(1.0, "")

        success, error, assertion_quantity = self.check_expression(assertion)
        if not success:
            return False, f"Assertion unit error: {error}"

        if assertion_quantity.unknown:
            return True, None

        if not target_quantity.is_compatible_with(assertion_quantity.quantity):
            return False, (
                "Comparison units are incompatible: "
                f"{target_col}({target_quantity.units}) {cmp} assertion({assertion_quantity.units})"
            )

        return True, None


class ARPlusUnitValidator:
    def __init__(self, context_definitions_path: Path):
        self.context_definitions_path = context_definitions_path
        self.field_units = self._load_field_units()
        self.unit_checker = ARPlusExpressionUnitChecker(self.field_units)

    def _load_field_units(self) -> dict[str, dict[str, str]]:
        if not self.context_definitions_path.exists():
            raise FileNotFoundError(f"Missing context_schema.toml: {self.context_definitions_path}")

        with open(self.context_definitions_path, "rb") as f:
            data = tomli.load(f)

        fields = data.get("context_definitions", {}).get("fields", {})
        if not fields:
            raise ValueError(f"No context_definitions.fields found in {self.context_definitions_path}")

        field_units: dict[str, dict[str, str]] = {}
        for field_name, field_info in fields.items():
            field_units[field_name] = field_info.get("unit", {})
        return field_units

    def load_constraint(self, constraint_file: Path) -> dict[str, Any] | None:
        if not constraint_file.exists():
            return None
        try:
            with open(constraint_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None

    def get_all_constraints(self, method_dir: Path) -> list[Path]:
        raw_dir = method_dir / "raw"
        if not raw_dir.exists():
            raise FileNotFoundError(f"Missing raw directory: {raw_dir}")
        return sorted(raw_dir.glob("constraint_*.json"))

    def construct_full_expression(self, constraint_data: dict[str, Any]) -> str:
        target_col = constraint_data["target_col"]
        cmp_value = constraint_data["cmp"]
        assertion = constraint_data["assertion"]
        cmp_map = {
            "gt": ">",
            "ge": ">=",
            "lt": "<",
            "le": "<=",
            "eq": "==",
            "ne": "!=",
        }
        return f"{target_col} {cmp_map.get(cmp_value, cmp_value)} {assertion}"

    def validate_constraint(self, constraint_data: dict[str, Any], constraint_name: str) -> dict[str, Any]:
        result: dict[str, Any] = {
            "constraint_name": constraint_name,
            "target_col": constraint_data.get("target_col"),
            "cmp": constraint_data.get("cmp"),
            "assertion": constraint_data.get("assertion"),
            "overall_passed": False,
            "error": None,
        }

        try:
            result["full_expression"] = self.construct_full_expression(constraint_data)
            success, error = self.unit_checker.check_comparison(
                constraint_data["target_col"],
                constraint_data["cmp"],
                constraint_data["assertion"],
            )
            result["overall_passed"] = success
            result["error"] = error
        except Exception as exc:
            result["overall_passed"] = False
            result["error"] = f"Validation error: {exc}"

        return result

    def validate_all_constraints(self, method_dir: Path) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        for constraint_file in self.get_all_constraints(method_dir):
            constraint_name = constraint_file.stem
            constraint_data = self.load_constraint(constraint_file)
            if constraint_data is None:
                results.append(
                    {
                        "constraint_name": constraint_name,
                        "overall_passed": False,
                        "error": "Failed to load constraint file",
                    }
                )
                continue
            results.append(self.validate_constraint(constraint_data, constraint_name))
        return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate AR+ unit compatibility. Reads "
            "constraints/<experiment>/AR+/raw and writes "
            "evaluation/unit_validation/<experiment>/AR+/results.json."
        )
    )
    parser.add_argument("experiment_name", type=str, help="Experiment name, e.g. taxi_RQ1&2_1")
    parser.add_argument("--scenario", type=str, default="taxi", help="Scenario name, default: taxi")
    return parser.parse_args()


def build_output(results: list[dict[str, Any]]) -> dict[str, Any]:
    total_constraints = len(results)
    passed_constraints = sum(1 for item in results if item.get("overall_passed", False))
    failed_constraints = total_constraints - passed_constraints
    pass_rate = round(passed_constraints / total_constraints * 100, 2) if total_constraints else 0
    return {
        "summary": {
            "total_constraints": total_constraints,
            "passed_constraints": passed_constraints,
            "failed_constraints": failed_constraints,
            "pass_rate": pass_rate,
        },
        "details": results,
    }


def main() -> None:
    args = parse_args()
    method_dir = CONSTRAINTS_DIR / args.experiment_name / "AR+"
    context_definitions_path = INPUTS_DIR / args.scenario / "context_schema.toml"
    output_path = OUTPUT_DIR / args.experiment_name / "AR+" / "results.json"

    validator = ARPlusUnitValidator(context_definitions_path)
    results = validator.validate_all_constraints(method_dir)
    output = build_output(results)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Validated {len(results)} constraints from {method_dir}")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
