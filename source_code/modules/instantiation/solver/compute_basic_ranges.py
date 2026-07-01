from pathlib import Path
import json
import warnings
import numpy as np
import scipy.optimize
import itertools
import random
import tomli
from typing import Optional
from lark import Tree, Lark
import sympy as sp
import re
import time

from .. import LOGGER_NAME, INDENT 
from ...invention import BODY_GRAMMAR
from ...invention.inventor import INVENTOR_OUTPUT_DIR, BFUNC_IMPLEMENTATION_FILE_NAME
from ...utils import (
    INPUT_DIR, CONTEXT_DEFINITIONS_FILE_NAME,
    log_warning, log_info, timeout_process, timeout_thread, TimeoutException
)


def compute(scenario: str, constraint: str) -> dict[str, tuple[float, float]]:
    
    dataset_file_path = INPUT_DIR / scenario / CONTEXT_DEFINITIONS_FILE_NAME
    if not dataset_file_path.exists():
        raise FileNotFoundError(f"Dataset file not found: {dataset_file_path}")
    
    bfunc_implementation_file_path = INVENTOR_OUTPUT_DIR / scenario / constraint / BFUNC_IMPLEMENTATION_FILE_NAME
    if not bfunc_implementation_file_path.exists():
        raise FileNotFoundError(f"Bfunc implementation file not found: {bfunc_implementation_file_path}")
    
    approximate_ranges = _approximate_compute(dataset_file_path, bfunc_implementation_file_path)
    
    try:
        theoretical_ranges = _theoretical_compute(dataset_file_path, bfunc_implementation_file_path)
    except TimeoutException:
        log_warning(LOGGER_NAME, f"Theoretical compute timeout in 60 seconds")
        theoretical_ranges = {}
    
    overall_ranges = {}
    overall_ranges.update(approximate_ranges)
    for symbol, (min_val, max_val) in theoretical_ranges.items():
        if symbol in overall_ranges:
            overall_ranges[symbol] = (min(min_val, overall_ranges[symbol][0]), max(max_val, overall_ranges[symbol][1]))
        else:
            overall_ranges[symbol] = (min_val, max_val)

    return_ranges = {}
    sym_pattern = r"NTHRESHOLD(\d+)"
    for symbol, (min_val, max_val) in overall_ranges.items():
        match = re.fullmatch(sym_pattern, symbol)
        assert match, f"Invalid symbol: {symbol}"
        return_ranges[f'_N_THRESHOLD_{match.group(1)}'] = (float(min_val), float(max_val))

    return return_ranges


def _load_field_ranges(dataset_file_path: Path) -> dict[str, tuple[float, float, bool, bool]]:
    """Load field range information"""
    
    def _parse_range_string(range_str: str) -> Optional[tuple[float, float, bool, bool]]:
        """Parse range string, e.g., '[0, +oo)' """
        try:
            # Remove whitespace
            range_str = range_str.strip()
            
            # Check open/closed intervals
            left_inclusive = range_str.startswith('[')
            right_inclusive = range_str.endswith(']')
            
            # Remove brackets
            content = range_str[1:-1]
            parts = [p.strip() for p in content.split(',')]
            
            if len(parts) != 2:
                return None
            
            # Parse minimum value
            min_str = parts[0]
            if min_str == '-oo':
                min_val = -float('inf')
            else:
                min_val = float(min_str)
            
            # Parse maximum value
            max_str = parts[1]
            if max_str == '+oo':
                max_val = float('inf')
            else:
                max_val = float(max_str)
            
            return min_val, max_val, left_inclusive, right_inclusive
            
        except Exception as e:
            raise ValueError(f"Failed to parse range string '{range_str}': {e}")
    
    field_ranges = {}

    with open(dataset_file_path, 'rb') as f:
        dataset_config = tomli.load(f)
        fields = dataset_config.get('context_definitions', {}).get('fields', {})
        
        for field_name, field_info in fields.items():
            if field_info.get('type') in ['int', 'float']:
                range_info = field_info.get('range')
                if range_info:
                    parsed_range = _parse_range_string(range_info)
                    if parsed_range:
                        field_ranges[field_name] = parsed_range
    
    return field_ranges
    
def _load_bfunc_implementations(bfunc_implementation_file_path: Path) -> dict[str, str]:
    """Load bfunc implementations"""
    with open(bfunc_implementation_file_path, 'r') as f:
        bfunc_implementation_json = json.load(f)
    
    bfunc_implementations = {}
    for body in bfunc_implementation_json['bodies']:
        bfunc_implementations[body['id']] = body['implementation']
    
    return bfunc_implementations
    

def _extract_num_thresholds_from_node(node: Tree) -> set[str]:
    """Extract all numeric thresholds from AST node"""
    num_thresholds = set()
    
    def _traverse(n):
        if isinstance(n, Tree):
            if n.data == 'prod_num_target_threshold' and len(n.children) >= 2:
                # NUM_SYMBOL_PREFIX NATURAL
                num_thresholds.add(n.children[0].value + str(n.children[1].value))
            for child in n.children:
                _traverse(child)
    
    _traverse(node)
    return num_thresholds    
    
def _contains_num_thresholds(node: Tree) -> bool:
    """Check if AST node contains numeric thresholds"""
    
    def _traverse(n):
        if isinstance(n, Tree):
            if n.data == 'prod_num_target_threshold':
                return True
            for child in n.children:
                if _traverse(child):
                    return True
        return False
    
    return _traverse(node)

def _contains_str_thresholds(node: Tree) -> bool:
    """Check if contains string thresholds"""
    def _traverse(n):
        if isinstance(n, Tree):
            if n.data == 'prod_str_target_threshold':
                return True
            for child in n.children:
                if _traverse(child):
                    return True
        return False
    return _traverse(node)

