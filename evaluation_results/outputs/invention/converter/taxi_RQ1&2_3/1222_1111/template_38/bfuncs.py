from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1, v2, and v3 belong to the same vehicle"""
    return (var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]) and (var_bindings["v2"]["carid"] == var_bindings["v3"]["carid"])

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1, v2, and v3 are three consecutive contexts"""
    return (var_bindings["v1"]["grpid"] + 1 == var_bindings["v2"]["grpid"]) and (var_bindings["v2"]["grpid"] + 1 == var_bindings["v3"]["grpid"])

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """both v1 and v3 have speeds significantly lower than a certain threshold while v2's speed is significantly higher than a certain threshold"""
    return (var_bindings["v1"]["speed"] < _N_THRESHOLD_1) and ((var_bindings["v3"]["speed"] < _N_THRESHOLD_1) and (var_bindings["v2"]["speed"] > _N_THRESHOLD_2))

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the coordinate differences between v1 and v3 are within a certain smaller reasonable range"""
    return sqrt(pow(var_bindings["v1"]["latitude"] - var_bindings["v3"]["latitude"], 2) + pow(var_bindings["v1"]["longitude"] - var_bindings["v3"]["longitude"], 2)) <= _N_THRESHOLD_3

