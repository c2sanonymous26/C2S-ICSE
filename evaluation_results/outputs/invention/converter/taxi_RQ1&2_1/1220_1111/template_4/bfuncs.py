from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle and v2 is the next consecutive context after v1"""
    return (var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]) and (var_bindings["v1"]["grpid"] + 1 == var_bindings["v2"]["grpid"])

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the speed difference and direction change between v1 and v2 are within a reasonable range"""
    return (abs(var_bindings["v2"]["speed"] - var_bindings["v1"]["speed"]) <= _N_THRESHOLD_1) and (abs(var_bindings["v2"]["direction"] - var_bindings["v1"]["direction"]) <= _N_THRESHOLD_2)

