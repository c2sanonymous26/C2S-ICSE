from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle"""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v2 is the consecutive next record after v1 for that vehicle"""
    return var_bindings["v2"]["grpid"] - var_bindings["v1"]["grpid"] == 1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the time difference from v1 to v2 is sufficiently small and positive"""
    return (var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"] > 0) and (var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"] <= 5.0)

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the speed recorded in v1 is sufficiently large"""
    return var_bindings["v1"]["speed"] >= 40.0

def bfunc_5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the speed recorded in v2 is sufficiently low"""
    return var_bindings["v2"]["speed"] <= 10.0

def bfunc_6(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the difference between the direction recorded in v1 and the travel bearing from the location in v1 to the location in v2 is within a certain range"""
    return min(abs(var_bindings["v1"]["direction"] - ((degrees(atan2(sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"])) * cos(radians(var_bindings["v2"]["latitude"])), cos(radians(var_bindings["v1"]["latitude"])) * sin(radians(var_bindings["v2"]["latitude"])) - sin(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v2"]["latitude"])) * cos(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"])))) + 360) % 360)), 360 - abs(var_bindings["v1"]["direction"] - ((degrees(atan2(sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"])) * cos(radians(var_bindings["v2"]["latitude"])), cos(radians(var_bindings["v1"]["latitude"])) * sin(radians(var_bindings["v2"]["latitude"])) - sin(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v2"]["latitude"])) * cos(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"])))) + 360) % 360))) <= 45.0

