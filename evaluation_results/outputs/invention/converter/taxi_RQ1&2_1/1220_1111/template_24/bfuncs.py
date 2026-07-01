from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle"""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 are consecutive contexts of that vehicle"""
    return abs(var_bindings["v1"]["grpid"] - var_bindings["v2"]["grpid"]) == 1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the ratio of the absolute speed difference between v1 and v2 to their timestamp difference does not exceed a certain reasonable acceleration upper bound"""
    return abs(var_bindings["v1"]["speed"] - var_bindings["v2"]["speed"]) / (var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"]) <= _N_THRESHOLD_1

