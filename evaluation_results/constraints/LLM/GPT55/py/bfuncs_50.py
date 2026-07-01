from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle"""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 are consecutive records of that vehicle"""
    return abs(var_bindings["v1"]["grpid"] - var_bindings["v2"]["grpid"]) == 1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v2 occurs after v1 in time"""
    return var_bindings["v2"]["timestamp"] > var_bindings["v1"]["timestamp"]

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the absolute angular difference between the recorded directions of v1 and v2 is sufficiently large"""
    return min(abs(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"]), 360 - abs(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"])) >= 90.0

def bfunc_5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the average speed implied by the geographic distance between the GPS locations of v1 and v2 divided by their timestamp difference does not exceed a certain upper bound for sharp-turn movement"""
    return (6371.0 * 2 * atan2(sqrt(sin(radians(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) * sin(radians(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) + cos(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v2"]["latitude"])) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) / 2) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) / 2)), sqrt(1 - (sin(radians(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) * sin(radians(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) + cos(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v2"]["latitude"])) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) / 2) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) / 2))))) / ((var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"]) / (60 * 60)) <= 50.0

