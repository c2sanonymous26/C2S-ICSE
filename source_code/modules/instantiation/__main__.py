import time
import glob
import argparse
import shutil
import logging
from pathlib import Path
from fractions import Fraction

from ..utils import (
    NUMERIC_SYMBOLIC_PREFIX, STRING_SYMBOLIC_PREFIX, 
    decompose, construct_ctx_data, load_data_field_types,
    set_log_file_handler, clean_log_file_handler, log_info, log_warning, log_error,
    TimeoutException
)
from ..invention.converter import CONVERTER_OUTPUT_DIR
from ..invention.converter import TEMPLATE_XML_FILE_NAME, BFUNC_FILE_NAME, RESTRICTIONS_FILE_NAME
from . import LOGGER_NAME, INSTANTIATION_DIR_NAME, INTERMEDIATE_DIR_NAME, INSTANTIATION_OUTPUT_DIR, CONSTRAINT_XML_FILE_NAME
from .solver import solve, SOLVE_TIMEOUT
from .solver.compute_basic_ranges import compute
from .validator import validate, VALIDATE_TIMEOUT


def parse_args():
    parser = argparse.ArgumentParser(description="Parse command line arguments.")
    
    parser.add_argument(
        '--scenario', '-s',
        required=True, 
        type=str, 
        help='specify the scenario'
    )
    
    # Mutually exclusive group for single vs batch mode
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        '--template', '-t',
        type=str, 
        help='specify the template to be instantiated (single mode)'
    )
    mode_group.add_argument(
        '--run-dir', '-r',
        nargs='+',
        dest='run_dirs',
        help='one or more converter run directories (batch mode)'
    )
    
    parser.add_argument(
        '--data', '-d',
        required=True,
        type=str,
        help='specify the data'
    )
            
    parser.add_argument(
        '--concurrent',
        action='store_true', 
        help='specify to run concurrently'
    )

    parser.add_argument(
        '--disable-parameter-domain-discretization',
        action='store_false',
        dest='parameter_domain_discretization',
        default=True,
        help='disable parameter domain discretization (enabled by default)'
    )
    
    parser.add_argument(
        '--disable-predicate-sensitivity-promotion',
        action='store_false',
        dest='predicate_sensitivity_promotion',
        default=True,
        help='disable predicate sensitivity promotion (enabled by default)'
    )
        
    args = parser.parse_args()
    return args


def _resolve_converter_dir(dir_arg: str, scenario: str) -> Path:
    direct = CONVERTER_OUTPUT_DIR / dir_arg
    if direct.exists():
        return direct

    legacy = CONVERTER_OUTPUT_DIR / scenario / dir_arg
    if legacy.exists():
        return legacy

    return direct

def run(args):
    """Main entry point"""
    if args.run_dirs:
        instantiate_batch_templates(args)
    else:
        instantiate_single_template(args)

