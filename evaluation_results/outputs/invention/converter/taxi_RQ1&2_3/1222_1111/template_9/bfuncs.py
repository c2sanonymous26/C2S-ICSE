from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle"""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 are consecutive contexts of that vehicle"""
    return var_bindings["v1"]["grpid"] + 1 == var_bindings["v2"]["grpid"]

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1's speed is significantly higher than a certain threshold"""
    return var_bindings["v1"]["speed"] > _N_THRESHOLD_1

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v2's speed is less than or equal to v1's speed"""
    return var_bindings["v2"]["speed"] <= var_bindings["v1"]["speed"]

