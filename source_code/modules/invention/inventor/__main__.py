import time
import tomli
import argparse
from pathlib import Path
from datetime import datetime

from ...utils import (
    log_warning,
    SCENARIO_FILE_NAME, CONTEXT_DEFINITIONS_FILE_NAME, SCOPES_DIR_NAME, SCOPE_FILE_NAME, INPUT_DIR
)
from .. import LOGGER_NAME
from ...utils import log_info
from .invent import invent
from .invent_ias import _init_sim_model
from . import INVENTOR_OUTPUT_DIR


def parse_args():
    parser = argparse.ArgumentParser(description='inventor arguments parser')
    
    parser.add_argument('--scenario', '-s', required=True, type=str, help='specify the scenario')
    parser.add_argument('--scope', type=str, default='NS', help='specify the scope of the constraint')
    parser.add_argument('--invent-times', type=int, default=10, help='invention times')
    parser.add_argument('--existing-dirs', type=lambda x: [item.strip() for item in x.split(',')], help='existing dirs')
    parser.add_argument('--disable-similarity-check', action='store_false', dest='similarity_check', default=True, help='disable similarity check (enabled by default)')
    parser.add_argument('--disable-semantic-validation', action='store_false', dest='semantic_validation', default=True, help='disable semantic validation (enabled by default)')
    parser.add_argument('--disable-parameter-domain-discretization', action='store_false', dest='parameter_domain_discretization', default=True, help='disable parameter domain discretization (enabled by default)')
    parser.add_argument('--disable-predicate-sensitivity-promotion', action='store_false', dest='predicate_sensitivity_promotion', default=True, help='disable predicate sensitivity promotion (enabled by default)')
    
    args = parser.parse_args()
    
    if args.existing_dirs:
        existing_dirs = []
        for dir in args.existing_dirs:
            dir_path = INVENTOR_OUTPUT_DIR / args.scenario / dir
            if not dir_path.exists():
                log_warning(LOGGER_NAME, f"Existing directory {dir_path} does not exist, ignored")
            else:
                existing_dirs.append(dir_path)
        args.existing_dirs = existing_dirs
    
    return args

def run(args):
    
    def _check_input_files(input_dir: Path, scope: str) -> None:
        # Check scenario file
        scenario_path = input_dir / SCENARIO_FILE_NAME
        if not scenario_path.exists():
            raise FileNotFoundError(f"Scenario file {scenario_path} does not exist")
        
        # Check dataset file
        sequence_path = input_dir / CONTEXT_DEFINITIONS_FILE_NAME
        if not sequence_path.exists():
            raise FileNotFoundError(f"Sequence file {sequence_path} does not exist")
        with open(sequence_path, 'rb') as f:
            sequence_info = tomli.load(f)['context_definitions']
            if 'description' not in sequence_info:
                raise ValueError("description is not defined in context_schema.toml")
            if 'fields' not in sequence_info:
                raise ValueError("fields is not defined in context_schema.toml")
            if 'explanation' not in sequence_info:
                raise ValueError("explanation is not defined in context_schema.toml")
            
            for field_name, field_info in sequence_info['fields'].items():
                if 'description' not in field_info:
                    raise ValueError(f"description for field {field_name} is not defined in context_schema.toml")
                if 'type' not in field_info:
                    raise ValueError(f"type for field {field_name} is not defined in context_schema.toml")
                if field_info['type'] not in ['int', 'float', 'str']:
                    raise ValueError(f"type for field {field_name} is not int, float, or str in context_schema.toml")
                if field_info['type'] in ['int', 'float']:
                    if 'unit' not in field_info:
                        raise ValueError(f"unit for field {field_name} is not defined in context_schema.toml")                                       
        
        # Check scope file
        if scope != 'NS':
            scope_file_path = input_dir / SCOPES_DIR_NAME / scope / SCOPE_FILE_NAME
            if not scope_file_path.exists():
                raise FileNotFoundError(f"Scope file {scope_file_path} does not exist")
    
    def _set_output_dir(args) -> Path:
        
        def _encode_tech_configs() -> str:
            encoded = ''
            if args.similarity_check:
                encoded += '1'
            else:
                encoded += '0'
            
            if args.semantic_validation:
                encoded += '1'
            else:
                encoded += '0'
                
            if args.parameter_domain_discretization:
                encoded += '1'
            else:
                encoded += '0'

            if args.predicate_sensitivity_promotion:
                encoded += '1'
            else:
                encoded += '0'
            return encoded
            
        scope_suffix = f'_{args.scope}' if args.scope != 'NS' else ''
        output_dir_name = f'{datetime.now().strftime("%m%d%H%M%S")}' + scope_suffix + \
            f'_{_encode_tech_configs()}' + f'_{args.invent_times}'
        output_dir = INVENTOR_OUTPUT_DIR / args.scenario / output_dir_name
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir
    
    start_time = time.time()

    # Find input directory corresponding to scenario and check necessary files
    input_dir = INPUT_DIR / args.scenario
    if not input_dir.exists():
        raise FileNotFoundError(f"input directory {input_dir} does not exist")

    _check_input_files(input_dir, args.scope)
    output_dir = _set_output_dir(args)
    
    # Initialize sim_model
    if args.similarity_check:
        _init_sim_model()
    
    invention_start_time = time.time()
    for invention_index in range(args.invent_times):
        invent(invention_index, input_dir, output_dir, args.scope, args.existing_dirs, args.similarity_check, args.semantic_validation, args.parameter_domain_discretization)     
    invention_end_time = time.time()
    log_info(LOGGER_NAME, f"Invention done in {invention_end_time - invention_start_time} seconds")

    end_time = time.time()
    log_info(LOGGER_NAME, f"Invention done in {end_time - start_time} seconds")
    
    return output_dir

if __name__ == "__main__":
    args = parse_args()
    run(args)
