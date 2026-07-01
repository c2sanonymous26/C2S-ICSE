from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same taxi (same carid)"""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the time difference (timestamp of v2 minus timestamp of v1) is positive and within a certain short time window"""
    return (var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"] > 0) and (var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"] <= 10.0)

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the speed in v1 is above a certain threshold"""
    return var_bindings["v1"]["speed"] > 10.0

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the angular difference between the direction in v1 and the bearing from v1's location (longitude, latitude) to v2's location (longitude, latitude) is within a certain angle"""
    return min(abs(var_bindings["v1"]["direction"] - ((degrees(atan2(cos(radians(var_bindings["v2"]["latitude"])) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"])), cos(radians(var_bindings["v1"]["latitude"])) * sin(radians(var_bindings["v2"]["latitude"])) - sin(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v2"]["latitude"])) * cos(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"])))) + 360) % 360)), 360 - abs(var_bindings["v1"]["direction"] - ((degrees(atan2(cos(radians(var_bindings["v2"]["latitude"])) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"])), cos(radians(var_bindings["v1"]["latitude"])) * sin(radians(var_bindings["v2"]["latitude"])) - sin(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v2"]["latitude"])) * cos(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"])))) + 360) % 360))) <= 30.0

