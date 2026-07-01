from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the speed of v1 is significantly higher than a certain threshold"""
    return var_bindings["v1"]["speed"] > _N_THRESHOLD_1

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v2 belongs to the same vehicle and is the next consecutive context after v1"""
    return (var_bindings["v2"]["carid"] == var_bindings["v1"]["carid"]) and (var_bindings["v2"]["grpid"] == var_bindings["v1"]["grpid"] + 1)

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the ratio of the absolute speed difference between v1 and v2 to their timestamp difference does not exceed a certain reasonable upper bound"""
    return abs(var_bindings["v1"]["speed"] - var_bindings["v2"]["speed"]) / (var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"]) <= _N_THRESHOLD_2

