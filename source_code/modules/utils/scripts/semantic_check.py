from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any

import tomli
from agno.agent import Agent
from agno.models.openai.like import OpenAILike
from agno.models.openrouter import OpenRouter
from lark import Lark, Transformer, Tree, UnexpectedCharacters, UnexpectedToken
from lark.lexer import Token

from modules.invention import BODY_GRAMMAR, STRUCTURE_GRAMMAR, LOGGER_NAME
from modules.invention.inventor.UnitAnalyzer import UnitAnalyzer
from modules.invention.inventor.errors import ImplSemanticError, SasSemanticError, SasSyntaxError
from modules.invention.inventor.responses import Template
from modules.utils import log_error


SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parent.parent.parent.parent
INPUTS_DIR = REPO_ROOT / "inputs"
INVENTOR_DIR = REPO_ROOT / "outputs" / "invention" / "inventor"
EVALUATION_DIR = REPO_ROOT / "evaluation" / "unit_validation"


class ConstraintSemanticValidator:
    def __init__(self, enable_unit_check: bool = True, input_dir: Path | None = None):
        self.parser = Lark(STRUCTURE_GRAMMAR, parser="earley", propagate_positions=True, ambiguity="resolve")
        self.enable_unit_check = enable_unit_check
        self.body_parser: Lark | None = None
        self.unit_analyzer: UnitAnalyzer | None = None
        self.agent: Agent | None = None
        self.init_error: str | None = None

        if self.enable_unit_check:
            if input_dir is None:
                raise ValueError("input_dir is required when unit checking is enabled")
            self._init_unit_check(input_dir)

    def _init_unit_check(self, input_dir: Path) -> None:
        context_definitions_path = input_dir / "context_schema.toml"
        if not context_definitions_path.exists():
            raise FileNotFoundError(f"Missing context_schema.toml: {context_definitions_path}")

        with open(context_definitions_path, "rb") as f:
            fields = tomli.load(f)["context_definitions"]["fields"]

        str_field_names: list[str] = []
        num_field_names: list[str] = []
        for field_name, field_info in fields.items():
            if field_info["type"] in ["int", "float"]:
                num_field_names.append(field_name)
            else:
                str_field_names.append(field_name)

        str_field_name_regex = "|".join(re.escape(name) for name in sorted(str_field_names, key=len, reverse=True))
        num_field_name_regex = "|".join(re.escape(name) for name in sorted(num_field_names, key=len, reverse=True))

        body_grammar = BODY_GRAMMAR.format(
            str_field_name_regex=str_field_name_regex,
            num_field_name_regex=num_field_name_regex,
        )
        self.body_parser = Lark(body_grammar, parser="earley", propagate_positions=True)

        self.agent = self._init_agent()
        if self.agent is None:
            self.init_error = "Unit checking initialization failed."
            return

        validation_prompt = """
You are validating the unit consistency of expressions in data constraints.

The dataset has the following field units:
<field_units>
{% for field_info in field_units %}
- {{ field_info.field }}: {{ field_info.unit }}
{% endfor %}
</field_units>

IMPORTANT: The unit format follows pint package convention with their corresponding powers:
- {} means unitless/dimensionless fields
- {"s": "1"} means seconds
- {"km": "1", "h": "-1"} means kilometers per hour (km/h)
- {"degree": "1"} means degrees
When you return units, use the SAME format.

Now, analyze the units of the given constants and symbols in the expression below.

<constants>
{{ constants }}
</constants>

<symbols>
{{ symbols }}
</symbols>

<expression>
semantics: {{ semantics }}
implementation: {{ implementation }}
</expression>

IMPORTANT NOTES:
1. For field references (e.g., v1.timestamp, v2.speed), use the field units provided above.
2. For constants, infer their units based on the context and mathematical operations.
3. For symbols (e.g., NTHRESHOLD1), infer their units based on how they are used in comparisons.
4. The constants and symbols are both collected from left to right in the given expression.
5. The name of unit should be acceptable by pint package (e.g., 'second', 'meter', 'kilometer', 'hour').
6. The order of constants and symbols in your response must strictly follow the order provided above.
"""
        self.unit_analyzer = UnitAnalyzer(input_dir, custom_prompt_template=validation_prompt)

    def _init_agent(self) -> Agent | None:
        model_spec = os.getenv("C2S_MODEL")
        api_key = os.getenv("C2S_API_KEY")
        if not model_spec:
            log_error(
                LOGGER_NAME,
                "C2S_MODEL environment variable is not set. "
                "Please set it with: export C2S_MODEL='provider:model_id'"
            )
            return None
        if not api_key:
            log_error(
                LOGGER_NAME,
                "C2S_API_KEY environment variable is not set. "
                "Please set it with: export C2S_API_KEY='your-api-key'"
            )
            return None

        parts = model_spec.split(":", 1)
        if len(parts) != 2:
            log_error(
                LOGGER_NAME,
                f"Invalid C2S_MODEL format: '{model_spec}'. "
                "Expected format: 'provider:model_id'"
            )
            return None

        provider, model_id = parts
        provider = provider.lower()
        if provider == "ark":
            model = OpenAILike(
                base_url="https://ark.cn-beijing.volces.com/api/v3",
                id=model_id,
                api_key=api_key,
                temperature=1.0,
            )
        elif provider == "openrouter":
            model = OpenRouter(
                api_key=api_key,
                id=model_id,
                temperature=1.0,
                max_tokens=None,
            )
        else:
            log_error(
                LOGGER_NAME,
                f"Unsupported provider: '{provider}'. Supported providers: 'ark', 'openrouter'"
            )
            return None

        return Agent(
            model=model,
            add_history_to_messages=True,
            num_history_responses=1000,
            use_json_mode=True,
        )

    def check_structure_syntax(self, structure: str) -> tuple[bool, str, Tree | None]:
        class StructureTransformer(Transformer):
            def structure(self, items):
                return items[0]

            def prod_structure_expr(self, items):
                return items[0]

            def prod_or_expr(self, items):
                return items[0]

            def prod_and_expr(self, items):
                return items[0]

            def prod_not_expr(self, items):
                return items[0]

            def prod_atom_expr(self, items):
                return items[0]

            def prod_paren(self, items):
                return items[0]

            def prod_bfunc(self, items):
                return items[0]

        try:
            tree = self.parser.parse(structure)
            tree = StructureTransformer().transform(tree)
            return True, "", tree
        except UnexpectedToken as e:
            expected = ", ".join(e.expected)
            token_info = f"'{e.token}'"
            if hasattr(e.token, "type"):
                token_info += f" (type: {e.token.type})"
            if hasattr(e.token, "value"):
                token_info += f" (value: '{e.token.value}')"
            error = SasSyntaxError(
                f"Expected: {expected}\nFound: {token_info}",
                e.line,
                e.column,
                e.get_context(structure, span=len(structure)),
            )
            return False, str(error), None
        except UnexpectedCharacters as e:
            error = SasSyntaxError(
                f"Unexpected character: '{e.char}'",
                e.line,
                e.column,
                e.get_context(structure, span=len(structure)),
            )
            return False, str(error), None
        except Exception as exc:
            error = SasSyntaxError(f"Error occurred during parsing: {exc}", 1, 1, structure)
            return False, str(error), None

    def extract_variable_name(self, node: Tree) -> str:
        assert node.data == "prod_variable"
        assert len(node.children) == 1 and isinstance(node.children[0], Token)
        return f"v{node.children[0].value}"

    def get_id_param_map_from_tree(self, tree: Tree) -> dict[str, list[str]]:
        id_param_map: dict[str, list[str]] = {}

        def _traverse(node: Tree) -> None:
            if node.data == "prod_bfunc_signature":
                bfunc_id = f"bfunc{node.children[0].value}"
                params = [self.extract_variable_name(var_node) for var_node in node.children[1].children]
                id_param_map[bfunc_id] = params
            elif node.data in ["prod_forall", "prod_exists"]:
                _traverse(node.children[1])
            elif node.data in ["prod_and", "prod_or", "prod_implies"]:
                _traverse(node.children[0])
                _traverse(node.children[1])
            elif node.data == "prod_not":
                _traverse(node.children[0])

        _traverse(tree)
        return id_param_map

    def check_param_validity_in_tree(self, tree: Tree) -> tuple[bool, str]:
        def _traverse(node: Tree, current_scope: set[str]) -> tuple[bool, str]:
            if node.data == "prod_bfunc_signature":
                bfunc_id = f"bfunc{node.children[0].value}"
                used_vars = {self.extract_variable_name(var_node) for var_node in node.children[1].children}
                invalid_vars = used_vars - current_scope
                if invalid_vars:
                    return False, (
                        f"bfunc {bfunc_id} uses variables {sorted(invalid_vars)} "
                        "that are not defined outside of the bfunc"
                    )
                return True, ""

            if node.data in ["prod_forall", "prod_exists"]:
                new_scope = current_scope.copy()
                new_scope.add(self.extract_variable_name(node.children[0]))
                return _traverse(node.children[1], new_scope)

            if node.data in ["prod_and", "prod_or", "prod_implies"]:
                left_ok, left_msg = _traverse(node.children[0], current_scope)
                if not left_ok:
                    return False, left_msg
                return _traverse(node.children[1], current_scope)

            if node.data == "prod_not":
                return _traverse(node.children[0], current_scope)

            raise ValueError(f"Unexpected node type: {node.data}")

        return _traverse(tree, set())

    def check_signature_consistency(self, tree: Tree, bfuncs: list[dict[str, Any]]) -> tuple[bool, str]:
        id_params_from_tree = self.get_id_param_map_from_tree(tree)
        id_params_from_signatures = {bfunc["id"]: bfunc["parameters"] for bfunc in bfuncs}

        used_ids = set(id_params_from_tree.keys())
        defined_ids = set(id_params_from_signatures.keys())
        if used_ids != defined_ids:
            missing = used_ids - defined_ids
            extra = defined_ids - used_ids
            message = "Bfunc ID mismatch between structure and signatures.\n"
            if missing:
                message += f"Used in structure but not defined: {sorted(missing)}\n"
            if extra:
                message += f"Defined but not used in structure: {sorted(extra)}"
            return False, message.strip()

        for bfunc_id in used_ids:
            params_in_tree = id_params_from_tree[bfunc_id]
            params_in_signature = id_params_from_signatures[bfunc_id]
            if len(params_in_tree) != len(params_in_signature):
                return False, (
                    f"Parameter count mismatch for {bfunc_id}.\n"
                    f"In structure: {len(params_in_tree)} parameters {params_in_tree}\n"
                    f"In signature: {len(params_in_signature)} parameters {params_in_signature}"
                )

        return True, ""

    def check_implementation_consistency(self, bfuncs: list[dict[str, Any]]) -> tuple[bool, str]:
        param_pattern = r"v\d+\."
        for bfunc in bfuncs:
            declared_params = set(bfunc["parameters"])
            found_params = {param[:-1] for param in re.findall(param_pattern, bfunc["implementation"])}
            if not found_params.issubset(declared_params):
                return False, (
                    f"Parameters mismatch for {bfunc['id']}.\n"
                    f"Used but not declared parameters: {sorted(found_params - declared_params)}"
                )
        return True, ""

    def check_unit_compatibility(self, constraint_data: dict[str, Any]) -> tuple[bool, str]:
        if not self.enable_unit_check:
            return True, ""
        assert self.body_parser is not None
        assert self.unit_analyzer is not None
        assert self.agent is not None

        for bfunc in constraint_data["bfuncs"]:
            try:
                tree = self.body_parser.parse(bfunc["implementation"])
                success, error = self.unit_analyzer.analyze(
                    self.agent,
                    bfunc["id"],
                    tree,
                    bfunc["semantics"],
                    bfunc["implementation"],
                )
                if not success:
                    return False, f"Unit check failed for {bfunc['id']}: {error}"
            except Exception as exc:
                return False, f"Unit analysis error for {bfunc['id']}: {exc}"

        return True, ""

    def validate_constraint(self, constraint_data: dict[str, Any]) -> dict[str, Any]:
        result: dict[str, Any] = {
            "structure": constraint_data["structure"],
            "semantics": constraint_data["semantics"],
            "checks": {
                "1.1_param_scope": {"passed": False, "error": ""},
                "1.2_signature_consistency": {"passed": False, "error": ""},
                "2.1_impl_consistency": {"passed": False, "error": ""},
            },
            "overall_passed": False,
        }
        if self.enable_unit_check:
            result["checks"]["2.2_unit_compatibility"] = {"passed": False, "error": ""}

        _, _, tree = self.check_structure_syntax(constraint_data["structure"])
        if tree is None:
            result["error"] = (
                "Unexpected: Failed to parse structure "
                "(this should not happen for invention-generated constraints)"
            )
            return result

        scope_success, scope_error = self.check_param_validity_in_tree(tree)
        result["checks"]["1.1_param_scope"]["passed"] = scope_success
        if not scope_success:
            result["checks"]["1.1_param_scope"]["error"] = scope_error
            return result

        sig_success, sig_error = self.check_signature_consistency(tree, constraint_data["bfuncs"])
        result["checks"]["1.2_signature_consistency"]["passed"] = sig_success
        if not sig_success:
            result["checks"]["1.2_signature_consistency"]["error"] = sig_error
            return result

        impl_success, impl_error = self.check_implementation_consistency(constraint_data["bfuncs"])
        result["checks"]["2.1_impl_consistency"]["passed"] = impl_success
        if not impl_success:
            result["checks"]["2.1_impl_consistency"]["error"] = impl_error
            return result

        if self.enable_unit_check:
            unit_success, unit_error = self.check_unit_compatibility(constraint_data)
            result["checks"]["2.2_unit_compatibility"]["passed"] = unit_success
            if not unit_success:
                result["checks"]["2.2_unit_compatibility"]["error"] = unit_error
                return result

        result["overall_passed"] = True
        return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run semantic checking for unit validation on extracted constraints under the current directory structure."
    )
    parser.add_argument("--scenario", "-s", required=True, help="Scenario name, e.g. taxi")
    parser.add_argument(
        "--constraint-dir",
        required=True,
        help="Constraint directory that directly contains xml/, py/, and mapping.json",
    )
    parser.add_argument(
        "--disable-unit-check",
        action="store_true",
        help="Disable unit compatibility checking",
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


def output_file(constraint_dir: Path) -> Path:
    return EVALUATION_DIR / constraint_dir.parent.name / constraint_dir.name / "results.json"


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
        if not path_value:
            continue
        relative_path = Path(str(path_value))
        candidate = relative_path.parent.name if relative_path.name == "template.json" else relative_path.name
        match = re.fullmatch(r"template_(\d+)", candidate)
        if match:
            return int(match.group(1))

    return None


def resolved_template_json_path(path_value: str) -> Path | None:
    raw_path = Path(path_value)
    candidate = raw_path if raw_path.is_absolute() else REPO_ROOT / raw_path
    if candidate.name != "template.json":
        candidate = candidate / "template.json"
    if candidate.exists():
        return candidate
    return None


def inventor_template_json_path(
    scenario: str,
    inventor_run_name: str,
    method_name: str,
    mapping: dict[str, Any],
    item: dict[str, Any],
) -> Path:
    for path_key in ("template_path", "original_path"):
        path_value = item.get(path_key)
        if path_value:
            direct_path = resolved_template_json_path(str(path_value))
            if direct_path is not None:
                return direct_path

    source_template_id = source_template_id_from_item(item)
    if source_template_id is None:
        raise ValueError("Incomplete extracted constraint entry in mapping.json")

    inferred_path = infer_template_json_path(scenario, inventor_run_name, method_name, source_template_id)
    if inferred_path is not None:
        return inferred_path

    return (
        INVENTOR_DIR
        / scenario
        / inventor_run_name
        / f"template_{source_template_id}"
        / "template.json"
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


def collect_targets(scenario: str, constraint_dir: Path) -> list[dict[str, Any]]:
    mapping = load_mapping(constraint_dir)
    inventor_run_name = inventor_run_name_from_mapping(mapping, constraint_dir)
    method_name = constraint_dir.name
    targets: list[dict[str, Any]] = []
    for item in mapping.get("constraints", []):
        source_template_id = source_template_id_from_item(item)
        constraint_id = item.get("constraint_id")
        if constraint_id is None:
            constraint_id = source_template_id
        if constraint_id is None:
            continue
        template_json = inventor_template_json_path(scenario, inventor_run_name, method_name, mapping, item)
        targets.append(
            {
                "constraint_id": int(constraint_id),
                "constraint_name": f"constraint_{int(constraint_id)}",
                "template_json": template_json,
            }
        )
    targets.sort(key=lambda item: item["constraint_id"])
    return targets


def validate_targets(
    scenario: str,
    targets: list[dict[str, Any]],
    enable_unit_check: bool,
) -> list[dict[str, Any]]:
    validator = ConstraintSemanticValidator(
        enable_unit_check=enable_unit_check,
        input_dir=(INPUTS_DIR / scenario) if enable_unit_check else None,
    )
    if validator.init_error:
        raise ValueError(validator.init_error)

    results: list[dict[str, Any]] = []
    total = len(targets)
    for idx, target in enumerate(targets, start=1):
        print(f"[{idx}/{total}] Validating {target['constraint_name']} ...", end=" ", flush=True)
        template_json = target["template_json"]
        if not template_json.exists():
            results.append(
                {
                    "constraint_id": target["constraint_id"],
                    "constraint_name": target["constraint_name"],
                    "template_json": str(template_json.relative_to(REPO_ROOT)),
                    "error": "Failed to load template.json",
                    "overall_passed": False,
                }
            )
            print("FAILED")
            continue

        try:
            template_data = Template.model_validate_json(template_json.read_text(encoding="utf-8")).model_dump()
            result = validator.validate_constraint(template_data)
            result["constraint_id"] = target["constraint_id"]
            result["constraint_name"] = target["constraint_name"]
            result["template_json"] = str(template_json.relative_to(REPO_ROOT))
            results.append(result)
            print("PASSED" if result.get("overall_passed", False) else "FAILED")
        except Exception as exc:
            results.append(
                {
                    "constraint_id": target["constraint_id"],
                    "constraint_name": target["constraint_name"],
                    "template_json": str(template_json.relative_to(REPO_ROOT)),
                    "error": str(exc),
                    "overall_passed": False,
                }
            )
            print("FAILED")

    return results


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    total_constraints = len(results)
    passed_constraints = sum(1 for item in results if item.get("overall_passed", False))
    failed_constraints = total_constraints - passed_constraints
    failed_constraint_names = [
        item["constraint_name"] for item in results if not item.get("overall_passed", False)
    ]
    return {
        "total_constraints": total_constraints,
        "passed_constraints": passed_constraints,
        "failed_constraints": failed_constraints,
        "pass_rate": round(passed_constraints / total_constraints * 100, 2) if total_constraints else 0.0,
        "failed_constraint_names": failed_constraint_names,
    }


def write_results(path: Path, summary: dict[str, Any], details: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "summary": summary,
        "details": details,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    try:
        args = parse_args()
        constraint_dir = resolve_repo_path(args.constraint_dir)
        enable_unit_check = not args.disable_unit_check

        if enable_unit_check and not (INPUTS_DIR / args.scenario).exists():
            raise FileNotFoundError(f"Missing scenario input dir: {INPUTS_DIR / args.scenario}")

        targets = collect_targets(args.scenario, constraint_dir)
        if not targets:
            raise ValueError("No extracted constraints matched the given selection")

        results = validate_targets(args.scenario, targets, enable_unit_check)
        summary = summarize(results)
        out_file = output_file(constraint_dir)
        write_results(out_file, summary, results)

        print(f"Wrote {out_file.relative_to(REPO_ROOT)}")
        print(f"Unit check enabled: {enable_unit_check}")
        print(f"Total constraints: {summary['total_constraints']}")
        print(f"Passed constraints: {summary['passed_constraints']}")
        print(f"Failed constraints: {summary['failed_constraints']}")
        print(f"Pass rate: {summary['pass_rate']:.2f}%")
        return 0
    except KeyboardInterrupt:
        print("\nSemantic checking interrupted")
        return 1
    except Exception as exc:
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
