# Types
Link = frozenset[tuple[str, str]]    
ValidationResult = tuple[bool, frozenset[Link]]

# Constants
ILLEGAL_DATA_RATIO_BOUND: float = 0.005

# Functions
from .validate import validate, VALIDATE_TIMEOUT # noqa: E402

__all__ = [
    "validate",
    "VALIDATE_TIMEOUT"
]