def _process_comparison_expressions(dataset_file_path: Path, bfunc_implementations: dict[str, str]) -> dict[str, list[tuple[sp.Expr, str]]]:
    """Process comparison expressions, separate threshold symbols and field expressions"""
    
    # Internal function definitions
    
        
    def _get_field_names_for_parser() -> tuple[list[str], list[str]]:
        """Get field names for building parser"""
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
    
    def _build_body_parser(str_field_names: list[str], num_field_names: list[str]) -> Lark:
        """Build body parser"""
        str_field_name_regex = '|'.join(re.escape(name) for name in sorted(str_field_names, key=len, reverse=True))
        num_field_name_regex = '|'.join(re.escape(name) for name in sorted(num_field_names, key=len, reverse=True))
        
        grammar = BODY_GRAMMAR.format(
            str_field_name_regex=str_field_name_regex,
            num_field_name_regex=num_field_name_regex
        )
        return Lark(grammar, parser='earley', propagate_positions=True, ambiguity='resolve')

    def _find_num_comparison_nodes(tree: Tree) -> list[Tree]:
        """Find all comparison nodes from syntax tree"""
        comparison_nodes = []
        
        def _traverse(node):
            if isinstance(node, Tree):
                # Only focus on numeric comparison expressions
                if node.data in ['prod_num_cmp_expr_1', 'prod_num_cmp_expr_2']:
                    comparison_nodes.append(node)
                
                for child in node.children:
                    _traverse(child)
        
        _traverse(tree)
        return comparison_nodes

    def _separate_threshold_and_field_sides(
        comparison_node: Tree
    ) -> tuple[Tree, Tree, str]:
        """Separate threshold terms and field terms based on grammar rules"""
        
        def _separate_expressions(threshold_side_expr: Tree, field_side_expr: Tree) -> tuple[Tree, Tree]:
            """
            Separate threshold and field expressions
            
            Args:
                threshold_side_expr: Expression possibly containing threshold
                field_side_expr: Field side expression
                
            Returns:
                (threshold_expr, field_expr): Separated threshold expression and field expression
            """
            
            # Handle negative sign
            if threshold_side_expr.data == 'prod_num_target_neg':
                # Add negative sign to field_side_expr
                neg_field_expr = Tree('prod_num_factor_neg', [field_side_expr])
                return _separate_expressions(threshold_side_expr.children[0], neg_field_expr)
            
            # Handle pass-through nodes
            if threshold_side_expr.data in ['prod_num_target_term', 'prod_num_target_factor']:
                return _separate_expressions(threshold_side_expr.children[0], field_side_expr)
            
            # Handle parentheses
            if threshold_side_expr.data == 'prod_num_target_paren':
                return _separate_expressions(threshold_side_expr.children[0], field_side_expr)
            
            # Handle modulo operation - modulo has no simple inverse operation, don't separate
            if threshold_side_expr.data == 'prod_num_target_mod':
                return threshold_side_expr, field_side_expr
            
            # Handle binary operations
            if threshold_side_expr.data == 'prod_num_target_add':
                current_op = 'add'
            elif threshold_side_expr.data == 'prod_num_target_sub':
                current_op = 'sub'
            elif threshold_side_expr.data == 'prod_num_target_mul':
                current_op = 'mul'
            elif threshold_side_expr.data == 'prod_num_target_div':
                current_op = 'div'
            else:
                # Leaf node, cannot separate further
                return threshold_side_expr, field_side_expr
            
            # Get left and right sub-expressions
            left_expr = threshold_side_expr.children[0]
            right_expr = threshold_side_expr.children[1]
            
            # Check if left and right contain numeric symbols
            left_has_symbols = _contains_num_thresholds(left_expr)
            right_has_symbols = _contains_num_thresholds(right_expr)
            
            if left_has_symbols and not right_has_symbols:
                # Case 1: left contains, right doesn't → move right side
                if current_op == 'add':
                    # a + b → a, field - b
                    new_field = Tree('prod_num_sub', [field_side_expr, right_expr])
                elif current_op == 'sub':
                    # a - b → a, field + b
                    new_field = Tree('prod_num_add', [field_side_expr, right_expr])
                elif current_op == 'mul':
                    # a * b → a, field / b
                    new_field = Tree('prod_num_div', [field_side_expr, right_expr])
                elif current_op == 'div':
                    # a / b → a, field * b
                    new_field = Tree('prod_num_mul', [field_side_expr, right_expr])
                
                # Recursively process left expression
                return _separate_expressions(left_expr, new_field)
            
            elif not left_has_symbols and right_has_symbols:
                # Case 2: left doesn't contain, right contains → move left side
                if current_op == 'add':
                    # a + b → b, field - a
                    new_field = Tree('prod_num_sub', [field_side_expr, left_expr])
                    return _separate_expressions(right_expr, new_field)
                elif current_op == 'sub':
                    # a - b → b, -(field - a)
                    new_field = Tree('prod_num_sub', [field_side_expr, left_expr])
                    neg_new_field = Tree('prod_num_factor_neg', [new_field])
                    return _separate_expressions(right_expr, neg_new_field)
                elif current_op == 'mul':
                    # a * b → b, field / a
                    new_field = Tree('prod_num_div', [field_side_expr, left_expr])
                    return _separate_expressions(right_expr, new_field)
                elif current_op == 'div':
                    # a / b → b, a / field
                    new_field = Tree('prod_num_div', [left_expr, field_side_expr])
                    return _separate_expressions(right_expr, new_field)
            
            else:
                # Both sides don't contain symbols, or both contain symbols (latter shouldn't happen in single symbol case)
                # Cannot move, keep original
                return threshold_side_expr, field_side_expr
        
        # Main logic: handle comparison expressions
        if comparison_node.data == 'prod_num_cmp_expr_1':
            # num_target_expr NUM_CMP_OP num_expr
            left_expr = comparison_node.children[0]  # num_target_expr
            comparison_op = comparison_node.children[1].value
            right_expr = comparison_node.children[2]  # num_expr
            
            threshold_expr, field_expr = _separate_expressions(left_expr, right_expr)
            return threshold_expr, field_expr, comparison_op
                
        elif comparison_node.data == 'prod_num_cmp_expr_2':
            # num_expr NUM_CMP_OP num_target_expr  
            left_expr = comparison_node.children[0]  # num_expr
            comparison_op = comparison_node.children[1].value
            right_expr = comparison_node.children[2]  # num_target_expr
            
            threshold_expr, field_expr = _separate_expressions(right_expr, left_expr)                
            return threshold_expr, field_expr, comparison_op
        
        assert False, f"Unknown comparison node: {comparison_node.data}"

    def _convert_ast_to_sympy(ast_node: Tree) -> sp.Expr:
        """Convert AST node to SymPy expression"""
        try:
            # ===== num_expr series =====
            # num_expr: num_term "+" num_expr -> prod_num_add
            if ast_node.data == 'prod_num_add':
                left = _convert_ast_to_sympy(ast_node.children[0])
                right = _convert_ast_to_sympy(ast_node.children[1])
                return left + right
            
            # num_expr: num_term "-" num_expr -> prod_num_sub
            elif ast_node.data == 'prod_num_sub':
                left = _convert_ast_to_sympy(ast_node.children[0])
                right = _convert_ast_to_sympy(ast_node.children[1])
                return left - right
            
            # num_expr: num_term -> prod_num_term_single
            elif ast_node.data == 'prod_num_term_single':
                return _convert_ast_to_sympy(ast_node.children[0])
            
            # ===== num_term series =====
            # num_term: num_factor "×" num_term -> prod_num_mul
            elif ast_node.data == 'prod_num_mul':
                left = _convert_ast_to_sympy(ast_node.children[0])
                right = _convert_ast_to_sympy(ast_node.children[1])
                return left * right
            
            # num_term: num_factor "÷" num_term -> prod_num_div
            elif ast_node.data == 'prod_num_div':
                left = _convert_ast_to_sympy(ast_node.children[0])
                right = _convert_ast_to_sympy(ast_node.children[1])
                return left / right
            
            # num_term: num_factor "%" num_term -> prod_num_mod
            elif ast_node.data == 'prod_num_mod':
                left = _convert_ast_to_sympy(ast_node.children[0])
                right = _convert_ast_to_sympy(ast_node.children[1])
                return sp.Mod(left, right)
            
            # num_term: num_factor -> prod_num_factor_single
            elif ast_node.data == 'prod_num_factor_single':
                return _convert_ast_to_sympy(ast_node.children[0])
            
            # ===== num_factor series =====
            # num_factor: "-" num_expr -> prod_num_factor_neg
            elif ast_node.data == 'prod_num_factor_neg':
                inner = _convert_ast_to_sympy(ast_node.children[0])
                return -inner
            
            # num_factor: "(" num_expr ")" -> prod_num_factor_paren
            elif ast_node.data == 'prod_num_factor_paren':
                return _convert_ast_to_sympy(ast_node.children[0])
            
            # num_factor: math_func_expr -> prod_num_factor_math_func
            elif ast_node.data == 'prod_num_factor_math_func':
                return _convert_ast_to_sympy(ast_node.children[0])
            
            # num_factor: num_field -> prod_num_factor_field
            elif ast_node.data == 'prod_num_factor_field':
                return _convert_ast_to_sympy(ast_node.children[0])
            
            # num_factor: SIGNED_NUMBER -> prod_num_factor_literal
            elif ast_node.data == 'prod_num_factor_literal':
                return float(ast_node.children[0].value)
            
            # ===== math_func_expr series (in grammar file order) =====
            # "abs" "(" num_expr ")" -> prod_math_func_abs
            elif ast_node.data == 'prod_math_func_abs':
                arg = _convert_ast_to_sympy(ast_node.children[0])
                return sp.Abs(arg)
            
            # "sin" "(" num_expr ")" -> prod_math_func_sin
            elif ast_node.data == 'prod_math_func_sin':
                arg = _convert_ast_to_sympy(ast_node.children[0])
                return sp.sin(arg)
            
            # "asin" "(" num_expr ")" -> prod_math_func_asin
            elif ast_node.data == 'prod_math_func_asin':
                arg = _convert_ast_to_sympy(ast_node.children[0])
                return sp.asin(arg)
            
            # "cos" "(" num_expr ")" -> prod_math_func_cos
            elif ast_node.data == 'prod_math_func_cos':
                arg = _convert_ast_to_sympy(ast_node.children[0])
                return sp.cos(arg)
            
            # "acos" "(" num_expr ")" -> prod_math_func_acos
            elif ast_node.data == 'prod_math_func_acos':
                arg = _convert_ast_to_sympy(ast_node.children[0])
                return sp.acos(arg)
            
            # "tan" "(" num_expr ")" -> prod_math_func_tan
            elif ast_node.data == 'prod_math_func_tan':
                arg = _convert_ast_to_sympy(ast_node.children[0])
                return sp.tan(arg)
            
            # "atan" "(" num_expr ")" -> prod_math_func_atan
            elif ast_node.data == 'prod_math_func_atan':
                arg = _convert_ast_to_sympy(ast_node.children[0])
                return sp.atan(arg)
            
            # "atan2" "(" num_expr "," num_expr ")" -> prod_math_func_atan2
            elif ast_node.data == 'prod_math_func_atan2':
                arg1 = _convert_ast_to_sympy(ast_node.children[0])
                arg2 = _convert_ast_to_sympy(ast_node.children[1])
                return sp.atan2(arg1, arg2)
            
            # "degrees" "(" num_expr ")" -> prod_math_func_degrees
            elif ast_node.data == 'prod_math_func_degrees':
                arg = _convert_ast_to_sympy(ast_node.children[0])
                return arg * 180 / sp.pi
            
            # "radians" "(" num_expr ")" -> prod_math_func_radians
            elif ast_node.data == 'prod_math_func_radians':
                arg = _convert_ast_to_sympy(ast_node.children[0])
                return arg * sp.pi / 180
            
            # "pow" "(" num_expr "," SIGNED_NUMBER ")" -> prod_math_func_pow
            elif ast_node.data == 'prod_math_func_pow':
                base = _convert_ast_to_sympy(ast_node.children[0])
                # The second parameter of pow function is SIGNED_NUMBER, take value directly
                exponent = float(ast_node.children[1].value)
                return sp.Pow(base, exponent)
            
            # "sqrt" "(" num_expr ")" -> prod_math_func_sqrt
            elif ast_node.data == 'prod_math_func_sqrt':
                arg = _convert_ast_to_sympy(ast_node.children[0])
                return sp.sqrt(arg)
            
            # "cbrt" "(" num_expr ")" -> prod_math_func_cbrt
            elif ast_node.data == 'prod_math_func_cbrt':
                arg = _convert_ast_to_sympy(ast_node.children[0])
                return sp.Pow(arg, sp.Rational(1, 3))
            
            # "exp" "(" num_expr ")" -> prod_math_func_exp
            elif ast_node.data == 'prod_math_func_exp':
                arg = _convert_ast_to_sympy(ast_node.children[0])
                return sp.exp(arg)
            
            # "log" "(" num_expr ")" -> prod_math_func_log
            elif ast_node.data == 'prod_math_func_log':
                arg = _convert_ast_to_sympy(ast_node.children[0])
                return sp.log(arg)
            
            # "log10" "(" num_expr ")" -> prod_math_func_log10
            elif ast_node.data == 'prod_math_func_log10':
                arg = _convert_ast_to_sympy(ast_node.children[0])
                return sp.log(arg, 10)
            
            # "log1p" "(" num_expr ")" -> prod_math_func_log1p
            elif ast_node.data == 'prod_math_func_log1p':
                arg = _convert_ast_to_sympy(ast_node.children[0])
                return sp.log(arg + 1)
            
            # "min" "(" num_expr "," num_expr ")" -> prod_math_func_min
            elif ast_node.data == 'prod_math_func_min':
                arg1 = _convert_ast_to_sympy(ast_node.children[0])
                arg2 = _convert_ast_to_sympy(ast_node.children[1])
                return sp.Min(arg1, arg2)
            
            # "max" "(" num_expr "," num_expr ")" -> prod_math_func_max
            elif ast_node.data == 'prod_math_func_max':
                arg1 = _convert_ast_to_sympy(ast_node.children[0])
                arg2 = _convert_ast_to_sympy(ast_node.children[1])
                return sp.Max(arg1, arg2)
            
            # ===== num_field series =====
            # "v" NATURAL "." CUSTOM_NUM_FIELD_NAME -> prod_num_field
            elif ast_node.data == 'prod_num_field':
                var_index = ast_node.children[0].value  # NATURAL, e.g., "1" or "2"
                field_name = ast_node.children[1].value  # CUSTOM_NUM_FIELD_NAME, e.g., "speed"
                full_symbol_name = f"v{var_index}_{field_name}"
                return sp.Symbol(full_symbol_name)
            
            # ===== num_target_expr series =====
            # num_target_term "+" num_target_expr -> prod_num_target_add
            elif ast_node.data == 'prod_num_target_add':
                left = _convert_ast_to_sympy(ast_node.children[0])
                right = _convert_ast_to_sympy(ast_node.children[1])
                return left + right
            
            # num_target_term "-" num_target_expr -> prod_num_target_sub
            elif ast_node.data == 'prod_num_target_sub':
                left = _convert_ast_to_sympy(ast_node.children[0])
                right = _convert_ast_to_sympy(ast_node.children[1])
                return left - right
            
            # num_target_term -> prod_num_target_term
            elif ast_node.data == 'prod_num_target_term':
                return _convert_ast_to_sympy(ast_node.children[0])
            
            # ===== num_target_term series =====
            # num_target_factor "×" num_target_term -> prod_num_target_mul
            elif ast_node.data == 'prod_num_target_mul':
                left = _convert_ast_to_sympy(ast_node.children[0])
                right = _convert_ast_to_sympy(ast_node.children[1])
                return left * right
            
            # num_target_factor "÷" num_target_term -> prod_num_target_div
            elif ast_node.data == 'prod_num_target_div':
                left = _convert_ast_to_sympy(ast_node.children[0])
                right = _convert_ast_to_sympy(ast_node.children[1])
                return left / right
            
            # num_target_factor "%" num_target_term -> prod_num_target_mod
            elif ast_node.data == 'prod_num_target_mod':
                left = _convert_ast_to_sympy(ast_node.children[0])
                right = _convert_ast_to_sympy(ast_node.children[1])
                return sp.Mod(left, right)
            
            # num_target_factor -> prod_num_target_factor
            elif ast_node.data == 'prod_num_target_factor':
                return _convert_ast_to_sympy(ast_node.children[0])
            
            # ===== num_target_factor series =====
            # NUM_SYMBOL_PREFIX NATURAL -> prod_num_target_threshold
            elif ast_node.data == 'prod_num_target_threshold':
                # This is a symbol, should not be converted to SymPy expression
                assert False, "prod_num_target_threshold should not be converted to SymPy expression"
            
            # num_expr -> prod_num_target_num_expr
            elif ast_node.data == 'prod_num_target_num_expr':
                return _convert_ast_to_sympy(ast_node.children[0])
            
            # "(" num_target_expr ")" -> prod_num_target_paren
            elif ast_node.data == 'prod_num_target_paren':
                return _convert_ast_to_sympy(ast_node.children[0])
            
            # "-" num_target_expr -> prod_num_target_neg
            elif ast_node.data == 'prod_num_target_neg':
                inner = _convert_ast_to_sympy(ast_node.children[0])
                return -inner
            
            assert False, f"Unknown ast node: {ast_node.data}"
            
        except Exception as e:
            assert False, f"Exception in _convert_ast_to_sympy: {e}, ast_node: {ast_node.data}"

    # ================================
    # Main execution logic
    # ================================
    
    threshold_expressions = {}
    
    # Build parser
    str_field_names, num_field_names = _get_field_names_for_parser()
    body_parser = _build_body_parser(str_field_names, num_field_names)
    
    # Parse all bfuncs
    parsed_bfuncs = {}
    for name, impl in bfunc_implementations.items():
        try:
            tree = body_parser.parse(impl)
            parsed_bfuncs[name] = tree
        except Exception as e:
            raise RuntimeError(f"Failed to parse bfunc {name}: {e}")
    
    if not parsed_bfuncs:
        return threshold_expressions
    
    threshold_constraints = {}
    for name, parsed_tree in parsed_bfuncs.items():
        try:
            comparison_nodes = _find_num_comparison_nodes(parsed_tree)
            for comp_node in comparison_nodes:
                # Filter each comparison node: only process comparison nodes that contain numeric symbols and no string symbols
                num_thresholds = _extract_num_thresholds_from_node(comp_node)
                has_str_thresholds = _contains_str_thresholds(comp_node)
                
                # Filter: only process comparison nodes that contain exactly one numeric symbol and no string symbols
                if len(num_thresholds) == 1 and not has_str_thresholds:
                    threshold_side, field_side, op = _separate_threshold_and_field_sides(comp_node)
                    
                    # Check if threshold_side is really a single threshold
                    threshold_side_symbols = _extract_num_thresholds_from_node(threshold_side)
                    if len(threshold_side_symbols) == 1:
                        threshold_symbol = list(threshold_side_symbols)[0]
                        if threshold_symbol not in threshold_constraints:
                            threshold_constraints[threshold_symbol] = []
                        threshold_constraints[threshold_symbol].append((threshold_side, field_side, op))
                        
        except Exception as e:
            raise RuntimeError(f"Failed to process bfunc {name}: {e}")
    
    # Collect field expressions corresponding to each threshold symbol
    threshold_expressions = {}
    for threshold_symbol, constraints in threshold_constraints.items():
        threshold_expr_list = []
        
        for _, field_expr, op in constraints:
            try:
                # Convert field expression to sympy expression
                sympy_expr = _convert_ast_to_sympy(field_expr)
                threshold_expr_list.append((sympy_expr, op))
                
            except Exception as e:
                log_warning(LOGGER_NAME, f"Failed to convert field expression for threshold symbol {threshold_symbol}: {e}")
                continue
        
        # Only save threshold symbols with expressions
        if threshold_expr_list:
            threshold_expressions[threshold_symbol] = threshold_expr_list
    
    return threshold_expressions


