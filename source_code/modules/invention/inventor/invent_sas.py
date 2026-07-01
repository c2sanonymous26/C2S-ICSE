from agno.agent import Agent
from lark import Lark, UnexpectedToken, UnexpectedCharacters, Transformer, Tree
from lark.lexer import Token
from jinja2 import Environment
from typing import Any

from ...utils import log_info, log_warning
from .. import STRUCTURE_GRAMMAR, LOGGER_NAME
from ..statistics import SasStatistics
from . import MAX_TRY_TIMES
from .responses import (
    StructureAndSignatures, 
    BfuncSignature
)
from .prompts import (
    PHASE2_USER_PROMPT_TEMPLATE,
    PHASE2_ROLLBACK_PROMPT_TEMPLATE,
    PHASE2_SYNTAX_ERROR_PROMPT_TEMPLATE,
    PHASE2_SEMANTIC_ERROR_PROMPT_TEMPLATE,
    STRUCTURED_OUTPUT_ERROR_PROMPT
)
from .errors import SasSyntaxError, SasSemanticError

def invent_sas_without_semantic_validation(
    agno_agent: Agent, 
    few_shots: list[dict[str, Any]], 
    statistics: SasStatistics
) -> StructureAndSignatures | None:
    
    log_info(LOGGER_NAME, "Structure and signatures invention (no semantic check) starts", center=True, symbol="~")
    
    # Initialize StructureParser
    parser = Lark(STRUCTURE_GRAMMAR, parser='earley', propagate_positions=True, ambiguity='resolve')
    
    # Get user prompt
    user_prompt = _render_user_prompt(few_shots)
    
    # Iterative generation
    structure_and_signatures = None
    try_times = 0
    while try_times < MAX_TRY_TIMES:
        # Update attempt count
        statistics.llm_call_count += 1
        
        # Update and call agent
        agno_agent.response_model = StructureAndSignatures
        response = agno_agent.run(user_prompt, stream=False)
        structure_and_signatures = response.content
    
        # Check conversion result
        if not isinstance(structure_and_signatures, StructureAndSignatures):
            structure_and_signatures = None
            try_times += 1
            user_prompt = STRUCTURED_OUTPUT_ERROR_PROMPT
            continue
        
        if structure_and_signatures.structure is None or structure_and_signatures.signatures is None:
            log_warning(LOGGER_NAME, "Structure and signatures invention returns empty result.")
            return None
        
        # Check structure
        success, error_or_tree = _check_syntax(parser, structure_and_signatures.structure)
        if success:
            break
        else:
            # Record syntax error count
            statistics.syntax_error_count += 1
            
            structure_and_signatures = None
            try_times += 1
            user_prompt = _render_syntax_error_prompt(error_or_tree)
            continue
    
    log_info(LOGGER_NAME, "Structure and signatures invention (no semantic check) done", center=True, symbol="~", newlines=2)
    return structure_and_signatures

def invent_sas_with_semantic_validation(
    agno_agent: Agent, 
    few_shots: list[dict[str, Any]], 
    rollback_times: int, 
    rollback_reason: str,
    statistics: SasStatistics
) -> StructureAndSignatures | None:
    
    log_info(LOGGER_NAME, f"Structure and signatures invention (with semantic check) (rollback {rollback_times} times) starts", center=True, symbol="~")
    
    # Get user prompt
    if rollback_times > 0:
        user_prompt = _render_rollback_prompt(rollback_reason)
    else:
        user_prompt = _render_user_prompt(few_shots)
        
    # Initialize StructureParser
    parser = Lark(STRUCTURE_GRAMMAR, parser='earley', propagate_positions=True, ambiguity='resolve')
    
    # Iterative generation
    structure_and_signatures = None
    try_times = 0
    while try_times < MAX_TRY_TIMES:  
        # Update attempt count
        statistics.llm_call_count += 1
        
        # Update and call agent
        agno_agent.response_model = StructureAndSignatures      
        response = agno_agent.run(user_prompt, stream=False)
        structure_and_signatures = response.content
        
        # Check conversion result
        if not isinstance(structure_and_signatures, StructureAndSignatures):
            structure_and_signatures = None
            try_times += 1
            user_prompt = STRUCTURED_OUTPUT_ERROR_PROMPT
            continue
        
        if structure_and_signatures.structure is None or structure_and_signatures.signatures is None:
            log_warning(LOGGER_NAME, "Structure and signatures invention returns empty result.")
            return None

        # Check structure
        success, error_or_tree = _check_syntax(parser, structure_and_signatures.structure)
        if success:
            pass
        else:
            # Record syntax error count
            statistics.syntax_error_count += 1
            
            structure_and_signatures = None
            try_times += 1
            user_prompt = _render_syntax_error_prompt(error_or_tree)
            continue
        
        # Check bfuncs signatures
        success, error = _check_semantics(error_or_tree, structure_and_signatures.signatures)
        if success:
            break
        else:
            # Record semantic error count
            statistics.semantic_error_count += 1
            
            structure_and_signatures = None
            try_times += 1
            user_prompt = _render_semantics_error_prompt(error)
    
    log_info(LOGGER_NAME, f"Structure and signatures invention (with semantic check) (rollback {rollback_times} times) done", center=True, symbol="~", newlines=2)
    return structure_and_signatures

