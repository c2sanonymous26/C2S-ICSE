import re
import tomli
from agno.agent import Agent
from pathlib import Path
from jinja2 import Environment
from typing import Any
from lark import Lark, UnexpectedToken, UnexpectedCharacters, Tree

from ...utils import log_info, log_warning, CONTEXT_DEFINITIONS_FILE_NAME
from .. import (
    LOGGER_NAME,
    BODY_GRAMMAR, 
    BG_LOGIC_PRODS, 
    BG_STR_CMP_PRODS, 
    BG_STR_CMP_TERMINALS, 
    BG_NUM_CMP_PRODS, 
    BG_NUM_CMP_TERMINALS
)
from ..statistics import ImplStatistics
from . import MAX_TRY_TIMES
from .responses import ( 
    StructureAndSignatures,
    BfuncImplementationNoCheck,
    BfuncImplementationWithCheck,
    BfuncSignature, 
    BfuncBody
)
from .prompts import (
    PHASE3_USER_PROMPT_TEMPLATE,
    PHASE3_NO_SEMANTIC_CHECK_RESPONSE_PROMPT,
    PHASE3_SEMANTIC_CHECK_RESPONSE_PROMPT,
    PHASE3_SEMANTIC_CHECK_FIELD_MUTUALLY_EXCLUSIVE_PROMPT,
    PHASE3_CONSISTENCY_ERROR_PROMPT_TEMPLATE,
    PHASE3_SYNTAX_ERROR_PROMPT_TEMPLATE,
    PHASE3_UNIT_ERROR_PROMPT_TEMPLATE,
    STRUCTURED_OUTPUT_ERROR_PROMPT
)
from .UnitAnalyzer import UnitAnalyzer
from .errors import ImplSyntaxError, ImplSemanticError

def invent_impl_without_semantic_validation(
    agno_agent: Agent, 
    input_dir: Path, 
    few_shots: list[dict[str, Any]],
    statistics: ImplStatistics
) -> BfuncImplementationNoCheck:
    
    log_info(LOGGER_NAME, "Implementations invention (no semantic check) starts", center=True, symbol="~")
    
    # Get field names
    str_field_names, num_field_names = _get_field_names(input_dir)
    str_field_name_regex = '|'.join(re.escape(name) for name in sorted(str_field_names, key=len, reverse=True))
    num_field_name_regex = '|'.join(re.escape(name) for name in sorted(num_field_names, key=len, reverse=True))
    
    # Initialize BfuncBodyParser
    grammar = BODY_GRAMMAR.format(
        str_field_name_regex=str_field_name_regex,
        num_field_name_regex=num_field_name_regex
    )
    parser = Lark(grammar, parser='earley', propagate_positions=True, ambiguity='resolve')

    # Get user prompt
    user_prompt = _render_user_prompt(str_field_name_regex, num_field_name_regex, False, few_shots)

    # Iterative generation
    bfunc_implementations = None
    try_times = 0
    while try_times < MAX_TRY_TIMES:
        # Update attempt count
        statistics.llm_call_count += 1
        
        # Update and call agent
        agno_agent.response_model = BfuncImplementationNoCheck
        response = agno_agent.run(user_prompt, stream=False)
        bfunc_implementations = response.content
    
        # Check conversion result
        if not isinstance(bfunc_implementations, BfuncImplementationNoCheck):
            try_times += 1
            user_prompt = STRUCTURED_OUTPUT_ERROR_PROMPT
            continue
        
        if bfunc_implementations.bodies is None:
            log_warning(LOGGER_NAME, "Implementations invention (no feedback) returns empty result.")
            return None

        # Check syntax of each body
        success, errors_or_trees = _check_syntax(parser, bfunc_implementations.bodies)
        if success:
            break
        else:
            # Record syntax error count
            statistics.syntax_error_count += 1
            
            bfunc_implementations = None
            try_times += 1
            user_prompt = _render_syntax_error_prompt(errors_or_trees, False)
            continue

    log_info(LOGGER_NAME, "Implementations invention (no semantic check) done", center=True, symbol="~", newlines=2)
    return bfunc_implementations

