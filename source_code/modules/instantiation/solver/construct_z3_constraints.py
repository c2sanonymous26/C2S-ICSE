import multiprocessing as mp
from typing import Any, Callable, Union
from z3 import z3
from pathlib import Path
from fractions import Fraction
from sympy.core.relational import Relational
from sympy.logic.boolalg import BooleanFalse, BooleanTrue
import sympy as sp
import re

from ...utils import (
    CPU_COUNT, generate_data_chunks, load_bfuncs, analyze_bfunc_symbol_counts,
    STRING_SYMBOLIC_PREFIX, CTreeNode
)
from . import EFormulaDict, SymbolInequalities, TACTICS_BATCH_SIZE
from .construct_restriction_constraints import construct_restriction_constraints_per_bfunc

# Variables
_bfuncs_file_path: Path = None
_pure_bfuncs: dict[str, Callable] = None
_n_symbolic_bfuncs: dict[str, Callable] = None
_s_symbolic_bfuncs: dict[str, Callable] = None
_bfunc_symbol_counts: dict[str, int] = None

_restrictions_file_path: Path | None = None
_restrictions_dict: dict[str, z3.BoolRef] = None

_eformulas_tuple: tuple[list[str], list[str], dict[str, tuple[str, str]]] = None
_field_type_map: dict[str, Any] = None

tactic_combination = z3.Repeat(
    z3.Then(
        z3.With(z3.Tactic('simplify'), arith_ineq_lhs=True, arith_lhs=True),
        z3.With(z3.Tactic('propagate-values'), arith_ineq_lhs=True, arith_lhs=True),
        z3.Tactic('propagate-ineqs'),
        z3.Tactic('ctx-solver-simplify')
    ),
    5
)

def construct_main_constraint(ctree_root: CTreeNode, bfuncs_file_path: Path, restrictions_file_path: Path | None, eformulas: EFormulaDict, field_type_map: dict[str, Any]) \
    -> tuple[z3.BoolRef, SymbolInequalities, list[z3.BoolRef], dict[str, list[str]]]:
    
    global _bfuncs_file_path, _pure_bfuncs, _n_symbolic_bfuncs, _s_symbolic_bfuncs, _bfunc_symbol_counts
    global _restrictions_file_path, _restrictions_dict
    global _eformulas_tuple, _field_type_map
    
    _bfuncs_file_path = bfuncs_file_path
    _pure_bfuncs, _n_symbolic_bfuncs, _s_symbolic_bfuncs = load_bfuncs(_bfuncs_file_path)
    _bfunc_symbol_counts = analyze_bfunc_symbol_counts(_bfuncs_file_path)
    
    _restrictions_file_path = restrictions_file_path
    _restrictions_dict = construct_restriction_constraints_per_bfunc(_restrictions_file_path)
    
    _field_type_map = field_type_map
    _eformulas_tuple = ([], [], {})
    for (id, _, _), (l_id, r_id) in eformulas.items():
        _eformulas_tuple[0].append(id)
        _eformulas_tuple[1].append(l_id)
        _eformulas_tuple[1].append(r_id)
        _eformulas_tuple[2][id] = (l_id, r_id)

    main_constraint, symbol_inequalities, index_constraints, cct_node_id_dict = _construct_methods[ctree_root[0]](ctree_root, {})
    
    return main_constraint, symbol_inequalities, index_constraints, cct_node_id_dict

