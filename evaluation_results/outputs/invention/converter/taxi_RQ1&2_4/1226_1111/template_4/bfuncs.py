from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle"""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 are consecutive contexts of that vehicle"""
    return var_bindings["v1"]["grpid"] + 1 == var_bindings["v2"]["grpid"]

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the angle between the coordinate displacement direction and the direction angle change direction of v1 and v2 does not exceed a certain reasonable range"""
    return abs(degrees(atan2(sin(radians(var_bindings["v2"]["direction"] - var_bindings["v1"]["direction"])), cos(radians(var_bindings["v1"]["direction"])) * cos(radians(var_bindings["v2"]["direction"])) + sin(radians(var_bindings["v1"]["direction"])) * sin(radians(var_bindings["v2"]["direction"])))) - degrees(atan2(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"], var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]))) <= _N_THRESHOLD_1

