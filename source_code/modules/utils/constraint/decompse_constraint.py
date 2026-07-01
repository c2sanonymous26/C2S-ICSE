import ast
import copy
from pathlib import Path
from lxml import etree as ET
from typing import Any, Union

from ..bfunc.load_bfunc import get_bfunc_nodes

# Types
_CompExpr = tuple[ast.expr, ast.cmpop, ast.expr]
_LogicStructValue = Union[_CompExpr, ast.Name, list['_LogicStruct'], '_LogicStruct']
_LogicStruct = tuple[str, '_LogicStructValue']

# Variables
_bfunc_mapping: dict[str, Union[_LogicStruct, ast.expr]] = {}
_counters: dict[str, int] = {}

def decompose(output_dir: Path, constraint_file_path: Path, bfuncs_file_path: Path) -> tuple[Path, Path]:
    try:           
        global _bfunc_mapping, _counters
        _bfunc_mapping = {}
        _counters = {}

        with open(bfuncs_file_path, 'r') as f:
            module_content = f.read()
            
        pure_nodes, n_symbolic_nodes, s_symbolic_nodes = get_bfunc_nodes(module_content)
        bfunc_nodes = list(pure_nodes.values()) + list(n_symbolic_nodes.values()) + list(s_symbolic_nodes.values())
        for node in bfunc_nodes:
            original_id = '_'.join(node.name.split('_')[1:])
            _process_bfunc(node, original_id)
        
        try:
            parser = ET.XMLParser(remove_comments=True, remove_blank_text=True)
            tree = ET.parse(constraint_file_path, parser=parser)
        except ET.XMLSyntaxError as e:
            raise ValueError(f"Invalid XML syntax in {constraint_file_path}: {e}")    
        root = tree.getroot()
        _update_xml_bfuncs(root)
        
        output_path = output_dir / f"{constraint_file_path.stem}_decomposed{constraint_file_path.suffix}"
        ET.indent(tree, space="  ") 
        tree.write(output_path, encoding='utf-8', xml_declaration=True)
        
        new_bfuncs_path = output_dir / f"{bfuncs_file_path.stem}_decomposed{bfuncs_file_path.suffix}"
        _generate_new_bfuncs(bfuncs_file_path, new_bfuncs_path)

        return output_path, new_bfuncs_path 
    
    except Exception as e:
        raise RuntimeError(f"Error during decomposition: {str(e)}") from e

def _process_bfunc(node: ast.FunctionDef, original_id: str) -> None:
    """Process a single bfunc function"""
                
    return_stmts = [n for n in node.body if isinstance(n, ast.Return)]
    if not return_stmts:
        raise ValueError(f"No return statement found in bfunc_{original_id}")
    if len(return_stmts) > 1:
        raise ValueError(f"Multiple return statements found in bfunc_{original_id}")
    
    return_value = return_stmts[0].value
    assert return_value is not None, f"Return statement in bfunc_{original_id} has no value"
    
    structure = _extract_logic_structure(return_value)
    _bfunc_mapping[original_id] = structure

def _extract_logic_structure(node: ast.AST) -> _LogicStruct:
    """Extract logical structure from AST node"""
    try:
        if isinstance(node, ast.BoolOp):
            op_type = 'and' if isinstance(node.op, ast.And) else 'or'
            sub_structures = [_extract_logic_structure(value) for value in node.values]
            return (op_type, sub_structures)
        elif isinstance(node, ast.Call):
            assert isinstance(node.func, ast.Name), f'Expected ast.Name, but got {type(node.func)}'
            assert node.func.id == 'implies', f'Expected call to implies, but got {node.func.id}'
            sub_structures = [_extract_logic_structure(node.args[0]), _extract_logic_structure(node.args[1])]
            return ('implies', sub_structures)
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
            return ('not', _extract_logic_structure(node.operand))
        elif isinstance(node, ast.Compare):
            comparisons = []
            left = node.left
            for op, comparator in zip(node.ops, node.comparators):
                comparisons.append(('compare', (left, op, comparator)))
                left = comparator
            if len(comparisons) == 1:
                return comparisons[0]
            return ('and', comparisons)
        elif isinstance(node, ast.Name):
            return ('boolval', node)
        else:
            raise ValueError(f"Only comparison operations are supported, got: {type(node)}")
            
    except Exception as e:
        raise ValueError(f"Failed to extract logic structure: {str(e)}") from e

def _update_xml_bfuncs(root: ET._Element) -> None:
    """Update bfunc nodes in XML"""
    try:
        parent_map = {c: p for p in root.iter() for c in p}
        # Pre-generate XML structure for each bfunc that needs to be decomposed, ensuring bfuncs with the same ID use the same decomposition result
        decomposed_xml_cache = {}
        
        # First pass: pre-generate decomposition structure for each unique bfunc ID
        unique_bfunc_ids = set()
        for elem in root.findall('.//bfunc'):
            original_id = elem.get('id')
            if original_id and original_id in _bfunc_mapping:
                structure = _bfunc_mapping[original_id]
                unique_bfunc_ids.add(original_id)
        
        # Generate decomposition structure for each unique bfunc ID
        for original_id in unique_bfunc_ids:
            structure = _bfunc_mapping[original_id]
            # Reset counter to ensure decomposition for each bfunc ID starts from c1
            _counters[original_id] = 0
            decomposed_xml_cache[original_id] = _create_xml_structure(structure, original_id)
        
        # Second pass: replace bfunc elements in XML
        for elem in root.findall('.//bfunc'):
            original_id = elem.get('id')
            if not original_id:
                raise ValueError("Found bfunc element without id attribute")
                
            if original_id in decomposed_xml_cache:
                # Use cached decomposition structure, but need deep copy to avoid XML tree structure issues
                new_elem = copy.deepcopy(decomposed_xml_cache[original_id])
                
                parent = parent_map[elem]
                if parent is None:
                    raise ValueError(f"bfunc element with id {original_id} has no parent")
                parent.replace(elem, new_elem)

    except Exception as e:
        raise RuntimeError(f"Error updating XML: {str(e)}") from e