def invent_impl_with_semantic_validation(
    agno_agent: Agent, 
    input_dir: Path, 
    few_shots: list[dict[str, Any]],
    rollback_times: int,
    structure_and_signatures: StructureAndSignatures,
    statistics: ImplStatistics
) -> BfuncImplementationWithCheck | str | None:
    log_info(LOGGER_NAME, f"Implementations invention (with semantic check) (rollback {rollback_times} times) starts", center=True, symbol="~")
    
    # Get field names
    str_field_names, num_field_names = _get_field_names(input_dir)
    str_field_name_regex = '|'.join(re.escape(name) for name in sorted(str_field_names, key=len, reverse=True))
    num_field_name_regex = '|'.join(re.escape(name) for name in sorted(num_field_names, key=len, reverse=True))

    # Initialize BfuncBodyParser
    grammar = BODY_GRAMMAR.format(
        str_field_name_regex=str_field_name_regex,
        num_field_name_regex=num_field_name_regex
    )
    parser = Lark(grammar, parser='earley', propagate_positions=True, ambiguity='resolve')

    # Initialize UnitAnalyzer
    analyzer = UnitAnalyzer(input_dir)
    
    # Get user prompt
    user_prompt = _render_user_prompt(str_field_name_regex, num_field_name_regex, True, few_shots)
    
    # Iterative generation
    bfunc_implementations = None
    try_times = 0
    while try_times < MAX_TRY_TIMES:
        # Update attempt count
        statistics.llm_call_count += 1
        
        # Update and call agent
        agno_agent.response_model = BfuncImplementationWithCheck
        response = agno_agent.run(user_prompt, stream=False)
        instance = response.content
        
        # Check conversion result
        if not isinstance(instance, BfuncImplementationWithCheck):
            try_times += 1
            user_prompt = STRUCTURED_OUTPUT_ERROR_PROMPT
            continue
        
        if (instance.reason is None and instance.bodies is None) \
            or (instance.reason is not None and instance.bodies is not None):
            try_times += 1
            user_prompt = PHASE3_SEMANTIC_CHECK_FIELD_MUTUALLY_EXCLUSIVE_PROMPT
            continue
        
        if instance.reason is not None:
            return instance.reason
        bfunc_implementations = instance
            
        # Check syntax of each body
        success, errors_or_trees = _check_syntax(parser, bfunc_implementations.bodies)
        if success:
            pass
        else:
            # Record syntax error count
            statistics.syntax_error_count += 1
            
            bfunc_implementations = None
            try_times += 1
            user_prompt = _render_syntax_error_prompt(errors_or_trees, True)
            continue
        
        # Check semantics of each body
        success, errors, passed_check_num = _check_semantics(
            structure_and_signatures.signatures,
            bfunc_implementations.bodies,
            analyzer,
            agno_agent,
            errors_or_trees
        )
        if success:
            break
        else:
            # Record semantic error count
            if passed_check_num == 0:
                statistics.consistency_error_count += 1
            elif passed_check_num == 1:
                statistics.unit_error_count += 1
            
            bfunc_implementations = None
            try_times += 1
            user_prompt = _render_semantic_error_prompt(errors, passed_check_num)
            continue
        
    log_info(LOGGER_NAME, f"Implementations invention (with semantic check) (rollback {rollback_times} times) done", center=True, symbol="~", newlines=2)
    return bfunc_implementations

def _get_field_names(input_dir: Path) -> tuple[list[str], list[str]]:
    str_field_names = []
    num_field_names = []

    dataset_path = input_dir / CONTEXT_DEFINITIONS_FILE_NAME
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset file {dataset_path} does not exist")
    with open(dataset_path, 'rb') as f:
        fields = tomli.load(f)['context_definitions']['fields']
        for field_name, field_info in fields.items():
            if field_info['type'] in ['int', 'float']:
                num_field_names.append(field_name)
            else:
                str_field_names.append(field_name)
                
    return str_field_names, num_field_names

def _render_user_prompt(str_field_name_regex: str, num_field_name_regex: str, semantic_validation: bool, few_shots: list[dict[str, Any]]) -> str:
    jinjia_env = Environment(trim_blocks=True, lstrip_blocks=True)
    user_prompt_template = jinjia_env.from_string(PHASE3_USER_PROMPT_TEMPLATE)
    user_prompt = user_prompt_template.render(
        bg_logic_prods=BG_LOGIC_PRODS,
        bg_str_cmp_prods=BG_STR_CMP_PRODS,
        bg_str_cmp_terminals=BG_STR_CMP_TERMINALS.format(str_field_name_regex=str_field_name_regex),
        bg_num_cmp_prods=BG_NUM_CMP_PRODS,
        bg_num_cmp_terminals=BG_NUM_CMP_TERMINALS.format(num_field_name_regex=num_field_name_regex),
        few_shots=few_shots,
        response_prompt = PHASE3_SEMANTIC_CHECK_RESPONSE_PROMPT.strip() if semantic_validation else PHASE3_NO_SEMANTIC_CHECK_RESPONSE_PROMPT.strip()
    )
    return user_prompt

