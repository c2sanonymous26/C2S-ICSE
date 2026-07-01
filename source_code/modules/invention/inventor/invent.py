import os
import shutil
import json
import random
import re
from types import SimpleNamespace
from agno.models.openai.like import OpenAILike  # noqa: F401
from agno.models.openrouter import OpenRouter  # noqa: F401
from agno.agent import Agent
from typing import Any
from pathlib import Path

from ...utils import (
    log_info, log_warning, log_error,
    FEW_SHOTS_DIR_NAME, SCOPES_DIR_NAME
)
from .. import LOGGER_NAME
from ..statistics import (
    TemplateStatistics, IasStatistics, 
    SasStatistics, ImplStatistics,
    RewriteStatistics, ReimagineStatistics
)
from . import (
    INTENT_AND_SEMANTICS_FILE_NAME,
    STRUCTURE_AND_SIGNATURES_FILE_NAME,
    BFUNC_IMPLEMENTATION_FILE_NAME,
    RESTRICTIONS_INVT_FILE_NAME,
    TEMPLATE_JSON_FILE_NAME,
    TEMPLATE_DIR_PREFIX,
    STATISTICS_FILE_NAME,
    MAX_REIMAGINE_ROLLBACK,
    MAX_REWRITE_ROLLBACK
)
from .prompts import (
    AGENT_DISCRIPTION_SCOPE
)
from .responses import (
    IntentAndSemantics, 
    StructureAndSignatures, 
    Bfunc,
    SymbolRestrictions,
    Template,
    BfuncImplementationNoCheck,
    BfuncImplementationWithCheck
)
from .invent_ias import invent_intent_and_semantics
from .invent_sas import invent_sas_without_semantic_validation, invent_sas_with_semantic_validation
from .invent_impl import invent_impl_without_semantic_validation, invent_impl_with_semantic_validation
from .invent_rst import invent_restrictions

def invent(
    invention_index: int, 
    input_dir: Path, 
    output_dir: Path, 
    scope: str,
    existing_dirs: list[Path] | None,
    similarity_check: bool,
    semantic_validation: bool,
    parameter_domain_discretization: bool
) -> None:
    """
    Main invention function with rollback support.
    
    Architecture:
        - Layer 1 (outer): Reimagine Rollback - triggered by similarity_check (structure+impl duplicate → retry from semantics)
        - Layer 2 (middle): Rewrite Rollback - triggered by semantic_validation (cannot implement → retry structure)
        - Layer 3 (inner): LLM retry in each phase (max 5 times per phase)
    """
    
    log_info(LOGGER_NAME, f"The {invention_index + 1} times invention starts", center=True, symbol="+")
    
    # Create template directory
    template_dir = output_dir / f'{TEMPLATE_DIR_PREFIX}{invention_index + 1}'
    if template_dir.exists():
        log_warning(LOGGER_NAME, f"Directory {TEMPLATE_DIR_PREFIX}{invention_index + 1} already exists, remove it")
        shutil.rmtree(template_dir)
    template_dir.mkdir(parents=True, exist_ok=False)
    
    #Create statistics for timing
    final_stats = TemplateStatistics()

    # Get agent & few shots
    agno_agent = _init_agent()
    if agno_agent is None:
        log_warning(LOGGER_NAME, f"The {invention_index + 1} times invention failed")
        final_stats.save_to_file(template_dir / STATISTICS_FILE_NAME)
        log_info(LOGGER_NAME, f"Statistics saved to {template_dir / STATISTICS_FILE_NAME}")
        log_info(LOGGER_NAME, f"The {invention_index + 1} times invention done", center=True, symbol="+", newlines=4)
        return

    few_shots = _get_few_shots(input_dir, scope)
    
    try:
        with final_stats.time_template():
            if similarity_check:
                # Has Reimagine Rollback: check structure+implementation duplicate
                success = _invent_with_reimagine_rollback(
                    agno_agent, 
                    invention_index, 
                    input_dir, 
                    output_dir,
                    template_dir, 
                    scope,
                    existing_dirs,
                    few_shots, 
                    semantic_validation,
                    parameter_domain_discretization,
                    final_stats
                )
            else:
                # No Reimagine Rollback: directly invent one template
                success = _invent_without_reimagine_rollback(
                    agno_agent, 
                    invention_index, 
                    input_dir, 
                    output_dir,
                    template_dir, 
                    scope,
                    existing_dirs,
                    few_shots, 
                    semantic_validation,
                    parameter_domain_discretization,
                    final_stats
                )
        
        if success:
            log_info(LOGGER_NAME, f"The {invention_index + 1} times invention succeeded")
        else:
            log_warning(LOGGER_NAME, f"The {invention_index + 1} times invention failed")
        
    finally:
        # Ensure statistics are saved even if there's an exception
        final_stats.save_to_file(template_dir / STATISTICS_FILE_NAME)
        log_info(LOGGER_NAME, f"Statistics saved to {template_dir / STATISTICS_FILE_NAME}")
    
    log_info(LOGGER_NAME, f"The {invention_index + 1} times invention done", center=True, symbol="+", newlines=4)

