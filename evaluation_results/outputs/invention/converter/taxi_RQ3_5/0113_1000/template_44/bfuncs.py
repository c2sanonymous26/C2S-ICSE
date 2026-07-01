from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The speed of v1 is significantly higher than a certain threshold."""
    return var_bindings["v1"]["speed"] > _N_THRESHOLD_1

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v2 is the previous context of v1."""
    return (var_bindings["v2"]["grpid"] == var_bindings["v1"]["grpid"] - 1) and (var_bindings["v2"]["carid"] == var_bindings["v1"]["carid"])

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The absolute value of the angle between the coordinate-change direction of v1 computed from the coordinates of v2 and the direction of major city roads does not exceed a certain reasonable range."""
    return abs(atan2(sin(radians(var_bindings["v1"]["longitude"] - var_bindings["v2"]["longitude"])) * cos(radians(var_bindings["v1"]["latitude"])), cos(radians(var_bindings["v2"]["latitude"])) * sin(radians(var_bindings["v1"]["latitude"])) - sin(radians(var_bindings["v2"]["latitude"])) * cos(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v1"]["longitude"] - var_bindings["v2"]["longitude"]))) - degrees(atan2(0.5, 0.5))) <= _N_THRESHOLD_2

