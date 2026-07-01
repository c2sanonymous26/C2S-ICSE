import json
import tomli
import re
from typing import Any
from pathlib import Path
from lark import Lark

from ...utils import log_info
from .. import BODY_GRAMMAR, RESTRICTION_GRAMMAR, LOGGER_NAME
from . import BFUNC_FILE_NAME, RESTRICTIONS_FILE_NAME


def convert_bfuncs(
    bfuncs: list[dict[str, Any]], 
    dataset_file_path: Path, 
    output_dir: Path
) -> None:
    
    assert output_dir is not None, "output_dir is required"

    log_info(LOGGER_NAME, "Converting bfuncs into python file starts")

    # Get field names
    str_field_names, num_field_names = _get_field_names(dataset_file_path)
    
    # Initialize BfuncBodyParser
    str_field_name_regex = '|'.join(re.escape(name) for name in sorted(str_field_names, key=len, reverse=True))
    num_field_name_regex = '|'.join(re.escape(name) for name in sorted(num_field_names, key=len, reverse=True))
    body_grammar = BODY_GRAMMAR.format(
        str_field_name_regex=str_field_name_regex,
        num_field_name_regex=num_field_name_regex
    )
    body_parser = Lark(body_grammar, parser='earley', propagate_positions=True, ambiguity='resolve')
    
    # Parse bfuncs
    bfunc_strs = []
    bfunc_pattern = re.compile("^bfunc(\\d+)$")
    for bfunc in bfuncs:
        match = re.match(bfunc_pattern, bfunc['id'])
        assert match, f"Invalid bfunc id: {bfunc['id']}"
        id_num = int(match.group(1))
        id = f"bfunc_{id_num}"
        semantics = bfunc['semantics']
        implementation = bfunc['implementation']

        # Parse implementation (syntax already verified)
        converted_implementation = _convert_implementation(body_parser, implementation)
        bfunc_body = f'return {converted_implementation}'
        
        # Synthesize a bfunc string
        bfunc_str = _synthesize_bfunc_str(id, semantics, bfunc_body)
        bfunc_strs.append(bfunc_str)
        
    # Write to Python file
    output_file = output_dir / BFUNC_FILE_NAME
    with open(output_file, 'w') as f:
        f.write("from math import *\n")
        f.write("from typing import Any\n\n")
        
        for bfunc_str in bfunc_strs:
            f.write(bfunc_str)
            f.write("\n\n")
    

    # Initialize restriction parser
    restriction_grammar = RESTRICTION_GRAMMAR
    restriction_parser = Lark(restriction_grammar, parser='earley', propagate_positions=True, ambiguity='resolve')
    
    # Parse restrictions
    restriction_dict = {}
    for bfunc in bfuncs:
        match = re.match(bfunc_pattern, bfunc['id'])
        assert match, f"Invalid bfunc id: {bfunc['id']}"
        id_num = int(match.group(1))
        id = f"bfunc_{id_num}"
        restrictions = bfunc['restrictions']
        if len(restrictions) == 0:
            continue
        else:
            converted_restrictions = _convert_restrictions(restriction_parser, restrictions)
            restriction_dict[id] = converted_restrictions
    
    # Write to JSON file
    if len(restriction_dict) > 0:
        restriction_file = output_dir / RESTRICTIONS_FILE_NAME
        with open(restriction_file, 'w') as f:
            json.dump(restriction_dict, f, indent=4)
    
    log_info(LOGGER_NAME, f"Saved bfuncs to {output_file}")
    if len(restriction_dict) > 0:
        log_info(LOGGER_NAME, f"Saved restrictions to {restriction_file}")
    log_info(LOGGER_NAME, "Converting bfuncs into python file done")

def _get_field_names(dataset_file_path: Path) -> tuple[list[str], list[str]]:
    str_field_names = []
    num_field_names = []

    with open(dataset_file_path, 'rb') as f:
        fields = tomli.load(f)['context_definitions']['fields']
        for field_name, field_info in fields.items():
            if field_info['type'] in ['int', 'float']:
                num_field_names.append(field_name)
            else:
                str_field_names.append(field_name)
                
    return str_field_names, num_field_names