def _construct_bfunc(node: CTreeNode, var_bindings: dict[str, Any]) -> tuple[z3.BoolRef, SymbolInequalities, list[z3.BoolRef], dict[str, list[str]]]:
    
    def _convert_sp_to_z3(expr: Relational | BooleanFalse | BooleanTrue, original_symbol_count: int) -> tuple[z3.BoolRef, tuple[str, str] | None, Fraction | None]:   
    
        def _quantize_expr_to_precision(expr_to_quantize: sp.Expr, precision: float = 1e-9) -> sp.Expr:
            """Quantize all floating-point numbers in the expression to specified precision"""
            def quantize_number(e):
                if isinstance(e, (sp.Float, sp.Number)) and not isinstance(e, sp.Integer):
                    # Convert to float, apply round precision processing, then convert back to sympy
                    float_val = float(e)
                    multiplier = round(1.0 / precision)  # Use round to avoid floating-point errors
                    rounded_val = round(float_val * multiplier) / multiplier
                    return sp.Float(rounded_val)
                elif hasattr(e, 'args') and e.args:
                    # Recursively process composite expressions
                    return e.func(*[quantize_number(arg) for arg in e.args])
                else:
                    return e
            return quantize_number(expr_to_quantize)
        
        def _convert_side(side: sp.Expr) -> Union[z3.ArithRef, Fraction]:
            if isinstance(side, sp.Symbol):
                return z3.Real(f'{side}')
            elif isinstance(side, (sp.Integer, sp.Float, sp.Number)):
                try:
                    # Apply simple round precision processing, consistent with AutoRec/Check
                    float_value = float(side)
                    precision = 1e-9
                    multiplier = round(1.0 / precision)  # Use round to avoid floating-point errors
                    rounded_value = round(float_value * multiplier) / multiplier
                    return Fraction(rounded_value)
                except (ValueError, TypeError):
                    raise ValueError(f"Unsupported expression type: {type(side)}, expression: {side}")
            elif isinstance(side, sp.Add):
                result = None
                for arg in side.args:
                    term = _convert_side(arg)
                    if result is None:
                        result = term
                    else:
                        result = result + term
                return result
            elif isinstance(side, sp.Mul):
                result = None
                for arg in side.args:
                    term = _convert_side(arg)
                    if result is None:
                        result = term
                    else:
                        result = result * term
                return result
            elif isinstance(side, sp.Pow):
                base = _convert_side(side.args[0])
                exponent = _convert_side(side.args[1])
                return base ** exponent
            elif isinstance(side, sp.Mod):
                left_result = _convert_side(side.args[0])
                right_result = _convert_side(side.args[1])
                return left_result % right_result
            else:
                raise ValueError(f"Unsupported expression type: {type(side)}, expression: {side}")

        def _handle_single_symbol(expr: Relational, symbol: sp.Symbol) -> tuple[z3.BoolRef, tuple[str, str], Fraction]:
            """
            Handle single symbol expressions, try to simplify to `symbol op value` form
            """
            left = expr.lhs
            right = expr.rhs
            
            # Fast pass (enable for meta-domain-reduction): check if it's already in `symbol op value` or `value op symbol` form
            left_is_symbol = (left == symbol)
            right_is_symbol = (right == symbol)
            left_has_no_symbols = len(left.free_symbols) == 0
            right_has_no_symbols = len(right.free_symbols) == 0
            
            # Case 1: symbol op value (left is symbol, right is constant)
            if left_is_symbol and right_has_no_symbols:
                z3_symbol = z3.Real(str(symbol))
                z3_value = _convert_side(right)

                if isinstance(expr, sp.Eq):
                    return z3_symbol == z3_value, ('==', str(symbol)), z3_value
                elif isinstance(expr, sp.Ne):
                    return z3_symbol != z3_value, ('!=', str(symbol)), z3_value
                elif isinstance(expr, sp.Lt):
                    return z3_symbol < z3_value, ('<', str(symbol)), z3_value
                elif isinstance(expr, sp.Le):
                    return z3_symbol <= z3_value, ('<=', str(symbol)), z3_value
                elif isinstance(expr, sp.Gt):
                    return z3_symbol > z3_value, ('>', str(symbol)), z3_value
                elif isinstance(expr, sp.Ge):
                    return z3_symbol >= z3_value, ('>=', str(symbol)), z3_value
            
            # Case 2: value op symbol (left is constant, right is symbol)
            elif left_has_no_symbols and right_is_symbol:
                z3_symbol = z3.Real(str(symbol))
                z3_value = _convert_side(left)
                
                if isinstance(expr, sp.Eq):
                    return z3_symbol == z3_value, ('==', str(symbol)), z3_value
                elif isinstance(expr, sp.Ne):
                    return z3_symbol != z3_value, ('!=', str(symbol)), z3_value
                elif isinstance(expr, sp.Lt):  # value < symbol => symbol > value
                    return z3_symbol > z3_value, ('>', str(symbol)), z3_value
                elif isinstance(expr, sp.Le):  # value <= symbol => symbol >= value
                    return z3_symbol >= z3_value, ('>=', str(symbol)), z3_value
                elif isinstance(expr, sp.Gt):  # value > symbol => symbol < value
                    return z3_symbol < z3_value, ('<', str(symbol)), z3_value
                elif isinstance(expr, sp.Ge):  # value >= symbol => symbol <= value
                    return z3_symbol <= z3_value, ('<=', str(symbol)), z3_value
            
            # If not in simple `symbol op value` form, use solve for complex processing
            try:
                # Handle equations
                if isinstance(expr, sp.Eq):
                    # Quantize expression before solving to ensure consistent precision-based solving
                    quantized_expr = _quantize_expr_to_precision(expr)
                    solution = sp.solve(quantized_expr, symbol)
                    if solution:
                        # Directly construct new Z3 expression
                        z3_symbol = z3.Real(str(symbol))
                        z3_value = _convert_side(solution[0])
                        # Keep equation operator unchanged
                        return z3_symbol == z3_value, ('==', str(symbol)), z3_value
                
                # Handle not-equal relations
                elif isinstance(expr, sp.Ne):
                    # First treat not-equal as equal for solving, and quantize expression
                    eq_expr = sp.Eq(expr.lhs, expr.rhs)
                    quantized_eq_expr = _quantize_expr_to_precision(eq_expr)
                    solution = sp.solve(quantized_eq_expr, symbol)
                    if solution:
                        # Directly construct new Z3 expression, but use not-equal operator
                        z3_symbol = z3.Real(str(symbol))
                        z3_value = _convert_side(solution[0])
                        # Convert back to not-equal operator
                        return z3_symbol != z3_value, ('!=', str(symbol)), z3_value
                
                # Handle inequalities
                elif isinstance(expr, (sp.Lt, sp.Le, sp.Gt, sp.Ge)):
                    # Rearrange, put all content on left side, 0 on right side
                    rearranged = expr.lhs - expr.rhs
                    # Quantize rearranged expression
                    quantized_rearranged = _quantize_expr_to_precision(rearranged)
                    # Calculate coefficient of symbol
                    coeff = sp.diff(quantized_rearranged, symbol)
                    
                    # Solve quantized_rearranged = 0
                    solution = sp.solve(quantized_rearranged, symbol)
                    if solution:
                        value = solution[0]
                        z3_symbol = z3.Real(str(symbol))
                        z3_value = _convert_side(value)
                        
                        # Determine new operator based on coefficient sign and original operator
                        if coeff > 0:  # Positive coefficient maintains inequality direction
                            if isinstance(expr, sp.Lt):
                                return z3_symbol < z3_value, ('<', str(symbol)), z3_value
                            elif isinstance(expr, sp.Le):
                                return z3_symbol <= z3_value, ('<=', str(symbol)), z3_value
                            elif isinstance(expr, sp.Gt):
                                return z3_symbol > z3_value, ('>', str(symbol)), z3_value
                            elif isinstance(expr, sp.Ge):
                                return z3_symbol >= z3_value, ('>=', str(symbol)), z3_value
                        else:  # Negative coefficient flips inequality direction
                            if isinstance(expr, sp.Lt):
                                return z3_symbol > z3_value, ('>', str(symbol)), z3_value
                            elif isinstance(expr, sp.Le):
                                return z3_symbol >= z3_value, ('>=', str(symbol)), z3_value
                            elif isinstance(expr, sp.Gt):
                                return z3_symbol < z3_value, ('<', str(symbol)), z3_value
                            elif isinstance(expr, sp.Ge):
                                return z3_symbol <= z3_value, ('<=', str(symbol)), z3_value
            except Exception:
                # Solving failed, return None to indicate need to fall back to multi-variable processing
                return None, None, None

        def _handle_multi_symbol(expr: Relational) -> tuple[z3.BoolRef, None, None]:
            """
            Handle multi-symbol expressions or cases where single symbol processing failed, directly convert left and right sides
            """
            left = expr.lhs
            right = expr.rhs
            
            # Operator mapping table
            operators = { 
                sp.Eq: '==', sp.Ne: '!=', sp.Lt: '<', 
                sp.Le: '<=', sp.Gt: '>', sp.Ge: '>='
            }
            op = operators[expr.__class__]
            
            # Directly convert left and right sides
            z3_left = _convert_side(left)
            z3_right = _convert_side(right)
        
            # Directly construct corresponding Z3 expression
            if op == '==':
                return z3_left == z3_right, None, None
            elif op == '!=':
                return z3_left != z3_right, None, None
            elif op == '<':
                return z3_left < z3_right, None, None
            elif op == '<=':
                return z3_left <= z3_right, None, None
            elif op == '>':
                return z3_left > z3_right, None, None
            elif op == '>=':
                return z3_left >= z3_right, None, None
            else:
                raise ValueError(f"Unknown operator: {op}")

        # Main function logic begins
        if isinstance(expr, BooleanTrue):
            return z3.BoolVal(True), None, None
        elif isinstance(expr, BooleanFalse):
            return z3.BoolVal(False), None, None
        else:
            assert isinstance(expr, Relational), f"Unknown expression type: {type(expr)}"
                
        left = expr.lhs
        right = expr.rhs
        
        # Calculate total number of different symbols in expression
        # Use union operation to ensure no duplicate counting
        all_symbols = left.free_symbols.union(right.free_symbols)
        total_symbols = len(all_symbols)
        
        # Case 1: only one symbol, try to simplify to `symbol cmp_op value` form
        if total_symbols == 1 and original_symbol_count == 1:
            # Get the unique symbol in the expression
            symbol = list(all_symbols)[0]
            
            # Try single symbol processing
            z3_expr, symbol_info, threshold = _handle_single_symbol(expr, symbol)
            if z3_expr is not None:
                return z3_expr, symbol_info, threshold
        
        # If not single symbol case or single symbol processing failed, use multi-symbol processing
        return _handle_multi_symbol(expr)
            
    def _convert_strsymexpr_to_z3(expr) -> tuple[z3.BoolRef, tuple[str, str] | None, str | None]:
        """
        Convert string symbolic expressions to Z3 constraints
        Parameters:
            expr: String symbolic expression object, should have `left`, `right`, and `op_type` attributes
        Returns:
            z3_expr: Z3 boolean expression
            symbol_info: Symbol information tuple in the form (operator, symbol_name), None if cannot be recognized as single symbol expression
            threshold: Threshold string, None if cannot be recognized as single symbol expression
        """
        # Extract left and right operands and operation type from expression
        left, right, op_type = expr.left, expr.right, expr.op_type
        
        # Use assertion to ensure correct input types
        assert isinstance(left, str) and isinstance(right, str), "String symbolic expression must have string operands"
        
        # Determine operator, only eq and ne cases
        op = "==" if op_type == "eq" else "!="
        
        # Try to identify if it's in `symbol cmp_op value` pattern
        symbol_pattern = re.compile(f'^{STRING_SYMBOLIC_PREFIX}\\d+$')
        
        # Case 1: symbol on left side, value on right side
        if symbol_pattern.match(left):
            # Left side is symbol, right side is value
            z3_str_left = z3.String(left)
            z3_str_right = z3.StringVal(right)
            if op == "==":
                return z3_str_left == z3_str_right, ("==", left), right
            else:  # op == "!="
                return z3_str_left != z3_str_right, ("!=", left), right
        
        # Case 2: value on left side, symbol on right side
        elif symbol_pattern.match(right):
            # Right side is symbol, left side is value
            z3_str_left = z3.StringVal(left)
            z3_str_right = z3.String(right)
            if op == "==":
                return z3_str_right == z3_str_left, ("==", right), left
            else:  # op == "!="
                return z3_str_right != z3_str_left, ("!=", right), left
        
        # Other cases (such as comparison between two string constants or two fields)
        else:
            raise ValueError(f"Unknown expression type: {type(expr)}")
            
    def _valid_threshold(raw_id, symbol_info, threshold) -> bool:        
        if raw_id not in _restrictions_dict:
            return True
        if symbol_info is None:
            return True
        
        restriction = _restrictions_dict[raw_id]
        symbol = symbol_info[1]
        if symbol.startswith('_N_THRESHOLD_'):
            domain_constrant = z3.Real(symbol) == threshold
        else:
            domain_constrant = z3.String(symbol) == threshold
        
        solver = z3.Solver()
        solver.add(restriction)
        solver.add(domain_constrant)
        return solver.check() == z3.sat
    
    assert node[0] == "bfunc", f"Expected bfunc node, but got {node[0]}"

    bfunc_name = f'bfunc_{node[1]}'
    original_symbol_count = _bfunc_symbol_counts.get(bfunc_name, 0)
    try:     
        if bfunc_name in _pure_bfuncs:
            main_constraint = z3.BoolVal(_pure_bfuncs[bfunc_name](var_bindings))
            symbol_inequalities = {}
        elif bfunc_name in _n_symbolic_bfuncs:
            main_constraint, symbol_info, threshold = _convert_sp_to_z3(_n_symbolic_bfuncs[bfunc_name](var_bindings), original_symbol_count)
            if symbol_info is None:
                symbol_inequalities = {}
            else:
                symbol_inequalities = {symbol_info: {threshold}}
        elif bfunc_name in _s_symbolic_bfuncs:
            main_constraint, symbol_info, threshold = _convert_strsymexpr_to_z3(_s_symbolic_bfuncs[bfunc_name](var_bindings))
            if symbol_info is None:
                symbol_inequalities = {}
            else:
                symbol_inequalities = {symbol_info: {threshold}}
        else:
            raise ValueError(f"Unknown bfunc: {bfunc_name}")
    except ZeroDivisionError:
        main_constraint = z3.BoolVal(False)
        symbol_inequalities = {}
        
    # log_debug(LOGGER_NAME, f'{bfunc_name}: {main_constraint}')
    
    # for pure bfuncs
    if z3.is_false(main_constraint) or z3.is_true(main_constraint):
        return main_constraint, {}, [], {}
    
    # for symbolic_bfuncs
    raw_id = bfunc_name.rsplit('_', 1)[0] if '_c' in bfunc_name else bfunc_name
    if raw_id in _restrictions_dict:
        main_constraint = z3.And(main_constraint, _restrictions_dict[raw_id]) # Check if it conflicts with restriction
    main_constraint = tactic_combination(main_constraint)[0].as_expr() 
    if z3.is_false(main_constraint) or z3.is_true(main_constraint):
        return main_constraint, {}, [], {}
    if not _valid_threshold(raw_id, symbol_info, threshold): # Check if this threshold can be taken without conflicting with restriction
        symbol_inequalities = {}
    
    return main_constraint, symbol_inequalities, [], {}