def instantiate_single_template(args):
    
    def _get_input_file_paths() -> tuple[Path, Path, Path|None]:
        template_dir = _resolve_converter_dir(args.template, args.scenario)
        template_file_path = template_dir / TEMPLATE_XML_FILE_NAME
        bfuncs_file_path = template_dir / BFUNC_FILE_NAME
        restrictions_file_path = template_dir / RESTRICTIONS_FILE_NAME
        if not template_file_path.exists() or not template_file_path.is_file():
            raise FileNotFoundError(f"Template file {template_file_path} not found")
        if not bfuncs_file_path.exists() or not bfuncs_file_path.is_file():
            raise FileNotFoundError(f"bfuncs file {bfuncs_file_path} not found")        
        if restrictions_file_path.exists() and restrictions_file_path.is_file() and args.parameter_domain_discretization:
            return template_file_path, bfuncs_file_path, restrictions_file_path
        else:
            return template_file_path, bfuncs_file_path, None
    
    def _is_symbolic_template(bfuncs_file_path: Path) -> bool:
        is_symbolic = False
        with open(bfuncs_file_path, 'r') as file:
            content = file.read()
            if NUMERIC_SYMBOLIC_PREFIX in content or STRING_SYMBOLIC_PREFIX in content:
                is_symbolic = True
        return is_symbolic
    
    def _set_output_dir(is_symbolic: bool) -> Path:
        
        def _encode_tech_configs() -> str:
            encoded = ''
            if args.parameter_domain_discretization:
                encoded += '1'
            else:
                encoded += '0'
            
            if args.predicate_sensitivity_promotion:
                encoded += '1'
            else:
                encoded += '0'
            return encoded
        
        # Extract invention_dir from template path
        template_parts = args.template.split('/')
        assert len(template_parts) >= 2, "Template path should contain at least two parts"
        invention_dir = template_parts[0]
        template_name = '/'.join(template_parts[1:])

        tech_config_code = _encode_tech_configs()
        if tech_config_code:
            tech_config_suffix = f'_{tech_config_code}'
        else:
            tech_config_suffix = ''
            
        if is_symbolic:
            output_dir = INSTANTIATION_OUTPUT_DIR / invention_dir / f'{args.data}{tech_config_suffix}_solve' / template_name
        else:
            output_dir = INSTANTIATION_OUTPUT_DIR / invention_dir / f'{args.data}{tech_config_suffix}_validate' / template_name

        if output_dir.exists():
            shutil.rmtree(output_dir)
        output_dir.mkdir(parents=True, exist_ok=False)
        return output_dir
    
    def _prepare(scenario: str, template_file_path: Path, bfuncs_file_path: Path, 
        is_symbolic: bool, data: str, output_dir: Path
    ) -> tuple[Path, Path, dict[str, Path] | None, dict[str, Path] | None, dict[str, str | int | float]]:
        start_time = time.time()
        intermediate_dir = output_dir / INTERMEDIATE_DIR_NAME
        intermediate_dir.mkdir(parents=True, exist_ok=True)
        decomp_template_path, decomp_bfuncs_path = decompose(intermediate_dir, template_file_path, bfuncs_file_path)
        log_info(LOGGER_NAME, f"Decomposed template in {time.time() - start_time} seconds")
        
        start_time = time.time()
        solve_ctx2data, validate_ctx2data = construct_ctx_data(scenario, data, is_symbolic)
        log_info(LOGGER_NAME, f"Constructed ctx data in {time.time() - start_time} seconds")
        
        start_time = time.time()
        data_field_types = load_data_field_types(scenario)
        log_info(LOGGER_NAME, f"Loaded data field types in {time.time() - start_time} seconds")
        
        return decomp_template_path, decomp_bfuncs_path, solve_ctx2data, validate_ctx2data, data_field_types

    start_time = time.time()

    # get input file paths
    template_path, bfuncs_path, restrictions_path = _get_input_file_paths()
    # check whether the template is symbolic
    is_symbolic = _is_symbolic_template(bfuncs_path)
    # set output directory
    output_dir = _set_output_dir(is_symbolic)

    set_log_file_handler(LOGGER_NAME, output_dir / 'instantiation.log', logging.DEBUG)    
    log_info(LOGGER_NAME, f'{args.template} ({output_dir.parent.name}) instantiation starts', center=True, symbol='=')
    log_info(LOGGER_NAME, f'- scenario: {args.scenario}')
    log_info(LOGGER_NAME, f'- template: {args.template}')
    log_info(LOGGER_NAME, f'- data: {args.data}')
    log_info(LOGGER_NAME, f'- concurrent: {args.concurrent}')
    log_info(LOGGER_NAME, f'- parameter domain discretization: {"enabled" if args.parameter_domain_discretization else "disabled"}')
    log_info(LOGGER_NAME, f'- predicate sensitivity promotion: {"enabled" if args.predicate_sensitivity_promotion else "disabled"}')
    
    # prepare
    log_info(LOGGER_NAME, "Preparation starts", center=True, symbol="*")
    decomp_template_path, decomp_bfuncs_path, solve_ctx2data, validate_ctx2data, data_field_types = _prepare(
        scenario=args.scenario,
        template_file_path=template_path,
        bfuncs_file_path=bfuncs_path,
        is_symbolic=is_symbolic,
        data=args.data,
        output_dir=output_dir
    )
    log_info(LOGGER_NAME, "Preparation completes", center=True, symbol="*")
    
    if is_symbolic:
        # compute basic ranges 
        if args.predicate_sensitivity_promotion and args.parameter_domain_discretization:
            log_info(LOGGER_NAME, "Symbol basic ranges computing starts", center=True, symbol="*")
            symbol_basic_ranges = compute(args.scenario, args.template)
            log_info(LOGGER_NAME, f"Symbol basic ranges: {symbol_basic_ranges}")
            log_info(LOGGER_NAME, "Symbol basic ranges computing completes", center=True, symbol="*")
        else:
            symbol_basic_ranges = {}
        
        # solve
        log_info(LOGGER_NAME, "Solving process starts", center=True, symbol="*")
        assert solve_ctx2data is not None, "solve_ctx2data is None when has symbols"
        
        try:
            models = solve(
                constraint_path=decomp_template_path,
                bfuncs_path=decomp_bfuncs_path,
                restrictions_path=restrictions_path,
                solve_ctx2data=solve_ctx2data,
                data_field_types=data_field_types,
                concurrent=args.concurrent,
                parameter_domain_discretization=args.parameter_domain_discretization,
                predicate_sensitivity_promotion=args.predicate_sensitivity_promotion,
                symbol_basic_ranges=symbol_basic_ranges
            )
        except TimeoutException:
            models = None
        except Exception:
            models = []
        
        if models is None:
            log_warning(LOGGER_NAME, f"Solving process timeout in {SOLVE_TIMEOUT} seconds") 
        else:
            if len(models) > 0:
                dump_instantiation_solve(models, output_dir, decomp_template_path, decomp_bfuncs_path)
            log_info(LOGGER_NAME, f'{args.template} ({output_dir.parent.name}) has {len(models)} valid models')
                        
        log_info(LOGGER_NAME, "Solving process completes", center=True, symbol="*")        
    else:
        # validate
        log_info(LOGGER_NAME, "Validating process starts", center=True, symbol="*")
        assert validate_ctx2data is not None, "validate_ctx2data is None when no symbols"

        try:
            valid = validate(
                constraint_file_path=decomp_template_path,
                bfunc_file_path=decomp_bfuncs_path,
                validate_ctx2data=validate_ctx2data,
                data_field_types=data_field_types,
                concurrent=args.concurrent
            )
        except TimeoutException:
            valid = None
        except Exception:
            valid = False
        
        if valid is None:
            log_warning(LOGGER_NAME, f"Validating process timeout in {VALIDATE_TIMEOUT} seconds")
        else:
            if valid:
                dump_instantiation_validate(output_dir, decomp_template_path, decomp_bfuncs_path)
                log_info(LOGGER_NAME, f'{args.template} ({output_dir.parent.name}) is valid')
            else:
                log_info(LOGGER_NAME, f'{args.template} ({output_dir.parent.name}) is invalid')
        
        log_info(LOGGER_NAME, "Validating process completes", center=True, symbol="*")
        
    # Calculate and log instantiation time
    end_time = time.time()
    elapsed_time = end_time - start_time
    log_info(LOGGER_NAME, f'{args.template} ({output_dir.parent.name}) instantiation completes', center=True, symbol='=')
    log_info(LOGGER_NAME, f"Total instantiation time: {elapsed_time:.2f} seconds")
    clean_log_file_handler(LOGGER_NAME)

