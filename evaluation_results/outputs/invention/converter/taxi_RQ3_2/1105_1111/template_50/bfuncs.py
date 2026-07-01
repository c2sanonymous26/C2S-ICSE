from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The speed of v1 is 0."""
    return var_bindings["v1"]["speed"] == 0

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle, and v2 is the next context of v1."""
    return (var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]) and (var_bindings["v2"]["grpid"] == var_bindings["v1"]["grpid"] + 1)

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The product of the absolute speed difference between v1 and v2 and the absolute difference in direction angle between them should lie within a certain reasonable range."""
    return abs(var_bindings["v1"]["speed"] - var_bindings["v2"]["speed"]) * abs(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"]) <= _N_THRESHOLD_2

