import multiprocessing as mp
from pathlib import Path
from typing import Any, Callable

from ...utils import CPU_COUNT, generate_data_chunks, load_bfuncs, CTreeNode
from . import Link, ValidationResult

# Variables
_bfuncs: dict[str, Callable] = None
_bfuncs_file_path: Path = None
_field_type_map: dict[str, Any] = None

def validate_formula(ctree_root: CTreeNode, bfuncs_file_path: Path, field_type_map: dict[str, Any]) -> ValidationResult:
    global _bfuncs, _bfuncs_file_path, _field_type_map
    
    _bfuncs_file_path = bfuncs_file_path
    _field_type_map = field_type_map
    
    _bfuncs, _, _ = load_bfuncs(bfuncs_file_path)
    
    return _validate_methods[ctree_root[0]](ctree_root, {})

def _merge_links(links_1: frozenset[frozenset[Link]], 
                    links_2: frozenset[frozenset[Link]]) -> frozenset[frozenset[Link]]:
    if not links_1:
        return links_2
    if not links_2:
        return links_1
    
    merged_links = set()
    for link_1 in links_1:
        for link_2 in links_2:
            merged_links.add(link_1.union(link_2))
    return frozenset(merged_links)

def _validate_bfunc(node: CTreeNode, var_bindings: dict[str, Any]) -> ValidationResult:
    assert node[0] == "bfunc", f"Expect bfunc node, but got {node[0]}"
    bfunc_name = f'bfunc_{node[1]}'
    
    try:
        truth = _bfuncs[bfunc_name](var_bindings)
    except ZeroDivisionError:
        truth = False
    
    return truth, frozenset()

def _validate_and(node: CTreeNode, var_bindings: dict[str, Any]) -> ValidationResult:
    assert node[0] == "and", f"Expect and node, but got {node[0]}"
    
    left_node, right_node = node[3][0], node[3][1]
    left_result = _validate_methods[left_node[0]](left_node, var_bindings)
    right_result = _validate_methods[right_node[0]](right_node, var_bindings)
    
    truth = left_result[0] and right_result[0]
    links = set()
    if left_result[0]: 
        if right_result[0]:
            links.update(
                _merge_links(
                    left_result[1],
                    right_result[1]
                )
            )
        else:
            links.update(right_result[1])
    else:
        if right_result[0]:
            links.update(left_result[1])
        else:
            links.update(left_result[1])
            links.update(right_result[1])
    return truth, frozenset(links)

def _validate_or(node: CTreeNode, var_bindings: dict[str, Any]) -> ValidationResult:
    assert node[0] == "or", f"Expect or node, but got {node[0]}"
    
    left_node, right_node = node[3][0], node[3][1]
    left_result = _validate_methods[left_node[0]](left_node, var_bindings)
    right_result = _validate_methods[right_node[0]](right_node, var_bindings)
    
    truth = left_result[0] or right_result[0]
    links = set()
    if left_result[0]: 
        if right_result[0]:
            links.update(left_result[1])
            links.update(right_result[1])
        else:
            links.update(left_result[1])
    else:
        if right_result[0]:
            links.update(right_result[1])
        else:
            links.update(
                _merge_links(
                    left_result[1],
                    right_result[1]
                )
            )
    return truth, frozenset(links)

def _validate_implies(node: CTreeNode, var_bindings: dict[str, Any]) -> ValidationResult:
    assert node[0] == "implies", f"Expect implies node, but got {node[0]}"
    
    left_node, right_node = node[3][0], node[3][1]
    left_result = _validate_methods[left_node[0]](left_node, var_bindings)
    right_result = _validate_methods[right_node[0]](right_node, var_bindings)
    
    truth = (not left_result[0]) or right_result[0]
    links = set()
    if left_result[0]:
        if right_result[0]:
            links.update(right_result[1])
        else:
            links.update(
                _merge_links(
                    left_result[1],
                    right_result[1]
                )
            )
    else:
        if right_result[0]:
            links.update(left_result[1])
            links.update(right_result[1])
        else:
            links.update(left_result[1])
    return truth, frozenset(links)

def _validate_not(node: CTreeNode, var_bindings: dict[str, Any]) -> ValidationResult:
    assert node[0] == "not", f"Expect not node, but got {node[0]}"
    
    sub_node = node[3][0]
    sub_result = _validate_methods[sub_node[0]](sub_node, var_bindings)
    
    truth = not sub_result[0]
    links = set()
    links.update(sub_result[1])
    return truth, frozenset(links)