def instantiate_batch_templates(args):
    """Run batch mode - process multiple templates"""
    
    def _discover_templates(run_dirs: list[str], scenario: str) -> list[str]:
        """Discover all templates in the given converter run directories"""

        all_templates = []
        
        for run_dir in run_dirs:
            run_dir_path = _resolve_converter_dir(run_dir, scenario)
            log_info(LOGGER_NAME, f"Discovering templates in: {run_dir_path}")
            
            if not run_dir_path.exists() or not run_dir_path.is_dir():
                log_warning(LOGGER_NAME, f"Converter run directory {run_dir_path} does not exist, skipping")
                continue
            
            # Find all template_* directories
            template_pattern = str(run_dir_path / "template_*")
            template_dirs = glob.glob(template_pattern)
            templates = [Path(d).name for d in template_dirs if Path(d).is_dir()]
            
            if not templates:
                log_warning(LOGGER_NAME, f"No templates found in {run_dir_path}")
                continue
            
            # Create full template paths
            full_templates = [f"{run_dir}/{template}" for template in templates]
            all_templates.extend(full_templates)
            
            log_info(LOGGER_NAME, f"Found {len(templates)} templates in {run_dir}: {templates}")
        
        log_info(LOGGER_NAME, f"Total discovered templates: {len(all_templates)}")
        return all_templates
    
    start_time = time.time()
    
    log_info(LOGGER_NAME, "Starting batch instantiation", center=True, symbol='=')
    log_info(LOGGER_NAME, f"Scenario: {args.scenario}")
    log_info(LOGGER_NAME, f"Run directories: {args.run_dirs}")
    log_info(LOGGER_NAME, f"Data: {args.data}")
    log_info(LOGGER_NAME, f"Concurrent: {args.concurrent}")
    log_info(LOGGER_NAME, f"Parameter domain discretization: {'enabled' if args.parameter_domain_discretization else 'disabled'}")
    log_info(LOGGER_NAME, f"Predicate sensitivity promotion: {'enabled' if args.predicate_sensitivity_promotion else 'disabled'}")
    
    # Discover all templates
    templates = _discover_templates(args.run_dirs, args.scenario)
    
    if not templates:
        log_error(LOGGER_NAME, "No templates found in any converter directory")
        return
    
    # Statistics
    total_templates = len(templates)
    success_count = 0
    failure_count = 0
    failure_list = []
    
    # Process each template
    for template in templates:
        # Create args for single template
        single_args = argparse.Namespace(**vars(args))
        single_args.template = template
        single_args.run_dirs = None
        
        try:
            instantiate_single_template(single_args)
            success_count += 1
            log_info(LOGGER_NAME, f"Successfully processed: {template}")
        except Exception as e:
            failure_count += 1
            failure_list.append(template)
            log_error(LOGGER_NAME, f"Failed to process {template}: {str(e)}")
    
    # Summary
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    log_info(LOGGER_NAME, "Batch instantiation completed", center=True, symbol='=')
    log_info(LOGGER_NAME, f"Total templates: {total_templates}")
    log_info(LOGGER_NAME, f"Successful: {success_count}")
    log_info(LOGGER_NAME, f"Failed: {failure_count} ({failure_list})")
    log_info(LOGGER_NAME, f"Total time: {elapsed_time:.2f} seconds")
    log_info(LOGGER_NAME, f"Average time per template: {elapsed_time/total_templates:.2f} seconds")
        
    if failure_count > 0:
        log_warning(LOGGER_NAME, f"{failure_count} templates failed to process")

