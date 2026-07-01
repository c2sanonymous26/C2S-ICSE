from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The speed of v1 is significantly higher than a certain threshold."""
    return var_bindings["v1"]["speed"] > _N_THRESHOLD_1

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v2 belongs to the same vehicle and the grpid value of v2 is 1 smaller than that of v1."""
    return (var_bindings["v2"]["carid"] == var_bindings["v1"]["carid"]) and (var_bindings["v2"]["grpid"] == var_bindings["v1"]["grpid"] - 1)

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The direction-angle change rate between v1 and v2 computed from direction angle and timestamps does not exceed a certain reasonable upper bound."""
    return abs(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"]) / (var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"]) <= _N_THRESHOLD_2

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The speed-change rate between v1 and v2 computed from speed and timestamps does not exceed a certain reasonable upper bound."""
    return abs(var_bindings["v1"]["speed"] - var_bindings["v2"]["speed"]) / (var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"]) <= _N_THRESHOLD_3

