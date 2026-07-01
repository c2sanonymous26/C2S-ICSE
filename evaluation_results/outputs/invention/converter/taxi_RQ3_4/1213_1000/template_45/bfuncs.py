from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle."""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 are two adjacent contexts of that vehicle."""
    return abs(var_bindings["v1"]["grpid"] - var_bindings["v2"]["grpid"]) == 1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The sign of the ratio between the absolute speed difference and the timestamp difference of v1 and v2, that is, the acceleration-like quantity, should be consistent with the sign of their direction difference."""
    return implies(((var_bindings["v2"]["speed"] - var_bindings["v1"]["speed"]) / (var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"]) > 0), ((var_bindings["v2"]["direction"] - var_bindings["v1"]["direction"]) > 0))

