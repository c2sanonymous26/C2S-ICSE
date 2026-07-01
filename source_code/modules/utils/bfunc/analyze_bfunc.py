import ast
import re
from pathlib import Path
from typing import Set

from .. import NUMERIC_SYMBOLIC_PREFIX, STRING_SYMBOLIC_PREFIX


def extract_symbols(bfuncs_path: Path) -> Set[str]:
    with open(bfuncs_path, 'r') as f:
        module_content = f.read()
    
    module_ast = ast.parse(module_content)
    symbols = set()
    
    for node in module_ast.body:
        if isinstance(node, ast.FunctionDef):
            numeric_symbols = _extract_numeric_symbols_from_bfunc(node)
            string_symbols = _extract_string_symbols_from_bfunc(node)
            symbols.update(numeric_symbols)
            symbols.update(string_symbols)
    
    return symbols
    
def _extract_numeric_symbols_from_bfunc(node: ast.FunctionDef) -> Set[str]:
    numeric_symbols = set()
    numeric_symbol_pattern = re.compile(f'^{re.escape(NUMERIC_SYMBOLIC_PREFIX)}\\d+$')
    for sub_node in ast.walk(node):
        if isinstance(sub_node, ast.Name) and numeric_symbol_pattern.match(sub_node.id):
            numeric_symbols.add(sub_node.id)
    return numeric_symbols

def _extract_string_symbols_from_bfunc(node: ast.FunctionDef) -> Set[str]:
    string_symbols = set()
    string_symbol_pattern = re.compile(f'^{re.escape(STRING_SYMBOLIC_PREFIX)}\\d+$')
    for sub_node in ast.walk(node):
        if isinstance(sub_node, ast.Name) and string_symbol_pattern.match(sub_node.id):
            string_symbols.add(sub_node.id)
    return string_symbols

def analyze_bfunc_symbol_counts(bfuncs_path: Path) -> dict[str, int]:
    with open(bfuncs_path, 'r') as f:
        module_content = f.read()
    
    module_ast = ast.parse(module_content)
    
    numeric_symbol_pattern = re.compile(f'^{re.escape(NUMERIC_SYMBOLIC_PREFIX)}\\d+$')
    string_symbol_pattern = re.compile(f'^{re.escape(STRING_SYMBOLIC_PREFIX)}\\d+$')
    
    bfunc_symbol_counts = {}
    
    for node in module_ast.body:
        if isinstance(node, ast.FunctionDef) and node.name.startswith('bfunc_'):
            symbols = set()
            for n in ast.walk(node):
                if isinstance(n, ast.Name):
                    if numeric_symbol_pattern.match(n.id) or string_symbol_pattern.match(n.id):
                        symbols.add(n.id)
            
            bfunc_symbol_counts[node.name] = len(symbols)
    
    return bfunc_symbol_counts