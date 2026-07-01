from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle."""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The grpid difference of v1 and v2 is greater than 1, and they are non-adjacent contexts."""
    return abs(var_bindings["v1"]["grpid"] - var_bindings["v2"]["grpid"]) > 1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The average value of the absolute differences between the displacement direction computed from v1 and v2 based on their coordinates and the direction values of v1 and v2 does not exceed a certain value."""
    return abs(degrees(atan2(sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"])) * cos(radians(var_bindings["v2"]["latitude"])), cos(radians(var_bindings["v1"]["latitude"])) * sin(radians(var_bindings["v2"]["latitude"])) - sin(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v2"]["latitude"])) * cos(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"])))) - (var_bindings["v1"]["direction"] + var_bindings["v2"]["direction"]) / 2) <= _N_THRESHOLD_1

