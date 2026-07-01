"""AR+ baseline entry point.

Usage:
python -m modules.baseline.ar_plus --data-file inputs/taxi/data/5000.csv --run-times 10 --output-dir constraints/ar_plus_run

Features:
- Randomly selects mode (single/pairwise/carid_join) for each run
- Randomly selects comparison operator (eq/le/lt/ge/gt) for each run
- Randomly selects one target column for constraint mining in each run
"""

import argparse
import logging
import time
import random
from pathlib import Path

from .pipeline import ARPlusPipeline
from . import AVAILABLE_MODES, AVAILABLE_CMPS, LEVEL1_SEPARATOR


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="AR+ baseline constraint generation")
    parser.add_argument("--run-times", type=int, required=True,
                        help="Number of runs")
    parser.add_argument(
        "--data-file",
        type=Path,
        required=True,
        help="CSV input file.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Output constraint directory.",
    )
    parser.add_argument(
        "--scope",
        choices=AVAILABLE_MODES,
        help="Fix AR+ to one scope/mode. If omitted, AR+ randomly samples from all supported scopes.",
    )
    
    return parser.parse_args()


def setup_logging(log_file_path: Path = None):
    """Setup logging configuration, supports creating separate log files for each run
    
    Args:
        log_file_path: Log file path, if None only output to console
    """
    # Get root logger
    logger = logging.getLogger()
    
    # Clean existing handlers to prevent duplicates
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)
    
    # Set log level and format
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # Add console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Add file handler if log file path is specified
    if log_file_path:
        log_file_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file_path, mode='w', encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)


def get_project_paths(script_file: Path):
    """Get project paths"""
    script_dir = script_file.parent.resolve()
    proj_dir = next(
        parent for parent in [script_dir, *script_dir.parents]
        if (parent / "modules").is_dir()
    )
    return script_dir, proj_dir


def main():
    """Main function"""
    
    start_time = time.time()
    args = parse_arguments()
    setup_logging()
    
    _, proj_dir = get_project_paths(Path(__file__))
    
    output_dir = args.output_dir
    if not output_dir.is_absolute():
        output_dir = proj_dir / output_dir
    raw_output_dir = output_dir / "raw"
    raw_output_dir.mkdir(parents=True, exist_ok=True)

    data_file_path = args.data_file
    if not data_file_path.is_absolute():
        data_file_path = proj_dir / data_file_path
    if not data_file_path.exists():
        logging.error(f"Data file not found: {data_file_path}")
        return False
    
    logging.info(f"Data file: {data_file_path}")
    logging.info(f"Number of runs: {args.run_times}")
    logging.info(f"Available modes: {AVAILABLE_MODES}")
    logging.info(f"Available comparisons: {AVAILABLE_CMPS}")
    if args.scope:
        logging.info(f"Fixed scope/mode: {args.scope}")
    
    successful_runs = 0
    for run_idx in range(args.run_times):
        mode = args.scope if args.scope else random.choice(AVAILABLE_MODES)
        cmp = random.choice(AVAILABLE_CMPS)
        
        # Setup separate log file for current run
        log_file = raw_output_dir / f"constraint_{run_idx + 1}.log"
        setup_logging(log_file)
        
        logging.info(LEVEL1_SEPARATOR)
        logging.info(f"Starting run {run_idx + 1}/{args.run_times}")
        logging.info(f"Mode: {mode}, Comparison: {cmp}")
        
        try:
            pipeline = ARPlusPipeline(
                mode=mode,
                cmp=cmp,
                output_dir=raw_output_dir
            )
            success = pipeline.run_once(data_file_path, run_idx + 1)
            if success:
                logging.info(f"Run {run_idx + 1} successfully generated constraint")
                successful_runs += 1
            else:
                logging.warning(f"Run {run_idx + 1} failed to generate constraint")
                
        except Exception as e:
            logging.error(f"Exception occurred in run {run_idx + 1}: {e}")
            import traceback
            logging.error(traceback.format_exc())
        finally:
            logging.info(LEVEL1_SEPARATOR)
        
    setup_logging()
    logging.info(f"AR+ completed: {successful_runs}/{args.run_times} constraints successfully generated")
    logging.info(f"Total runtime: {time.time() - start_time:.2f}s")
    
    return successful_runs > 0


if __name__ == "__main__":
    main() 
