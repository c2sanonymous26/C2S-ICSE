from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The speed of v1 is significantly higher than a certain threshold."""
    return var_bindings["v1"]["speed"] > _N_THRESHOLD_1

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v2 belongs to the same vehicle and the grpid value of v2 is 1 smaller than that of v1."""
    return (var_bindings["v2"]["carid"] == var_bindings["v1"]["carid"]) and (var_bindings["v2"]["grpid"] == var_bindings["v1"]["grpid"] - 1)

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The absolute difference between the coordinate-change direction from v2 to v1 and the direction angle of v1 should lie within a certain reasonable range."""
    return abs(atan2(sin(radians(var_bindings["v1"]["longitude"] - var_bindings["v2"]["longitude"])) * cos(radians(var_bindings["v1"]["latitude"])), cos(radians(var_bindings["v2"]["latitude"])) * sin(radians(var_bindings["v1"]["latitude"])) - sin(radians(var_bindings["v2"]["latitude"])) * cos(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v1"]["longitude"] - var_bindings["v2"]["longitude"]))) - var_bindings["v1"]["direction"]) <= _N_THRESHOLD_2

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The speed change between v1 and v2 should lie within a certain reasonable range."""
    return abs(var_bindings["v1"]["speed"] - var_bindings["v2"]["speed"]) <= _N_THRESHOLD_3

