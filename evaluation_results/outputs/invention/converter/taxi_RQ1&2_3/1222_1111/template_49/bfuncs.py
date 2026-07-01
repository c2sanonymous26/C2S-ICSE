from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle"""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 are consecutive contexts of that vehicle"""
    return abs(var_bindings["v1"]["grpid"] - var_bindings["v2"]["grpid"]) == 1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1's speed is zero while v2's speed is non-zero"""
    return (var_bindings["v1"]["speed"] == 0) and (var_bindings["v2"]["speed"] > 0)

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the coordinate differences between v1 and v2 are within a certain smaller reasonable range"""
    return pow(abs(var_bindings["v1"]["latitude"] - var_bindings["v2"]["latitude"]), 2) + pow(abs(var_bindings["v1"]["longitude"] - var_bindings["v2"]["longitude"]), 2) <= _N_THRESHOLD_1

def bfunc_5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v2's direction is the same as v1's direction"""
    return var_bindings["v1"]["direction"] == var_bindings["v2"]["direction"]

