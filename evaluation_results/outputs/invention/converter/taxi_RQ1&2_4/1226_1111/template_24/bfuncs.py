from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle and are consecutive contexts"""
    return (var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]) and (abs(var_bindings["v1"]["grpid"] - var_bindings["v2"]["grpid"]) == 1)

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """both v1 and v2 have zero speed"""
    return (var_bindings["v1"]["speed"] == 0) and (var_bindings["v2"]["speed"] == 0)

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the absolute direction difference between v1 and v2 does not exceed a negligibly small range"""
    return abs(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"]) <= _N_THRESHOLD_1

