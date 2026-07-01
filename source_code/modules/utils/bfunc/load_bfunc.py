import ast
import re
import sympy as sp
from typing import Callable, Union, Any
from fractions import Fraction
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

from .. import NUMERIC_SYMBOLIC_PREFIX, STRING_SYMBOLIC_PREFIX, BFUNC_PREFIX
from .decorate_bfunc import make_fractional, make_symbolic


def load_bfuncs(bfuncs_file_path: str) -> tuple[dict[str, Callable], dict[str, Callable], dict[str, Callable]]:
    with open(bfuncs_file_path, 'r') as f:
        module_content = f.read()
        
    pure_nodes, n_symbolic_nodes, s_symbolic_nodes = get_bfunc_nodes(module_content)    
        
    pure_bfuncs, n_symbolic_bfuncs, s_symbolic_bfuncs = {}, {}, {}
    if len(pure_nodes) > 0:
        pure_bfuncs = _load_pure_bfuncs(pure_nodes, module_content)
    if len(n_symbolic_nodes) > 0:
        n_symbolic_bfuncs = _load_numeric_symbolic_bfuncs(n_symbolic_nodes, module_content)
    if len(s_symbolic_nodes) > 0:
        s_symbolic_bfuncs = _load_string_symbolic_bfuncs(s_symbolic_nodes, module_content)
        
    return pure_bfuncs, n_symbolic_bfuncs, s_symbolic_bfuncs

def update_and_load_bfuncs(bfuncs_file_path: str, model: dict[str, Fraction|str]) -> dict[str, Callable]:
    with open(bfuncs_file_path, 'r') as f:
        module_content = f.read()
        
    pure_nodes, n_symbolic_nodes, s_symbolic_nodes = get_bfunc_nodes(module_content)
    pure_nodes.update(
        _update_symbolic_nodes(n_symbolic_nodes, model)
    )
    pure_nodes.update(
        _update_symbolic_nodes(s_symbolic_nodes, model)
    )
    pure_bfuncs = {}
    if len(pure_nodes) > 0:
        pure_bfuncs = _load_pure_bfuncs(pure_nodes, module_content)

    return pure_bfuncs

def get_bfunc_nodes(module_content: str) -> tuple[dict[str, ast.FunctionDef], dict[str, ast.FunctionDef], dict[str, ast.FunctionDef]]:  
    
    def _is_pure_bfunc(node: ast.FunctionDef) -> bool:
        is_bfunc = node.name.startswith(BFUNC_PREFIX)
        if not is_bfunc:
            return False
        
        numeric_symbol_pattern = re.compile(f'^{NUMERIC_SYMBOLIC_PREFIX}\\d+$')
        string_symbol_pattern = re.compile(f'^{STRING_SYMBOLIC_PREFIX}\\d+$')
        for n in ast.walk(node):
            if isinstance(n, ast.Name) and numeric_symbol_pattern.match(n.id):
                return False
            if isinstance(n, ast.Name) and string_symbol_pattern.match(n.id):
                return False
        return True
    
    def _is_numeric_symbolic_bfunc(node: ast.FunctionDef) -> bool:
        is_bfunc = node.name.startswith(BFUNC_PREFIX)
        if not is_bfunc:
            return False
        
        numeric_symbol_pattern = re.compile(f'^{NUMERIC_SYMBOLIC_PREFIX}\\d+$')
        string_symbol_pattern = re.compile(f'^{STRING_SYMBOLIC_PREFIX}\\d+$')
        
        is_numeric = False
        is_string = False
        for n in ast.walk(node):
            if isinstance(n, ast.Name) and numeric_symbol_pattern.match(n.id):
                is_numeric = True
            if isinstance(n, ast.Name) and string_symbol_pattern.match(n.id):
                is_string = True

        return is_numeric and not is_string
    
    def _is_string_symbolic_bfunc(node: ast.FunctionDef) -> bool:
        is_bfunc = node.name.startswith(BFUNC_PREFIX)
        if not is_bfunc:
            return False
        
        numeric_symbol_pattern = re.compile(f'^{NUMERIC_SYMBOLIC_PREFIX}\\d+$')
        string_symbol_pattern = re.compile(f'^{STRING_SYMBOLIC_PREFIX}\\d+$')
        
        is_numeric = False
        is_string = False
        for n in ast.walk(node):
            if isinstance(n, ast.Name) and numeric_symbol_pattern.match(n.id):
                is_numeric = True
            if isinstance(n, ast.Name) and string_symbol_pattern.match(n.id):
                is_string = True
                
        return is_string and not is_numeric
    
    module_ast = ast.parse(module_content)
    pure_nodes = {}
    n_symbolic_nodes = {}
    s_symbolic_nodes = {}
    for node in module_ast.body:
        if isinstance(node, ast.FunctionDef):
            if _is_pure_bfunc(node):        
                pure_nodes[node.name] = node
            elif _is_numeric_symbolic_bfunc(node):
                n_symbolic_nodes[node.name] = node
            elif _is_string_symbolic_bfunc(node):
                s_symbolic_nodes[node.name] = node
            else:
                raise ValueError(f"unsupported node: {node.name}")
    
    return pure_nodes, n_symbolic_nodes, s_symbolic_nodes
    
