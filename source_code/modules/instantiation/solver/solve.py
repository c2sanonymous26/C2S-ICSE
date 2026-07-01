import time
import string
import math
import random
from fractions import Fraction
from pathlib import Path
from typing import Any
from z3 import z3

from ...utils import (
    NUMERIC_SYMBOLIC_PREFIX, STRING_SYMBOLIC_PREFIX, get_data_size, CTreeNode,
    log_info, log_warning, log_debug, 
    timeout_process, parse_constraint, extract_symbols
)
from .. import INDENT, LOGGER_NAME
from . import (
    EFormulaDict, SymbolInequalities, SymbolDomains, TruthValueInfo,
    SOLVED_MODEL_NUM, CONSECUTIVE_BACKTRACKING_NUM
)
from .construct_z3_constraints import construct_main_constraint
from .enhance_validity import find_Eformulas, construct_ve_constraints, BASE_WEIGHT
from .abstract_domains import abstract_symbol_domains, get_symbol_domains_size
from .decide_solve_order import decide


SOLVE_TIMEOUT = 1.0 * 60 * 60
# SOLVE_TIMEOUT = 1.0 * 60
ADVANCED_RLAYERS = {1}

main_constraint = None

@timeout_process(SOLVE_TIMEOUT, logger_name=LOGGER_NAME)
def solve(
    constraint_path: Path,
    bfuncs_path: Path,
    restrictions_path: Path | None,
    solve_ctx2data: dict[str, Path],
    data_field_types: dict[str, str | int | float],
    concurrent: bool,
    parameter_domain_discretization: bool,
    predicate_sensitivity_promotion: bool,
    symbol_basic_ranges: dict[str, tuple[float, float]]
) -> list[dict[str, Fraction|str]] | None:
    
    # parse template
    start_time = time.time()
    ctree_root = parse_constraint(constraint_path, bfuncs_path, concurrent)
    log_info(LOGGER_NAME, f"Parsed template in {time.time() - start_time} seconds")
            
    # set solve data
    start_time = time.time()
    slv_data_num_dict = _set_solve_data(ctree_root, solve_ctx2data)
    log_info(LOGGER_NAME, f"Set solve data in {time.time() - start_time} seconds")
    log_info(LOGGER_NAME, f"{' ' * INDENT}- solve data num info: {slv_data_num_dict}")
    
    # find Eformulas
    start_time = time.time()
    if predicate_sensitivity_promotion:
        eformulas = find_Eformulas(ctree_root, ADVANCED_RLAYERS)
        log_info(LOGGER_NAME, f"{' ' * INDENT}- Eformulas:")
        for root, children in eformulas.items():
            log_info(LOGGER_NAME, f"{' ' * (INDENT * 2)}- {root}: {children}")
    else:
        eformulas = {}
        log_info(LOGGER_NAME, f"{' ' * INDENT}- Eformulas: {eformulas}")
    log_info(LOGGER_NAME, f"Found Eformulas in {time.time() - start_time} seconds")
        
    z3_solver = z3.Optimize()
    z3_solver.set("timeout", 1000 * 1000)  # in milliseconds
        
    # construct main constraint
    start_time = time.time()
    construct_results = _construct_main_constraint(
        z3_solver=z3_solver,
        ctree_root=ctree_root,
        bfuncs_path=bfuncs_path,
        restrictions_path=restrictions_path,
        eformulas=eformulas,
        data_field_types=data_field_types
    )
    if construct_results is None:
        log_warning(LOGGER_NAME, "Main Constraint is always False or True")
        log_info(LOGGER_NAME, f"Constructed main constraint in {time.time() - start_time} seconds")
        return []
    else:
        symbol_inequalities, cct_node_id_dict = construct_results
        log_info(LOGGER_NAME, f"Constructed main constraint in {time.time() - start_time} seconds")
    
    # construct ve constraints
    if predicate_sensitivity_promotion:
        start_time = time.time()
        max_possible_weight = _construct_ve_constraints(
            z3_solver=z3_solver,
            ctree_root=ctree_root,
            cct_node_id_dict=cct_node_id_dict,
            eformulas=eformulas,
            slv_data_num_dict=slv_data_num_dict,
            symbol_basic_ranges=symbol_basic_ranges
        )
        log_info(LOGGER_NAME, f"Constructed VE constraints in {time.time() - start_time} seconds")  
    else:
        max_possible_weight = 0      

    # construct domain constraints
    if parameter_domain_discretization:
        start_time = time.time()
        symbol_domains = _construct_domain_constraints(
            z3_solver=z3_solver,
            symbol_inequalities=symbol_inequalities,
            restrictions_path=restrictions_path
        )
        log_info(LOGGER_NAME, f"Constructed symbol domain constraints in {time.time() - start_time} seconds") 
        log_debug(LOGGER_NAME, f"{' ' * INDENT}- symbol inequalities:")
        for (op, symbol), inequalities in symbol_inequalities.items():
            log_debug(LOGGER_NAME, f"{' ' * (INDENT * 2)}- ({op}, {symbol}): {len(inequalities)}")
        log_debug(LOGGER_NAME, f"{' ' * INDENT}- symbol domains:")
        for symbol, domains in symbol_domains.items():
            # domains_str = ', '.join([f"({domain}, {float(domain):.6f})" if isinstance(domain, Fraction) else f"({domain})" for domain in domains])
            log_debug(LOGGER_NAME, f"{' ' * (INDENT * 2)}- {symbol}: {len(domains)}")
    else:
        symbol_domains = {}
    
    # solve iteratively
    models = _solve_iteratively(
        z3_solver=z3_solver,
        ctree_root=ctree_root,
        bfuncs_path=bfuncs_path,
        max_possible_weight=max_possible_weight,
        symbol_domains=symbol_domains,
        parameter_domain_discretization=parameter_domain_discretization,
        predicate_sensitivity_promotion=predicate_sensitivity_promotion
    )
    
    return _populate_missing_symbols(bfuncs_path=bfuncs_path, current_models=models)

