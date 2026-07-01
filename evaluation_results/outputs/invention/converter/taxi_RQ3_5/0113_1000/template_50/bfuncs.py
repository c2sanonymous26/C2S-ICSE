from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The speed of v1 is significantly higher than a certain threshold."""
    return var_bindings["v1"]["speed"] > _N_THRESHOLD_1

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v2 belongs to the same vehicle and is the previous context of v1."""
    return (var_bindings["v2"]["carid"] == var_bindings["v1"]["carid"]) and (var_bindings["v2"]["grpid"] == var_bindings["v1"]["grpid"] - 1)

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The absolute value of the difference between the angle of the coordinate-change direction of v1 and v2 and the angle of the major city road direction does not exceed a certain reasonable range."""
    return abs(atan2(sin(radians(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"])) * cos(radians(var_bindings["v1"]["latitude"])), cos(radians(var_bindings["v2"]["latitude"])) * sin(radians(var_bindings["v1"]["latitude"])) - sin(radians(var_bindings["v2"]["latitude"])) * cos(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"])))) <= _N_THRESHOLD_2

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The coordinate-change direction of v1 and v2."""
    return atan2(sin(radians(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"])) * cos(radians(var_bindings["v1"]["latitude"])), cos(radians(var_bindings["v2"]["latitude"])) * sin(radians(var_bindings["v1"]["latitude"])) - sin(radians(var_bindings["v2"]["latitude"])) * cos(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"]))) <= _N_THRESHOLD_3