'''
Conditions for adding `index_constraints` and `cct_node_id_dict`:
1. Current node is an element in `eformulas_tuple[0]` (i.e., `e_root_formulas`)
2. The truth values of the left and right child nodes of the current node are not simple boolean values
3. The truth value of the current node is not a simple boolean value
'''

def _construct_and(node: CTreeNode, var_bindings: dict[str, Any]) -> tuple[z3.BoolRef, SymbolInequalities, list[z3.BoolRef], dict[str, list[str]]]:
    assert node[0] == "and", f"Expected and node, but got {node[0]}"
    
    binding_suffix = "_".join(f"{k}-{v['id']}" for k, v in sorted(var_bindings.items()))
    and_id = f'and_{node[1]}'
    
    left_sub_node, right_sub_node = node[3][0], node[3][1]
    sub_is_trival = False
    
    left_main_constraint, left_symbol_inequalities, \
        left_index_constraints, left_cct_node_id_dict = _construct_methods[left_sub_node[0]](left_sub_node, var_bindings)
    if z3.is_false(left_main_constraint): # Short circuit, current node is simple boolean value
        main_constraint = z3.BoolVal(False)
        return main_constraint, {}, [], {}
    elif z3.is_true(left_main_constraint):
        sub_is_trival = True    
        
    right_main_constraint, right_symbol_inequalities, \
        right_index_constraints, right_cct_node_id_dict = _construct_methods[right_sub_node[0]](right_sub_node, var_bindings)
    if z3.is_false(right_main_constraint): # Short circuit, current node is simple boolean value
        main_constraint = z3.BoolVal(False)
        return main_constraint, {}, [], {}
    elif z3.is_true(right_main_constraint):
        sub_is_trival = True
    
    main_constraint = z3.And(left_main_constraint, right_main_constraint)
    main_constraint = tactic_combination(main_constraint)[0].as_expr()
    if z3.is_false(main_constraint) or z3.is_true(main_constraint): # Current node is simple boolean value
        return main_constraint, {}, [], {}
    
    symbol_inequalities = left_symbol_inequalities.copy()
    for symbol_info, domains in right_symbol_inequalities.items():
        symbol_inequalities.setdefault(symbol_info, set()).update(domains)
    
    index_constraints = left_index_constraints + right_index_constraints
    cct_node_id_dict = left_cct_node_id_dict.copy()
    for node_id, cct_node_id_list in right_cct_node_id_dict.items():
        cct_node_id_dict.setdefault(node_id, []).extend(cct_node_id_list)
    
    if sub_is_trival: # Child nodes have simple boolean values
        return main_constraint, symbol_inequalities, index_constraints, cct_node_id_dict
    else:
        if and_id in _eformulas_tuple[0]: # Current node is e_root_formulas
            left_node_id, right_node_id = _eformulas_tuple[2][and_id]
            left_cct_node_id = f'{left_node_id}_({binding_suffix})'
            right_cct_node_id = f'{right_node_id}_({binding_suffix})'
            
            cct_node_id_dict.setdefault(left_node_id, []).append(left_cct_node_id)
            left_index_ref = z3.Bool(left_cct_node_id)
            index_constraints.append(left_index_ref == left_main_constraint)
            
            cct_node_id_dict.setdefault(right_node_id, []).append(right_cct_node_id)
            right_index_ref = z3.Bool(right_cct_node_id)
            index_constraints.append(right_index_ref == right_main_constraint)
    
        return main_constraint, symbol_inequalities, index_constraints, cct_node_id_dict