def _convert_implementation(body_parser: Lark, implementation: str) -> str:
    def process_node(node):
        if node.data == 'prod_body_expr':
            return process_node(node.children[0])
        
        # Logical operations
        elif node.data == 'prod_body_implies':
            left = process_node(node.children[0])
            right = process_node(node.children[1])
            return f"implies({left}, {right})"
        elif node.data == 'prod_body_or':
            left = process_node(node.children[0])
            right = process_node(node.children[1])
            return f"({left}) or ({right})"
        elif node.data == 'prod_body_and':
            left = process_node(node.children[0])
            right = process_node(node.children[1])
            return f"({left}) and ({right})"
        elif node.data == 'prod_body_not':
            expr = process_node(node.children[0])
            return f"not ({expr})"
        
        # Pass-through nodes
        elif node.data in ['prod_body_or_expr', 'prod_body_and_expr', 
                        'prod_body_not_expr', 'prod_body_atom_expr', 
                        'prod_body_cmp_expr']:
            return process_node(node.children[0])
        
        # Parentheses
        elif node.data == 'prod_body_paren':
            return f"({process_node(node.children[0])})"
        
        # String comparison
        elif node.data in ['prod_str_cmp_expr_1', 'prod_str_cmp_expr_2']:
            field = process_node(node.children[0])
            op = node.children[1].value
            target = process_node(node.children[2])
            return f"{field} {op} {target}"
        
        # String field
        elif node.data == 'prod_str_field':
            var_num = node.children[0].value
            field_name = node.children[1].value
            return f'var_bindings["v{var_num}"]["{field_name}"]'
        
        # String target
        elif node.data == 'prod_str_target_literal':
            return node.children[0].value
        elif node.data == 'prod_str_target_threshold':
            threshold_num = node.children[1].value
            return f"_S_THRESHOLD_{threshold_num}"
        elif node.data == 'prod_str_target_field':
            return process_node(node.children[0])
        
        # Numeric comparison
        elif node.data in ['prod_num_cmp_expr_2', 'prod_num_cmp_expr_1']:
            left = process_node(node.children[0])
            op = node.children[1].value
            right = process_node(node.children[2])
            return f"{left} {op} {right}"
        
        # Numeric expressions
        elif node.data == 'prod_num_term_single':
            return process_node(node.children[0])
        elif node.data == 'prod_num_factor_single':
            return process_node(node.children[0])
        elif node.data == 'prod_num_add':
            left = process_node(node.children[0])
            right = process_node(node.children[1])
            return f"{left} + {right}"
        elif node.data == 'prod_num_sub':
            left = process_node(node.children[0])
            right = process_node(node.children[1])
            return f"{left} - {right}"
        elif node.data == 'prod_num_mul':
            left = process_node(node.children[0])
            right = process_node(node.children[1])
            return f"{left} * {right}"
        elif node.data == 'prod_num_div':
            left = process_node(node.children[0])
            right = process_node(node.children[1])
            return f"{left} / {right}"
        elif node.data == 'prod_num_mod':
            left = process_node(node.children[0])
            right = process_node(node.children[1])
            return f"{left} % {right}"
        
        # Numeric factors
        elif node.data == 'prod_num_factor_neg':
            return f"-{process_node(node.children[0])}"
        elif node.data == 'prod_num_factor_paren':
            return f"({process_node(node.children[0])})"
        elif node.data == 'prod_num_factor_math_func':
            return process_node(node.children[0])
        elif node.data == 'prod_num_factor_field':
            return process_node(node.children[0])
        elif node.data == 'prod_num_factor_literal':
            return node.children[0].value
        
        # Math functions
        elif node.data == 'prod_math_func_abs':
            return f"abs({process_node(node.children[0])})"
        elif node.data.startswith('prod_math_func_'):
            func_name = node.data.replace('prod_math_func_', '')
        
            if func_name in ['atan2', 'min', 'max', 'pow']:
                arg1 = process_node(node.children[0])
                arg2 = process_node(node.children[1]) if func_name != 'pow' else node.children[1].value
                return f"{func_name}({arg1}, {arg2})"
            elif func_name == 'cbrt':
                return f"{process_node(node.children[0])} ** (1/3)"
            else:
                return f"{func_name}({process_node(node.children[0])})"
        
        # Numeric field
        elif node.data == 'prod_num_field':
            var_num = node.children[0].value
            field_name = node.children[1].value
            return f'var_bindings["v{var_num}"]["{field_name}"]'
        
        # Numeric target
        elif node.data == 'prod_num_target_term':
            return process_node(node.children[0])
        elif node.data == 'prod_num_target_factor':
            return process_node(node.children[0])
        elif node.data == 'prod_num_target_add':
            left = process_node(node.children[0])
            right = process_node(node.children[1])
            return f"{left} + {right}"
        elif node.data == 'prod_num_target_sub':
            left = process_node(node.children[0])
            right = process_node(node.children[1])
            return f"{left} - {right}"
        elif node.data == 'prod_num_target_mul':
            left = process_node(node.children[0])
            right = process_node(node.children[1])
            return f"{left} * {right}"
        elif node.data == 'prod_num_target_div':
            left = process_node(node.children[0])
            right = process_node(node.children[1])
            return f"{left} / {right}"
        elif node.data == 'prod_num_target_mod':
            left = process_node(node.children[0])
            right = process_node(node.children[1])
            return f"{left} % {right}"
        elif node.data == 'prod_num_target_threshold':
            threshold_num = node.children[1].value
            return f"_N_THRESHOLD_{threshold_num}"
        elif node.data == 'prod_num_target_num_expr':
            return process_node(node.children[0])
        elif node.data == 'prod_num_target_paren':
            return process_node(node.children[0])
        elif node.data == 'prod_num_target_neg':
            return f"-{process_node(node.children[0])}"
        else:
            raise ValueError(f"Unknown node type: {node.data}")

    tree = body_parser.parse(implementation)
    return process_node(tree)    

