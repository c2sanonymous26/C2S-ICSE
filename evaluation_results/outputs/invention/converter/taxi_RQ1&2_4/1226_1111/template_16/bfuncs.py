from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle"""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 is the immediately preceding context of v2"""
    return (var_bindings["v2"]["grpid"] == var_bindings["v1"]["grpid"] + 1) and (var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"])

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """both v1 and v2 have non-zero speed"""
    return (var_bindings["v1"]["speed"] > 0) and (var_bindings["v2"]["speed"] > 0)

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the coordinate displacement direction and the direction angle change direction of v1 and v2 are consistent"""
    return (abs(degrees(atan2(sin(radians(var_bindings["v2"]["direction"] - var_bindings["v1"]["direction"])), cos(radians(var_bindings["v2"]["direction"] - var_bindings["v1"]["direction"]))))) <= _N_THRESHOLD_1) and (abs(degrees(atan2(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"], var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"])) - degrees(atan2(sin(radians(var_bindings["v2"]["direction"] - var_bindings["v1"]["direction"])), cos(radians(var_bindings["v2"]["direction"] - var_bindings["v1"]["direction"]))))) <= _N_THRESHOLD_2)

