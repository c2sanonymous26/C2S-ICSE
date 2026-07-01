from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The grpid recorded in context v1 lies within a valid and reasonable sequence-number range."""
    return (var_bindings["v1"]["grpid"] >= 13.0) and (var_bindings["v1"]["grpid"] <= 205.0)