def _set_solve_data(ctree_root: CTreeNode, solve_ctx2data: dict[str, Path]) -> dict[str, int]:
    slv_data_num_dict = {}
    
    queue = [ctree_root]
    while queue:
        node = queue.pop(0)
        if node[0] in ('forall', 'exists'):
            ctx = node[2]['in']
            slv_data_num = get_data_size(solve_ctx2data[ctx])
            slv_data_num_dict[ctx] = slv_data_num
            node[2]['solve_data_info'] = (
                solve_ctx2data[ctx],
                slv_data_num
            )
        if node[3] is not None:
            for child in node[3]:
                queue.append(child)
    
    return slv_data_num_dict

def _construct_main_constraint(
    z3_solver: z3.Optimize, 
    ctree_root: CTreeNode, 
    bfuncs_path: Path, 
    restrictions_path: Path | None,
    eformulas: EFormulaDict,
    data_field_types: dict[str, Any]
    ) -> tuple[SymbolInequalities, dict[str, list[str]]] | None:
    
    constraint, symbol_inequalities, \
        index_constraints, cct_node_id_dict = construct_main_constraint(ctree_root, bfuncs_path, restrictions_path, eformulas, data_field_types)
    
    global main_constraint
    main_constraint = constraint
    
    if constraint == z3.BoolVal(False) or constraint == z3.BoolVal(True):
        return None
    
    #log_debug(LOGGER_NAME, f"MAIN CONSTRAINT: {constraint.sexpr()}")
    z3_solver.add(constraint)
    for index_constraint in index_constraints:
        z3_solver.add(index_constraint)
    
    return (symbol_inequalities, cct_node_id_dict)

