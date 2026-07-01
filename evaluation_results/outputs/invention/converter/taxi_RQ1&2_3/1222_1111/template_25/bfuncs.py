from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle"""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 are consecutive contexts of that vehicle"""
    return abs(var_bindings["v1"]["grpid"] - var_bindings["v2"]["grpid"]) == 1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1's speed is zero"""
    return var_bindings["v1"]["speed"] == 0

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the coordinates of v2 are the same as those of v1"""
    return (var_bindings["v1"]["latitude"] == var_bindings["v2"]["latitude"]) and (var_bindings["v1"]["longitude"] == var_bindings["v2"]["longitude"])

