from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same taxi (same carid)"""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 are consecutive records of that taxi (grpid of v2 equals grpid of v1 plus 1)"""
    return var_bindings["v2"]["grpid"] == var_bindings["v1"]["grpid"] + 1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the speed in v1 is above a certain low threshold"""
    return var_bindings["v1"]["speed"] > 10.0

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the absolute difference in speed between v2 and v1 divided by the speed in v1 does not exceed a certain maximum relative change threshold"""
    return abs(var_bindings["v2"]["speed"] - var_bindings["v1"]["speed"]) / var_bindings["v1"]["speed"] <= 2.0

