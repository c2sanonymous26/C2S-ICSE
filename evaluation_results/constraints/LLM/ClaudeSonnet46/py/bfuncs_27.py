from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to different vehicles"""
    return var_bindings["v1"]["carid"] != var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the time difference between v1 and v2 is sufficiently small"""
    return abs(var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"]) <= 1.0

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the speeds recorded in both v1 and v2 are sufficiently large"""
    return (var_bindings["v1"]["speed"] >= 40.0) and (var_bindings["v2"]["speed"] >= 40.0)

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the change between the directions recorded in v1 and v2 is within a certain small range"""
    return min(abs(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"]), 360 - abs(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"])) <= 15.0

def bfunc_5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the longitude recorded in v1 equals the longitude recorded in v2 and the latitude recorded in v1 equals the latitude recorded in v2"""
    return (var_bindings["v1"]["longitude"] == var_bindings["v2"]["longitude"]) and (var_bindings["v1"]["latitude"] == var_bindings["v2"]["latitude"])

