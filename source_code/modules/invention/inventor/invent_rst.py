import re
import tomli
from agno.agent import Agent
from pathlib import Path
from jinja2 import Environment
from lark import Lark, UnexpectedToken, UnexpectedCharacters, Tree, Transformer, LarkError
from typing import Any

from ...utils import log_info, log_warning, CONTEXT_DEFINITIONS_FILE_NAME, log_error
from .. import (
    LOGGER_NAME,
    BODY_GRAMMAR,
    RESTRICTION_GRAMMAR,
    STRUCTURE_GRAMMAR
)
from . import MAX_TRY_TIMES
from .responses import (
    StructureAndSignatures, 
    BfuncImplementationWithCheck,
    SymbolRestrictions
)
from .prompts import (
    PHASE4_ADD_RESTRICTIONS_PROMPT_TEMPLATE,
    STRUCTURED_OUTPUT_ERROR_PROMPT,
    PHASE4_FIX_RESTRICTION_SYNTAX_ERROR_PROMPT_TEMPLATE
)

def invent_restrictions(
    agno_agent: Agent,
    input_dir: Path,
    structure_and_signatures: StructureAndSignatures,
    bfunc_implementations: BfuncImplementationWithCheck,
    few_shots: list[dict[str, Any]]
) -> tuple[SymbolRestrictions | None, dict[str, set[str]] | None]:
    log_info(LOGGER_NAME, "Restrictions invention starts", center=True, symbol="~")
        
    # First get all bfunc symbols to know which bfuncs contain thresholds
    bfunc_symbol_dict = _get_bfunc_symbol_dict(input_dir, bfunc_implementations)
    
    # Then determine which bfuncs need restrictions based on position AND whether other side has symbols
    restrict_bfuncs = _get_restrict_bfuncs(structure_and_signatures, bfunc_symbol_dict)
    
    restrict_bfunc_symbol_dict = {}
    # Create dictionary mapping for restrict_bfuncs for easy lookup
    restrict_bfuncs_dict = {bfunc_id: semantics for bfunc_id, semantics in restrict_bfuncs}
    # Create dictionary mapping for bfunc_implementations
    bfunc_implementations_dict = {body.id: body.implementation for body in bfunc_implementations.bodies}
    
    for bfunc_id, symbols in bfunc_symbol_dict.items():
        if bfunc_id in restrict_bfuncs_dict:
            restrict_bfunc_symbol_dict[bfunc_id] = {
                "semantics": restrict_bfuncs_dict[bfunc_id],
                "implementation": bfunc_implementations_dict[bfunc_id],
                "symbols": symbols
            }
            
    if len(restrict_bfunc_symbol_dict) == 0:
        log_info(LOGGER_NAME, "No restrictions to add")
        return None, None
        
    user_prompt = _render_add_restrictions_prompt(restrict_bfunc_symbol_dict, few_shots)
    parser = Lark(RESTRICTION_GRAMMAR, parser='earley', propagate_positions=True, ambiguity='resolve')
    
    restrictions = None 
    restrict_times = 0
    while restrict_times < MAX_TRY_TIMES:
        # Update and call agent
        agno_agent.response_model = SymbolRestrictions
        response = agno_agent.run(user_prompt, stream=False)
        restrictions = response.content
        
        # Check conversion result
        if not isinstance(restrictions, SymbolRestrictions):
            restrictions = None
            restrict_times += 1
            user_prompt = STRUCTURED_OUTPUT_ERROR_PROMPT
            continue
        
        if restrictions.restrictions is None:
            log_warning(LOGGER_NAME, "Restrictions invention returns empty result.")
            return None, None
        
        # Remove over-reported restrictions
        # Collect all valid symbols
        all_valid_symbols = set()
        for bfunc_info in restrict_bfunc_symbol_dict.values():
            all_valid_symbols.update(bfunc_info["symbols"])
        
        restrictions.restrictions = [
            restriction for restriction in restrictions.restrictions if restriction.symbol in all_valid_symbols
        ]
        
        # Check syntax of each restriction
        success, errors = _check_syntax(parser, restrictions)
        if success:
            break
        else:
            restrictions = None
            restrict_times += 1
            user_prompt = _render_fix_syntax_error_prompt(errors)
            continue
    
    if restrictions is None:
        log_warning(LOGGER_NAME, "Restrictions invention failed")
        return None, None
    else:
        log_info(LOGGER_NAME, "Restrictions invention done", center=True, symbol="~", newlines=2)
        return restrictions, bfunc_symbol_dict

