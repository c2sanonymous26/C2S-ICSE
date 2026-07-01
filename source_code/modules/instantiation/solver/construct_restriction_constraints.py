import json
from z3 import z3
from pathlib import Path

from ...utils import NUMERIC_SYMBOLIC_PREFIX, STRING_SYMBOLIC_PREFIX

def construct_restriction_constraints_per_bfunc(restrictions_file_path: Path | None) -> dict[str, z3.BoolRef]:
    
    if restrictions_file_path is None:
        return {}
    
    with open(restrictions_file_path, 'r') as f:
        restrictions = f.read()
    json_obj = json.loads(restrictions)
    restrictions_dict = {}
    
    for id, restrictions_list in json_obj.items():
        assert len(restrictions_list) > 0, f"No restrictions found for {id}"
            
        # Store all constraints under this ID
        constraint_list = []
        
        for expr_str in restrictions_list:
            # Parse expression string
            expr_str = expr_str.strip()
            
            # Match operators
            if '>=' in expr_str:
                parts = expr_str.split('>=')
                op = '>='
            elif '<=' in expr_str:
                parts = expr_str.split('<=')
                op = '<='
            elif '==' in expr_str:
                parts = expr_str.split('==')
                op = '=='
            elif '!=' in expr_str:
                parts = expr_str.split('!=')
                op = '!='
            elif '>' in expr_str:
                parts = expr_str.split('>')
                op = '>'
            elif '<' in expr_str:
                parts = expr_str.split('<')
                op = '<'
            else:
                raise ValueError(f"Unsupported operator in expression: {expr_str}")
            
            # Ensure there are left and right parts
            if len(parts) != 2:
                raise ValueError(f"Invalid expression format: {expr_str}")
                
            left = parts[0].strip()
            right = parts[1].strip()
            
            # Create Z3 expressions directly in original order
            if NUMERIC_SYMBOLIC_PREFIX in expr_str:
                # Numeric variables
                if left.startswith(NUMERIC_SYMBOLIC_PREFIX):
                    z3_left = z3.Real(left)
                    z3_right = float(right)
                else:
                    z3_left = float(left)
                    z3_right = z3.Real(right)
                
                if op == '==':
                    constraint = z3_left == z3_right
                elif op == '!=':
                    constraint = z3_left != z3_right
                elif op == '>=':
                    constraint = z3_left >= z3_right
                elif op == '<=':
                    constraint = z3_left <= z3_right
                elif op == '>':
                    constraint = z3_left > z3_right
                elif op == '<':
                    constraint = z3_left < z3_right
            
            elif STRING_SYMBOLIC_PREFIX in expr_str:
                # String variables
                if left.startswith(STRING_SYMBOLIC_PREFIX):
                    z3_left = z3.String(left)
                    z3_right = z3.StringVal(right)
                else:
                    z3_left = z3.StringVal(left)
                    z3_right = z3.String(right)
                
                if op == '==':
                    constraint = z3_left == z3_right
                elif op == '!=':
                    constraint = z3_left != z3_right
                else:
                    raise ValueError(f"Unsupported operator '{op}' for string variable: {expr_str}")
            
            else:
                raise ValueError(f"No threshold variable found in expression: {expr_str}")
            
            # Add to constraint list
            constraint_list.append(constraint)
        
        # Combine all constraints using And
        if len(constraint_list) == 1:
            restrictions_dict[id] = constraint_list[0]
        else:
            restrictions_dict[id] = z3.And(*constraint_list)
    
    return restrictions_dict

def construct_restriction_constraints_per_symbol(restrictions_file_path: Path | None) -> dict[str, z3.BoolRef]:
    if restrictions_file_path is None:
        return {}
    
    with open(restrictions_file_path, 'r') as f:
        restrictions = f.read()
    json_obj = json.loads(restrictions)
    
    symbol_to_restrictions = {}
    for id, restrictions_list in json_obj.items():
        assert len(restrictions_list) > 0, f"No restrictions found for {id}"
                    
        for expr_str in restrictions_list:
            # Parse expression string
            expr_str = expr_str.strip()
            
            # Match operators
            if '>=' in expr_str:
                parts = expr_str.split('>=')
                op = '>='
            elif '<=' in expr_str:
                parts = expr_str.split('<=')
                op = '<='
            elif '==' in expr_str:
                parts = expr_str.split('==')
                op = '=='
            elif '!=' in expr_str:
                parts = expr_str.split('!=')
                op = '!='
            elif '>' in expr_str:
                parts = expr_str.split('>')
                op = '>'
            elif '<' in expr_str:
                parts = expr_str.split('<')
                op = '<'
            else:
                raise ValueError(f"Unsupported operator in expression: {expr_str}")
            
            # Ensure there are left and right parts
            if len(parts) != 2:
                raise ValueError(f"Invalid expression format: {expr_str}")
                
            left = parts[0].strip()
            right = parts[1].strip()
            symbol = None
            
            # Create Z3 expressions directly in original order
            if NUMERIC_SYMBOLIC_PREFIX in expr_str:
                # Numeric variables
                if left.startswith(NUMERIC_SYMBOLIC_PREFIX):
                    symbol = left
                    z3_left = z3.Real(left)
                    z3_right = float(right)
                else:
                    symbol = right
                    z3_left = float(left)
                    z3_right = z3.Real(right)
                
                if op == '==':
                    constraint = z3_left == z3_right
                elif op == '!=':
                    constraint = z3_left != z3_right
                elif op == '>=':
                    constraint = z3_left >= z3_right
                elif op == '<=':
                    constraint = z3_left <= z3_right
                elif op == '>':
                    constraint = z3_left > z3_right
                elif op == '<':
                    constraint = z3_left < z3_right
            
            elif STRING_SYMBOLIC_PREFIX in expr_str:
                # String variables
                if left.startswith(STRING_SYMBOLIC_PREFIX):
                    symbol = left
                    z3_left = z3.String(left)
                    z3_right = z3.StringVal(right)
                else:
                    symbol = right
                    z3_left = z3.StringVal(left)
                    z3_right = z3.String(right)
                
                if op == '==':
                    constraint = z3_left == z3_right
                elif op == '!=':
                    constraint = z3_left != z3_right
                else:
                    raise ValueError(f"Unsupported operator '{op}' for string variable: {expr_str}")
            
            else:
                raise ValueError(f"No threshold variable found in expression: {expr_str}")
            
            symbol_to_restrictions.setdefault(symbol, []).append(constraint)
    
    return {k : z3.And(*v) for k, v in symbol_to_restrictions.items()}
        
        