def _traverse_structure(structure: _LogicStruct, original_id: str, visitor: callable) -> Any:
    """Generic function for traversing logical structures
    The visitor function receives (op_type, content, original_id) as parameters and returns processing results
    """

    try:
        op_type, content = structure
        
        if op_type in ('and', 'or'):
            assert isinstance(content, list) and len(content) > 0, \
                f"Expected content to be a list for {op_type}, got {type(content)}"
            first = content[0]
            rest = content[1:]
            first_result = _traverse_structure(first, original_id, visitor)
            if len(rest) == 1:
                rest_result = _traverse_structure(rest[0], original_id, visitor)
            else:
                rest_result = _traverse_structure((op_type, rest), original_id, visitor)
            return visitor(op_type, (first_result, rest_result), original_id)
        elif op_type == 'implies':
            assert isinstance(content, list) and len(content) == 2, \
                f"Expected content to be a list of two elements for implies, got {type(content)}"
            result = (
                _traverse_structure(content[0], original_id, visitor), 
                _traverse_structure(content[1], original_id, visitor)
            )
            return visitor('implies', result, original_id)
        elif op_type == 'not':
            
            return visitor('not', 
                        _traverse_structure(content, original_id, visitor), original_id # type: ignore
            )  
        elif op_type in ('compare', 'boolval'):
            if original_id not in _counters:
                _counters[original_id] = 0
            _counters[original_id] += 1
            return visitor(op_type, content, original_id)
        else:
            raise ValueError(f"Unknown operation type: {op_type}")
            
    except Exception as e:
        raise ValueError(f"Error traversing structure: {str(e)}") from e

def _create_xml_structure(structure: _LogicStruct, original_id: str) -> ET._Element:
    """Create XML element based on logical structure"""
    def xml_visitor(op_type: str, 
                    content: Union[_CompExpr, ET._Element, tuple[ET._Element, ET._Element]], 
                    original_id: str) -> ET._Element:
        
        if op_type in ('and', 'or'):
            elem = ET.Element(op_type, attrib={}, nsmap=None)
            assert isinstance(content, tuple) and len(content) == 2, \
                f"Expected content to be a tuple of two elements for {op_type}, got {type(content)}"
            elem.append(content[0])
            elem.append(content[1])
            return elem
        elif op_type == 'implies':
            elem = ET.Element('implies', attrib={}, nsmap=None)
            assert isinstance(content, tuple) and len(content) == 2, \
                f"Expected content to be a tuple of two elements for implies, got {type(content)}"
            elem.append(content[0])
            elem.append(content[1])
            return elem
        elif op_type == 'not':
            elem = ET.Element('not', attrib={}, nsmap=None)
            elem.append(content)
            return elem
        elif op_type in ('compare', 'boolval'):
            new_id = f"{original_id}_c{_counters[original_id]}"
            bfunc_elem = ET.Element('bfunc', attrib={'id': new_id}, nsmap=None)
            return bfunc_elem
        else:
            raise ValueError(f"Unknown operation type in xml_visitor: {op_type}")

    return _traverse_structure(structure, original_id, xml_visitor)

def _generate_new_bfuncs(original_path: Path, output_path: Path) -> None:
    """Generate new bfuncs.py file"""

    try:
        new_bfuncs = {}

        def collect_visitor(op_type: str, 
                            content: Union[_CompExpr, _LogicStruct], 
                            original_id: str) -> _LogicStruct:
            if op_type == 'compare':
                new_id = f"{original_id}_c{_counters[original_id]}"
                left, op, right = content
                expr_node = ast.Compare(left=left, ops=[op], comparators=[right])
                new_bfuncs[new_id] = (original_id, expr_node)
            elif op_type == 'boolval':
                new_id = f"{original_id}_c{_counters[original_id]}"
                new_bfuncs[new_id] = (original_id, content)
            return (op_type, content)
        
        # Collect expressions from functions that need to be split
        for original_id, structure in _bfunc_mapping.items():
            _counters[original_id] = 0
            _traverse_structure(structure, original_id, collect_visitor)
        
        # Copy import statements from original file
        imports = []
        with open(original_path, 'r') as f:
            tree = ast.parse(f.read())
            for node in tree.body:
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    imports.append(ast.unparse(node))
        
        # Generate new file
        with open(output_path, 'w') as f:
            # Write import statements
            for imp in imports:
                f.write(f"{imp}\n")
            f.write("\n")
            
            # Write new split functions
            for new_id, (original_id, expr_node) in sorted(new_bfuncs.items()):
                f.write(f"def bfunc_{new_id}(var_bindings: dict[str, dict[str, Any]]) -> bool:\n")
                f.write(f"    return {ast.unparse(expr_node)}\n\n")
                
    except Exception as e:
        raise RuntimeError(f"Error generating new bfuncs: {str(e)}") from e
