from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1, v2, and v3 belong to the same vehicle"""
    return (var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]) and (var_bindings["v2"]["carid"] == var_bindings["v3"]["carid"])

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1, v2, and v3 are three consecutive contexts"""
    return (abs(var_bindings["v1"]["grpid"] - var_bindings["v2"]["grpid"]) == 1) and (abs(var_bindings["v2"]["grpid"] - var_bindings["v3"]["grpid"]) == 1)

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """both v1 and v3 have speeds significantly higher than a certain threshold"""
    return (var_bindings["v1"]["speed"] > _N_THRESHOLD_1) and (var_bindings["v3"]["speed"] > _N_THRESHOLD_1)

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v2's speed is significantly lower than the average of v1 and v3's speeds"""
    return var_bindings["v2"]["speed"] < ((var_bindings["v1"]["speed"] + var_bindings["v3"]["speed"]) / 2) - _N_THRESHOLD_2

