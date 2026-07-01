import multiprocessing as mp
from pathlib import Path
from typing import Any, Optional

# Constants
INPUT_DIR = Path(__file__).parent.parent.parent / "inputs"
OUTPUT_DIR = Path(__file__).parent.parent.parent / "outputs"

SCENARIO_FILE_NAME = 'scenario.txt'
CONTEXT_DEFINITIONS_FILE_NAME = 'context_schema.toml'
SCOPES_DIR_NAME = 'scopes'
SCOPE_FILE_NAME = 'scope.txt'
FEW_SHOTS_DIR_NAME = 'few_shots'

BFUNC_PREFIX = 'bfunc_'
NUMERIC_SYMBOLIC_PREFIX = '_N_THRESHOLD_'
STRING_SYMBOLIC_PREFIX = '_S_THRESHOLD_'

CPU_COUNT: int = mp.cpu_count()

# Types
CTreeNode = tuple[str, str, dict[str, Any], Optional[list[Any]]] # (node_type, node_id, node_attrs, children)

# Export-Methods
from .data.construct_ctx_data import construct_ctx_data  # noqa: E402
from .data.load_data import load_data_field_types, get_data_size, generate_data_chunks  # noqa: E402
from .bfunc.decorate_bfunc import make_fractional, make_symbolic # noqa: E402
from .bfunc.load_bfunc import load_bfuncs, update_and_load_bfuncs, get_bfunc_nodes # noqa: E402
from .bfunc.analyze_bfunc import extract_symbols, analyze_bfunc_symbol_counts # noqa: E402
from .constraint.decompse_constraint import decompose # noqa: E402
from .constraint.parse_constraint import parse_constraint # noqa: E402
from .log import log_debug, log_info, log_warning, log_error, log_exception, set_log_file_handler, clean_log_file_handler, INVT_LOGGER_NAME, INST_LOGGER_NAME, CHCK_LOGGER_NAME # noqa: E402
from .timeout import timeout_process, timeout_thread, TimeoutException # noqa: E402

__all__ = [
    "CONTEXT_DEFINITIONS_FILE_NAME",
    "BFUNC_PREFIX",
    "NUMERIC_SYMBOLIC_PREFIX",
    "STRING_SYMBOLIC_PREFIX",
    "CPU_COUNT",
    
    "CTreeNode",
    
    "construct_ctx_data",
    "load_data_field_types",
    "get_data_size",
    "generate_data_chunks",
    "make_fractional",
    "make_symbolic",
    "load_bfuncs",
    "update_and_load_bfuncs",
    "get_bfunc_nodes",
    "extract_symbols",
    "analyze_bfunc_symbol_counts",
    "decompose",
    "parse_constraint",
    "log_debug",
    "log_info",
    "log_warning",
    "log_error",
    "log_exception",
    "set_log_file_handler",
    "clean_log_file_handler",
    "INVT_LOGGER_NAME",
    "INST_LOGGER_NAME",
    "CHCK_LOGGER_NAME",
    
    "timeout_process",
    "timeout_thread",
    "TimeoutException"
]