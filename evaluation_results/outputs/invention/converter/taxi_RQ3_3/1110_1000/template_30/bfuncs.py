from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle."""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The timestamp difference between v1 and v2 lies within a certain range."""
    return abs(var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"]) <= _N_THRESHOLD_1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The product of the average acceleration and the direction-change rate computed from v1 and v2 does not exceed a certain reasonable range."""
    return ((var_bindings["v2"]["speed"] - var_bindings["v1"]["speed"]) / (var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"])) * (abs(var_bindings["v2"]["direction"] - var_bindings["v1"]["direction"]) / (var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"])) <= _N_THRESHOLD_2

