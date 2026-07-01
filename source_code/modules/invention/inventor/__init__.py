from ...utils import OUTPUT_DIR

INVENTOR_OUTPUT_DIR = OUTPUT_DIR / "invention" / "inventor"

# File names
INTENT_AND_SEMANTICS_FILE_NAME = 'intent_and_semantics.json'
STRUCTURE_AND_SIGNATURES_FILE_NAME = 'structure_and_signatures.json'
BFUNC_IMPLEMENTATION_FILE_NAME = 'bfunc_implementation.json'
RESTRICTIONS_INVT_FILE_NAME = 'restrictions.json'
TEMPLATE_JSON_FILE_NAME = 'template.json'
TEMPLATE_DIR_PREFIX = 'template_'
STATISTICS_FILE_NAME = 'statistics.json'

# Rollback limits
MAX_REIMAGINE_ROLLBACK = 3  # Max number of reimagine rollbacks (semantics → template)
MAX_REWRITE_ROLLBACK = 3    # Max number of rewrite rollbacks (structure ↔ implementation)

# LLM retry limits
MAX_TRY_TIMES = 5  # Max number of LLM call attempts per phase

__all__ = [
    "INVENTOR_OUTPUT_DIR",
    "TEMPLATE_JSON_FILE_NAME",
    "TEMPLATE_DIR_PREFIX",
    "STATISTICS_FILE_NAME",
    "MAX_REIMAGINE_ROLLBACK",
    "MAX_REWRITE_ROLLBACK",
    "MAX_TRY_TIMES",
]
