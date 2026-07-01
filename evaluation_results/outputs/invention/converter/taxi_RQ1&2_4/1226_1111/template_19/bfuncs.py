from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle"""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 are consecutive contexts of that vehicle"""
    return abs(var_bindings["v1"]["grpid"] - var_bindings["v2"]["grpid"]) == 1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """both v1 and v2 have non-zero speed"""
    return (var_bindings["v1"]["speed"] > 0) and (var_bindings["v2"]["speed"] > 0)

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the product of the average of the instantaneous speeds and the absolute direction difference of v1 and v2 does not exceed a certain reasonable range"""
    return ((var_bindings["v1"]["speed"] + var_bindings["v2"]["speed"]) / 2) * abs(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"]) <= _N_THRESHOLD_1

