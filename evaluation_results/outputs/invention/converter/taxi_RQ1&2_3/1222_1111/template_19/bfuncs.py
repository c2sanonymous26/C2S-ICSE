from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle"""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 are consecutive contexts of that vehicle"""
    return abs(var_bindings["v1"]["grpid"] - var_bindings["v2"]["grpid"]) == 1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """both v1 and v2 have speeds significantly higher than a certain threshold"""
    return (var_bindings["v1"]["speed"] > _N_THRESHOLD_1) and (var_bindings["v2"]["speed"] > _N_THRESHOLD_1)

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the absolute direction difference between v1 and v2 is within a certain smaller reasonable range"""
    return abs(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"]) <= _N_THRESHOLD_2

