from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle"""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 are consecutive records of that vehicle"""
    return var_bindings["v2"]["grpid"] - var_bindings["v1"]["grpid"] == 1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the distance between the actual GPS location of v2 and the location predicted from v1 using v1's speed and direction and the time difference between v2 and v1 does not exceed a certain bound"""
    return sqrt(pow(((var_bindings["v2"]["latitude"] - (var_bindings["v1"]["latitude"] + ((var_bindings["v1"]["speed"] * (var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"]) / 3600) / 111.32 * cos(radians(var_bindings["v1"]["direction"]))))) * 111.32), 2) + pow(((var_bindings["v2"]["longitude"] - (var_bindings["v1"]["longitude"] + ((var_bindings["v1"]["speed"] * (var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"]) / 3600) / 111.32 / cos(radians(var_bindings["v1"]["latitude"])) * sin(radians(var_bindings["v1"]["direction"]))))) * 111.32 * cos(radians(var_bindings["v1"]["latitude"]))), 2)) <= 1.5

