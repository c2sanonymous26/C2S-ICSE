from pathlib import Path
import ast

from ...utils import get_bfunc_nodes, NUMERIC_SYMBOLIC_PREFIX, STRING_SYMBOLIC_PREFIX,  CTreeNode


def decide(ctree_root: CTreeNode, bfunc_file_path: Path) -> dict[int, list[str]]:
    """
    Determine the solving order of symbolic variables.
    For implies nodes with goal_truth set to true, symbolic variables in the left branch should be solved before those in the right branch.
    
    Args:
        ctree_root: Root node of the constraint tree
        bfunc_file_path: Path to the bfunc file
    
    Returns:
        A dictionary where keys are solving orders (smaller numbers are solved first) and values are lists of symbolic variables for the corresponding order
    """
    # Get all function definitions from bfunc file
    with open(bfunc_file_path, 'r') as f:
        module_content = f.read()
    pure_bfunc_nodes, numeric_symbolic_bfunc_nodes, string_symbolic_bfunc_nodes = get_bfunc_nodes(module_content)
    
    # Analyze symbolic variables used in each bfunc function
    bfunc_to_symbols = {}
    all_symbols = set()  # Collect all symbolic variables
    for bfunc_name, node in {**pure_bfunc_nodes, **numeric_symbolic_bfunc_nodes, **string_symbolic_bfunc_nodes}.items():
        symbols = _find_symbols_in_function(node)
        bfunc_to_symbols[bfunc_name] = symbols
        all_symbols.update(symbols)  # Add all symbolic variables to the set
    
    # Find all implies nodes with goal_truth set to true, and analyze symbolic variables in left and right subtrees
    symbol_dependencies = {}  # Store dependency relationships between symbolic variables
    _process_implies_nodes(ctree_root, bfunc_to_symbols, symbol_dependencies)
    
    # Sort symbolic variables based on dependency relationships to determine solving order
    solve_order = {}
    _determine_solve_order(symbol_dependencies, solve_order, all_symbols)
    
    return solve_order


def _find_symbols_in_function(func_node: ast.FunctionDef) -> list[str]:
    """Analyze all symbolic variables used in the function"""
    symbols = []
    
    class SymbolVisitor(ast.NodeVisitor):
        def visit_Name(self, node):
            if node.id.startswith(NUMERIC_SYMBOLIC_PREFIX):
                if node.id not in symbols:
                    symbols.append(node.id)
            if node.id.startswith(STRING_SYMBOLIC_PREFIX):
                if node.id not in symbols:
                    symbols.append(node.id)
            self.generic_visit(node)
    
    visitor = SymbolVisitor()
    visitor.visit(func_node)
    return symbols

def _process_implies_nodes(node: CTreeNode, bfunc_to_symbols: dict, symbol_dependencies: dict):
    """Process implies nodes and analyze the order of symbolic variables in left and right subtrees"""
    if node[0] == "implies" and node[2]["goal_truth"] is True:
        # For implies nodes with goal_truth set to true, left-side symbolic variables should be solved before right-side ones
        left_symbols = _collect_symbols_in_subtree(node[3][0], bfunc_to_symbols)
        right_symbols = _collect_symbols_in_subtree(node[3][1], bfunc_to_symbols)
        
        # Establish dependency relationship: left-side symbolic variables -> right-side symbolic variables
        for left_symbol in left_symbols:
            for right_symbol in right_symbols:
                if left_symbol != right_symbol:  # Avoid self-reference
                    if left_symbol not in symbol_dependencies:
                        symbol_dependencies[left_symbol] = set()
                    symbol_dependencies[left_symbol].add(right_symbol)
    
    # Recursively process child nodes
    if node[3] is not None:
        for child in node[3]:
            _process_implies_nodes(child, bfunc_to_symbols, symbol_dependencies)

def _collect_symbols_in_subtree(node: CTreeNode, bfunc_to_symbols: dict) -> set:
    """Collect all symbolic variables in the subtree"""
    symbols = set()
    
    if node[0] == "bfunc":
        bfunc_id = node[1]
        bfunc_name = f"bfunc_{bfunc_id}"
        if bfunc_name in bfunc_to_symbols:
            symbols.update(bfunc_to_symbols[bfunc_name])
    
    # Recursively process child nodes
    if node[3] is not None:
        for child in node[3]:
            child_symbols = _collect_symbols_in_subtree(child, bfunc_to_symbols)
            symbols.update(child_symbols)
    
    return symbols

def _determine_solve_order(symbol_dependencies: dict, solve_order: dict, all_symbols: set):
    """Assign solving order to symbolic variables based on dependency relationships
    
    Smaller order numbers are solved first
    Dependent symbolic variables will get smaller order numbers (solved first)
    Variables that depend on others will get larger order numbers (solved later)
    """
        
    # Initialize order numbers for all symbolic variables to 0
    symbol_orders = {symbol: 0 for symbol in all_symbols}
    
    # Ensure symbol_dependencies contains all symbolic variables
    for symbol in all_symbols:
        if symbol not in symbol_dependencies:
            symbol_dependencies[symbol] = set()
    
    # Adjust order numbers based on dependency relationships, ensuring dependent symbolic variables are solved first
    changed = True
    while changed:
        changed = False
        for symbol, deps in symbol_dependencies.items():
            for dep in deps:
                if dep in all_symbols and symbol in all_symbols:  # Ensure both variables are within processing scope
                    if symbol_orders[symbol] >= symbol_orders[dep]:
                        symbol_orders[dep] = symbol_orders[symbol] + 1
                        changed = True
    
    # Group symbolic variables by order number
    for symbol, order in symbol_orders.items():
        if order not in solve_order:
            solve_order[order] = []
        solve_order[order].append(symbol)
    
    # Sort symbolic variables within each order number to ensure deterministic results
    for order in solve_order:
        solve_order[order].sort()
    
    return solve_order