def _convert_restrictions(restriction_parser: Lark, restrictions: list[str]) -> list[str] | None:
    def process_node(node):
        if node.data in ['prod_num_restriction', 'prod_str_restriction']:
            return process_node(node.children[0])
        elif node.data in ['prod_num_value_restriction', 'prod_num_range_restriction']:
            return process_node(node.children[0])
        elif node.data == 'prod_num_value_eq':
            left = process_node(node.children[0])
            right_val = node.children[1].value
            return [f"{left} == {right_val}"]
        elif node.data == 'prod_num_value_neq':
            left = process_node(node.children[0])
            right_val = node.children[1].value
            return [f"{left} != {right_val}"]
        elif node.data in ['prod_num_range_lt', 'prod_num_range_gt']:
            # Check if there is an optional left boundary
            if len(node.children) == 5:
                # Case with left boundary
                left_bound = node.children[0].value
                left_op = node.children[1].value
                symbol = process_node(node.children[2])
                right_op = node.children[3].value
                right_bound = node.children[4].value
                return [f"{left_bound} {left_op} {symbol}", f"{symbol} {right_op} {right_bound}"]
            else:
                # Case without left boundary
                symbol = process_node(node.children[0])
                op = node.children[1].value
                bound = node.children[2].value
                return [f"{symbol} {op} {bound}"]
        elif node.data == 'prod_num_symbol':
            threshold_num = node.children[1].value
            return f"_N_THRESHOLD_{threshold_num}"
        elif node.data == 'prod_str_value_restriction':
            return process_node(node.children[0])
        elif node.data == 'prod_str_value_eq':
            left = process_node(node.children[0])
            right_val = node.children[1].value
            return [f"{left} == {right_val}"]
        elif node.data == 'prod_str_value_neq':
            left = process_node(node.children[0])
            right_val = node.children[1].value
            return [f"{left} != {right_val}"]
        elif node.data == 'prod_str_symbol':
            threshold_num = node.children[1].value
            return f"_S_THRESHOLD_{threshold_num}"
        else:
            raise ValueError(f"Unknown node type: {node.data}")

    converted_restrictions = []
    for restriction in restrictions:
        tree = restriction_parser.parse(restriction)
        converted_restrictions.extend(process_node(tree))
    
    if len(converted_restrictions) == 0:
        return None
    
    return converted_restrictions

def _synthesize_bfunc_str(id: str, semantics: str, bfunc_body: str) -> str:
    param_str = 'var_bindings: dict[str, dict[str, Any]]'
    doc_str = f'    """{semantics}"""'
    return f"def {id}({param_str}) -> bool:\n{doc_str}\n    {bfunc_body}"