def _construct_or(node: CTreeNode, var_bindings: dict[str, Any]) -> tuple[z3.BoolRef, SymbolInequalities, list[z3.BoolRef], dict[str, list[str]]]:
    assert node[0] == "or", f"Expected or node, but got {node[0]}"

    binding_suffix = "_".join(f"{k}-{v['id']}" for k, v in sorted(var_bindings.items()))
    or_id = f'or_{node[1]}'

    left_sub_node, right_sub_node = node[3][0], node[3][1]
    sub_is_trival = False
    
    left_main_constraint, left_symbol_inequalities, \
        left_index_constraints, left_cct_node_id_dict = _construct_methods[left_sub_node[0]](left_sub_node, var_bindings)
    if z3.is_true(left_main_constraint): # Short circuit, current node is simple boolean value
        main_constraint = z3.BoolVal(True)
        return main_constraint, {}, [], {}
    elif z3.is_false(left_main_constraint):
        sub_is_trival = True
    
    right_main_constraint, right_symbol_inequalities, \
        right_index_constraints, right_cct_node_id_dict = _construct_methods[right_sub_node[0]](right_sub_node, var_bindings)
    if z3.is_true(right_main_constraint): # Short circuit, current node is simple boolean value
        main_constraint = z3.BoolVal(True)
        return main_constraint, {}, [], {}
    elif z3.is_false(right_main_constraint):
        sub_is_trival = True
    
    main_constraint = z3.Or(left_main_constraint, right_main_constraint)
    main_constraint = tactic_combination(main_constraint)[0].as_expr()
    if z3.is_false(main_constraint) or z3.is_true(main_constraint): # Current node is simple boolean value
        return main_constraint, {}, [], {}

    symbol_inequalities = left_symbol_inequalities.copy()
    for symbol_info, domains in right_symbol_inequalities.items():
        symbol_inequalities.setdefault(symbol_info, set()).update(domains)
        
    index_constraints = left_index_constraints + right_index_constraints
    cct_node_id_dict = left_cct_node_id_dict.copy()
    for node_id, cct_node_id_list in right_cct_node_id_dict.items():
        cct_node_id_dict.setdefault(node_id, []).extend(cct_node_id_list)
    
    if sub_is_trival: # Child nodes have simple boolean values
        return main_constraint, symbol_inequalities, index_constraints, cct_node_id_dict
    else:
        if or_id in _eformulas_tuple[0]: # Current node is e_root_formulas
            left_node_id, right_node_id = _eformulas_tuple[2][or_id]
            left_cct_node_id = f'{left_node_id}_({binding_suffix})'
            right_cct_node_id = f'{right_node_id}_({binding_suffix})'
            
            cct_node_id_dict.setdefault(left_node_id, []).append(left_cct_node_id)
            left_index_ref = z3.Bool(left_cct_node_id)
            index_constraints.append(left_index_ref == left_main_constraint)
            
            cct_node_id_dict.setdefault(right_node_id, []).append(right_cct_node_id)
            right_index_ref = z3.Bool(right_cct_node_id)
            index_constraints.append(right_index_ref == right_main_constraint)
    
    return main_constraint, symbol_inequalities, index_constraints, cct_node_id_dict

