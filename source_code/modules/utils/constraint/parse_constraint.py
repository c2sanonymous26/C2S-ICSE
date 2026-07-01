import ast
import lxml.etree as ET
from pathlib import Path

from .. import CTreeNode
from ..bfunc.load_bfunc import get_bfunc_nodes

# Variables
_pure_nodes: dict[str, ast.FunctionDef] = {}
_n_symbolic_nodes: dict[str, ast.FunctionDef] = {}
_s_symbolic_nodes: dict[str, ast.FunctionDef] = {}

def parse_constraint(constraint_path: Path, bfuncs_path: Path, concurrent: bool) -> CTreeNode:
    
    global _pure_nodes, _n_symbolic_nodes, _s_symbolic_nodes
    
    with open(bfuncs_path, 'r') as f:
        module_content = f.read()
    _pure_nodes, _n_symbolic_nodes, _s_symbolic_nodes = get_bfunc_nodes(module_content)
    
    parser = ET.XMLParser(remove_comments=True)
    with open(constraint_path, 'r') as cfile:
        content = cfile.read()
        root = ET.fromstring(content.encode(), parser=parser)
    
    id_counter = {
        "forall": 0, "exists": 0,
        "and": 0, "or": 0,
        "implies": 0, "not": 0
    }
    tree_root = _parse_node(root, concurrent, id_counter, True, 0)
    return tree_root

def _parse_node(node: ET.Element, concurrent: bool, id_counter: dict[str, int], 
                goal_truth: bool, depth: int) -> CTreeNode:

    if node.tag == "formula":
        return _parse_node(node[0], concurrent, id_counter, goal_truth, depth)
    elif node.tag == "bfunc":  
        bfunc_name = f'bfunc_{node.attrib.get("id")}'
        assert bfunc_name in _pure_nodes or bfunc_name in _n_symbolic_nodes or bfunc_name in _s_symbolic_nodes, \
            f"Unknown bfunc id: {node.attrib.get('id')}"
        return ( 
            "bfunc",
            node.attrib.get("id"),
            {
                "goal_truth": goal_truth,
                "depth": depth,
                "has_symbol": bfunc_name in _n_symbolic_nodes or bfunc_name in _s_symbolic_nodes
            },
            None
        ) 
    elif node.tag in {"and", "or"}:        
        left_subnode = _parse_node(node[0], concurrent, id_counter, goal_truth, depth + 1)
        right_subnode = _parse_node(node[1], concurrent, id_counter, goal_truth, depth + 1)    
        
        id_counter[node.tag] += 1
        return (
            node.tag,
            id_counter[node.tag],
            {
                "goal_truth": goal_truth,
                "depth": depth,
                "has_symbol": left_subnode[2]["has_symbol"] or right_subnode[2]["has_symbol"]
            },
            [left_subnode, right_subnode]
        )    
    elif node.tag == "implies":   
        left_subnode = _parse_node(node[0], concurrent, id_counter, not goal_truth, depth + 1)
        right_subnode = _parse_node(node[1], concurrent, id_counter, goal_truth, depth + 1)
        
        id_counter[node.tag] += 1    
        return (
            node.tag,
            id_counter[node.tag],
            {
                "goal_truth": goal_truth,
                "depth": depth,
                "has_symbol": left_subnode[2]["has_symbol"] or right_subnode[2]["has_symbol"]
            },
            [left_subnode, right_subnode]
        )
    elif node.tag == "not": 
        subnode = _parse_node(node[0], concurrent, id_counter, not goal_truth, depth + 1)
        
        id_counter[node.tag] += 1
        return (
            "not",              
            id_counter[node.tag],
            {
                "goal_truth": goal_truth,
                "depth": depth,
                "has_symbol": subnode[2]["has_symbol"]
            },
            [subnode]
        )
    elif node.tag in  {"forall", "exists"}:
        subnode = _parse_node(node[0], False, id_counter, goal_truth, depth + 1)
        
        id_counter[node.tag] += 1
        
        return (
            node.tag,
            id_counter[node.tag],
            {
                "var": node.attrib.get("var"), 
                "in": node.attrib.get("in"),
                "concurrent": concurrent,
                "goal_truth": goal_truth,
                "depth": depth,
                "has_symbol": subnode[2]["has_symbol"]
            },
            [subnode]
        )
    else:
        assert False, f"Unknown tag: {node.tag}"