def _construct_ve_constraints(
    z3_solver: z3.Optimize, 
    ctree_root: CTreeNode, 
    cct_node_id_dict: dict[str, list[str]], 
    eformulas: EFormulaDict, 
    slv_data_num_dict: dict[str, int],
    symbol_basic_ranges: dict[str, tuple[float, float]]
    ) -> int:
    
    ve_constraints = construct_ve_constraints(ctree_root, cct_node_id_dict, eformulas, slv_data_num_dict)
    max_possible_weight = 0
    for ve_constraint, weight in ve_constraints:
        if ve_constraint == z3.BoolVal(True) or ve_constraint == z3.BoolVal(False):
            continue
        z3_solver.add_soft(ve_constraint, weight=weight)
        max_possible_weight += weight
    
    basic_range_weight = 4 * BASE_WEIGHT
    for symbol, (min_val, max_val) in symbol_basic_ranges.items():
        assert min_val != -float('inf') or max_val != float('inf'), f"Invalid basic range for symbol {symbol}: [{min_val}, {max_val}]"
        if min_val == -float('inf'):
            z3_solver.add_soft(z3.Real(symbol) < max_val, weight=basic_range_weight)
            max_possible_weight += basic_range_weight
        elif max_val == float('inf'):
            z3_solver.add_soft(z3.Real(symbol) > min_val, weight=basic_range_weight)
            max_possible_weight += basic_range_weight
        else:
            z3_solver.add_soft(z3.And(z3.Real(symbol) > min_val, z3.Real(symbol) < max_val), weight=basic_range_weight)
            max_possible_weight += basic_range_weight
    
    return max_possible_weight

def _construct_domain_constraints(
    z3_solver: z3.Optimize, 
    symbol_inequalities: SymbolInequalities,
    restrictions_path: Path | None,
    ) -> SymbolDomains:
    
    abstract_domains = abstract_symbol_domains(symbol_inequalities, restrictions_path)
    for symbol, domains in abstract_domains.items():
        if isinstance(domains[0], Fraction):
            var = z3.Real(symbol)
            domain_constraint = z3.Or([var == d for d in domains])
        else:
            assert isinstance(domains[0], str), f"domain value must be Fraction or str, instead of {type(domains[0])}"
            var = z3.String(symbol)
            domain_constraint = z3.Or([var == d for d in domains])
        z3_solver.add(domain_constraint)
    
    return abstract_domains