def _update_symbolic_nodes(symbolic_nodes: dict[str, ast.FunctionDef], model: dict[str, Fraction|str]) -> dict[str, ast.FunctionDef]:
    for node in symbolic_nodes.values():
        for n in ast.walk(node):
            if isinstance(n, ast.Name) and n.id in model:
                value = model[n.id]
                if isinstance(value, Fraction):
                    new_node = ast.Call(
                        func=ast.Name(id='Fraction', ctx=ast.Load()),
                        args=[
                            ast.Constant(value=value.numerator), 
                            ast.Constant(value=value.denominator)
                        ],
                        keywords=[]
                    )
                    ast.copy_location(new_node, n)
                    for parent in ast.walk(node):
                        for field, old_value in ast.iter_fields(parent):
                            if isinstance(old_value, list):
                                for i, item in enumerate(old_value):
                                    if item == n:
                                        old_value[i] = new_node
                            elif old_value == n:
                                setattr(parent, field, new_node)
                elif isinstance(value, str):
                    new_node = ast.Constant(value=value, kind=None)
                    ast.copy_location(new_node, n)
                    for parent in ast.walk(node):
                        for field, old_value in ast.iter_fields(parent):
                            if isinstance(old_value, list):
                                for i, item in enumerate(old_value):
                                    if item == n:
                                        old_value[i] = new_node
                            elif old_value == n:
                                setattr(parent, field, new_node)
                else:
                    raise ValueError(f"unsupported type: {value}:{type(value)}")
    return symbolic_nodes
    
def _load_pure_bfuncs(pure_nodes: dict[str, ast.FunctionDef], module_content: str) -> dict[str, Callable]:
    namespace = {
        'Union': Union,
        'Any': Any,
        'Fraction': Fraction,
        '__builtins__': __builtins__
    }
    
    fractional_nodes = make_fractional(pure_nodes)
    fraction_func_src = '''
def try_to_fraction(value: Any) -> Union[Fraction, Any]:
    if not isinstance(value, (int, float)):
        return value
        
    try:
        precision = 1e-9
        multiplier = round(1.0 / precision)
        rounded_value = round(value * multiplier) / multiplier
        return Fraction(rounded_value)
    except (ValueError, TypeError) as e:
            return value
    '''
    
    imports_str = _collect_imports_of_module(module_content)
    fractional_func_sources_str = _collect_source_codes_of_funcs(fractional_nodes)
    full_source = f'{imports_str}\n{fraction_func_src}\n{fractional_func_sources_str}'    
    try:
        loaded_funcs = {}
        exec(full_source, namespace)
        loaded_funcs = {node.name: namespace[node.name] for node in fractional_nodes.values() if node.name in namespace}
        missing_funcs = [node.name for node in fractional_nodes.values() if node.name not in namespace]
        if missing_funcs:
            raise Exception(f'Failed to load pure bfuncs: {missing_funcs}')
        return loaded_funcs
    except Exception as e:
        raise Exception(f'Failed to load pure bfuncs: {e}\nSource:\n{full_source}')