def _approximate_compute(dataset_file_path: Path, bfunc_implemetation_file_path: Path) -> dict[str, tuple[float, float]]:
    
    def _compute_range(field_ranges: dict[str, tuple[float, float, bool, bool]], field_expr: sp.Expr) -> tuple[float, float]:
        """
        Numerically compute the value range of the given field expression
        
        Args:
            field_ranges: Field range dictionary {field_name: (min_val, max_val, left_inclusive, right_inclusive)}
            field_expr: Field expression to compute range for (containing field symbols like v1_fieldname, v2_fieldname)
            
        Returns:
            (min_val, max_val): Value range of the field expression
        """
        
        def _numerical_approximation(field_expr: sp.Expr, field_symbol_domains: dict) -> set:
            """
            Level 3: Numerical approximation - global numerical optimization fallback strategy
            Use numerical optimization methods to find global optimal solutions, always executed to ensure completeness
            """
            candidate_values = set()
            
            try:
                
                # Build numerical function
                f_numeric = sp.lambdify(list(field_symbol_domains.keys()), field_expr, modules=['numpy', 'scipy'])
                    
                # Build boundary constraints
                bounds = []
                for _, domain in field_symbol_domains.items():
                    if domain.start == -sp.oo:
                        start = -1e9
                    elif domain.start == sp.oo:
                        start = 1e9
                    elif domain.left_open:
                        start = float(domain.start) + 1e-9
                    else:
                        start = float(domain.start)
                        
                    if domain.end == sp.oo:
                        end = 1e9
                    elif domain.end == -sp.oo:
                        end = -1e9
                    elif domain.right_open:
                        end = float(domain.end) - 1e-9
                    else:
                        end = float(domain.end)
                        
                    bounds.append((start, end))
                
                # Catch RuntimeWarning inside f_numeric
                def safe_evaluate(p):
                    """Catch RuntimeWarning during function evaluation, convert to np.inf"""
                    with warnings.catch_warnings(record=True) as w:
                        warnings.simplefilter("always", RuntimeWarning)
                        result = f_numeric(*p)
                        if w:  # Caught warning from f_numeric
                            return np.inf
                    if not np.isfinite(result):
                        return np.inf
                    return result
                
                # Catch RuntimeWarning inside differential_evolution
                def safe_differential_evolution(func, bounds, maxiter=200):
                    """Catch numerical computation RuntimeWarning inside scipy"""
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore", RuntimeWarning)  # Suppress scipy internal warnings
                        return scipy.optimize.differential_evolution(func, bounds, maxiter=maxiter)
                
                # Find minimum value
                res_min = safe_differential_evolution(safe_evaluate, bounds)
                if np.isfinite(res_min.fun):
                    candidate_values.add(res_min.fun)
                else:
                    candidate_values.add(-np.inf)
                
                # Find maximum value
                res_max = safe_differential_evolution(lambda p: -safe_evaluate(p), bounds)
                if np.isfinite(res_max.fun):
                    candidate_values.add(-res_max.fun)  # Take negative to get real maximum
                else:
                    candidate_values.add(np.inf)
                    
            except Exception:
                pass
            
            return candidate_values
        
        
        expr_symbols = field_expr.free_symbols
        
        # Build mapping from field symbols to intervals
        field_symbol_domains = {}
        for field_sym in expr_symbols:
            field_sym_name = str(field_sym) # Field symbol name format: v1_fieldname, v2_fieldname 
            assert '_' in field_sym_name and field_sym_name.startswith('v'), f"Unknown field symbol {field_sym_name}"     
            parts = field_sym_name.split('_', 1)
            assert len(parts) == 2, f"Unknown field symbol {field_sym_name}"
            field_name = parts[1] 
            assert field_name in field_ranges, f"No range info for field {field_name} (from field symbol {field_sym_name})"
            min_val, max_val, left_incl, right_incl = field_ranges[field_name]

            interval = sp.Interval(min_val, max_val, left_open=not left_incl, right_open=not right_incl)
            field_symbol_domains[field_sym] = interval
        
        if not field_symbol_domains:
            assert field_expr.is_number, f"field expression {field_expr} is not a number" 
            val = float(field_expr)
            return val, val
        
        try:
            
            candidate_values = _numerical_approximation(field_expr, field_symbol_domains)
            numeric_candidates = {val for val in candidate_values if isinstance(val, (int, float))}

            if numeric_candidates:
                min_val = min(numeric_candidates)
                max_val = max(numeric_candidates)
                return min_val, max_val
            else:
                return float('-inf'), float('inf')
            
        except Exception as e:
            log_warning(LOGGER_NAME, f"{' ' * (INDENT * 2)}- failed to approximate compute range for field expression {field_expr}: {e}")
            return float('-inf'), float('inf')

    log_info(LOGGER_NAME, "Approximate computing basic ranges")
    
    start_time = time.time()
    
    field_ranges = _load_field_ranges(dataset_file_path)
    log_info(LOGGER_NAME, f"{' ' * INDENT}- loaded field ranges for {len(field_ranges)} fields")

    bfunc_implementations = _load_bfunc_implementations(bfunc_implemetation_file_path)
    log_info(LOGGER_NAME, f"{' ' * INDENT}- loaded {len(bfunc_implementations)} bfunc implementations")

    threshold_expressions = _process_comparison_expressions(dataset_file_path, bfunc_implementations)
    log_info(LOGGER_NAME, f"{' ' * INDENT}- processed comparison expressions for {len(threshold_expressions)} threshold symbols")

    symbol_ranges = {}
    for threshold_symbol, expressions in threshold_expressions.items():
        log_info(LOGGER_NAME, f"{' ' * INDENT}- computing range for threshold symbol '{threshold_symbol}' with {len(expressions)} field expressions")
        
        all_ranges = []
        for field_expr, _ in expressions:
            try:
                min_val, max_val = _compute_range(field_ranges, field_expr)
                all_ranges.append((min_val, max_val))
                log_info(LOGGER_NAME, f"{' ' * (INDENT * 2)}- field expression {field_expr} → range [{min_val}, {max_val}]")
            except Exception as e:
                log_warning(LOGGER_NAME, f"{' ' * (INDENT * 2)}- failed to compute range for field expression {field_expr}: {e}")
                continue
    
        # Merge all ranges (intersection)
        if all_ranges:
            # Intersection: take the maximum of all minimum values, minimum of all maximum values
            combined_min = max(r[0] for r in all_ranges)
            combined_max = min(r[1] for r in all_ranges)
            
            # Check if meaningful
            if (combined_min == -float('inf') or combined_min == float('inf')) and (combined_max == -float('inf') or combined_max == float('inf')):
                log_warning(LOGGER_NAME, f"{' ' * (INDENT * 2)}- meaningless range for threshold symbol '{threshold_symbol}': [{combined_min}, {combined_max}]")
            else:
                # Check if intersection is empty
                if combined_min <= combined_max:
                    symbol_ranges[threshold_symbol] = (combined_min, combined_max)
                    log_info(LOGGER_NAME, f"{' ' * (INDENT * 2)}- final range for threshold symbol '{threshold_symbol}': [{combined_min}, {combined_max}]")
                else:
                    log_warning(LOGGER_NAME, f"{' ' * (INDENT * 2)}- empty intersection for threshold symbol '{threshold_symbol}': {combined_min} > {combined_max}")
        else:
            log_warning(LOGGER_NAME, f"{' ' * (INDENT * 2)}- no valid ranges computed for threshold symbol '{threshold_symbol}'")

    approximate_time = time.time() - start_time
    log_info(LOGGER_NAME, f"Approximate computed ranges for {len(symbol_ranges)} threshold symbols in {approximate_time:.2f} seconds")
    return symbol_ranges
    
