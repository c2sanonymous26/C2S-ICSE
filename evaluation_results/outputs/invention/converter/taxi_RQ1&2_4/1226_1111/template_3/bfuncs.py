from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1's speed is zero"""
    return var_bindings["v1"]["speed"] == 0

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v2 is the next context of v1"""
    return (var_bindings["v2"]["grpid"] == var_bindings["v1"]["grpid"] + 1) and (var_bindings["v2"]["carid"] == var_bindings["v1"]["carid"])

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the coordinates of v1 and v2 are the same"""
    return (var_bindings["v1"]["latitude"] == var_bindings["v2"]["latitude"]) and (var_bindings["v1"]["longitude"] == var_bindings["v2"]["longitude"])

