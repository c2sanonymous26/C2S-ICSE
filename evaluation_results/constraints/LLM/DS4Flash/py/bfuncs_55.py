from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same taxi (same carid)"""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 are consecutive records (grpid of v2 equals grpid of v1 plus 1)"""
    return var_bindings["v2"]["grpid"] == var_bindings["v1"]["grpid"] + 1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the speed in v1 is above a certain threshold"""
    return var_bindings["v1"]["speed"] > 110.0

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the time difference (timestamp of v2 minus timestamp of v1) is below a certain maximum"""
    return var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"] < 22.0