def _get_restrict_bfuncs(structure_and_signatures: StructureAndSignatures, bfunc_symbol_dict: dict[str, set[str]]) -> list[str]:
    restrict_bfunc_ids = []
    
    def _parse_structure(structure: str) -> Tree:
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
            parser = Lark(STRUCTURE_GRAMMAR, parser='earley', propagate_positions=True, ambiguity='resolve')
            tree = parser.parse(structure)
            transformer = StructureTransformer()
            tree = transformer.transform(tree)
            return tree
        except LarkError as e:
            log_error(LOGGER_NAME, f"Failed to parse structure: {str(e)}")
            raise

    def _has_symbols(node: Tree) -> bool:
        """Check if a subtree contains any bfunc with symbols
        
        Note: prod_paren nodes are already removed by StructureTransformer
        """
        if node.data == 'prod_bfunc_signature':
            bfunc_id = f'bfunc{node.children[0].value}'
            return bfunc_id in bfunc_symbol_dict
        elif node.data == 'prod_forall':
            return _has_symbols(node.children[1])
        elif node.data == 'prod_exists':
            return _has_symbols(node.children[1])
        elif node.data in ['prod_and', 'prod_or', 'prod_implies']:
            return _has_symbols(node.children[0]) or _has_symbols(node.children[1])
        elif node.data == 'prod_not':
            return _has_symbols(node.children[0])
        else:
            raise ValueError(f"Unexpected node type in structure tree: {node.data}")
    
    def _traverse(node: Tree, goal: bool) -> None:
        nonlocal restrict_bfunc_ids
        
        if node.data == 'prod_forall':
            return _traverse(node.children[1], True)
        elif node.data == 'prod_exists':
            return _traverse(node.children[1], True)
        elif node.data == 'prod_and':
            if not goal:
                # Only update left side if right side has symbols
                if _has_symbols(node.children[1]):
                    _update_bfuncs(node.children[0])
                _traverse(node.children[1], goal)
            else:
                return _traverse(node.children[0], goal) and _traverse(node.children[1], goal)
        elif node.data == 'prod_or':
            if goal:
                # Only update left side if right side has symbols
                if _has_symbols(node.children[1]):
                    _update_bfuncs(node.children[0])
                _traverse(node.children[1], goal)
            else:
                return _traverse(node.children[0], goal) or _traverse(node.children[1], goal)
        elif node.data == 'prod_implies':
            if goal:
                # Only update antecedent if consequent has symbols
                if _has_symbols(node.children[1]):
                    _update_bfuncs(node.children[0])
                _traverse(node.children[1], goal)
            else:
                return _traverse(node.children[0], not goal) or _traverse(node.children[1], goal)
        elif node.data == 'prod_not':
            return _traverse(node.children[0], not goal)
        elif node.data == 'prod_bfunc_signature':
            return
            
    def _update_bfuncs(node: Tree) -> None:
        nonlocal restrict_bfunc_ids
        
        if node.data == 'prod_bfunc_signature':
            restrict_bfunc_ids.append(f'bfunc{node.children[0].value}')
        elif node.data == 'prod_forall':
            _update_bfuncs(node.children[1])
        elif node.data == 'prod_exists':
            _update_bfuncs(node.children[1])
        elif node.data == 'prod_and':
            _update_bfuncs(node.children[0])
            _update_bfuncs(node.children[1])
        elif node.data == 'prod_or':
            _update_bfuncs(node.children[0])
            _update_bfuncs(node.children[1])
        elif node.data == 'prod_implies':
            _update_bfuncs(node.children[0])
            _update_bfuncs(node.children[1])
        elif node.data == 'prod_not':
            _update_bfuncs(node.children[0])
    
    def _add_semantics(restrict_bfunc_ids: list[str]) -> list[tuple[str, str]]:
        restrict_bfuncs = []
        signatures = structure_and_signatures.signatures
        for bfunc_id in restrict_bfunc_ids:
            semantics = next((signature.semantics for signature in signatures if signature.id == bfunc_id), None)
            assert semantics is not None, f"Semantics for bfunc {bfunc_id} not found"
            restrict_bfuncs.append((bfunc_id, semantics))
        return restrict_bfuncs
            
    tree = _parse_structure(structure_and_signatures.structure)                
    _traverse(tree, True)
    restrict_bfuncs = _add_semantics(restrict_bfunc_ids)
    
    return restrict_bfuncs

