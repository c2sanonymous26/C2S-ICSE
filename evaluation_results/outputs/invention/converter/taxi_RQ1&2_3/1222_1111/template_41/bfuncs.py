from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle"""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 are consecutive contexts of that vehicle"""
    return (var_bindings["v1"]["grpid"] + 1 == var_bindings["v2"]["grpid"]) or (var_bindings["v2"]["grpid"] + 1 == var_bindings["v1"]["grpid"])

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1's speed is significantly higher than a certain threshold"""
    return var_bindings["v1"]["speed"] > _N_THRESHOLD_1

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v2's speed is significantly lower than a certain threshold"""
    return var_bindings["v2"]["speed"] < _N_THRESHOLD_2

def bfunc_5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the ratio of the displacement distance derived from the coordinate differences to the timestamp difference is close to v1's speed within a certain reasonable range"""
    return abs((6371.0 * 2 * atan2(sqrt(sin(radians(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) * sin(radians(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) + cos(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v2"]["latitude"])) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) / 2) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) / 2)), sqrt(1 - (sin(radians(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) * sin(radians(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) + cos(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v2"]["latitude"])) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) / 2) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) / 2))))) / (var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"]) - var_bindings["v1"]["speed"]) <= _N_THRESHOLD_3

