from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle"""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 are consecutive contexts of that vehicle"""
    return (var_bindings["v1"]["grpid"] + 1 == var_bindings["v2"]["grpid"]) or (var_bindings["v2"]["grpid"] + 1 == var_bindings["v1"]["grpid"])

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the displacement bearing derived from the coordinate differences of v1 and v2 is close to the average of the directions of v1 and v2 within a certain reasonable range"""
    return abs(degrees(atan2(sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"])) * cos(radians(var_bindings["v2"]["latitude"])), cos(radians(var_bindings["v1"]["latitude"])) * sin(radians(var_bindings["v2"]["latitude"])) - sin(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v2"]["latitude"])) * cos(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"])))) - ((var_bindings["v1"]["direction"] + var_bindings["v2"]["direction"]) / 2)) <= _N_THRESHOLD_1

