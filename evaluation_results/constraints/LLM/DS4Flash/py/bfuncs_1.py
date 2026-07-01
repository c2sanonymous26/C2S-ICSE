from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle (i.e., v1.carid = v2.carid)"""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 are consecutive records of that vehicle (i.e., v2.grpid - v1.grpid = 1)"""
    return var_bindings["v2"]["grpid"] - var_bindings["v1"]["grpid"] == 1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the absolute difference between the direction recorded in v2 and the bearing angle calculated from v1's GPS location (v1.latitude, v1.longitude) to v2's GPS location (v2.latitude, v2.longitude) does not exceed a certain bound"""
    return abs(var_bindings["v2"]["direction"] - ((degrees(atan2(sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"])) * cos(radians(var_bindings["v2"]["latitude"])), cos(radians(var_bindings["v1"]["latitude"])) * sin(radians(var_bindings["v2"]["latitude"])) - sin(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v2"]["latitude"])) * cos(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"])))) + 360) % 360)) <= 60.0