def _render_user_prompt(few_shots: list[dict[str, Any]]) -> str:
    jinjia_env = Environment(trim_blocks=True, lstrip_blocks=True)
    user_prompt_template = jinjia_env.from_string(PHASE2_USER_PROMPT_TEMPLATE)
    user_prompt = user_prompt_template.render(
        structure_grammar=STRUCTURE_GRAMMAR,
        few_shots=few_shots
    )
    return user_prompt

def _render_rollback_prompt(rollback_reason: str) -> str:
    jinjia_env = Environment(trim_blocks=True, lstrip_blocks=True)
    rollback_prompt_template = jinjia_env.from_string(PHASE2_ROLLBACK_PROMPT_TEMPLATE)
    rollback_prompt = rollback_prompt_template.render(
        rollback_reason=rollback_reason
    )
    return rollback_prompt

def _check_syntax(parser: Lark, structure: str) -> tuple[bool, str | Tree]:
    
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

    try:
        tree = parser.parse(structure)
        transformer = StructureTransformer()
        tree = transformer.transform(tree)
        return True, tree
    except UnexpectedToken as e:
        expected = ", ".join(e.expected)
        
        # Get more detailed token information
        token_info = f"'{e.token}'"
        if hasattr(e.token, 'type'):
            token_info += f" (type: {e.token.type})"
        if hasattr(e.token, 'value'):
            token_info += f" (value: '{e.token.value}')"
        
        error_msg = f"Expected: {expected}\nFound: {token_info}\n"
        if hasattr(e, 'token_history') and e.token_history:
            error_msg += f"Parsed: {' -> '.join(str(t) for t in e.token_history)}\n"
        
        error = SasSyntaxError(
            error_msg[:-1],
            e.line,
            e.column,
            e.get_context(structure, span=len(structure))
        )
        return False, str(error)
        
    except UnexpectedCharacters as e:
        
        error_msg = f"Unexpected character: '{e.char}'\n"
        if hasattr(e, 'token_history') and e.token_history:
            error_msg += f"Parsed: {' -> '.join(str(t) for t in e.token_history)}\n"
        
        if hasattr(e, 'allowed') and e.allowed:
            error_msg += f"Allowed here: {', '.join(e.allowed)}\n"
        
        if hasattr(e, 'interactive_parser') and e.interactive_parser:
            interactive_parser = e.interactive_parser
            if hasattr(interactive_parser, 'state_stack') and interactive_parser.state_stack:
                states = [str(s) for s in interactive_parser.state_stack]
                error_msg += f"Parse stack: {' -> '.join(states)}\n"
        
        error = SasSyntaxError(
            error_msg[:-1],
            e.line,
            e.column,
            e.get_context(structure, span=len(structure))
        )
        return False, str(error)
    
    except Exception as e:

        error_msg = f"Error occurred during parsing: {str(e)}"
        error = SasSyntaxError(
            error_msg,
            1,
            1,
            structure
        )
        
        return False, str(error)
        
def _render_syntax_error_prompt(error_msg: str) -> str:
    jinjia_env = Environment(trim_blocks=True, lstrip_blocks=True)
    fix_error_prompt_template = jinjia_env.from_string(PHASE2_SYNTAX_ERROR_PROMPT_TEMPLATE)
    fix_error_prompt = fix_error_prompt_template.render(
        error_message=error_msg
    )
    return fix_error_prompt        