def _init_agent() -> Agent | None:
    
    # Get model configuration from environment variable
    cminer_model = os.getenv("C2S_MODEL")
    cminer_api_key = os.getenv("C2S_API_KEY")
    c2s_llm_output_mode = os.getenv("C2S_LLM_OUTPUT_MODE")
    
    if not cminer_model:
        log_error(
            LOGGER_NAME,
            "C2S_MODEL environment variable is not set. "
            "Please set it with: export C2S_MODEL='provider:model_id' "
            "(e.g., 'openrouter:deepseek/deepseek-chat' or 'ark:deepseek-v3-250324')"
        )
        return None
    
    if not cminer_api_key:
        log_error(
            LOGGER_NAME,
            "C2S_API_KEY environment variable is not set. "
            "Please set it with: export C2S_API_KEY='your-api-key'"
        )
        return None

    if not c2s_llm_output_mode:
        log_error(
            LOGGER_NAME,
            "C2S_LLM_OUTPUT_MODE environment variable is not set. "
            "Please set it with: export C2S_LLM_OUTPUT_MODE='json' "
            "or 'schema' or 'prompt'"
        )
        return None
    
    # Parse provider and model_id
    parts = cminer_model.split(":", 1)
    if len(parts) != 2:
        log_error(
            LOGGER_NAME,
            f"Invalid C2S_MODEL format: '{cminer_model}'. "
            "Expected format: 'provider:model_id' (e.g., 'ark:deepseek-v3-250324')"
        )
        return None
    
    provider, model_id = parts
    provider = provider.lower()
    
    # Configure model based on provider
    if provider == "ark":
        model = OpenAILike(
            base_url="https://ark.cn-beijing.volces.com/api/v3",
            id=model_id,
            api_key=cminer_api_key,
            temperature=1.0
        )
    elif provider == "openrouter":
        model = OpenRouter(
            api_key=cminer_api_key,
            id=model_id,
            temperature=1.0,
            max_tokens=None
        )
    else:
        log_error(
            LOGGER_NAME,
            f"Unsupported provider: '{provider}'. "
            "Supported providers: 'ark', 'openrouter'"
        )
        return None
    
    output_mode = c2s_llm_output_mode.strip().lower()
    if output_mode not in {"json", "schema", "prompt"}:
        log_error(
            LOGGER_NAME,
            f"Invalid C2S_LLM_OUTPUT_MODE: '{c2s_llm_output_mode}'. "
            "Expected one of: 'json', 'schema', 'prompt'"
        )
        return None

    if output_mode == "json":
        use_json_mode = True
        structured_outputs = None
    elif output_mode == "schema":
        use_json_mode = False
        structured_outputs = True
    else:
        log_info(LOGGER_NAME, f"C2S LLM output mode: {output_mode}")
        base_agent = Agent(
            debug_mode=True,
            instructions=AGENT_DISCRIPTION_SCOPE,
            model=model,
            add_history_to_messages=True,
            num_history_responses=1000,
            use_json_mode=False,
            structured_outputs=False,
        )
        return PromptOnlyAgent(base_agent)

    log_info(LOGGER_NAME, f"C2S LLM output mode: {output_mode}")
    return Agent(
        debug_mode=True,
        instructions=AGENT_DISCRIPTION_SCOPE,
        model=model,
        add_history_to_messages=True,
        num_history_responses=1000,
        use_json_mode=use_json_mode,
        structured_outputs=structured_outputs,
    )

