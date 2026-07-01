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
    return (var_bindings["v1"]["speed"] != 0) and (var_bindings["v2"]["speed"] != 0)

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the angle between the coordinate displacement direction and the direction angle change direction does not exceed a certain reasonable range"""
    return abs(degrees(atan2(sin(radians(var_bindings["v2"]["direction"] - var_bindings["v1"]["direction"])), cos(radians(var_bindings["v1"]["direction"])) * cos(radians(var_bindings["v2"]["direction"])) + sin(radians(var_bindings["v1"]["direction"])) * sin(radians(var_bindings["v2"]["direction"])))) - degrees(atan2(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"], var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]))) <= _N_THRESHOLD_1

