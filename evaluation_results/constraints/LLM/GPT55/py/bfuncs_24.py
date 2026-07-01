from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to different vehicles"""
    return var_bindings["v1"]["carid"] != var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the timestamps of v1 and v2 are within the same short time period"""
    return abs(var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"]) <= 1.0

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the GPS locations of v1 and v2 are sufficiently close"""
    return pow(abs(var_bindings["v1"]["latitude"] - var_bindings["v2"]["latitude"]), 2) + pow(abs(var_bindings["v1"]["longitude"] - var_bindings["v2"]["longitude"]), 2) <= 4e-06

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the recorded directions of v1 and v2 are close to each other"""
    return min(abs(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"]), 360 - abs(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"])) <= 45.0

def bfunc_5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the absolute difference between the recorded speeds of v1 and v2 is sufficiently small"""
    return abs(var_bindings["v1"]["speed"] - var_bindings["v2"]["speed"]) <= 20.0

