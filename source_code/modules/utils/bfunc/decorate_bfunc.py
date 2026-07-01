import ast
from typing import Type
import re

from .. import STRING_SYMBOLIC_PREFIX


def make_fractional(nodes: dict[str, ast.FunctionDef]) -> dict[str, ast.FunctionDef]:

    class FractionTransformer(ast.NodeTransformer):
        
        def visit_Compare(self, node: ast.Compare) -> ast.Compare:        
            wrapped_left = ast.Call(
                            func=ast.Name(id='try_to_fraction', ctx=ast.Load()),
                            args=[node.left],
                            keywords=[]
                        )
        
            # Wrap right-side values (if not symbolic constants)
            wrapped_comparators = [
                ast.Call(
                    func=ast.Name(id='try_to_fraction', ctx=ast.Load()),
                    args=[comp],
                    keywords=[]
                )
                for comp in node.comparators
            ]
            
            # Return new comparison node
            return ast.Compare(
                left=wrapped_left,
                ops=node.ops,
                comparators=wrapped_comparators
            )        
                
    fractional_nodes = {}
    for node in nodes.values():
        fractional_node = FractionTransformer().visit(node)
        fractional_nodes[node.name] = fractional_node
    return fractional_nodes

def make_symbolic(nodes: dict[str, ast.FunctionDef]) -> dict[str, ast.FunctionDef]:
    """Convert regular functions to symbolic functions, supporting both numeric and string symbols"""
    
    class MixedSymTransformer(ast.NodeTransformer):
        """Transformer that supports simultaneous processing of numeric and string symbols"""
        def __init__(self):
            # Mapping from comparison operators to sympy functions
            self.COMPARE_OP_TO_SYMPY: dict[Type[ast.cmpop], str] = {
                ast.Lt: 'sp.Lt',
                ast.LtE: 'sp.Le',
                ast.Gt: 'sp.Gt',
                ast.GtE: 'sp.Ge',
                ast.Eq: 'sp.Eq',
                ast.NotEq: 'sp.Ne'
            }
            
            # For handling equality/inequality comparisons of string symbols
            self.STRING_COMPARE_OP: dict[Type[ast.cmpop], str] = {
                ast.Eq: 'symbolic_eq',
                ast.NotEq: 'symbolic_ne'
            }
            
            # Symbol pattern
            self.string_symbol_pattern = re.compile(f'^{STRING_SYMBOLIC_PREFIX}\\d+$')
            
        def _create_func_node(self, func_name: str) -> ast.AST:
            """Create function node"""
            if '.' in func_name:
                module, attr = func_name.split('.')
                return ast.Attribute(
                    value=ast.Name(id=module, ctx=ast.Load()),
                    attr=attr,
                    ctx=ast.Load()
                )
            return ast.Name(id=func_name, ctx=ast.Load())
        
        def _contains_string_symbol(self, node: ast.AST) -> bool:
            """Check if the expression contains string symbols"""
            if isinstance(node, ast.Name) and self.string_symbol_pattern.match(node.id):
                return True
                
            for child in ast.iter_child_nodes(node):
                if self._contains_string_symbol(child):
                    return True
                    
            return False
        
        def visit_Compare(self, node: ast.Compare) -> ast.AST:
            """Handle comparison expressions"""
            # First recursively process child nodes
            node = self.generic_visit(node)
            
            # Only handle single comparisons
            assert len(node.ops) == 1, "Only support single comparison"
            
            # For equality and inequality comparisons, check if string symbols are contained
            if isinstance(node.ops[0], (ast.Eq, ast.NotEq)) and (
                self._contains_string_symbol(node.left) or 
                self._contains_string_symbol(node.comparators[0])
            ):
                # Use string symbol processing
                return ast.Call(
                    func=ast.Name(id=self.STRING_COMPARE_OP[type(node.ops[0])], ctx=ast.Load()),
                    args=[node.left, node.comparators[0]],
                    keywords=[]
                )
            else:
                # Use sympy processing
                return ast.Call(
                    func=self._create_func_node(self.COMPARE_OP_TO_SYMPY[type(node.ops[0])]),
                    args=[node.left, node.comparators[0]],
                    keywords=[]
                )
    
    symbolic_nodes = {}
    transformer = MixedSymTransformer()
    
    for name, node in nodes.items():
        symbolic_node = transformer.visit(node)
        symbolic_nodes[name] = symbolic_node
        
    return symbolic_nodes