class PromptOnlyAgent:
    def __init__(self, agent: Agent) -> None:
        self.agent = agent
        self.response_model = None

    def run(self, prompt: str, *args: Any, **kwargs: Any) -> Any:
        if self.response_model is None:
            return self.agent.run(prompt, *args, **kwargs)

        schema = json.dumps(self.response_model.model_json_schema(), ensure_ascii=False)
        prompt_with_schema = (
            f"{prompt}\n\n"
            "Return only one valid JSON object. Do not wrap it in Markdown. "
            f"The JSON object must satisfy this schema:\n{schema}"
        )
        response = self.agent.run(prompt_with_schema, *args, **kwargs)
        raw_content = response.content
        try:
            parsed = json.loads(self._extract_json_object(str(raw_content)))
            content = self.response_model.model_validate(parsed)
        except Exception:
            content = raw_content

        try:
            response.content = content
            return response
        except Exception:
            return SimpleNamespace(content=content)

    def _extract_json_object(self, text: str) -> str:
        stripped = text.strip()
        if stripped.startswith("```"):
            stripped = re.sub(r"^```(?:json)?\s*", "", stripped)
            stripped = re.sub(r"\s*```$", "", stripped)
        if stripped.startswith("{") and stripped.endswith("}"):
            return stripped
        start = stripped.find("{")
        end = stripped.rfind("}")
        if start == -1 or end == -1 or end < start:
            raise ValueError("No JSON object found in LLM response.")
        return stripped[start : end + 1]


def _get_few_shots(input_dir: Path, scope: str) -> list[dict[str, Any]]:
    
    few_shots_dir = input_dir / SCOPES_DIR_NAME / scope / FEW_SHOTS_DIR_NAME
    if not few_shots_dir.exists():
        log_warning(LOGGER_NAME, f"Few shots directory {few_shots_dir} does not exist, using zero-shot")
        return []
    
    few_shots = []
    for shot_dir in few_shots_dir.iterdir():
        if shot_dir.is_dir() and shot_dir.name.startswith('shot'):
            intent_and_semantics_file = shot_dir / INTENT_AND_SEMANTICS_FILE_NAME
            structure_and_signatures_file = shot_dir / STRUCTURE_AND_SIGNATURES_FILE_NAME
            bfunc_implementation_file = shot_dir / BFUNC_IMPLEMENTATION_FILE_NAME
            restrictions_file = shot_dir / RESTRICTIONS_INVT_FILE_NAME
            
            if any(not file.exists() for file in [intent_and_semantics_file, structure_and_signatures_file, bfunc_implementation_file, restrictions_file]):
                log_warning(LOGGER_NAME, f"Few shot {shot_dir} is incomplete, ignored")
                continue
            
            intent_and_semantics = json.loads(intent_and_semantics_file.read_text(encoding="utf-8"))
            structure_and_signatures = json.loads(structure_and_signatures_file.read_text(encoding="utf-8"))
            bfunc_implementations = json.loads(bfunc_implementation_file.read_text(encoding="utf-8"))
            restrictions = json.loads(restrictions_file.read_text(encoding="utf-8"))
            
            few_shots.append({
                "intent_and_semantics": intent_and_semantics,
                "structure_and_signatures": structure_and_signatures,
                "bfunc_implementations": bfunc_implementations,
                "restrictions": restrictions
            })
            
    random.shuffle(few_shots)
    return few_shots

