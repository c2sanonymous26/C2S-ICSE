from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same taxi (same carid) and are consecutive records (grpid of v2 equals grpid of v1 plus 1)"""
    return (var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]) and (var_bindings["v2"]["grpid"] - var_bindings["v1"]["grpid"] == 1)

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the speed in v1 is above a certain threshold"""
    return var_bindings["v1"]["speed"] > 0.0

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the time difference (timestamp of v2 minus timestamp of v1) is positive"""
    return var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"] > 0

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the product of the speed in v1 and the absolute angular difference between the direction in v1 and the direction in v2 divided by the time difference does not exceed a certain maximum lateral acceleration"""
    return (var_bindings["v1"]["speed"] * abs(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"])) / (var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"]) <= 1100.0

