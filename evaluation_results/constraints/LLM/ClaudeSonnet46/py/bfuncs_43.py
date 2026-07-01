from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to different vehicles"""
    return var_bindings["v1"]["carid"] != var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the time difference between v1 and v2 is sufficiently small"""
    return abs(var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"]) <= 1.0

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the geographic distance between the locations in v1 and v2 is sufficiently small"""
    return (6371.0 * 2 * atan2(sqrt(sin(radians(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) * sin(radians(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) + cos(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v2"]["latitude"])) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) / 2) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) / 2)), sqrt(1 - (sin(radians(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) * sin(radians(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) + cos(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v2"]["latitude"])) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) / 2) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) / 2))))) <= 0.1

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the change between the directions recorded in v1 and v2 is within a range close to an about-face"""
    return (abs((abs(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"])) - 180) <= 22.5) or (abs((360 - abs(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"])) - 180) <= 22.5)

def bfunc_5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """at least one of the speeds recorded in v1 and v2 is sufficiently low"""
    return (var_bindings["v1"]["speed"] <= 20.0) or (var_bindings["v2"]["speed"] <= 20.0)

