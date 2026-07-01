import argparse
import time

from . import LOGGER_NAME
from .inventor import __main__ as inventor_main
from .inventor import INVENTOR_OUTPUT_DIR
from .converter import __main__ as converter_main
from ..utils import log_info, log_error, log_warning

def parse_args():
    parser = argparse.ArgumentParser(description='Invention Module')
    
    parser.add_argument('--scenario', '-s', required=True, help='scenario name')
    parser.add_argument('--scope', default='NS', help='constraint scope')
    parser.add_argument('--invent-times', type=int, required=True, help='invention times')
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
    
    start_time = time.time()
    
    # Step 1: Run inventor    
    inventor_output_dir = inventor_main.run(args)
    if inventor_output_dir is None:
        log_error(LOGGER_NAME, "Error: Template invention failed")
        return
        
    # Step 2: Run converter
    converter_args = argparse.Namespace()
    converter_args.scenario = args.scenario
    converter_args.convert_dirs = [inventor_output_dir]
    converter_main.run(converter_args)

    end_time = time.time()
    log_info(LOGGER_NAME, f"Invention and conversion done in {end_time - start_time} seconds")


if __name__ == "__main__":
    args = parse_args()
    run(args) 