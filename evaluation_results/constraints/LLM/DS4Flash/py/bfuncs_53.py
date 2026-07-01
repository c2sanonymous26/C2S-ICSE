from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same taxi (same carid)"""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 are consecutive records of that taxi (grpid of v2 equals grpid of v1 plus 1)"""
    return var_bindings["v2"]["grpid"] == var_bindings["v1"]["grpid"] + 1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the time difference (timestamp of v2 minus timestamp of v1) is positive"""
    return var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"] > 0

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the GPS displacement vector (change in longitude and latitude) between v1 and v2 is within a certain tolerance of the displacement vector predicted by the speed and direction recorded in v1 multiplied by the time difference, after appropriate unit conversion"""
    return (((min(abs(degrees(atan2(sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"])) * cos(radians(var_bindings["v2"]["latitude"])), cos(radians(var_bindings["v1"]["latitude"])) * sin(radians(var_bindings["v2"]["latitude"])) - sin(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v2"]["latitude"])) * cos(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"])))) - var_bindings["v1"]["direction"]), 360 - abs(degrees(atan2(sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"])) * cos(radians(var_bindings["v2"]["latitude"])), cos(radians(var_bindings["v1"]["latitude"])) * sin(radians(var_bindings["v2"]["latitude"])) - sin(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v2"]["latitude"])) * cos(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"])))) - var_bindings["v1"]["direction"]))) <= 180.0)) and ((abs((2 * 6371 * asin(sqrt(pow(sin((radians(var_bindings["v2"]["latitude"]) - radians(var_bindings["v1"]["latitude"])) / 2), 2) + cos(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v2"]["latitude"])) * pow(sin((radians(var_bindings["v2"]["longitude"]) - radians(var_bindings["v1"]["longitude"])) / 2), 2)))) - (var_bindings["v1"]["speed"] * ((var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"]) / 3600))) <= 0.1))

