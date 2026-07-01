from pathlib import Path
from lark import Lark, Tree, Transformer
from lark.exceptions import LarkError
from lxml import etree as ET
import re

from ...utils import log_info, log_error
from .. import STRUCTURE_GRAMMAR, LOGGER_NAME
from . import TEMPLATE_XML_FILE_NAME


def convert_structure(semantics: str, structure: str, output_dir: Path) -> None:
            
    log_info(LOGGER_NAME, "Converting structure to xml file starts")
    
    # Initialize parser
    parser = Lark(STRUCTURE_GRAMMAR, parser='earley', propagate_positions=True, ambiguity='resolve')
    
    # Parse structure
    tree = _parse_structure(parser, structure)
    
    # Convert to XML file
    xml_file_path =_convert_tree_into_xml(semantics, tree, output_dir)
    
    log_info(LOGGER_NAME, f"Structure xml file saved to {xml_file_path}")
    log_info(LOGGER_NAME, "Converting structure to xml file done")
    
def _parse_structure(parser: Lark, structure: str) -> Tree:
    try:
        class StructureTransformer(Transformer):
            def structure(self, items):
                return items[0]
            
            def prod_structure_expr(self, items):
                return items[0]
            
            def prod_or_expr(self, items):
                return items[0]
            
            def prod_and_expr(self, items):
                return items[0]

            def prod_not_expr(self, items):
                return items[0]
            
            def prod_atom_expr(self, items):
                return items[0]

            def prod_paren(self, items):
                return items[0]

            def prod_bfunc(self, items):
                return items[0]

        tree = parser.parse(structure)
        transformer = StructureTransformer()
        tree = transformer.transform(tree)
        return tree
    except LarkError as e:
        log_error(LOGGER_NAME, f"Failed to parse structure: {str(e)}")
        raise

def _convert_tree_into_xml(semantics: str, tree: Tree, output_dir: Path) -> Path:
    
    # Create comment and formula section strings
    xml_declaration = '<?xml version=\'1.0\' encoding=\'utf-8\'?>\n\n'
    comment_str = f'<!--Template semantics\n{semantics}\n-->\n'
    
    # Create formula xml tree
    formula = ET.Element("formula")
    _process_tree_node(tree, formula)
    
    # Generate XML string for formula section
    formula_xml = ET.tostring(
        formula, 
        pretty_print=True, 
        encoding='utf-8'
    ).decode('utf-8')
    
    # Remove possible XML declaration
    formula_xml = re.sub(r'<\?xml[^>]+\?>\s*', '', formula_xml)
    
    # Combine final XML
    xml_str = f"{xml_declaration}{comment_str}{formula_xml}"
    
    # Save XML file
    output_file = output_dir / TEMPLATE_XML_FILE_NAME
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_str)
    
    return output_file

def _process_tree_node(node: Tree, parent_element: ET.Element) -> None:

    if node.data == 'prod_forall':
        # Process forall structure
        var_node = node.children[0]
        formula_node = node.children[1]
        
        forall_element = ET.SubElement(parent_element, "forall")
        var_name = f"v{var_node.children[0]}"
        forall_element.set("var", var_name)
        forall_element.set("in", "ctx1")  # Default context name
        
        _process_tree_node(formula_node, forall_element)
        
    elif node.data == 'prod_exists':
        # Process exists structure
        var_node = node.children[0]
        formula_node = node.children[1]
        
        exists_element = ET.SubElement(parent_element, "exists")
        var_name = f"v{var_node.children[0]}"
        exists_element.set("var", var_name)
        exists_element.set("in", "ctx1")  # Default context name
        
        _process_tree_node(formula_node, exists_element)
        
    elif node.data == 'prod_and':
        # Process and structure
        left_node = node.children[0]
        right_node = node.children[1]
        
        and_element = ET.SubElement(parent_element, "and")
        _process_tree_node(left_node, and_element)
        _process_tree_node(right_node, and_element)
        
    elif node.data == 'prod_or':
        # Process or structure
        left_node = node.children[0]
        right_node = node.children[1]
        
        or_element = ET.SubElement(parent_element, "or")
        _process_tree_node(left_node, or_element)
        _process_tree_node(right_node, or_element)
        
    elif node.data == 'prod_implies':
        # Process implies structure
        left_node = node.children[0]
        right_node = node.children[1]
        
        implies_element = ET.SubElement(parent_element, "implies")
        _process_tree_node(left_node, implies_element)
        _process_tree_node(right_node, implies_element)
        
    elif node.data == 'prod_not':
        # Process not structure
        formula_node = node.children[0]
        
        not_element = ET.SubElement(parent_element, "not")
        _process_tree_node(formula_node, not_element)
        
    elif node.data == 'prod_bfunc_signature':
        # Process bfunc function signature
        bfunc_id = node.children[0].value
        
        bfunc_element = ET.SubElement(parent_element, "bfunc")
        bfunc_element.set("id", bfunc_id)
        
    else:
        raise ValueError(f"Unknown node data: {node.data}")
    