def _construct_implies(node: CTreeNode, var_bindings: dict[str, Any]) -> tuple[z3.BoolRef, SymbolInequalities, list[z3.BoolRef], dict[str, list[str]]]:
    assert node[0] == "implies", f"Expected implies node, but got {node[0]}"
    
    binding_suffix = "_".join(f"{k}-{v['id']}" for k, v in sorted(var_bindings.items()))
    implies_id = f'implies_{node[1]}'

    left_sub_node, right_sub_node = node[3][0], node[3][1]
    sub_is_trival = False
    
    left_main_constraint, left_symbol_inequalities, \
        left_index_constraints, left_cct_node_id_dict = _construct_methods[left_sub_node[0]](left_sub_node, var_bindings)
    if z3.is_false(left_main_constraint): # Short circuit, current node is simple boolean value
        main_constraint = z3.BoolVal(True)
        return main_constraint, {}, [], {}
    elif z3.is_true(left_main_constraint):
        sub_is_trival = True
            
    right_main_constraint, right_symbol_inequalities, \
        right_index_constraints, right_cct_node_id_dict = _construct_methods[right_sub_node[0]](right_sub_node, var_bindings)
    if z3.is_true(right_main_constraint): # Short circuit, current node is simple boolean value
        main_constraint = z3.BoolVal(True)
        return main_constraint, {}, [], {}
    elif z3.is_false(right_main_constraint):
        sub_is_trival = True
    
    main_constraint = z3.Implies(left_main_constraint, right_main_constraint)   
    main_constraint = tactic_combination(main_constraint)[0].as_expr()           
    if z3.is_false(main_constraint) or z3.is_true(main_constraint): # Current node is simple boolean value
        return main_constraint, {}, [], {}
    
    symbol_inequalities = left_symbol_inequalities.copy()
    for symbol_info, domains in right_symbol_inequalities.items():
        symbol_inequalities.setdefault(symbol_info, set()).update(domains)
        
    index_constraints = left_index_constraints + right_index_constraints    
    cct_node_id_dict = left_cct_node_id_dict.copy()
    for node_id, cct_node_id_list in right_cct_node_id_dict.items():
        cct_node_id_dict.setdefault(node_id, []).extend(cct_node_id_list)
    
    if sub_is_trival: # Child nodes have simple boolean values
        return main_constraint, symbol_inequalities, index_constraints, cct_node_id_dict
    else:
        if implies_id in _eformulas_tuple[0]: # Current node is e_root_formulas
            left_node_id, right_node_id = _eformulas_tuple[2][implies_id]
            left_cct_node_id = f'{left_node_id}_({binding_suffix})'
            right_cct_node_id = f'{right_node_id}_({binding_suffix})'
            
            cct_node_id_dict.setdefault(left_node_id, []).append(left_cct_node_id)
            left_index_ref = z3.Bool(left_cct_node_id)
            index_constraints.append(left_index_ref == left_main_constraint)
            
            cct_node_id_dict.setdefault(right_node_id, []).append(right_cct_node_id)
            right_index_ref = z3.Bool(right_cct_node_id)
            index_constraints.append(right_index_ref == right_main_constraint)
    
    return main_constraint, symbol_inequalities, index_constraints, cct_node_id_dict

