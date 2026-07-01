from agno.agent import Agent
from pathlib import Path
from typing import Any
import tomli
import json
from jinja2 import Environment
import os
import random
from sentence_transformers import SentenceTransformer, util

from ...utils import (
    log_info, log_warning,
    SCENARIO_FILE_NAME, CONTEXT_DEFINITIONS_FILE_NAME, SCOPES_DIR_NAME, SCOPE_FILE_NAME
)
from .. import LOGGER_NAME
from ..statistics import IasStatistics
from . import TEMPLATE_JSON_FILE_NAME, TEMPLATE_DIR_PREFIX, MAX_TRY_TIMES
from .responses import IntentAndSemantics
from .prompts import (
    PHASE1_USER_PROMPT_TEMPLATE_SCOPE,
    STRUCTURED_OUTPUT_ERROR_PROMPT,
    PHASE1_DUPLICATE_ERROR_PROMPT
)

sim_model = None

def invent_intent_and_semantics(
    agno_agent: Agent, 
    current_index: int, 
    input_dir: Path, 
    output_dir: Path, 
    scope: str,
    existing_dirs: list[Path] | None,
    few_shots: list[dict[str, Any]],
    similarity_check: bool,
    statistics: IasStatistics
) -> IntentAndSemantics | None:
    
    log_info(LOGGER_NAME, "Intent and semantics generation starts", center=True, symbol="~")
    
    # Get user prompt
    user_prompt, existing_template_semantics = _render_user_prompt(
        current_index,
        input_dir,
        output_dir,
        scope,
        existing_dirs,
        few_shots
    )
    
    ias = None
    try_times = 0
    while try_times < MAX_TRY_TIMES:
        # Update attempt count
        statistics.llm_call_count += 1
        
        # Update and call agent
        agno_agent.response_model = IntentAndSemantics
        response = agno_agent.run(user_prompt, stream=False)
        ias = response.content
        
        # Check conversion result
        if not isinstance(ias, IntentAndSemantics):
            ias = None
            try_times += 1
            user_prompt = STRUCTURED_OUTPUT_ERROR_PROMPT
            continue
        
        # Check similarity
        if similarity_check:
            similar, existing_semantics = _check_similarity(ias.semantics, existing_template_semantics)
            if not similar:
                break
            else:
                # Record semantic duplicate count
                statistics.semantic_duplicate_count += 1
                
                ias = None
                try_times += 1
                user_prompt = _render_duplicate_semantics_prompt(existing_semantics)
        else:
            break
    
    log_info(LOGGER_NAME, "Intent and semantics generation done", center=True, symbol="~", newlines=2)
    return ias

def _init_sim_model():
    global sim_model
    sim_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def _check_similarity(semantics: str, existing_template_semantics: list[str]) -> tuple[bool, str | None]:
    assert sim_model is not None, "sim_model is not initialized"
    
    for existing_semantics in existing_template_semantics:
        common_prefix = os.path.commonprefix([semantics, existing_semantics])
        diff1, diff2 = semantics[len(common_prefix) :], existing_semantics[len(common_prefix) :]
        overall_sim = util.cos_sim(sim_model.encode(semantics), sim_model.encode(existing_semantics)).item()
        
        # Calculate difference similarity with boundary case handling
        if diff1 and diff2:
            diff_sim = util.cos_sim(sim_model.encode(diff1), sim_model.encode(diff2)).item()
        else:
            diff_sim = 1.0 if not diff1 and not diff2 else 0.0

        ave_overall_len = (len(semantics) + len(existing_semantics)) / 2
        ave_diff_len = (len(diff1) + len(diff2)) / 2
        
        if ave_overall_len == 0:
            similarity = 1.0
        else:
            similarity = (
                len(common_prefix) / ave_overall_len * overall_sim
                + ave_diff_len / ave_overall_len * diff_sim
            )
        
        if similarity > 0.98:
            return True, existing_semantics
    return False, None

def _render_user_prompt(
    current_index: int,
    input_dir: Path, 
    output_dir: Path, 
    scope: str,
    existing_dirs: list[Path] | None,
    few_shots: list[dict[str, Any]]
) -> tuple[str, list[str]]:
    # Get scenario information
    scenario_path = input_dir / SCENARIO_FILE_NAME
    scenario = scenario_path.read_text().strip()

    # Get context definitions information
    context_definitions_path = input_dir / CONTEXT_DEFINITIONS_FILE_NAME
    with open(context_definitions_path, 'rb') as f:
        context_definitions_info = tomli.load(f)['context_definitions']
        ctx_definitions = {
            'description': context_definitions_info['description'],
            'fields': context_definitions_info['fields'],
            'explanation': context_definitions_info['explanation'],
        }
    
    # Get scope information
    if scope != 'NS':
        scope_path = input_dir / SCOPES_DIR_NAME / scope / SCOPE_FILE_NAME
        scope_content = scope_path.read_text().strip()
    else:
        scope_content = "Constraints about properties of individual contexts or relationships between context pairs"

    # Get existing template semantics
    existing_template_semantics = []
    if output_dir.exists():    
        for template_dir in output_dir.iterdir():
            if template_dir.is_dir() and \
                template_dir.name.startswith(TEMPLATE_DIR_PREFIX) and \
                int(template_dir.name.split('_')[-1]) < current_index:
                # Read JSON file and extract semantics field
                template_json_file_path = template_dir / TEMPLATE_JSON_FILE_NAME
                if template_json_file_path.exists():
                    with open(template_json_file_path, 'r', encoding='utf-8') as f:
                        template_data = json.load(f)
                        existing_template_semantics.append(template_data['semantics'])
                else:
                    log_warning(LOGGER_NAME, f"{TEMPLATE_JSON_FILE_NAME} file not found in {template_dir}")

    if existing_dirs:
        for existing_dir in existing_dirs:
            if existing_dir.is_dir():
                for template_dir in existing_dir.iterdir():
                    if template_dir.is_dir() and template_dir.name.startswith(TEMPLATE_DIR_PREFIX):
                        # Read JSON file and extract semantics field
                        template_json_file_path = template_dir / TEMPLATE_JSON_FILE_NAME
                        if template_json_file_path.exists():
                            with open(template_json_file_path, 'r', encoding='utf-8') as f:
                                template_data = json.load(f)
                                existing_template_semantics.append(template_data['semantics'])
                        else:
                            log_warning(LOGGER_NAME, f"{TEMPLATE_JSON_FILE_NAME} file not found in {template_dir}")

    # Build user prompt
    random.shuffle(existing_template_semantics)
    jinjia_env = Environment(trim_blocks=True, lstrip_blocks=True)
    user_prompt_template = jinjia_env.from_string(PHASE1_USER_PROMPT_TEMPLATE_SCOPE)
    user_prompt = user_prompt_template.render(
        scenario=scenario,
        ctx_definitions=ctx_definitions,
        existing_semantics=existing_template_semantics,
        scope=scope_content,
        few_shots=few_shots
    )
    
    return user_prompt, existing_template_semantics

def _render_duplicate_semantics_prompt(existing_semantics: str) -> str:
    jinjia_env = Environment(trim_blocks=True, lstrip_blocks=True)
    duplicate_semantics_prompt_template = jinjia_env.from_string(PHASE1_DUPLICATE_ERROR_PROMPT)
    duplicate_semantics_prompt = duplicate_semantics_prompt_template.render(
        existing_semantics=existing_semantics
    )
    return duplicate_semantics_prompt
