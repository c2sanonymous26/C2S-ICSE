from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 are distinct contexts"""
    return var_bindings["v1"]["id"] != var_bindings["v2"]["id"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle"""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the absolute difference between the timestamps of v1 and v2 is sufficiently small"""
    return abs(var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"]) <= 1.0

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the absolute difference between the instantaneous speeds recorded in v1 and v2 is sufficiently small"""
    return abs(var_bindings["v1"]["speed"] - var_bindings["v2"]["speed"]) <= 10.0