def _construct_not(node: CTreeNode, var_bindings: dict[str, Any]) -> tuple[z3.BoolRef, SymbolInequalities, list[z3.BoolRef], dict[str, list[str]]]:
    assert node[0] == "not", f"Expected not node, but got {node[0]}"
        
    sub_node = node[3][0]
    sub_main_constraint, sub_symbol_inequalities, \
        sub_index_constraints, sub_cct_node_id_dict = _construct_methods[sub_node[0]](sub_node, var_bindings)
    
    if z3.is_false(sub_main_constraint): # Current node is simple boolean value
        main_constraint = z3.BoolVal(True)
        return main_constraint, {}, [], {}
    elif z3.is_true(sub_main_constraint): # Current node is simple boolean value
        main_constraint = z3.BoolVal(False)
        return main_constraint, {}, [], {}
    else:
        main_constraint = z3.Not(sub_main_constraint)
        main_constraint = tactic_combination(main_constraint)[0].as_expr()
        symbol_inequalities = sub_symbol_inequalities.copy()
        index_constraints = sub_index_constraints
        cct_node_id_dict = sub_cct_node_id_dict.copy()
        return main_constraint, symbol_inequalities, index_constraints, cct_node_id_dict

def _construct_forall(node: CTreeNode, var_bindings: dict[str, Any]) -> tuple[z3.BoolRef, SymbolInequalities, list[z3.BoolRef], dict[str, list[str]]]:
    assert node[0] == "forall", f"Expected forall node, but got {node[0]}"
    
    var = node[2]['var']
    solve_data_file_path, solve_data_size = node[2]['solve_data_info']
    concurrent = node[2]['concurrent']
    sub_node = node[3][0]
    
    main_constraint = z3.BoolVal(True)
    symbol_inequalities = {}
    index_constraints = []
    cct_node_id_dict = {}
    
    count = 0
    if concurrent:
        
        chunk_size = solve_data_size // CPU_COUNT
        chunk_args = (
            (chunk, var, sub_node, var_bindings.copy(), _bfuncs_file_path, _restrictions_file_path, _eformulas_tuple, _field_type_map)
            for chunk in generate_data_chunks(solve_data_file_path, chunk_size, _field_type_map)
        )
        
        with mp.Pool(processes=CPU_COUNT - 1) as pool:
            try:  
                for sub_main_constraint_str, sub_symbol_inequalities, \
                    sub_index_constraints_str, sub_cct_node_id_dict in pool.imap_unordered(_process_forall_chunk, chunk_args):
                    
                    parsed_mc_smt = z3.parse_smt2_string(sub_main_constraint_str)
                    assert len(parsed_mc_smt) == 1 or len(parsed_mc_smt) == 0, \
                        f"Expected one or zero expression, but got {len(parsed_mc_smt)}"
                    if len(parsed_mc_smt) == 0: # True
                        pass
                    else:
                        sub_main_constraint = parsed_mc_smt[0]
                        if z3.is_false(sub_main_constraint):
                            main_constraint = z3.BoolVal(False)
                            break
                        else:
                            count += 1
                            main_constraint = z3.And(main_constraint, sub_main_constraint)
                            if count % (TACTICS_BATCH_SIZE // 2) == 0:
                                main_constraint = tactic_combination(main_constraint)[0].as_expr()
                            if z3.is_false(main_constraint):
                                break
                            
                            for symbol_info, domains in sub_symbol_inequalities.items():
                                symbol_inequalities.setdefault(symbol_info, set()).update(domains)
                            
                            parsed_ics_smt = z3.parse_smt2_string(sub_index_constraints_str)
                            index_constraints.extend(parsed_ics_smt)
                            for node_id, cct_node_id_list in sub_cct_node_id_dict.items():
                                cct_node_id_dict.setdefault(node_id, []).extend(cct_node_id_list)
            except Exception as e:
                raise e
    else:
        
        for data in generate_data_chunks(solve_data_file_path, 1, _field_type_map):
            var_bindings[var] = data[0]
            sub_main_constraint, sub_symbol_inequalities, \
                sub_index_constraints, sub_cct_node_id_dict = _construct_methods[sub_node[0]](sub_node, var_bindings)            
            if z3.is_false(sub_main_constraint):
                main_constraint = z3.BoolVal(False)
                break
            else:
                main_constraint = z3.And(main_constraint, sub_main_constraint)
                count += 1
                if count % TACTICS_BATCH_SIZE == 0:
                    main_constraint = tactic_combination(main_constraint)[0].as_expr()
                if z3.is_false(main_constraint):
                    break
                
                for symbol_info, domains in sub_symbol_inequalities.items():
                    symbol_inequalities.setdefault(symbol_info, set()).update(domains)
                
                index_constraints.extend(sub_index_constraints)
                for node_id, cct_node_id_list in sub_cct_node_id_dict.items():
                    cct_node_id_dict.setdefault(node_id, []).extend(cct_node_id_list)
                    
            var_bindings.pop(var)

    if count % TACTICS_BATCH_SIZE != 0:
        main_constraint = tactic_combination(main_constraint)[0].as_expr()
    
    if z3.is_true(main_constraint) or z3.is_false(main_constraint):
        return main_constraint, {}, [], {}
    else:
        return main_constraint, symbol_inequalities, index_constraints, cct_node_id_dict

def _construct_exists(node: CTreeNode, var_bindings: dict[str, Any]) -> tuple[z3.BoolRef, SymbolInequalities, list[z3.BoolRef], dict[str, list[str]]]:
    assert node[0] == "exists", f"Expected exists node, but got {node[0]}"
    
    var = node[2]['var']
    solve_data_file_path, solve_data_size = node[2]['solve_data_info']
    concurrent = node[2]['concurrent']
    sub_node = node[3][0]
    
    main_constraint = z3.BoolVal(False)
    symbol_inequalities = {}
    index_constraints = []
    cct_node_id_dict = {}
    
    count = 0
    if concurrent:
        chunk_size = solve_data_size // CPU_COUNT
        chunk_args = (
            (chunk, var, sub_node, var_bindings.copy(), _bfuncs_file_path, _restrictions_file_path, _eformulas_tuple, _field_type_map)
            for chunk in generate_data_chunks(solve_data_file_path, chunk_size, _field_type_map)
        )
        
        with mp.Pool(processes=CPU_COUNT - 1) as pool:
            try:
                for sub_main_constraint_str, sub_symbol_inequalities, \
                    sub_index_constraints_str, sub_cct_node_id_dict in pool.imap_unordered(_process_exists_chunk, chunk_args):
                    
                    parsed_mc_smt = z3.parse_smt2_string(sub_main_constraint_str)
                    assert len(parsed_mc_smt) == 1 or len(parsed_mc_smt) == 0, \
                        f"Expected one or zero expression, but got {len(parsed_mc_smt)}"
                    if len(parsed_mc_smt) == 0:
                        main_constraint = z3.BoolVal(True)
                        break
                    else:
                        sub_main_constraint = parsed_mc_smt[0]
                        if z3.is_false(sub_main_constraint):
                            pass
                        else:
                            count += 1
                            main_constraint = z3.Or(main_constraint, sub_main_constraint)
                            if count % (TACTICS_BATCH_SIZE // 2) == 0:
                                main_constraint = tactic_combination(main_constraint)[0].as_expr()
                            if z3.is_true(main_constraint):
                                break
                    
                            for symbol_info, domains in sub_symbol_inequalities.items():
                                symbol_inequalities.setdefault(symbol_info, set()).update(domains)
                            
                            parsed_ics_smt = z3.parse_smt2_string(sub_index_constraints_str)
                            index_constraints.extend(parsed_ics_smt)
                            for node_id, cct_node_id_list in sub_cct_node_id_dict.items():
                                cct_node_id_dict.setdefault(node_id, []).extend(cct_node_id_list)

            except Exception as e:
                raise e        
    else:
        
        for data in generate_data_chunks(solve_data_file_path, 1, _field_type_map):
            var_bindings[var] = data[0]
            sub_main_constraint, sub_symbol_inequalities, \
                sub_index_constraints, sub_cct_node_id_dict = _construct_methods[sub_node[0]](sub_node, var_bindings)
            if z3.is_true(sub_main_constraint):
                main_constraint = z3.BoolVal(True)
                break
            else:
                main_constraint = z3.Or(main_constraint, sub_main_constraint)
                count += 1
                if count % TACTICS_BATCH_SIZE == 0:
                    main_constraint = tactic_combination(main_constraint)[0].as_expr()
                if z3.is_true(main_constraint):
                    break
                
                for symbol_info, domains in sub_symbol_inequalities.items():
                    symbol_inequalities.setdefault(symbol_info, set()).update(domains)
                
                index_constraints.extend(sub_index_constraints)
                for node_id, cct_node_id_list in sub_cct_node_id_dict.items():
                    cct_node_id_dict.setdefault(node_id, []).extend(cct_node_id_list)
                    
            var_bindings.pop(var)
        
    if count % TACTICS_BATCH_SIZE != 0:
        main_constraint = tactic_combination(main_constraint)[0].as_expr()
    
    if z3.is_true(main_constraint) or z3.is_false(main_constraint):
        return main_constraint, {}, [], {}
    else:
        return main_constraint, symbol_inequalities, index_constraints, cct_node_id_dict

def _process_forall_chunk(args: tuple) -> tuple[str, SymbolInequalities, str, dict[str, list[str]]]:
    global _pure_bfuncs, _n_symbolic_bfuncs, _s_symbolic_bfuncs, _bfunc_symbol_counts
    global _restrictions_dict
    global _eformulas_tuple, _field_type_map

    chunk_data, var, sub_node, var_bindings, bfuncs_file_path, restrictions_file_path, eformulas_tuple, field_type_map = args
    
    _pure_bfuncs, _n_symbolic_bfuncs, _s_symbolic_bfuncs = load_bfuncs(bfuncs_file_path)
    _bfunc_symbol_counts = analyze_bfunc_symbol_counts(bfuncs_file_path)
    
    _restrictions_dict = construct_restriction_constraints_per_bfunc(restrictions_file_path)
    
    _eformulas_tuple = eformulas_tuple
    _field_type_map = field_type_map
    
    
    main_constraint = z3.BoolVal(True)
    symbol_inequalities = {}
    index_constraints = []
    cct_node_id_dict = {}
    
    count = 0
    for data in chunk_data:
        var_bindings[var] = data
        sub_main_constraint, sub_symbol_inequalities, \
            sub_index_constraints, sub_cct_node_id_dict = _construct_methods[sub_node[0]](sub_node, var_bindings)    
        if z3.is_false(sub_main_constraint):
            main_constraint = z3.BoolVal(False)
            break
        else:
            main_constraint = z3.And(main_constraint, sub_main_constraint)
            count += 1
            if count % TACTICS_BATCH_SIZE == 0:
                main_constraint = tactic_combination(main_constraint)[0].as_expr()
            if z3.is_false(main_constraint):
                break
            
            for symbol_info, domains in sub_symbol_inequalities.items():
                symbol_inequalities.setdefault(symbol_info, set()).update(domains)
            
            index_constraints.extend(sub_index_constraints)
            for node_id, cct_node_id_list in sub_cct_node_id_dict.items():
                cct_node_id_dict.setdefault(node_id, []).extend(cct_node_id_list)
                
        var_bindings.pop(var)
    
    if count % TACTICS_BATCH_SIZE != 0:  # Final processing of incomplete batch    
        main_constraint = tactic_combination(main_constraint)[0].as_expr()
        
    main_constraint_solver = z3.Solver()
    main_constraint_solver.add(main_constraint)
    if z3.is_true(main_constraint) or z3.is_false(main_constraint):
        main_constraint_str = main_constraint_solver.to_smt2()
        return main_constraint_str, {}, [], {}
    else: 
        index_constraints_solver = z3.Solver()
        for constraint in index_constraints:
            index_constraints_solver.add(constraint)
        main_constraint_str = main_constraint_solver.to_smt2()
        index_constraints_str = index_constraints_solver.to_smt2()    
        return main_constraint_str, symbol_inequalities, index_constraints_str, cct_node_id_dict

def _process_exists_chunk(args: tuple) -> tuple[str, SymbolInequalities, str, dict[str, list[str]]]:
    global _pure_bfuncs, _n_symbolic_bfuncs, _s_symbolic_bfuncs, _bfunc_symbol_counts
    global _restrictions_dict
    global _eformulas_tuple, _field_type_map
    
    chunk_data, var, sub_node, var_bindings, bfuncs_file_path, restrictions_file_path, eformulas_tuple, field_type_map = args
    
    _pure_bfuncs, _n_symbolic_bfuncs, _s_symbolic_bfuncs = load_bfuncs(bfuncs_file_path)
    _bfunc_symbol_counts = analyze_bfunc_symbol_counts(bfuncs_file_path) 
    
    _restrictions_dict = construct_restriction_constraints_per_bfunc(restrictions_file_path)
    
    _eformulas_tuple = eformulas_tuple
    _field_type_map = field_type_map

    main_constraint = z3.BoolVal(False)
    symbol_inequalities = {}
    index_constraints = []
    cct_node_id_dict = {}
    
    count = 0
    for data in chunk_data:
        var_bindings[var] = data
        sub_main_constraint, sub_symbol_inequalities, \
            sub_index_constraints, sub_cct_node_id_dict = _construct_methods[sub_node[0]](sub_node, var_bindings)    
        if z3.is_true(sub_main_constraint):
            main_constraint = z3.BoolVal(True)
            break
        else:
            main_constraint = z3.Or(main_constraint, sub_main_constraint)
            count += 1
            if count % TACTICS_BATCH_SIZE == 0:
                main_constraint = tactic_combination(main_constraint)[0].as_expr()
            if z3.is_true(main_constraint):
                break
            
            for symbol_info, domains in sub_symbol_inequalities.items():
                symbol_inequalities.setdefault(symbol_info, set()).update(domains)
                
            index_constraints.extend(sub_index_constraints)
            for node_id, cct_node_id_list in sub_cct_node_id_dict.items():
                cct_node_id_dict.setdefault(node_id, []).extend(cct_node_id_list)
                
        var_bindings.pop(var)

    if count % TACTICS_BATCH_SIZE != 0:  # Final processing of incomplete batch
        main_constraint = tactic_combination(main_constraint)[0].as_expr()
    
    main_constraint_solver = z3.Solver()
    main_constraint_solver.add(main_constraint)
    if z3.is_true(main_constraint) or z3.is_false(main_constraint):
        return main_constraint_solver.to_smt2(), {}, [], {}
    else:
        index_constraints_solver = z3.Solver()
        for constraint in index_constraints:
            index_constraints_solver.add(constraint)
        return main_constraint_solver.to_smt2(), symbol_inequalities, index_constraints_solver.to_smt2(), cct_node_id_dict

_construct_methods = {
    "bfunc": _construct_bfunc,
    "and": _construct_and,
    "or": _construct_or,
    "implies": _construct_implies,
    "not": _construct_not,
    "forall": _construct_forall,
    "exists": _construct_exists
}