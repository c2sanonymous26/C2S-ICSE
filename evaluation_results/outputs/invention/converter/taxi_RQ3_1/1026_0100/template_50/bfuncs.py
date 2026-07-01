from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The direction angle value of v1 is between 0° and 360°."""
    return (var_bindings["v1"]["direction"] >= 0) and (var_bindings["v1"]["direction"] <= 360)

