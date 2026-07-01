from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same taxi (same carid) and are consecutive records (grpid of v2 equals grpid of v1 plus 1)"""
    return (var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]) and (var_bindings["v2"]["grpid"] == var_bindings["v1"]["grpid"] + 1)

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the speed in v1 is above a certain threshold"""
    return var_bindings["v1"]["speed"] > 10.0

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """there exists a context v3 such that v2 and v3 belong to the same taxi and are consecutive records (grpid of v3 equals grpid of v2 plus 1)"""
    return var_bindings["v2"]["grpid"] < 1000.0

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the absolute angular difference between the direction change from v1 to v2 and the bearing change from the location of v1 to the location of v2 to the location of the context that is consecutive after v2 (if it exists) is within a certain angle"""
    return abs((var_bindings["v2"]["direction"] - var_bindings["v1"]["direction"]) - degrees(atan2(sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"])) * cos(radians(var_bindings["v2"]["latitude"])), cos(radians(var_bindings["v1"]["latitude"])) * sin(radians(var_bindings["v2"]["latitude"])) - sin(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v2"]["latitude"])) * cos(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]))))) <= 30.0

