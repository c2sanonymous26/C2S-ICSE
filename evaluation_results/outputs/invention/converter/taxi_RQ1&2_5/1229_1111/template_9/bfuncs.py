from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the speed of v1 is significantly higher than some threshold"""
    return var_bindings["v1"]["speed"] > _N_THRESHOLD_1

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v2 belongs to the same vehicle and the grpid of v2 is smaller than that of v1 by 1"""
    return (var_bindings["v2"]["carid"] == var_bindings["v1"]["carid"]) and (var_bindings["v2"]["grpid"] == var_bindings["v1"]["grpid"] - 1)

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the ratio of the speed difference between v1 and v2 to their timestamp difference (i.e., deceleration) is significantly greater than some lower bound"""
    return (var_bindings["v1"]["speed"] - var_bindings["v2"]["speed"]) / (var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"]) > _N_THRESHOLD_2

