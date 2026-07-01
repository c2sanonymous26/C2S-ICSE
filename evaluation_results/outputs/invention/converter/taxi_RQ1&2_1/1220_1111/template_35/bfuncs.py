from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the speed of v1 is significantly below a certain threshold"""
    return var_bindings["v1"]["speed"] < _N_THRESHOLD_1

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v2 is the next context of v1 (same vehicle)"""
    return (var_bindings["v2"]["grpid"] == var_bindings["v1"]["grpid"] + 1) and (var_bindings["v2"]["carid"] == var_bindings["v1"]["carid"])

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the absolute heading difference between v1 and v2 does not exceed a certain reasonable range"""
    return abs(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"]) <= _N_THRESHOLD_2

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the timestamp difference between v1 and v2 does not exceed a certain reasonable time range"""
    return var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"] <= _N_THRESHOLD_3