@timeout_process(60, logger_name=LOGGER_NAME)
def _theoretical_compute(dataset_file_path: Path, bfunc_implemetation_file_path: Path) -> dict[str, tuple[float, float]]:
    
    def _compute_range(field_ranges: dict[str, tuple[float, float, bool, bool]], field_expr: sp.Expr) -> tuple[float, float]:
        """
        Theoretically compute the value range of the given field expression
        
        Args:
            field_ranges: Field range dictionary {field_name: (min_val, max_val, left_inclusive, right_inclusive)}
            field_expr: Field expression to compute range for (containing field symbols like v1_fieldname, v2_fieldname)
            
        Returns:
            (min_val, max_val): Value range of the field expression
        """
        
        def _check_point_in_domain(point_dict, field_symbol_domains_dict):
            """Check if point is within domain
            
            Requirement: All values in point_dict must be concrete numbers, not symbolic expressions
            """
            for var, domain in field_symbol_domains_dict.items():
                if var not in point_dict:
                    return False
                val = point_dict[var]
                # Strict requirement: must be concrete number
                assert val.is_number, f"Point value for variable {var} must be a concrete number, got {val} (type: {type(val)})"
                # Check if within interval (domain is always sp.Interval object)
                if not domain.contains(val):
                    return False
            return True

        def _level1_calculus_analysis(field_expr: sp.Expr, field_symbol_domains: dict) -> set:
            """
            Level 1: Calculus analysis - find smooth critical points
            Based on Fermat's theorem: gradient is zero at interior extrema
            """
            
            candidate_values = set()
            try:
                all_vars = list(field_symbol_domains.keys())
                
                if len(all_vars) <= 5:  # Try symbolic solving for 5 or fewer variables
                    gradient = [sp.diff(field_expr, var) for var in all_vars]
                    
                    @timeout_thread(10, suppress_exceptions=True, logger_name=LOGGER_NAME)
                    def _solve_gradient():
                        return sp.solve(gradient, all_vars, dict=True)
                    
                    try:
                        critical_points = _solve_gradient()
                        if critical_points is None:
                            return set()
                    except TimeoutException:
                        log_warning(LOGGER_NAME, f"{' ' * (INDENT * 2)}- try to use level1_calculus_analysis failed: timeout")
                        return set()
                    
                    for point in critical_points:
                        if _check_point_in_domain(point, field_symbol_domains):
                            candidate_val = field_expr.subs(point)
                            if candidate_val.is_number:
                                candidate_values.add(float(candidate_val))
            except Exception as e:
                log_warning(LOGGER_NAME, f"{' ' * (INDENT * 2)}- try to use level1_calculus_analysis failed: {e}")
                return set()
            
            return candidate_values

        def _level2a_crease_analysis(field_expr: sp.Expr, field_symbol_domains: dict) -> set:
            """
            Level 2a: Interior "crease" analysis - handle non-smooth functions
            Based on subgradient theory: extrema of non-smooth functions occur at structured "crease" points
            """
            
            def _collect_critical_expressions_for_level2a(expr):
                """Collect critical expressions from non-smooth functions (Level 2a specific)"""
                critical_exprs = set()
                
                # Collect arguments of Abs functions
                for abs_atom in expr.atoms(sp.Abs):
                    critical_exprs.add(abs_atom.args[0])
                
                # Collect arguments of sign and Heaviside functions
                for func_type in [sp.sign, sp.Heaviside]:
                    for func_atom in expr.atoms(func_type):
                        critical_exprs.add(func_atom.args[0])
                
                # Collect difference expressions of Min/Max functions
                for func_type in [sp.Min, sp.Max]:
                    for func_atom in expr.atoms(func_type):
                        for arg1, arg2 in itertools.combinations(func_atom.args, 2):
                            critical_exprs.add(arg1 - arg2)
                
                # Collect arguments of square root functions (non-smooth at argument=0)
                for func_type in [sp.sqrt]:
                    for func_atom in expr.atoms(func_type):
                        critical_exprs.add(func_atom.args[0])
                
                # Collect arguments of logarithm functions (singularity at argument=0)
                for func_atom in expr.atoms(sp.log):
                    critical_exprs.add(func_atom.args[0])
                
                # Collect boundary points of inverse trigonometric functions
                for func_atom in expr.atoms(sp.asin):
                    arg = func_atom.args[0]
                    critical_exprs.add(arg - 1)  # asin has vertical tangent at x=1
                    critical_exprs.add(arg + 1)  # asin has vertical tangent at x=-1
                    
                for func_atom in expr.atoms(sp.acos):
                    arg = func_atom.args[0]
                    critical_exprs.add(arg - 1)  # acos has vertical tangent at x=1  
                    critical_exprs.add(arg + 1)  # acos has vertical tangent at x=-1
                
                return list(critical_exprs)

            def _try_direct_solve(crit_expr, crit_vars, field_symbol_domains) -> set:
                """Try direct solving"""
                candidate_values = set()
                
                @timeout_thread(5, suppress_exceptions=True, logger_name=LOGGER_NAME)
                def _solve_critical_expr():
                    return sp.solve(crit_expr, crit_vars, dict=True)
                
                try:
                    solutions = _solve_critical_expr()
                    if solutions is None:
                        return set()
                except TimeoutException:
                    log_warning(LOGGER_NAME, f"{' ' * (INDENT * 2)}- try to use _try_direct_solve failed: timeout")
                    return set()
                
                # Process solving results
                for sol_dict in solutions:
                    if all(var in sol_dict and sol_dict[var].is_number for var in crit_vars):
                        if _check_point_in_domain(sol_dict, field_symbol_domains):
                            val = field_expr.subs(sol_dict)
                            if val.is_number:
                                candidate_values.add(float(val))
                return candidate_values

            def _dimensional_reduction_solve(crit_expr, crit_vars, field_symbol_domains) -> set:
                """Use dimensional reduction strategy for solving (when many variables or direct solving fails)"""
                candidate_values = set()
                
                for solve_var in crit_vars:
                    @timeout_thread(3, suppress_exceptions=True, logger_name=LOGGER_NAME)
                    def _solve_single_var():
                        return sp.solve(crit_expr, solve_var, dict=True)
                    
                    try:
                        solutions = _solve_single_var()
                        if solutions is None:
                            continue
                    except TimeoutException:
                        continue           

                    for sol_dict in solutions:
                        if solve_var in sol_dict:
                            # Step 1: Build substitution dictionary containing symbolic expressions
                            substitution_dict = {solve_var: sol_dict[solve_var]}
                            # Set other variables to domain midpoint
                            for var, domain in field_symbol_domains.items():
                                if var != solve_var:
                                    mid_val = (domain.start + domain.end) / 2
                                    substitution_dict[var] = mid_val
                            
                            # Step 2: Solve for concrete numerical values of all variables
                            resolved_point = {}
                            all_resolved = True
                            for var in field_symbol_domains.keys():
                                if var in substitution_dict:
                                    val = substitution_dict[var]
                                    if hasattr(val, 'subs'):  # If it's a symbolic expression
                                        resolved_val = val.subs(substitution_dict)
                                        if resolved_val.is_number:
                                            resolved_point[var] = resolved_val
                                        else:
                                            all_resolved = False
                                            break
                                    else:
                                        resolved_point[var] = val
                                else:
                                    all_resolved = False
                                    break
                            
                            # Step 3: Check if numerical point is within domain and evaluate function value
                            if all_resolved and _check_point_in_domain(resolved_point, field_symbol_domains):
                                val = field_expr.subs(resolved_point)
                                if val.is_number:
                                    candidate_values.add(float(val))
                
                return candidate_values

            # ================================
            # Level 2a main logic
            # ================================
            candidate_values = set()
            all_vars = list(field_symbol_domains.keys())
            try:
            
                critical_expressions = _collect_critical_expressions_for_level2a(field_expr)
                for crit_expr in critical_expressions:
                    crit_vars = list(crit_expr.free_symbols)
                    
                    # Only try direct solving when all variables involved and few variables
                    if len(crit_vars) == len(all_vars) and len(all_vars) <= 5:
                        direct_candidates = _try_direct_solve(crit_expr, crit_vars, field_symbol_domains)
                        candidate_values.update(direct_candidates)
                        if direct_candidates:
                            continue
                    
                    # All other cases: uniformly use dimensional reduction strategy
                    reduction_candidates = _dimensional_reduction_solve(crit_expr, crit_vars, field_symbol_domains)
                    candidate_values.update(reduction_candidates)
            
            except Exception as e:
                log_warning(LOGGER_NAME, f"{' ' * (INDENT * 2)}- try to use level2a failed: {e}")
                return set()
            
            return candidate_values

        def _level2b_boundary_analysis(field_expr: sp.Expr, field_symbol_domains: dict) -> set:
            """
            Level 2b: Boundary analysis - check extrema on domain boundaries
            Based on extrema theory: extrema may occur at domain boundaries
            """
            candidate_values = set()
            all_vars = list(field_symbol_domains.keys())
            
            boundary_values_lists = []
            for _, domain in field_symbol_domains.items():
                values = []
                if domain.start == -sp.oo:
                    values.append(-1e9)
                elif domain.start == sp.oo:
                    values.append(1e9)
                elif domain.left_open:
                    values.append(float(domain.start) + 1e-9)
                else:
                    values.append(float(domain.start))
                
                if domain.end == sp.oo:
                    values.append(1e9)
                elif domain.end == -sp.oo:
                    values.append(-1e9)
                elif domain.right_open:
                    values.append(float(domain.end) - 1e-9)
                else:
                    values.append(float(domain.end))
                                
                boundary_values_lists.append(values)
            
            try:
                
                # Generate Cartesian product of boundary points (limit combinations to avoid explosion)
                total_combinations = 1
                for values in boundary_values_lists:
                    total_combinations *= len(values)
                
                if total_combinations <= 500:  # Limit number of combinations
                    for point_values in itertools.product(*boundary_values_lists):
                        substitutions = dict(zip(all_vars, point_values))
                        val = field_expr.subs(substitutions)
                        if val.is_number and not val.has(sp.oo):
                            candidate_values.add(float(val))
                else:
                    for _ in range(500):
                        point_values = []
                        for values in boundary_values_lists:
                            point_values.append(random.choice(values))
                        substitutions = dict(zip(all_vars, point_values))
                        val = field_expr.subs(substitutions)
                        if val.is_number and not val.has(sp.oo):
                            candidate_values.add(float(val))
            
            except Exception as e:
                log_warning(LOGGER_NAME, f"{' ' * (INDENT * 2)}- try to use level2b failed: {e}")
                return set()
        
            return candidate_values

        # ================================
        # Main execution logic
        # ================================
        
        # Get all field symbols in the expression
        expr_symbols = field_expr.free_symbols
        
        # Build mapping from field symbols to intervals
        field_symbol_domains = {}
        for field_sym in expr_symbols:
            field_sym_name = str(field_sym) # Field symbol name format: v1_fieldname, v2_fieldname 
            assert '_' in field_sym_name and field_sym_name.startswith('v'), f"Unknown field symbol {field_sym_name}"     
            parts = field_sym_name.split('_', 1)
            assert len(parts) == 2, f"Unknown field symbol {field_sym_name}"
            field_name = parts[1]  # Extract fieldname
            assert field_name in field_ranges, f"No range info for field {field_name} (from field symbol {field_sym_name})"
            min_val, max_val, left_incl, right_incl = field_ranges[field_name]
            # Create SymPy interval
            interval = sp.Interval(min_val, max_val, left_open=not left_incl, right_open=not right_incl)
            field_symbol_domains[field_sym] = interval
        
        if not field_symbol_domains:
            assert field_expr.is_number, f"Field expression {field_expr} is not a number" 
            val = float(field_expr)
            return val, val
        
        try:
            # Theoretical method to compute range
            candidate_values = set()
            # === Level 1: Calculus analysis (find smooth critical points) ===
            level1_candidate_values = _level1_calculus_analysis(field_expr, field_symbol_domains)
            candidate_values.update(level1_candidate_values)
            
            # === Level 2a: Interior "crease" analysis (handle non-smooth functions) ===
            level2a_candidate_values = _level2a_crease_analysis(field_expr, field_symbol_domains)
            candidate_values.update(level2a_candidate_values)
            
            # === Level 2b: Boundary analysis (check domain boundaries) ===
            level2b_candidate_values = _level2b_boundary_analysis(field_expr, field_symbol_domains)
            candidate_values.update(level2b_candidate_values)
            
            # Finally determine range
            numeric_candidates = {val for val in candidate_values if isinstance(val, (int, float))}

            if numeric_candidates:
                min_val = min(numeric_candidates)
                max_val = max(numeric_candidates)
                return min_val, max_val
            else:
                return float('-inf'), float('inf')
                
        except Exception as e:
            log_warning(LOGGER_NAME, f"{' ' * (INDENT * 2)}- failed to theoretical compute range for field expression {field_expr}: {e}")
            return float('-inf'), float('inf')

    log_info(LOGGER_NAME, "Theoretical computing basic ranges")
    start_time = time.time()
        
    field_ranges = _load_field_ranges(dataset_file_path)
    log_info(LOGGER_NAME, f"{' ' * INDENT}- loaded field ranges for {len(field_ranges)} fields")
    
    bfunc_implementations = _load_bfunc_implementations(bfunc_implemetation_file_path)
    log_info(LOGGER_NAME, f"{' ' * INDENT}- loaded {len(bfunc_implementations)} bfunc implementations")
    
    threshold_expressions = _process_comparison_expressions(dataset_file_path, bfunc_implementations)
    log_info(LOGGER_NAME, f"{' ' * INDENT}- processed comparison expressions for {len(threshold_expressions)} threshold symbols")

    symbol_ranges = {}
    for threshold_symbol, expressions in threshold_expressions.items():
        log_info(LOGGER_NAME, f"{' ' * INDENT}- theoretical computing range for threshold symbol '{threshold_symbol}' with {len(expressions)} field expressions")
        
        all_ranges = []
        for field_expr, _ in expressions:
            try:
                min_val, max_val = _compute_range(field_ranges, field_expr)
                all_ranges.append((min_val, max_val))
                log_info(LOGGER_NAME, f"{' ' * (INDENT * 2)}- field expression {field_expr} → range [{min_val}, {max_val}]")
            except Exception as e:
                log_warning(LOGGER_NAME, f"{' ' * (INDENT * 2)}- failed to compute range for field expression {field_expr}: {e}")
                continue
    
        if all_ranges:
            combined_min = max(r[0] for r in all_ranges)
            combined_max = min(r[1] for r in all_ranges)
            
            if combined_min == -float('inf') and combined_max == float('inf'):
                log_warning(LOGGER_NAME, f"{' ' * (INDENT * 2)}- meaningless range for threshold symbol '{threshold_symbol}': [{combined_min}, {combined_max}]")
            else:
                if combined_min <= combined_max:
                    symbol_ranges[threshold_symbol] = (combined_min, combined_max)
                    log_info(LOGGER_NAME, f"{' ' * (INDENT * 2)}- final range for threshold symbol '{threshold_symbol}': [{combined_min}, {combined_max}]")
                else:
                    log_warning(LOGGER_NAME, f"{' ' * (INDENT * 2)}- empty intersection for threshold symbol '{threshold_symbol}': {combined_min} > {combined_max}")
        else:
            log_warning(LOGGER_NAME, f"{' ' * (INDENT * 2)}- no valid ranges computed for threshold symbol '{threshold_symbol}'")

    theoretical_time = time.time() - start_time
    log_info(LOGGER_NAME, f"Theoretical computed ranges for {len(symbol_ranges)} threshold symbols in {theoretical_time:.2f} seconds")
    return symbol_ranges