def _validate_forall(node: CTreeNode, var_bindings: dict[str, Any]) -> ValidationResult:
    """Process forall validation in parallel"""
    
    var = node[2]['var']
    validate_data_file_path, validate_data_size = node[2]['validate_data_info']
    concurrent = node[2]['concurrent']
    sub_node = node[3][0]


    final_truth = True
    final_links = set()
    if concurrent:
        chunk_size = validate_data_size // CPU_COUNT 
        chunk_args = (
            (chunk, var, sub_node, var_bindings.copy(), _bfuncs_file_path, _field_type_map)
            for chunk in generate_data_chunks(validate_data_file_path, chunk_size, _field_type_map)
        )
    
        with mp.Pool() as pool:
            try:       
                for truth, links in pool.imap(
                    _process_forall_chunk,
                    chunk_args
                ):
                    final_truth = final_truth and truth
                    if not truth:
                        final_links.update(links)
            except Exception as e:
                pool.terminate()
                raise e   
    else:
        for chunk in generate_data_chunks(validate_data_file_path, 1, _field_type_map):
            data = chunk[0]
            var_bindings[var] = data
            sub_result = _validate_methods[sub_node[0]](sub_node, var_bindings)
            final_truth = final_truth and sub_result[0]
            if not sub_result[0]:
                final_links.update(
                    _merge_links(
                        frozenset({
                            frozenset({
                                (var, data['id'])
                            })
                        }),
                        sub_result[1]
                    )
                )
                                
            var_bindings.pop(var)
    
    return final_truth, frozenset(final_links)

def _validate_exists(node: CTreeNode, var_bindings: dict[str, Any]) -> ValidationResult:
    """Process exists validation in parallel"""
    var = node[2]['var']
    validate_data_file_path, validate_data_size = node[2]['validate_data_info']
    concurrent = node[2]['concurrent']
    sub_node = node[3][0]

                
    final_truth = False
    final_links = set()
    
    if concurrent:
        chunk_size = validate_data_size // CPU_COUNT 
        chunk_args = (
            (chunk, var, sub_node, var_bindings.copy(), _bfuncs_file_path, _field_type_map)
            for chunk in generate_data_chunks(validate_data_file_path, chunk_size, _field_type_map)
        )

        with mp.Pool() as pool:
            try:
                for truth, links in pool.imap(
                    _process_exists_chunk,
                    chunk_args
                ):
                    final_truth = final_truth or truth
                    if truth:
                        final_links.update(links)
            except Exception as e:
                pool.terminate()
                raise e
    else:
        for chunk in generate_data_chunks(validate_data_file_path, 1, _field_type_map):
            data = chunk[0]
            var_bindings[var] = data
            sub_result = _validate_methods[sub_node[0]](sub_node, var_bindings)
            final_truth = final_truth or sub_result[0]
            if sub_result[0]:
                final_links.update(
                    _merge_links(
                        frozenset({
                            frozenset({
                                (var, data['id'])
                            })
                        }),
                        sub_result[1]
                    )
                )
                
            var_bindings.pop(var)
            
    return final_truth, frozenset(final_links)

def _process_forall_chunk(args: tuple) -> tuple[bool, frozenset[Link]]:
    global _bfuncs, _field_type_map
    
    chunk_data, var, sub_node, var_bindings, bfuncs_file_path, field_type_map = args

    _bfuncs, _, _ = load_bfuncs(bfuncs_file_path)
    _field_type_map = field_type_map
    
    truth = True
    links = set()
    
    for data in chunk_data:
        var_bindings[var] = data
        sub_result = _validate_methods[sub_node[0]](sub_node, var_bindings)
        truth = truth and sub_result[0]
        if not sub_result[0]:
            links.update(
                _merge_links(
                    frozenset({
                        frozenset({
                            (var, data['id'])
                        })
                    }),
                    sub_result[1]
                )
            )
        
        var_bindings.pop(var)
    
    return truth, frozenset(links)

def _process_exists_chunk(args: tuple) -> tuple[bool, frozenset[Link]]:
    global _bfuncs, _field_type_map
    
    chunk_data, var, sub_node, var_bindings, bfuncs_file_path, field_type_map = args

    _bfuncs, _, _ = load_bfuncs(bfuncs_file_path)
    _field_type_map = field_type_map
    
    truth = False
    links = set()
    
    for data in chunk_data:
        var_bindings[var] = data
        sub_result = _validate_methods[sub_node[0]](sub_node, var_bindings)
        truth = truth or sub_result[0]
        if sub_result[0]:
            links.update(
                _merge_links(
                    frozenset({
                        frozenset({
                            (var, data['id'])
                        })
                    }),
                    sub_result[1]
                )
            )
            
        var_bindings.pop(var)
    
    return truth, frozenset(links)

_validate_methods = {
    "forall": _validate_forall,
    "exists": _validate_exists,
    "bfunc": _validate_bfunc,
    "and": _validate_and,
    "or": _validate_or,
    "implies": _validate_implies,
    "not": _validate_not
}