def _check_semantics(tree: Tree, signatures: list[BfuncSignature]) -> tuple[bool, str | None]:
        
    def _extract_variable_name(node: Tree) -> str:
        """Extract variable name from variable node"""
        assert node.data == 'prod_variable'
        assert len(node.children) == 1 and isinstance(node.children[0], Token)
        return f"v{node.children[0].value}"
    
    def _check_param_validity_in_tree(tree: Tree) -> tuple[bool, str | None]:
        """Check parameter validity in parse tree"""
        def _traverse(node: Tree, current_scope: set[str]) -> tuple[bool, str | None]:
            if node.data == 'prod_bfunc_signature':
                assert len(node.children) == 2
                assert isinstance(node.children[0], Token)
                assert node.children[1].data == 'prod_variable_list'
                
                bfunc_id = f"bfunc{node.children[0].value}"
                
                used_vars = set()
                for var_node in node.children[1].children:
                    used_vars.add(_extract_variable_name(var_node))
                
                invalid_vars = used_vars - current_scope
                if invalid_vars:
                    return False, SasSemanticError(f"bfunc {bfunc_id} uses variables {invalid_vars} that are not defined outside of the bfunc")
                return True, None
                
            elif node.data in ['prod_forall', 'prod_exists']:
                assert len(node.children) == 2
                assert isinstance(node.children[0], Tree)
                assert isinstance(node.children[1], Tree)
                
                var_node = node.children[0]
                structure_node = node.children[1]
                
                new_scope = current_scope.copy()
                new_scope.add(_extract_variable_name(var_node))
                
                return _traverse(structure_node, new_scope)
                    
            elif node.data in ['prod_and', 'prod_or', 'prod_implies']:
                assert len(node.children) == 2
                assert isinstance(node.children[0], Tree)
                assert isinstance(node.children[1], Tree)
                
                left_node, right_node = node.children[0], node.children[1]
                
                left, left_msg = _traverse(left_node, current_scope)
                if not left:
                    return False, left_msg
                
                right, right_msg = _traverse(right_node, current_scope)
                if not right:
                    return False, right_msg
            
                return True, None
                
            elif node.data == 'prod_not':
                assert len(node.children) == 1
                assert isinstance(node.children[0], Tree)
                
                structure_node = node.children[0]
                return _traverse(structure_node, current_scope)
                
            else:
                raise ValueError(f"Unexpected node type: {node.data}")
        
        return _traverse(tree, set())
    
    def _get_id_param_map_from_tree(tree: Tree) -> dict[str, list[str]]:
        """Extract bfunc ID and parameter mapping from parse tree"""
        id_param_map: dict[str, list[str]] = {}
        
        def _traverse(node: Tree) -> None:
            if node.data == 'prod_bfunc_signature':
                assert len(node.children) == 2
                assert isinstance(node.children[0], Token)
                assert node.children[1].data == 'prod_variable_list'
                
                bfunc_id = f"bfunc{node.children[0].value}"
                
                variables = []
                for var_node in node.children[1].children:
                    variables.append(_extract_variable_name(var_node))
                
                id_param_map[bfunc_id] = variables
            
            # For all nodes, traverse their child nodes
            for child in node.children:
                if isinstance(child, Tree):
                    _traverse(child)
        
        _traverse(tree)
        return id_param_map
    
    def _get_id_param_map_from_signatures() -> dict[str, list[str]]:
        id_param_map: dict[str, list[str]] = {}
        for signature in signatures:
            id_param_map[signature.id] = signature.parameters
        return id_param_map
    
    # Check parameter validity
    ast_param_validity, ast_param_validity_msg = _check_param_validity_in_tree(tree)
    if not ast_param_validity:
        return False, ast_param_validity_msg
    
    # Get ID-parameter mapping and compare
    map_from_tree = _get_id_param_map_from_tree(tree)
    map_from_signatures = _get_id_param_map_from_signatures()

    if map_from_tree.keys() != map_from_signatures.keys():
        return False, SasSemanticError(
            f"The bfuncs in the structure are not equal to the bfuncs in the signatures\n"
            f"structure: {map_from_tree}\n"
            f"signatures: {map_from_signatures}"
        )
    
    for tree_bfunc_id, tree_bfunc_params in map_from_tree.items():
        if tree_bfunc_params != map_from_signatures[tree_bfunc_id]:
            return False, SasSemanticError(
                f"The parameters of bfunc {tree_bfunc_id} in the structure are not equal to the parameters in the signatures\n"
                f"structure: {tree_bfunc_params}\n"
                f"signatures: {map_from_signatures[tree_bfunc_id]}"
            )
    
    return True, None
        
def _render_semantics_error_prompt(error_msg: str) -> str:
    jinjia_env = Environment(trim_blocks=True, lstrip_blocks=True)
    fix_error_prompt_template = jinjia_env.from_string(PHASE2_SEMANTIC_ERROR_PROMPT_TEMPLATE)
    fix_error_prompt = fix_error_prompt_template.render(
        error_message=error_msg
    )
    return fix_error_prompt