def _get_bfunc_symbol_dict(input_dir: Path, bfunc_implementations: BfuncImplementationWithCheck) -> dict[str, set[str]]:

    def _get_field_names(input_dir: Path) -> tuple[list[str], list[str]]:
        # Get field names for creating parser
        str_field_names = []
        num_field_names = []
        dataset_path = input_dir / CONTEXT_DEFINITIONS_FILE_NAME
        if dataset_path.exists():
            with open(dataset_path, 'rb') as f:
                fields = tomli.load(f)['context_definitions']['fields']
                for field_name, field_info in fields.items():
                    if field_info['type'] in ['int', 'float']:
                        num_field_names.append(field_name)
                    else:
                        str_field_names.append(field_name)
        
        return str_field_names, num_field_names

    def _get_symbols(structure_parser: Lark, implementation: str) -> set[str]:
        tree = structure_parser.parse(implementation)
        symbols = set()
        for node in tree.iter_subtrees():
            if node.data == 'prod_str_target_threshold':
                symbols.add(f'{node.children[0].value}{node.children[1].value}')
            elif node.data == 'prod_num_target_threshold':
                symbols.add(f'{node.children[0].value}{node.children[1].value}')
        return symbols if len(symbols) > 0 else None
    
    str_field_names, num_field_names = _get_field_names(input_dir)
    # Sort field names by length (descending) to avoid prefix matching issues
    str_field_name_regex = '|'.join(re.escape(name) for name in sorted(str_field_names, key=len, reverse=True))
    num_field_name_regex = '|'.join(re.escape(name) for name in sorted(num_field_names, key=len, reverse=True))
    
    grammar = BODY_GRAMMAR.format(
        str_field_name_regex=str_field_name_regex,
        num_field_name_regex=num_field_name_regex
    )
    structure_parser = Lark(grammar, parser='earley', propagate_positions=True, ambiguity='resolve')
    
    bfunc_symbol_dict = {}
    for body in bfunc_implementations.bodies:
        symbols = _get_symbols(structure_parser, body.implementation)
        if symbols is not None:
            bfunc_symbol_dict[body.id] = symbols
            
    return bfunc_symbol_dict

def _render_add_restrictions_prompt(restrict_bfunc_symbol_dict: dict[str, dict], few_shots: list[dict[str, Any]]) -> str:
    jinjia_env = Environment(trim_blocks=True, lstrip_blocks=True)
    add_restrictions_prompt_template = jinjia_env.from_string(PHASE4_ADD_RESTRICTIONS_PROMPT_TEMPLATE)
    add_restrictions_prompt = add_restrictions_prompt_template.render(
        restrict_bfunc_symbol_dict=restrict_bfunc_symbol_dict,
        restriction_grammar=RESTRICTION_GRAMMAR,
        few_shots=few_shots
    )
    return add_restrictions_prompt

def _check_syntax(parser: Lark, restrictions: SymbolRestrictions) -> tuple[bool, str | None]:    
    class SyntaxError(Exception):
        def __init__(self, id: str, message: str, line: int, column: int, context: str):
            self.id = id
            self.message = message
            self.line = line
            self.column = column
            self.context = context
            super().__init__(f"Syntax Error for {id}:\n{message}\nLocation: Line {line}, Column {column}\nContext: {context}")
            
    errors = []
    for restriction in restrictions.restrictions:
        try:
            parser.parse(restriction.restriction)
        except UnexpectedToken as e:
            expected = ", ".join(e.expected)
            error_msg = f"Expected: {expected}\nFound: {e.token}\n"
            error = SyntaxError(
                restriction.symbol,
                error_msg[:-1],
                e.line,
                e.column,
                e.get_context(restriction.restriction, span=len(restriction.restriction))
            )
            errors.append(str(error))
        except UnexpectedCharacters as e:
            error_msg = f"Unexpected character: '{e.char}'\n"
            error = SyntaxError(
                restriction.symbol,
                error_msg[:-1],
                e.line,
                e.column,
                e.get_context(restriction.restriction, span=len(restriction.restriction))
            )
            errors.append(str(error))
        except Exception as e:
            error_msg = f"Error occurred during parsing: {str(e)}"
            error = SyntaxError(
                restriction.symbol,
                error_msg,
                1,
                1,
                restriction.restriction
            )
            errors.append(str(error))
        
    if errors:
        return False, "\n".join(errors)
    else:
        return True, None

def _render_fix_syntax_error_prompt(errors: str) -> str:
    jinjia_env = Environment(trim_blocks=True, lstrip_blocks=True)
    fix_restriction_syntax_error_prompt_template = jinjia_env.from_string(PHASE4_FIX_RESTRICTION_SYNTAX_ERROR_PROMPT_TEMPLATE)
    fix_restriction_syntax_error_prompt = fix_restriction_syntax_error_prompt_template.render(
        errors=errors
    )
    return fix_restriction_syntax_error_prompt

