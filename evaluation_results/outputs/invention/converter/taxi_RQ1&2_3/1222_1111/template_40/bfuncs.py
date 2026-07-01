from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1, v2, and v3 belong to the same vehicle and are three consecutive contexts"""
    return (var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]) and ((var_bindings["v1"]["carid"] == var_bindings["v3"]["carid"]) and (((var_bindings["v2"]["grpid"] - var_bindings["v1"]["grpid"]) == 1) and ((var_bindings["v3"]["grpid"] - var_bindings["v2"]["grpid"]) == 1)))

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """both v1 and v3 have speeds significantly higher than a certain threshold"""
    return (var_bindings["v1"]["speed"] > _N_THRESHOLD_1) and (var_bindings["v3"]["speed"] > _N_THRESHOLD_1)

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v2's speed is significantly lower than a certain threshold"""
    return var_bindings["v2"]["speed"] < _N_THRESHOLD_2

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the displacement bearing derived from the coordinate differences of v1 and v3 is close to v2's direction angle within a certain reasonable range"""
    return abs(degrees(atan2(sin(radians(var_bindings["v3"]["longitude"] - var_bindings["v1"]["longitude"])) * cos(radians(var_bindings["v3"]["latitude"])), cos(radians(var_bindings["v1"]["latitude"])) * sin(radians(var_bindings["v3"]["latitude"])) - sin(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v3"]["latitude"])) * cos(radians(var_bindings["v3"]["longitude"] - var_bindings["v1"]["longitude"])))) - var_bindings["v2"]["direction"]) <= _N_THRESHOLD_3

