from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The rate of change in the longitude and latitude values of v1 lies within a certain reasonable range."""
    return (abs(var_bindings["v1"]["longitude"] - 0) <= 1) and (abs(var_bindings["v1"]["latitude"] - 0) <= 1)