def _check_syntax(parser: Lark, bodies: list[BfuncBody]) -> tuple[bool, str | dict[str, Tree]]:
    
    trees = {}
    errors = []
    for body in bodies:
        try:
            tree = parser.parse(body.implementation)
            trees[body.id] = tree
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
            
            error = ImplSyntaxError(
                body.id,
                error_msg[:-1],
                e.line,
                e.column,
                e.get_context(body.implementation, span=len(body.implementation))
            )
            errors.append(str(error))
            
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
            
            error = ImplSyntaxError(
                body.id,
                error_msg[:-1],
                e.line,
                e.column,
                e.get_context(body.implementation, span=len(body.implementation))
            )
            errors.append(str(error))
        
        except Exception as e:

            error_msg = f"Error occurred during parsing: {str(e)}"
            error = ImplSyntaxError(
                body.id,
                error_msg,
                1,
                1,
                body.implementation
            )
            errors.append(str(error))
    
    if errors:
        return False, "\n".join(errors)
    else:
        return True, trees

def _render_syntax_error_prompt(error_message: str, semantic_validation: bool) -> str:
    jinjia_env = Environment(trim_blocks=True, lstrip_blocks=True)
    fix_syntax_error_prompt_template = jinjia_env.from_string(PHASE3_SYNTAX_ERROR_PROMPT_TEMPLATE)
    fix_syntax_error_prompt = fix_syntax_error_prompt_template.render(
        error_message=error_message,
        response_prompt=PHASE3_SEMANTIC_CHECK_RESPONSE_PROMPT.strip() if semantic_validation else PHASE3_NO_SEMANTIC_CHECK_RESPONSE_PROMPT.strip()
    )
    return fix_syntax_error_prompt

def _check_semantics(
    signatures: list[BfuncSignature], 
    bodies: list[BfuncBody], 
    analyzer: UnitAnalyzer, 
    agno_agent: Agent, 
    trees: dict[str, Tree]
) -> tuple[bool, str | None, int]:
        
    def _check_consistency() -> tuple[bool, str | None]:
        # Check consistency of ids
        id_from_signatures = {signature.id for signature in signatures}
        id_from_bodies = {body.id for body in bodies}
        if id_from_signatures != id_from_bodies:
            return False,  \
                ImplSemanticError(
                    f"The ids of the bfuncs in the signatures and bodies are not the same.\n" \
                    f"signatures: {id_from_signatures}\n" \
                    f"bodies: {id_from_bodies}"
                )
        
        # Check consistency of parameters
        declared_params = {signature.id: signature.parameters for signature in signatures}
        used_params = {}
        
        # Use regular expression to match parameters like v1, v2, etc.
        param_pattern = r'v\d+\.'
        for body in bodies:
            # Extract all used parameters from implementation
            found_params = list(re.findall(param_pattern, body.implementation))
            found_params = set([param[:-1] for param in found_params])
            used_params[body.id] = found_params
            
            # Check if used parameters are subset of declared parameters
            declared = set(declared_params[body.id])
            if not found_params.issubset(declared):
                return False, \
                    ImplSemanticError(
                        f"Parameters mismatch for {body.id}.\n" \
                        f"Used but not declared parameters: {found_params - declared}\n"
                    )
        
        return True, None
        
    def _check_unit() -> tuple[bool, str | None]:
        errors = []
        semantics = {sign.id: sign.semantics for sign in signatures}
        implementations = {body.id: body.implementation for body in bodies}
    
        for bfunc_id in trees.keys():
            success, error = analyzer.analyze(
                agno_agent, 
                bfunc_id,
                trees[bfunc_id], 
                semantics[bfunc_id], 
                implementations[bfunc_id]
            )
            if not success:
                errors.append(error)
        
        if errors:
            return False, "\n".join(errors)
        else:
            return True, None
        
    # Check consistency between signatures and bodies
    success, errors = _check_consistency()
    if not success:
        return False, errors, 0
    
    # Check unit
    success, errors = _check_unit()
    if not success:
        return False, errors, 1
    
    return True, None, 2
    
def _render_semantic_error_prompt(error_message: str, passed_check_num: int) -> str:
    jinjia_env = Environment(trim_blocks=True, lstrip_blocks=True)
    if passed_check_num == 0:
        consistency_error_prompt_template = jinjia_env.from_string(PHASE3_CONSISTENCY_ERROR_PROMPT_TEMPLATE)
        consistency_error_prompt = consistency_error_prompt_template.render(
            error_message=error_message,
            response_prompt=PHASE3_SEMANTIC_CHECK_RESPONSE_PROMPT.strip()
        )
        return consistency_error_prompt
    else:
        assert passed_check_num == 1, f"passed_check_num must be 1, but got {passed_check_num}"
        unit_error_prompt_template = jinjia_env.from_string(PHASE3_UNIT_ERROR_PROMPT_TEMPLATE)
        unit_error_prompt = unit_error_prompt_template.render(
            error_message=error_message,
            response_prompt=PHASE3_SEMANTIC_CHECK_RESPONSE_PROMPT.strip()
        )
        return unit_error_prompt