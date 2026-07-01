from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The rates of change in the speed value and direction value of v1 lie within a certain reasonable range."""
    return (abs(var_bindings["v1"]["speed"] - 0) <= 120) and (abs(var_bindings["v1"]["direction"] - 0) <= 360)

