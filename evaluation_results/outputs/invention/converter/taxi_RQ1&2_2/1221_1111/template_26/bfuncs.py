from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the speed of v1 is zero and its heading is non-zero"""
    return (var_bindings["v1"]["speed"] == 0) and (var_bindings["v1"]["direction"] != 0)

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v2 belongs to the same vehicle and is the next consecutive context after v1"""
    return (var_bindings["v2"]["carid"] == var_bindings["v1"]["carid"]) and (var_bindings["v2"]["grpid"] == var_bindings["v1"]["grpid"] + 1)

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the speed of v2 is zero"""
    return var_bindings["v2"]["speed"] == 0

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the heading of v2 is the same as the heading of v1"""
    return var_bindings["v2"]["direction"] == var_bindings["v1"]["direction"]