def dump_instantiation_solve(models: list[dict[str, Fraction|str]], output_dir: Path, decomp_template_path: Path, decomp_bfuncs_path: Path):
    instantiation_dir = output_dir / INSTANTIATION_DIR_NAME
    instantiation_dir.mkdir(parents=True, exist_ok=True)
    
    first_constraint_content = None
    first_bfuncs_content = None

    for index, model in enumerate(models):
        inst_constraint_file_path = instantiation_dir / f'{CONSTRAINT_XML_FILE_NAME.split(".")[0]}_i{index + 1}.xml'
        constraint_content = decomp_template_path.read_text()
        inst_constraint_file_path.write_text(constraint_content)
        
        inst_bfuncs_file_path = instantiation_dir / f'{BFUNC_FILE_NAME.split(".")[0]}_i{index + 1}.py'
        bfuncs_content = decomp_bfuncs_path.read_text()
        for symbol, value in model.items():
            # Format according to data type
            if isinstance(value, Fraction):
                # Keep fraction type as is; if denominator is 1, convert to integer representation
                if value.denominator == 1:
                    value_str = str(value.numerator)
                else:
                    value_str = str(value)
            elif isinstance(value, str):
                # Add quotes for string type
                value_str = f"'{value}'" if "'" not in value else f'"{value}"'
            else:
                raise ValueError(f"Unsupported value type: {type(value)}")
            
            # Use more precise replacement to avoid partial matches
            import re
            pattern = re.compile(r'\b' + re.escape(symbol) + r'\b')
            bfuncs_content = pattern.sub(value_str, bfuncs_content)
        
        inst_bfuncs_file_path.write_text(bfuncs_content)

        if index == 0:
            first_constraint_content = constraint_content
            first_bfuncs_content = bfuncs_content

    # Write the first instantiation directly to output_dir with clean file names
    if first_constraint_content is not None:
        (output_dir / CONSTRAINT_XML_FILE_NAME).write_text(first_constraint_content)
        (output_dir / BFUNC_FILE_NAME).write_text(first_bfuncs_content)
        
def dump_instantiation_validate(output_dir: Path, decomp_template_path: Path, decomp_bfuncs_path: Path):
    instantiation_dir = output_dir / INSTANTIATION_DIR_NAME
    instantiation_dir.mkdir(parents=True, exist_ok=True)
    
    constraint_content = decomp_template_path.read_text()
    bfuncs_content = decomp_bfuncs_path.read_text()

    inst_constraint_file_path = instantiation_dir / f'{CONSTRAINT_XML_FILE_NAME.split(".")[0]}_i1.xml'
    inst_constraint_file_path.write_text(constraint_content)
    
    inst_bfuncs_file_path = instantiation_dir / f'{BFUNC_FILE_NAME.split(".")[0]}_i1.py'
    inst_bfuncs_file_path.write_text(bfuncs_content)

    # Write directly to output_dir with clean file names
    (output_dir / CONSTRAINT_XML_FILE_NAME).write_text(constraint_content)
    (output_dir / BFUNC_FILE_NAME).write_text(bfuncs_content)

if __name__ == "__main__":
    args = parse_args()
    run(args)
    
    