def _check_structure_implementation_duplicate(
    structure: str,
    bfunc_implementations: list,
    output_dir: Path,
    current_template_index: int,
    existing_dirs: list[Path] | None
) -> tuple[bool, str | None]:
    """
    Check if structure + implementation is identical to any existing template.
    
    Returns:
        (is_duplicate, duplicate_template_name)
    """
    
    def _is_bfuncs_implementation_identical(impls1: list, impls2: list) -> bool:
        """Check if two bfunc implementation lists are identical."""
        if len(impls1) != len(impls2):
            return False
        
        # Convert impls1 (BfuncBody objects) to dict format for comparison
        impls1_dict = [{'id': impl.id, 'implementation': impl.implementation} for impl in impls1]
        
        # Sort by id for comparison
        sorted_impls1 = sorted(impls1_dict, key=lambda x: x.get('id', ''))
        sorted_impls2 = sorted(impls2, key=lambda x: x.get('id', ''))
        
        for impl1, impl2 in zip(sorted_impls1, sorted_impls2):
            # Only compare implementation field (exact match, no strip)
            if impl1.get('implementation', '') != impl2.get('implementation', ''):
                return False
        
        return True
    
    # Collect all existing templates
    existing_templates = []
    
    # 1. Load from output_dir (exclude current and later templates)
    if output_dir.exists():
        for template_dir in output_dir.iterdir():
            if not template_dir.is_dir() or not template_dir.name.startswith(TEMPLATE_DIR_PREFIX):
                continue
            
            # Extract template number
            try:
                template_num = int(template_dir.name.split('_')[1])
                if template_num >= current_template_index:
                    continue  # Skip current and later templates
            except (IndexError, ValueError):
                continue
            
            template_file = template_dir / TEMPLATE_JSON_FILE_NAME
            if template_file.exists():
                try:
                    with open(template_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        existing_templates.append({
                            'name': template_dir.name,
                            'structure': data.get('structure', ''),
                            'bfuncs': data.get('bfuncs', [])
                        })
                except Exception as e:
                    log_warning(LOGGER_NAME, f"Failed to read {template_file}: {e}")
                    continue
    
    # 2. Load from existing_dirs
    if existing_dirs:
        for existing_dir in existing_dirs:
            if not existing_dir.exists() or not existing_dir.is_dir():
                continue
            
            for template_dir in existing_dir.iterdir():
                if not template_dir.is_dir() or not template_dir.name.startswith(TEMPLATE_DIR_PREFIX):
                    continue
                
                template_file = template_dir / TEMPLATE_JSON_FILE_NAME
                if template_file.exists():
                    try:
                        with open(template_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            existing_templates.append({
                                'name': f"{existing_dir.name}/{template_dir.name}",
                                'structure': data.get('structure', ''),
                                'bfuncs': data.get('bfuncs', [])
                            })
                    except Exception as e:
                        log_warning(LOGGER_NAME, f"Failed to read {template_file}: {e}")
                        continue
    
    # 3. Check for duplicates
    structure_normalized = structure.strip()
    
    # Empty structure should not be considered as duplicate
    if not structure_normalized:
        return False, None
    
    for existing in existing_templates:
        # Check if structure is identical (skip if existing structure is empty)
        existing_structure = existing['structure'].strip()
        if not existing_structure or existing_structure != structure_normalized:
            continue
        
        # Check if bfuncs implementation is identical
        if _is_bfuncs_implementation_identical(bfunc_implementations, existing['bfuncs']):
            return True, existing['name']
    
    return False, None


# ========== Core Invention Functions ==========

def _invent_with_reimagine_rollback(
    agno_agent: Agent, 
    invention_index: int, 
    input_dir: Path, 
    output_dir: Path,
    template_dir: Path, 
    scope: str,
    existing_dirs: list[Path] | None,
    few_shots: list[dict[str, Any]],
    semantic_validation: bool,
    parameter_domain_discretization: bool,
    final_stats: TemplateStatistics
) -> bool:
    """
    Invention with Reimagine Rollback: check structure+implementation duplicate and retry from semantics.
    
    Only duplicate triggers reimagine rollback. Other failures return immediately.
    
    Args:
        final_stats: TemplateStatistics object to be filled with statistics
    
    Returns:
        success: whether the template was successfully generated
    """
    reimagine_rollback_times = 0
    
    while reimagine_rollback_times < MAX_REIMAGINE_ROLLBACK:
        log_info(
            LOGGER_NAME,
            f"Reimagine rollback attempt {reimagine_rollback_times + 1}/{MAX_REIMAGINE_ROLLBACK}",
            center=True,
            symbol="="
        )
        
        # Create statistics for this reimagine attempt
        attempt = ReimagineStatistics(
            attempt_number=reimagine_rollback_times + 1,
            result="pending"
        )
        
        with attempt.time_reimagine():
            # Generate one complete template
            success, intent_and_semantics, structure_and_signatures, bfunc_implementations, restrictions, bfunc_symbol_dict = _invent_once(
                agno_agent,
                invention_index,
                input_dir,
                output_dir,
                scope,
                existing_dirs,
                few_shots,
                similarity_check=True,  # Check semantic duplicate
                semantic_validation=semantic_validation,
                parameter_domain_discretization=parameter_domain_discretization,
                ias_stats=attempt.ias,
                rewrites=attempt.rewrites
            )
            
            if not success:
                # Template generation failed - record this attempt
                attempt.result = "failed"
                final_stats.reimagine_attempts.append(attempt)
                
                log_warning(LOGGER_NAME, f"Template generation failed")
                final_stats.reimagine_rollback_count = reimagine_rollback_times
                return False
            
            # Check for structure + implementation duplicate
            is_duplicate, duplicate_name = _check_structure_implementation_duplicate(
                structure_and_signatures.structure,
                bfunc_implementations.bodies,
                output_dir,
                invention_index + 1,
                existing_dirs
            )
            
            if is_duplicate:
                # Record this duplicate attempt (don't save files)
                attempt.result = "duplicate"
                attempt.duplicate_with = duplicate_name
                final_stats.reimagine_attempts.append(attempt)
                
                log_warning(
                    LOGGER_NAME,
                    f"Detected structure + implementation duplicate with {duplicate_name}, "
                    f"triggering reimagine rollback ({reimagine_rollback_times + 1}/{MAX_REIMAGINE_ROLLBACK})"
                )
                reimagine_rollback_times += 1
                continue
            
            # Success! No duplicate, now save all files
            _dump_intent_and_semantics(intent_and_semantics, template_dir)
            _dump_structure_and_signatures(structure_and_signatures, template_dir)
            _dump_bfunc_implementations(bfunc_implementations, template_dir)
            if restrictions is not None:
                _dump_restrictions(restrictions, template_dir)
            
            # Build and save final template
            template = _build_template(
                intent_and_semantics,
                structure_and_signatures,
                bfunc_implementations,
                restrictions,
                bfunc_symbol_dict
            )
            _dump_template(template, template_dir)
            
            # Record this successful attempt
            attempt.result = "success"
            attempt.duplicate_with = None
            final_stats.reimagine_attempts.append(attempt)
            
            # Mark final stats as successful
            final_stats.success = True
            final_stats.reimagine_rollback_count = reimagine_rollback_times
            
            log_info(
                LOGGER_NAME,
                f"Template generated successfully after {reimagine_rollback_times} reimagine rollback(s)"
            )
            return True
    
    # Reached max reimagine rollback limit
    log_warning(
        LOGGER_NAME,
        f"Failed after {MAX_REIMAGINE_ROLLBACK} reimagine rollback attempts"
    )
    final_stats.reimagine_rollback_count = reimagine_rollback_times
    return False


def _invent_without_reimagine_rollback(
    agno_agent: Agent,
    invention_index: int,
    input_dir: Path,
    output_dir: Path,
    template_dir: Path,
    scope: str,
    existing_dirs: list[Path] | None,
    few_shots: list[dict[str, Any]],
    semantic_validation: bool,
    parameter_domain_discretization: bool,
    final_stats: TemplateStatistics
) -> bool:
    """
    Invention without Reimagine Rollback: no structure+implementation duplicate check.
    
    Args:
        final_stats: TemplateStatistics object to be filled with statistics
    
    Returns:
        success: whether the template was successfully generated
    """
    # Create statistics for this single reimagine attempt
    attempt = ReimagineStatistics(
        attempt_number=1,
        result="pending"
    )
    
    with attempt.time_reimagine():
        # Generate one complete template
        success, intent_and_semantics, structure_and_signatures, bfunc_implementations, restrictions, bfunc_symbol_dict = _invent_once(
            agno_agent,
            invention_index,
            input_dir,
            output_dir,
            scope,
            existing_dirs,
            few_shots,
            similarity_check=False,  # No structure+impl duplicate check
            semantic_validation=semantic_validation,
            parameter_domain_discretization=parameter_domain_discretization,
            ias_stats=attempt.ias,
            rewrites=attempt.rewrites
        )
    
    # Record this single attempt and save files if successful
    if success:
        # Save all files
        _dump_intent_and_semantics(intent_and_semantics, template_dir)
        _dump_structure_and_signatures(structure_and_signatures, template_dir)
        _dump_bfunc_implementations(bfunc_implementations, template_dir)
        if restrictions is not None:
            _dump_restrictions(restrictions, template_dir)
        
        # Build and save final template
        template = _build_template(
            intent_and_semantics,
            structure_and_signatures,
            bfunc_implementations,
            restrictions,
            bfunc_symbol_dict
        )
        _dump_template(template, template_dir)
        
        attempt.result = "success"
        final_stats.success = True
    else:
        # Record failed attempt
        attempt.result = "failed"
    
    # Always record the attempt (success or failure)
    final_stats.reimagine_attempts.append(attempt)
    
    return success


def _invent_once(
    agno_agent: Agent, 
    invention_index: int, 
    input_dir: Path, 
    output_dir: Path,
    scope: str,
    existing_dirs: list[Path] | None,
    few_shots: list[dict[str, Any]],
    similarity_check: bool,
    semantic_validation: bool,
    parameter_domain_discretization: bool,
    ias_stats: IasStatistics,
    rewrites: list[RewriteStatistics]
) -> tuple[bool, IntentAndSemantics | None, StructureAndSignatures | None, BfuncImplementationWithCheck | None, SymbolRestrictions | None, dict | None]:
    """
    Generate one complete template (intent and semantics + structure + implementation + restrictions).
    
    NOTE: This function does NOT save files to avoid overwriting during reimagine rollback.
    The caller should save files only after confirming no duplicate.
    
    Returns:
        (success, intent_and_semantics, structure_and_signatures, bfunc_implementations, restrictions, bfunc_symbol_dict)
    """
    
    try:
        # Phase 1: Generate intent and semantics
        with ias_stats.time_ias():
            intent_and_semantics = invent_intent_and_semantics(
                agno_agent,
                invention_index + 1,
                input_dir,
                output_dir,
                scope,
                existing_dirs,
                few_shots,
                similarity_check=similarity_check,
                statistics=ias_stats
            )
        
        if intent_and_semantics is None:
            log_warning(LOGGER_NAME, f"Intent and semantics generation failed")
            return False, None, None, None, None, None
        
        # Phase 2-3: Generate structure and implementation
        if semantic_validation:
            # With semantic validation and Rewrite Rollback
            success, structure_and_signatures, bfunc_implementations = _invent_structure_and_implementation_with_rewrite_rollback(
                agno_agent,
                input_dir,
                few_shots,
                rewrites
            )
            
            if not success:
                return False, None, None, None, None, None
        else:
            # Without semantic validation and Rewrite Rollback
            success, structure_and_signatures, bfunc_implementations = _invent_structure_and_implementation_without_rewrite_rollback(
                agno_agent,
                input_dir,
                few_shots,
                rewrites
            )
            
            if not success:
                return False, None, None, None, None, None
        
        # Phase 4: Generate restrictions (optional, no statistics)
        if parameter_domain_discretization:
            restrictions, bfunc_symbol_dict = invent_restrictions(
                agno_agent,
                input_dir,
                structure_and_signatures,
                bfunc_implementations,
                few_shots
            )
        else:
            restrictions, bfunc_symbol_dict = None, None
        
        # Return intent_and_semantics, structure, implementation, restrictions, and symbol dict
        # NOTE: Files are NOT saved here to avoid overwriting on reimagine rollback
        # The caller should save files only after confirming no duplicate
        return True, intent_and_semantics, structure_and_signatures, bfunc_implementations, restrictions, bfunc_symbol_dict
        
    except Exception as e:
        log_error(LOGGER_NAME, f"Exception during invention: {e}")
        return False, None, None, None, None, None


def _invent_structure_and_implementation_with_rewrite_rollback(
    agno_agent: Agent,
    input_dir: Path,
    few_shots: list[dict[str, Any]],
    rewrites: list[RewriteStatistics]
) -> tuple[bool, StructureAndSignatures | None, BfuncImplementationWithCheck | None]:
    """
    Generate structure + implementation with Rewrite Rollback loop (for semantic_validation=True).
    
    Records all rewrite attempts in the rewrites list.
    
    Returns:
        (success, structure_and_signatures, bfunc_implementations)
    """
    
    rewrite_rollback_times = 0
    rewrite_rollback_reason = None
    
    while rewrite_rollback_times < MAX_REWRITE_ROLLBACK:
        # Create statistics for this rewrite attempt
        rewrite = RewriteStatistics(
            attempt_number=rewrite_rollback_times + 1,
            result="pending"
        )
        
        with rewrite.time_rewrite():
            # Phase 2: Generate structure and signatures
            with rewrite.sas_stats.time_phase():
                structure_and_signatures = invent_sas_with_semantic_validation(
                    agno_agent,
                    few_shots,
                    rewrite_rollback_times,
                    rewrite_rollback_reason,
                    statistics=rewrite.sas_stats
                )
            
            if structure_and_signatures is None:
                log_warning(LOGGER_NAME, f"Structure and signatures generation failed")
                return False, None, None
            
            # Phase 3: Generate implementation
            with rewrite.impl_stats.time_phase():
                response = invent_impl_with_semantic_validation(
                    agno_agent,
                    input_dir,
                    few_shots,
                    rewrite_rollback_times,
                    structure_and_signatures,
                    statistics=rewrite.impl_stats
                )
            
            if response is None:
                log_warning(LOGGER_NAME, f"Implementation generation failed")
                return False, None, None
            
            # Check if implementation stage requests rewrite rollback
            if isinstance(response, str):
                rewrite_rollback_reason = response
                rewrite.result = "cannot_implement"
                rewrites.append(rewrite)
                
                log_info(
                    LOGGER_NAME,
                    f"Implementation stage triggered rewrite rollback: {rewrite_rollback_reason}"
                )
                rewrite_rollback_times += 1
                continue
            
            # Success
            bfunc_implementations = response
            rewrite.result = "success"
            rewrites.append(rewrite)
            
            return True, structure_and_signatures, bfunc_implementations
    
    # Reached max rewrite rollback limit
    return False, None, None


def _invent_structure_and_implementation_without_rewrite_rollback(
    agno_agent: Agent,
    input_dir: Path,
    few_shots: list[dict[str, Any]],
    rewrites: list[RewriteStatistics]
) -> tuple[bool, StructureAndSignatures | None, BfuncImplementationWithCheck | None]:
    """
    Generate structure + implementation without Rewrite Rollback loop (for semantic_validation=False).
    
    Records one rewrite attempt in the rewrites list.
    
    Returns:
        (success, structure_and_signatures, bfunc_implementations)
    """
    # Create statistics for this single attempt
    rewrite = RewriteStatistics(
        attempt_number=1,
        result="pending"
    )
    
    with rewrite.time_rewrite():
        # Phase 2: Generate structure and signatures
        with rewrite.sas_stats.time_phase():
            structure_and_signatures = invent_sas_without_semantic_validation(
                agno_agent,
                few_shots,
                statistics=rewrite.sas_stats
            )
        
        if structure_and_signatures is None:
            log_warning(LOGGER_NAME, f"Structure and signatures invention failed")
            rewrite.result = "failed"
            rewrites.append(rewrite)
            return False, None, None
        
        # Phase 3: Generate implementation
        with rewrite.impl_stats.time_phase():
            bfunc_implementations = invent_impl_without_semantic_validation(
                agno_agent,
                input_dir,
                few_shots,
                statistics=rewrite.impl_stats
            )
        
        if bfunc_implementations is None:
            log_warning(LOGGER_NAME, f"Bfunc implementations invention failed")
            rewrite.result = "failed"
            rewrites.append(rewrite)
            return False, None, None
        
        # Success
        rewrite.result = "success"
        rewrites.append(rewrite)
        
        return True, structure_and_signatures, bfunc_implementations



# ========== Dump Functions ==========

def _dump_intent_and_semantics(intent_and_semantics: IntentAndSemantics, template_dir: Path) -> None:
    intent_and_semantics_file = template_dir / INTENT_AND_SEMANTICS_FILE_NAME
    
    with open(intent_and_semantics_file, "w", encoding="utf-8") as f:
        json.dump(intent_and_semantics.model_dump(), f, indent=2, ensure_ascii=False)
    
    log_info(LOGGER_NAME, f"Intent and semantics saved to {intent_and_semantics_file}")

def _dump_structure_and_signatures(structure_and_signatures: StructureAndSignatures, template_dir: Path) -> None:
    structure_and_signatures_file = template_dir / STRUCTURE_AND_SIGNATURES_FILE_NAME
    
    with open(structure_and_signatures_file, "w", encoding="utf-8") as f:
        json.dump(structure_and_signatures.model_dump(), f, indent=2, ensure_ascii=False)
    
    log_info(LOGGER_NAME, f"Structure and signatures saved to {structure_and_signatures_file}")

def _dump_bfunc_implementations(bfunc_implementations: BfuncImplementationNoCheck | BfuncImplementationWithCheck, template_dir: Path) -> None:
    bfunc_implementations_file = template_dir / BFUNC_IMPLEMENTATION_FILE_NAME
    
    with open(bfunc_implementations_file, "w", encoding="utf-8") as f:
        json.dump(bfunc_implementations.model_dump(), f, indent=2, ensure_ascii=False)
    
    log_info(LOGGER_NAME, f"Bfunc implementations saved to {bfunc_implementations_file}")

def _dump_restrictions(restrictions: SymbolRestrictions, template_dir: Path) -> None:
    restrictions_file = template_dir / RESTRICTIONS_INVT_FILE_NAME
    
    with open(restrictions_file, "w", encoding="utf-8") as f:
        json.dump(restrictions.model_dump(), f, indent=2, ensure_ascii=False)
    
    log_info(LOGGER_NAME, f"Restrictions saved to {restrictions_file}")

def _build_template(
    intent_and_semantics: IntentAndSemantics, 
    structure_and_signatures: StructureAndSignatures, 
    bfunc_implementations: BfuncImplementationNoCheck | BfuncImplementationWithCheck,
    restrictions: SymbolRestrictions | None,
    bfunc_symbol_dict: dict[str, set[str]] | None
) -> Template:
    # Check the number of signatures and implementations
    if len(structure_and_signatures.signatures) != len(bfunc_implementations.bodies):
        raise ValueError(
            f"The number of signatures ({len(structure_and_signatures.signatures)}) "
            f"does not match the number of implementations ({len(bfunc_implementations.bodies)})"
        )
    
    # Check if all signature IDs have corresponding implementations
    signature_ids = {sig.id for sig in structure_and_signatures.signatures}
    implementation_ids = {body.id for body in bfunc_implementations.bodies}
    
    missing_implementations = signature_ids - implementation_ids
    if missing_implementations:
        raise ValueError(f"Missing implementations for the following IDs: {', '.join(missing_implementations)}")
    
    extra_implementations = implementation_ids - signature_ids
    if extra_implementations:
        raise ValueError(f"Extra implementations for the following IDs: {', '.join(extra_implementations)}")
    
    # Create bfuncs list
    bfuncs = []
    
    # Iterate through all signatures
    for signature in structure_and_signatures.signatures:
        # Find corresponding implementation
        implementation = next(
            (body.implementation for body in bfunc_implementations.bodies if body.id == signature.id),
            None
        )
        
        if implementation is None:
            raise ValueError(f"No implementation found for bfunc ID {signature.id}")
        
        # Find corresponding restrictions
        if bfunc_symbol_dict is None or restrictions is None or signature.id not in bfunc_symbol_dict:
            related_rst_strs = []
        else:
            related_symbols = bfunc_symbol_dict[signature.id]
            related_rsts = [ restriction for restriction in restrictions.restrictions if restriction.symbol in related_symbols ]
            related_rst_strs = [ f'{restriction.restriction}' for restriction in related_rsts ]

        # Create Bfunc object
        bfunc = Bfunc(
            id=signature.id,
            parameters=signature.parameters,
            semantics=signature.semantics,
            implementation=implementation,
            restrictions=related_rst_strs
        )
        
        bfuncs.append(bfunc)
    
    # Create and return Template object
    return Template(
        intent=intent_and_semantics.intent,
        semantics=intent_and_semantics.semantics,
        structure=structure_and_signatures.structure,
        bfuncs=bfuncs
    )
            
def _dump_template(template: Template, template_dir: Path) -> None:
    
    # Create output file path
    output_file = template_dir / TEMPLATE_JSON_FILE_NAME
    
    # Use json.dump to directly serialize object and write to file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(template.model_dump(), f, indent=2, ensure_ascii=False)
        
    log_info(LOGGER_NAME, f"Template saved to {output_file}")
