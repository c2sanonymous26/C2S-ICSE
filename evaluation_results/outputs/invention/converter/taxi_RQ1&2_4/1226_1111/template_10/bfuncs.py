from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1's speed is significantly higher than a certain threshold"""
    return var_bindings["v1"]["speed"] > _N_THRESHOLD_1

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v2 belongs to the same vehicle and is the previous context of v1"""
    return (var_bindings["v2"]["carid"] == var_bindings["v1"]["carid"]) and (var_bindings["v2"]["grpid"] == var_bindings["v1"]["grpid"] - 1)

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the coordinate displacement between v1 and v2 does not exceed a certain threshold"""
    return pow(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"], 2) + pow(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"], 2) <= _N_THRESHOLD_2