def _solve_iteratively(
    z3_solver: z3.Optimize, 
    ctree_root: CTreeNode, 
    bfuncs_path: Path,
    max_possible_weight: int,
    symbol_domains: SymbolDomains,
    parameter_domain_discretization: bool,
    predicate_sensitivity_promotion: bool,
    ) -> list[dict[str, Fraction|str]]:
        
    def _serialize_solver_results(model: dict[str, Fraction|str], objective_value: int | None, solve_time: float) -> str:
        serialized_model = f'{" " * INDENT}- solver results:\n'
        serialized_model += f'{" " * (INDENT * 2)}- model: {model}\n'
        if objective_value is not None:
            serialized_model += f'{" " * (INDENT * 2)}- objective value: {objective_value} out of {max_possible_weight}\n'
        serialized_model += f'{" " * (INDENT * 2)}- solved in {solve_time} seconds'
        return serialized_model
    
    z3_solver_stack_depth = 0
        
    def _z3_solver_safe_push(z3_solver: z3.Optimize) -> None:
        nonlocal z3_solver_stack_depth
        z3_solver_stack_depth += 1
        z3_solver.push()
        
    def _z3_solver_safe_pop(z3_solver: z3.Optimize) -> None:
        nonlocal z3_solver_stack_depth
        z3_solver_stack_depth -= 1
        if z3_solver_stack_depth < 0:
            raise ValueError("z3_solver_stack_depth is less than 0")
        z3_solver.pop()
    
    def _iteration_00() -> list[dict[str, Fraction|str]]:
        
        def _get_model(z3_solver: z3.Optimize) -> dict[str, Fraction|str]:
            z3_model = z3_solver.model()

            model = {}
            for d in z3_model.decls():
                if d.name().startswith(NUMERIC_SYMBOLIC_PREFIX):
                    assert z3_model[d].is_real(), f"Expected real number, but got {z3_model[d]}"
                    rat_ref = z3_model[d]
                    model[d.name()] = Fraction(rat_ref.numerator().as_long(), rat_ref.denominator().as_long())
                elif d.name().startswith(STRING_SYMBOLIC_PREFIX):
                    assert z3_model[d].is_string_value(), f"Expected string value, but got {z3_model[d]}"
                    model[d.name()] = str(z3_model[d])
            
            return model
        
        def _get_necessary_domain_constraint(model: dict[str, Fraction|str]) -> z3.ExprRef:
            atom_constraints = []
            for symbol, value in model.items():
                if symbol.startswith(NUMERIC_SYMBOLIC_PREFIX):
                    atom_constraints.append(z3.Real(symbol) != value)
                elif symbol.startswith(STRING_SYMBOLIC_PREFIX):
                    atom_constraints.append(z3.String(symbol) != value)
            return z3.Or(atom_constraints)
        
        models = []
        
        # Start iteration solving
        iteration = 0
        while iteration < SOLVED_MODEL_NUM:
            iteration += 1
            log_info(LOGGER_NAME, f"Solving iteration {iteration}:")

            start_time = time.time()
            if z3_solver.check() == z3.sat:
                model = _get_model(z3_solver)
                log_info(LOGGER_NAME, _serialize_solver_results(model, None, time.time() - start_time))
                models.append(model)
                
                z3_solver.add(_get_necessary_domain_constraint(model))
            elif z3_solver.check() == z3.unknown:
                log_info(LOGGER_NAME, f"{' ' * (INDENT * 2)}- timeout")
                log_info(LOGGER_NAME, f"{' ' * (INDENT * 2)}- solved in {time.time() - start_time} seconds")
                break
            else:
                log_info(LOGGER_NAME, f"{' ' * (INDENT * 2)}- unsat")
                log_info(LOGGER_NAME, f"{' ' * (INDENT * 2)}- solved in {time.time() - start_time} seconds")
                break
        
        return models
    
    def _iteration_10() -> list[dict[str, Fraction|str]]:
        
        def _get_model(z3_solver: z3.Optimize) -> dict[str, Fraction|str]:
            z3_model = z3_solver.model()

            model = {}
            for d in z3_model.decls():
                if d.name().startswith(NUMERIC_SYMBOLIC_PREFIX):
                    assert z3_model[d].is_real(), f"Expected real number, but got {z3_model[d]}"
                    rat_ref = z3_model[d]
                    model[d.name()] = Fraction(rat_ref.numerator().as_long(), rat_ref.denominator().as_long())
                elif d.name().startswith(STRING_SYMBOLIC_PREFIX):
                    assert z3_model[d].is_string_value(), f"Expected string value, but got {z3_model[d]}"
                    model[d.name()] = str(z3_model[d])
            
            return model
        
        def _get_necessary_domain_constraint(model: dict[str, Fraction|str]) -> z3.ExprRef:
            atom_constraints = []
            for symbol, value in model.items():
                if symbol.startswith(NUMERIC_SYMBOLIC_PREFIX):
                    atom_constraints.append(z3.Real(symbol) != value)
                elif symbol.startswith(STRING_SYMBOLIC_PREFIX):
                    atom_constraints.append(z3.String(symbol) != value)
            return z3.Or(atom_constraints)
        
        def _get_diverse_domain_constraint(model: dict[str, Fraction|str], symbol_domains_size: dict[str, Fraction]) -> z3.ExprRef:
            symbols = list(model.keys())
            random.shuffle(symbols)
            name = symbols[0]
            value = model[name]
            if name.startswith(STRING_SYMBOLIC_PREFIX):
                return z3.String(name) != value
            else:
                if name in symbol_domains_size:
                    return z3.Abs(z3.Real(name) - value) >= symbol_domains_size[name] / SOLVED_MODEL_NUM
                else:
                    return z3.Real(name) != value
            
        models = []
        symbol_domains_size = get_symbol_domains_size(symbol_domains)
        
        # Start iteration solving
        iteration = 0
        latest_model = None
        latest_diverse_domain_constraint = None
        consecutive_backtracking_num = 0
        while iteration < SOLVED_MODEL_NUM:
            iteration += 1
            log_info(LOGGER_NAME, f"Solving iteration {iteration}:")

            start_time = time.time()
            if z3_solver.check() == z3.sat:
                model = _get_model(z3_solver)
                log_info(LOGGER_NAME, _serialize_solver_results(model, None, time.time() - start_time))
                models.append(model)
                
                consecutive_backtracking_num = 0
                if latest_diverse_domain_constraint is not None:
                    _z3_solver_safe_pop(z3_solver)
                    z3_solver.add(latest_diverse_domain_constraint)
                    
                # Avoid model duplication and add diversity constraints
                z3_solver.add(_get_necessary_domain_constraint(model))

                _z3_solver_safe_push(z3_solver)
                latest_model = model
                latest_diverse_domain_constraint = _get_diverse_domain_constraint(model, symbol_domains_size)
                z3_solver.add(latest_diverse_domain_constraint)
            elif z3_solver.check() == z3.unknown:
                log_info(LOGGER_NAME, f"{' ' * (INDENT * 2)}- timeout")
                log_info(LOGGER_NAME, f"{' ' * (INDENT * 2)}- solved in {time.time() - start_time} seconds")
                # Backtrack to previous solution
                try:
                    _z3_solver_safe_pop(z3_solver)
                    consecutive_backtracking_num += 1
                    if consecutive_backtracking_num >= CONSECUTIVE_BACKTRACKING_NUM:
                        log_info(LOGGER_NAME, f"{' ' * (INDENT * 2)}- consecutive backtracking over limit")
                        break
                    
                    assert latest_model is not None and latest_diverse_domain_constraint is not None, "latest_model or latest_diverse_domain_constraint is None during backtracking"
                    
                    _z3_solver_safe_push(z3_solver)
                    latest_diverse_domain_constraint = _get_diverse_domain_constraint(latest_model, symbol_domains_size)
                    z3_solver.add(latest_diverse_domain_constraint)
                except ValueError:
                    log_info(LOGGER_NAME, f"{' ' * (INDENT * 2)}- no more backtracking point")
                    break    
            else:
                log_info(LOGGER_NAME, f"{' ' * (INDENT * 2)}- unsat")
                log_info(LOGGER_NAME, f"{' ' * (INDENT * 2)}- solved in {time.time() - start_time} seconds")
                # Backtrack to previous solution
                try:
                    _z3_solver_safe_pop(z3_solver)
                    consecutive_backtracking_num += 1
                    if consecutive_backtracking_num >= CONSECUTIVE_BACKTRACKING_NUM:
                        log_info(LOGGER_NAME, f"{' ' * (INDENT * 2)}- consecutive backtracking over limit")
                        break
                    
                    assert latest_model is not None and latest_diverse_domain_constraint is not None, "latest_model or latest_diverse_domain_constraint is None during backtracking"
                    
                    _z3_solver_safe_push(z3_solver)
                    latest_diverse_domain_constraint = _get_diverse_domain_constraint(latest_model, symbol_domains_size)
                    z3_solver.add(latest_diverse_domain_constraint)
                except ValueError:
                    log_info(LOGGER_NAME, f"{' ' * (INDENT * 2)}- no more backtracking point")
                    break
    
        return models
    
    def _iteration_01() -> list[dict[str, Fraction|str]]:

        def _get_model_and_objective_value_orderly(z3_solver: z3.Optimize, solve_order: dict[int, list[str]]) -> tuple[dict[str, Fraction|str], int]:
            z3_solver.push()
            partial_model = {}
            max_order = max(solve_order.keys())                
            for order in range(max_order + 1):
                if order != 0:
                    assert z3_solver.check() == z3.sat, f"Expected sat, but got {z3_solver.check()}"
                z3_model = z3_solver.model()
                atom_constraints = []        
                for d in z3_model.decls():
                    if d.name().startswith(NUMERIC_SYMBOLIC_PREFIX) and d.name() in solve_order[order]:
                        assert z3_model[d].is_real(), f"Expected real number, but got {z3_model[d]}"
                        partial_model[d.name()] = z3_model[d]
                        atom_constraints.append(z3.Real(d.name()) == z3_model[d])
                    elif d.name().startswith(STRING_SYMBOLIC_PREFIX) and d.name() in solve_order[order]:
                        assert z3_model[d].is_string_value(), f"Expected string value, but got {z3_model[d]}"
                        partial_model[d.name()] = z3_model[d]
                        atom_constraints.append(z3.String(d.name()) == z3_model[d])
                
                fixed_constraint = z3.And(atom_constraints)
                z3_solver.add(fixed_constraint)            
            
            objective_value = 0
            if z3_solver.objectives():  # check if there are soft constraints
                penalty_expr = z3_solver.objectives()[0]
                penalty_value = z3_model.evaluate(penalty_expr).as_long()
                objective_value = max_possible_weight - penalty_value
    
            model ={}
            for symbol, value in partial_model.items():
                if symbol.startswith(NUMERIC_SYMBOLIC_PREFIX):
                    model[symbol] = Fraction(value.numerator().as_long(), value.denominator().as_long())
                elif symbol.startswith(STRING_SYMBOLIC_PREFIX):
                    model[symbol] = str(value)
            
            z3_solver.pop()
            return model, objective_value
    
        def _get_necessary_domain_constraint_orderly(model: dict[str, Fraction|str], solve_order: dict[int, list[str]]) -> z3.ExprRef:
            
            max_order = max(solve_order.keys())
            neccessary_order = max_order if max_order > 0 else 1   
            
            symbols = [symbol for order in range(neccessary_order) for symbol in solve_order[order]]
            atom_constraints = []
            for symbol, value in model.items():
                if symbol not in symbols:
                    continue
                if symbol.startswith(NUMERIC_SYMBOLIC_PREFIX):
                    atom_constraints.append(z3.Real(symbol) != value)
                elif symbol.startswith(STRING_SYMBOLIC_PREFIX):
                    atom_constraints.append(z3.String(symbol) != value)
            return z3.Or(atom_constraints)
        
        model_priority_pairs = []
        
        # Get solve order
        solve_order = decide(ctree_root, bfuncs_path)
        
        # Start iteration solving
        iteration = 0
        while iteration < SOLVED_MODEL_NUM:
            iteration += 1
            log_info(LOGGER_NAME, f"Solving iteration {iteration}:")
            
            start_time = time.time()
            if z3_solver.check() == z3.sat:
                
                # Get model and objective value
                model, objective_value = _get_model_and_objective_value_orderly(z3_solver, solve_order)
                log_info(LOGGER_NAME, _serialize_solver_results(model, objective_value, time.time() - start_time))
                
                model_priority_pairs.append((objective_value, model))
                                
                # Avoid model duplication
                z3_solver.add(_get_necessary_domain_constraint_orderly(model, solve_order))
                    
            elif z3_solver.check() == z3.unknown:
                log_info(LOGGER_NAME, f"{' ' * (INDENT * 2)}- timeout")
                log_info(LOGGER_NAME, f"{' ' * (INDENT * 2)}- solved in {time.time() - start_time} seconds")
                break
            else:
                log_info(LOGGER_NAME, f"{' ' * (INDENT * 2)}- unsat")
                log_info(LOGGER_NAME, f"{' ' * (INDENT * 2)}- solved in {time.time() - start_time} seconds")
                break
        
        if len(model_priority_pairs) == 0:
            return []
        else:
            model_priority_pairs.sort(key=lambda x: x[0], reverse=True)
            return [model for _, model in model_priority_pairs]
    
    def _iteration_11() -> list[dict[str, Fraction|str]]:
        
        def _get_model_and_objective_value_orderly(z3_solver: z3.Optimize, solve_order: dict[int, list[str]]) -> tuple[dict[str, Fraction|str], int]:
            z3_solver.push()
            partial_model = {}
            max_order = max(solve_order.keys())                
            for order in range(max_order + 1):
                if order != 0:
                    assert z3_solver.check() == z3.sat, f"Expected sat, but got {z3_solver.check()}"
                z3_model = z3_solver.model()
                atom_constraints = []        
                for d in z3_model.decls():
                    if d.name().startswith(NUMERIC_SYMBOLIC_PREFIX) and d.name() in solve_order[order]:
                        assert z3_model[d].is_real(), f"Expected real number, but got {z3_model[d]}"
                        partial_model[d.name()] = z3_model[d]
                        atom_constraints.append(z3.Real(d.name()) == z3_model[d])
                    elif d.name().startswith(STRING_SYMBOLIC_PREFIX) and d.name() in solve_order[order]:
                        assert z3_model[d].is_string_value(), f"Expected string value, but got {z3_model[d]}"
                        partial_model[d.name()] = z3_model[d]
                        atom_constraints.append(z3.String(d.name()) == z3_model[d])
                
                fixed_constraint = z3.And(atom_constraints)
                z3_solver.add(fixed_constraint)            
            
            objective_value = 0
            if z3_solver.objectives():  # check if there are soft constraints
                penalty_expr = z3_solver.objectives()[0]
                penalty_value = z3_model.evaluate(penalty_expr).as_long()
                objective_value = max_possible_weight - penalty_value
    
            model ={}
            for symbol, value in partial_model.items():
                if symbol.startswith(NUMERIC_SYMBOLIC_PREFIX):
                    model[symbol] = Fraction(value.numerator().as_long(), value.denominator().as_long())
                elif symbol.startswith(STRING_SYMBOLIC_PREFIX):
                    model[symbol] = str(value)
            
            z3_solver.pop()
            return model, objective_value
    
        def _get_necessary_domain_constraint_orderly(model: dict[str, Fraction|str], solve_order: dict[int, list[str]]) -> z3.ExprRef:

            max_order = max(solve_order.keys())
            neccessary_order = max_order if max_order > 0 else 1   
            
            symbols = [symbol for order in range(neccessary_order) for symbol in solve_order[order]]
            atom_constraints = []
            for symbol, value in model.items():
                if symbol not in symbols:
                    continue
                if symbol.startswith(NUMERIC_SYMBOLIC_PREFIX):
                    atom_constraints.append(z3.Real(symbol) != value)
                elif symbol.startswith(STRING_SYMBOLIC_PREFIX):
                    atom_constraints.append(z3.String(symbol) != value)
            return z3.Or(atom_constraints)
        
        def _get_diverse_domain_constraint_orderly(model: dict[str, Fraction|str], symbol_domains_size: dict[str, Fraction], solve_order: dict[int, list[str]]) -> z3.ExprRef:
            
            max_order = max(solve_order.keys())
            diverse_order = max_order if max_order > 0 else 1
            
            symbols = [symbol for order in range(diverse_order) for symbol in solve_order[order]]
            random.shuffle(symbols)
            name = symbols[0]
            value = model[name]
            if name.startswith(STRING_SYMBOLIC_PREFIX):
                return z3.String(name) != value
            else:
                if name in symbol_domains_size:
                    return z3.Abs(z3.Real(name) - value) >= symbol_domains_size[name] / SOLVED_MODEL_NUM
                else:
                    return z3.Real(name) != value
            
        model_priority_pairs = [] 
        
        # Get solve order
        solve_order = decide(ctree_root, bfuncs_path)

        # Get symbol domain size
        symbol_domains_size = get_symbol_domains_size(symbol_domains)
        
        # Start iteration solving
        latest_model = None
        latest_diverse_domain_constraint = None
        consecutive_backtracking_num = 0
        iteration = 0
        while iteration < SOLVED_MODEL_NUM:
            iteration += 1
            log_info(LOGGER_NAME, f"Solving iteration {iteration}:")
            
            start_time = time.time()
            if z3_solver.check() == z3.sat:
                
                # Get model and objective value
                model, objective_value = _get_model_and_objective_value_orderly(z3_solver, solve_order)
                log_info(LOGGER_NAME, _serialize_solver_results(model, objective_value, time.time() - start_time))
                
                model_priority_pairs.append((objective_value, model))
                                
                consecutive_backtracking_num = 0
                if latest_diverse_domain_constraint is not None:
                    _z3_solver_safe_pop(z3_solver)
                    z3_solver.add(latest_diverse_domain_constraint)
                    
                # Avoid model duplication and add diversity constraints
                z3_solver.add(_get_necessary_domain_constraint_orderly(model, solve_order))
    
                _z3_solver_safe_push(z3_solver)
                latest_model = model
                latest_diverse_domain_constraint = _get_diverse_domain_constraint_orderly(model, symbol_domains_size, solve_order)
                z3_solver.add(latest_diverse_domain_constraint)
                    
            elif z3_solver.check() == z3.unknown:
                log_info(LOGGER_NAME, f"{' ' * (INDENT * 2)}- timeout")
                log_info(LOGGER_NAME, f"{' ' * (INDENT * 2)}- solved in {time.time() - start_time} seconds")
                # Backtrack to previous solution
                try:
                    _z3_solver_safe_pop(z3_solver)
                    consecutive_backtracking_num += 1
                    if consecutive_backtracking_num >= CONSECUTIVE_BACKTRACKING_NUM:
                        log_info(LOGGER_NAME, f"{' ' * (INDENT * 2)}- consecutive backtracking over limit")
                        break
                    
                    assert latest_model is not None and latest_diverse_domain_constraint is not None, "latest_model or latest_diverse_domain_constraint is None during backtracking"
                    _z3_solver_safe_push(z3_solver)
                    latest_diverse_domain_constraint = _get_diverse_domain_constraint_orderly(latest_model, symbol_domains_size, solve_order)
                    z3_solver.add(latest_diverse_domain_constraint)
                except ValueError:
                    log_info(LOGGER_NAME, f"{' ' * (INDENT * 2)}- no more backtracking point")
                    break
            else:
                log_info(LOGGER_NAME, f"{' ' * (INDENT * 2)}- unsat")
                log_info(LOGGER_NAME, f"{' ' * (INDENT * 2)}- solved in {time.time() - start_time} seconds")
                # Backtrack to previous solution
                try:
                    _z3_solver_safe_pop(z3_solver)
                    consecutive_backtracking_num += 1
                    if consecutive_backtracking_num >= CONSECUTIVE_BACKTRACKING_NUM:
                        log_info(LOGGER_NAME, f"{' ' * (INDENT * 2)}- consecutive backtracking over limit")
                        break
                    
                    assert latest_model is not None and latest_diverse_domain_constraint is not None, "latest_model or latest_diverse_domain_constraint is None during backtracking"
                    _z3_solver_safe_push(z3_solver)
                    latest_diverse_domain_constraint = _get_diverse_domain_constraint_orderly(latest_model, symbol_domains_size, solve_order)
                    z3_solver.add(latest_diverse_domain_constraint)
                except ValueError:
                    log_info(LOGGER_NAME, f"{' ' * (INDENT * 2)}- no more backtracking point")
                    break
        
        if len(model_priority_pairs) == 0:
            return []
        else:
            model_priority_pairs.sort(key=lambda x: x[0], reverse=True)
            return [model for _, model in model_priority_pairs]
            
    if not parameter_domain_discretization and not predicate_sensitivity_promotion:
        return _iteration_00()
    elif parameter_domain_discretization and not predicate_sensitivity_promotion:
        return _iteration_10()
    elif not parameter_domain_discretization and predicate_sensitivity_promotion:
        return _iteration_01()
    else:
        return _iteration_11()            

def _populate_missing_symbols(bfuncs_path: Path, current_models: list[dict[str, Fraction|str]]) -> list[dict[str, Fraction|str]]:

    if not current_models:
        return current_models
    
    symbols = extract_symbols(bfuncs_path)
    completed_models = []
    for current_model in current_models:
        completed_model = current_model.copy()
        missing_symbols = symbols - set(current_model.keys())
        for missing_symbol in missing_symbols:
            if missing_symbol.startswith(NUMERIC_SYMBOLIC_PREFIX):
                sign = random.choice([-1.0, 1.0])
                mantissa = random.random()
                exponent = float(random.randint(-100, 100))
                symbol_value = sign * mantissa * math.pow(2, exponent)
                completed_model[missing_symbol] = Fraction(symbol_value)
            else:
                symbol_value_length = random.randint(1, 10)
                symbol_value = ''.join(
                    random.choices(string.ascii_letters + string.digits, k=symbol_value_length)
                )
                completed_model[missing_symbol] = symbol_value
        completed_models.append(completed_model)
    return completed_models
