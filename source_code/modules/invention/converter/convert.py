from typing import Any
from pathlib import Path
import time

from ...utils import log_info
from .. import LOGGER_NAME
from ..statistics import ConverterStatistics
from . import STATISTICS_FILE_NAME
from .convert_structure import convert_structure
from .convert_bfuncs import convert_bfuncs


def convert_to_files(
    template_dir: Path, 
    dataset_file_path: Path, 
    template: dict[str, Any], 
    output_dir: Path
) -> None:
    
    log_info(LOGGER_NAME, f"Converting {template_dir.name} in {template_dir.parent} starts", center=True, symbol="~")
    
    # Create statistics object
    stats = ConverterStatistics()
    start_time = time.time()
    
    try:
        # Convert template structure
        convert_structure(template['semantics'], template['structure'], output_dir)
        
        # Convert bfuncs
        convert_bfuncs(template['bfuncs'], dataset_file_path, output_dir)
        
        stats.success = True
        
    finally:
        # Record total time and save statistics
        stats.total_time = time.time() - start_time
        stats.save_to_file(output_dir / STATISTICS_FILE_NAME)
        log_info(LOGGER_NAME, f"Statistics saved to {output_dir / STATISTICS_FILE_NAME}")
    
    log_info(LOGGER_NAME, f"Converting {template_dir.name} in {template_dir.parent} done", center=True, symbol="~", newlines=1)