def _load_numeric_symbolic_bfuncs(symbolic_nodes: dict[str, ast.FunctionDef], module_content: str) -> dict[str, Callable]:
    namespace = {
        'sp': sp,
        '__builtins__': __builtins__
    }
    
    # symbolize the parametric bfuncs
    symbolic_nodes = make_symbolic(symbolic_nodes)
    
    # collect all _N_TRESHOLD_i symbols from symbolic funcs and update namespace
    numeric_symbol_pattern = re.compile(f'^{NUMERIC_SYMBOLIC_PREFIX}\\d+$')
    symbols = {}
    for node in symbolic_nodes.values():
        for n in ast.walk(node):
            if isinstance(n, ast.Name) and numeric_symbol_pattern.match(n.id):
                symbols[n.id] = sp.Symbol(n.id)
    namespace.update(symbols)

    imports_str = _collect_imports_of_module(module_content)
    symbolic_func_sources_str = _collect_source_codes_of_funcs(symbolic_nodes)
    full_source = f'{imports_str}\n{symbolic_func_sources_str}'
    try:
        exec(full_source, namespace)
        loaded_funcs = {node.name: namespace[node.name] for node in symbolic_nodes.values() if node.name in namespace}
        missing_funcs = [node.name for node in symbolic_nodes.values() if node.name not in namespace]
        if missing_funcs:
            raise Exception(f'Failed to load numeric symbolic bfuncs: {missing_funcs}')
        return loaded_funcs
    except Exception as e:
        raise Exception(f'Failed to load numeric symbolic bfuncs: {e}\nSource:\n{full_source}')
    
def _load_string_symbolic_bfuncs(symbolic_nodes: dict[str, ast.FunctionDef], module_content: str) -> dict[str, Callable]:
    namespace = {
        '__builtins__': __builtins__
    }
    
    # symbolize the parametric bfuncs
    symbolic_nodes = make_symbolic(symbolic_nodes)
    
    # collect all _S_TRESHOLD_i symbols from symbolic funcs and update namespace
    string_symbol_pattern = re.compile(f'^{STRING_SYMBOLIC_PREFIX}\\d+$')
    symbols = {}
    for node in symbolic_nodes.values():
        for n in ast.walk(node):
            if isinstance(n, ast.Name) and string_symbol_pattern.match(n.id):
                symbols[n.id] = n.id
    namespace.update(symbols)
    
    string_symbolic_code = """
# String symbolic expression class and functions
class StringSymbolicExpr:
    def __init__(self, left, right, op_type):
        self.left = left
        self.right = right
        self.op_type = op_type  # "eq" or "ne"
    
    def __repr__(self):
        op_str = "==" if self.op_type == "eq" else "!="
        return f"{self.left} {op_str} {self.right}"

def symbolic_eq(left, right):
    return StringSymbolicExpr(left, right, "eq")

def symbolic_ne(left, right):
    return StringSymbolicExpr(left, right, "ne")
"""   

    imports_str = _collect_imports_of_module(module_content)
    symbolic_func_sources_str = _collect_source_codes_of_funcs(symbolic_nodes)
    full_source = f'{imports_str}\n{string_symbolic_code}\n{symbolic_func_sources_str}'
    try:
        exec(full_source, namespace)
        load_bfuncs = {node.name: namespace[node.name] for node in symbolic_nodes.values() if node.name in namespace}
        missing_funcs = [node.name for node in symbolic_nodes.values() if node.name not in namespace]
        if missing_funcs:
            raise Exception(f'Failed to load string symbolic bfuncs: {missing_funcs}')
        return load_bfuncs
    except Exception as e:
        raise Exception(f'Failed to load string symbolic bfuncs: {e}\nSource:\n{full_source}')

def _collect_imports_of_module(module_content: str) -> str:
    module_ast = ast.parse(module_content)
    imports = []
    for node in ast.walk(module_ast):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            import_str = ast.get_source_segment(module_content, node)
            import_str = import_str.strip()
            imports.append(import_str)
    return '\n'.join(imports)

def _collect_source_codes_of_funcs(func_nodes: dict[str, ast.FunctionDef]) -> str:
    func_sources = []
    for node in func_nodes.values():
        func_sources.append(ast.unparse(node))
    return '\n\n'.join(func_sources)
