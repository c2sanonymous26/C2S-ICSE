import argparse
import json
import shutil
from pathlib import Path

from ...utils import (
    log_warning,
    INPUT_DIR, 
    CONTEXT_DEFINITIONS_FILE_NAME
)
from ..inventor import (
    INVENTOR_OUTPUT_DIR,
    TEMPLATE_JSON_FILE_NAME,
    TEMPLATE_DIR_PREFIX,
)
from .. import LOGGER_NAME
from .convert import convert_to_files
from . import CONVERTER_OUTPUT_DIR


def _resolve_inventor_dir(dir_arg: str, scenario: str) -> Path:
    """Resolve an inventor directory argument against the current workspace layout.

    Current results live under outputs/invention/inventor/<rq_dir>/..., while some
    older callers may still pass paths as if a scenario layer existed. Support both.
    """
    direct_path = INVENTOR_OUTPUT_DIR / dir_arg
    if direct_path.exists():
        return direct_path

    legacy_path = INVENTOR_OUTPUT_DIR / scenario / dir_arg
    if legacy_path.exists():
        return legacy_path

    return direct_path


def parse_args():
    parser = argparse.ArgumentParser(description='converter argument parser')

    parser.add_argument('--scenario', '-s', required=True, type=str, help='specify the scenario')

    # Mutually exclusive: either specify directories or a single template
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--convert-dirs', nargs='+', help='specify directories to convert')
    group.add_argument('--convert-template', type=str,
                      help='specify a single template in format: converter_dir/template_name')

    args = parser.parse_args()

    # Directory mode
    if args.convert_dirs:
        dirs_list = []
        for dir in args.convert_dirs:
            dir_path = _resolve_inventor_dir(dir, args.scenario)
            if not dir_path.exists():
                log_warning(LOGGER_NAME, f"Directory {dir_path} does not exist, ignored")
            else:
                dirs_list.append(dir_path)
        args.convert_dirs = dirs_list

    # Single template mode
    elif args.convert_template:
        # Parse converter_dir/template_name format
        if '/' not in args.convert_template:
            raise ValueError(f"Invalid template format: {args.convert_template}. Expected: converter_dir/template_name")

        converter_dir, template_name = args.convert_template.rsplit('/', 1)

        # Validate template name format
        if not template_name.startswith(TEMPLATE_DIR_PREFIX):
            raise ValueError(
                f"Invalid template name: {template_name}. Expected format: {TEMPLATE_DIR_PREFIX}*"
            )

        # Build full paths
        converter_dir_path = _resolve_inventor_dir(converter_dir, args.scenario)
        template_dir_path = converter_dir_path / template_name

        if not converter_dir_path.exists():
            raise FileNotFoundError(f"Converter directory {converter_dir_path} does not exist")

        if not template_dir_path.exists():
            raise FileNotFoundError(f"Template directory {template_dir_path} does not exist")

        # Set processing parameters
        args.single_template_mode = True
        args.converter_dir = converter_dir_path
        args.converter_dir_relative = converter_dir_path.relative_to(INVENTOR_OUTPUT_DIR)
        args.template_name = template_name

    return args


def run(args):

    dataset_file_path = INPUT_DIR / args.scenario / CONTEXT_DEFINITIONS_FILE_NAME
    if not dataset_file_path.exists():
        raise FileNotFoundError(f"Dataset file {dataset_file_path} does not exist")

    # Single template mode
    if hasattr(args, 'single_template_mode') and args.single_template_mode:
        template_dir = args.converter_dir / args.template_name
        template_file_path = template_dir / TEMPLATE_JSON_FILE_NAME

        if not template_file_path.exists():
            raise FileNotFoundError(f"Template file {template_file_path} does not exist")

        # Build output dir mirroring inventor layout under outputs/invention/converter.
        output_dir = CONVERTER_OUTPUT_DIR / args.converter_dir_relative / args.template_name
        if output_dir.exists():
            log_warning(LOGGER_NAME, f"Output directory {output_dir} already exists, remove it")
            shutil.rmtree(output_dir)
        output_dir.mkdir(parents=True, exist_ok=False)

        template = json.loads(template_file_path.read_text())
        convert_to_files(template_dir, dataset_file_path, template, output_dir)

    # Directory mode
    else:
        for dir in args.convert_dirs:

            output_dir = CONVERTER_OUTPUT_DIR / dir.relative_to(INVENTOR_OUTPUT_DIR)
            if output_dir.exists():
                log_warning(LOGGER_NAME, f"Output directory {output_dir} already exists, remove it")
                shutil.rmtree(output_dir)
            output_dir.mkdir(parents=True, exist_ok=False)

            for template_dir in dir.iterdir():
                if template_dir.is_dir() and template_dir.name.startswith(TEMPLATE_DIR_PREFIX):
                    template_file_path = template_dir / TEMPLATE_JSON_FILE_NAME

                    if not template_file_path.exists():
                        log_warning(LOGGER_NAME, f"Template file {template_file_path} does not exist, ignored")
                    else:

                        template_output_dir = output_dir / template_dir.name
                        if template_output_dir.exists():
                            log_warning(LOGGER_NAME, f"Template output directory {template_output_dir} already exists, remove it")
                            shutil.rmtree(template_output_dir)
                        template_output_dir.mkdir(parents=True, exist_ok=False)

                        template = json.loads(template_file_path.read_text())
                        convert_to_files(template_dir, dataset_file_path, template, template_output_dir)


if __name__ == "__main__":
    args = parse_args()
    run(args)
