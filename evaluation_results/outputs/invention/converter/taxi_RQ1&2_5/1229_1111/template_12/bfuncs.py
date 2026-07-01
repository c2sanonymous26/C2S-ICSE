from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the speed of v1 is 0"""
    return var_bindings["v1"]["speed"] == 0

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v2 belongs to the same vehicle and the grpid of v2 is smaller than that of v1 by 1"""
    return (var_bindings["v2"]["carid"] == var_bindings["v1"]["carid"]) and (var_bindings["v2"]["grpid"] == var_bindings["v1"]["grpid"] - 1)

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the absolute difference between the direction of v1 and the direction of v2 does not exceed some upper bound"""
    return abs(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"]) <= _N_THRESHOLD_1

