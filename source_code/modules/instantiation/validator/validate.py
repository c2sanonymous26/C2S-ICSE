import time
from pathlib import Path
import sympy as sp

from ...utils import get_data_size, CTreeNode, log_info, parse_constraint, timeout_process
from .. import INDENT, LOGGER_NAME
from . import ValidationResult, ILLEGAL_DATA_RATIO_BOUND
from .validate_formula import validate_formula


VALIDATE_TIMEOUT = 1.0 * 60 * 60

@timeout_process(VALIDATE_TIMEOUT, logger_name=LOGGER_NAME)
def validate(
    constraint_file_path: Path,
    bfunc_file_path: Path,
    validate_ctx2data: dict[str, Path],
    data_field_types: dict[str, str | int | float],
    concurrent: bool
) -> bool:
    
    # Parse template
    start_time = time.time()
    ctree_root = parse_constraint(constraint_file_path, bfunc_file_path, concurrent)
    log_info(LOGGER_NAME, f"Parsed template in {time.time() - start_time} seconds")
    
    # Prepare validation data
    start_time = time.time()
    val_data_num_dict = _set_validate_data(ctree_root, validate_ctx2data)
    log_info(LOGGER_NAME, f'Set validate data in {time.time() - start_time} seconds')
    log_info(LOGGER_NAME, f'{" " * INDENT}- validate data num info: {val_data_num_dict}')
    
    # Get possible number of links
    start_time = time.time()
    total_data_num = sum(val_data_num_dict.values())
    possible_links_size = _get_possible_link_size(ctree_root)
    log_info(LOGGER_NAME, f'Get possible links size in {time.time() - start_time} seconds')
    log_info(LOGGER_NAME, f'{" " * INDENT}- possible links size: {possible_links_size}')
    
    # Validate model
    start_time = time.time()
    validation_results = validate_formula(ctree_root, bfunc_file_path, data_field_types)
    validate_time = time.time() - start_time
    illegal_data_num = _extract_data_num_from_validation_results(validation_results)
    log_info(LOGGER_NAME, _serialize_validation_results(validation_results, possible_links_size, illegal_data_num, total_data_num, validate_time))
    
    if illegal_data_num / total_data_num > ILLEGAL_DATA_RATIO_BOUND:
        return False
    else:
        return True
    
    
def _set_validate_data(ctree_root: CTreeNode, validate_ctx2data: dict[str, Path]) -> dict[str, int]:
    
    val_data_num_dict = {}
    
    queue = [ctree_root]
    while queue:
        node = queue.pop(0)
        if node[0] in ('forall', 'exists'):
            ctx = node[2]['in']
            val_data_num = get_data_size(validate_ctx2data[ctx])
            val_data_num_dict[ctx] = val_data_num
            node[2]['validate_data_info'] = (
                validate_ctx2data[ctx],
                val_data_num
            )   
        
        if node[3] is not None:
            for child in node[3]:
                queue.append(child)
    
    return val_data_num_dict

def _extract_data_num_from_validation_results(validation_results: ValidationResult) -> int:
    truth, links = validation_results
    if truth:
        return 0
    else:
        data_id_set = set()
        for link in links:
            for _, data_id in link:
                data_id_set.add(data_id)
        return len(data_id_set)

def _get_possible_link_size(ctree_root: CTreeNode) -> int:
    sym_val_dict = {}
    
    def _recursive(node: CTreeNode, truth: bool) -> sp.Expr:
        if node[0] == 'forall':
            if truth:
                return sp.Integer(1)
            else:
                symbol = sp.Symbol(node[2]['var'])
                sym_val_dict[symbol] = node[2]['validate_data_info'][1]
                return symbol * _recursive(node[3][0], truth)
        elif node[0] == 'exists':
            if truth:
                symbol = sp.Symbol(node[2]['var'])
                sym_val_dict[symbol] = node[2]['validate_data_info'][1]
                return symbol * _recursive(node[3][0], truth)
            else:
                return sp.Integer(1)
        elif node[0] == 'and':
            left = _recursive(node[3][0], truth)
            right = _recursive(node[3][1], truth)
            if truth:
                return left * right
            else:
                result = left + right
                if not result.free_symbols:
                    return sp.Integer(1)
                return result
        elif node[0] == 'or':
            left = _recursive(node[3][0], truth)
            right = _recursive(node[3][1], truth)
            if truth:
                result = left + right
                if not result.free_symbols:
                    return sp.Integer(1)
                return result
            else:
                return left * right
        elif node[0] == 'implies':
            left = _recursive(node[3][0], not truth)
            right = _recursive(node[3][1], truth)                
            if truth:
                result = left + right
                if not result.free_symbols:
                    return sp.Integer(1)
                return result
            else:
                return left * right
        elif node[0] == 'not':
            return _recursive(node[3][0], not truth)
        elif node[0] == 'bfunc':
            return sp.Integer(1)
        else:
            raise ValueError(f"Unknown node type: {node[0]}")
        
    expr = _recursive(ctree_root, False)
    return int(expr.subs(sym_val_dict))

def _serialize_validation_results(results: ValidationResult, possible_links_size: int, vio_data_num: int, total_data_num: int, validate_time: float) -> str:
    truth, links = results
    serialized_validation_results = 'Validation results:\n'
    
    if not truth:
        serialized_validation_results += f'{" " * INDENT}- {vio_data_num} out of {total_data_num} illegal ({round(vio_data_num / total_data_num * 100, 4)}%)\n'
        serialized_validation_results += f'{" " * INDENT}- {len(links)} out of {possible_links_size} violated ({round(len(links) / possible_links_size * 100, 4)}%)\n'
    else:
        serialized_validation_results += f'{" " * INDENT}- no violation\n'
    
    serialized_validation_results += f'{" " * INDENT}- validated in {validate_time} seconds\n'
    return serialized_validation_results[:-1]
