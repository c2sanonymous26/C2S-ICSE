from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to different vehicles."""
    return var_bindings["v1"]["carid"] != var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The timestamps of v1 and v2 are close, and their absolute time difference does not exceed a certain value."""
    return abs(var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"]) <= _N_THRESHOLD_1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 each have a previous context."""
    return (var_bindings["v1"]["grpid"] > 1) and (var_bindings["v2"]["grpid"] > 1)

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The angle between the coordinate-change directions of v1 and v2 computed from their respective previous contexts does not exceed a certain reasonable range."""
    return abs(atan2(sin(radians(var_bindings["v1"]["longitude"] - var_bindings["v3"]["longitude"])) * cos(radians(var_bindings["v1"]["latitude"])), cos(radians(var_bindings["v3"]["latitude"])) * sin(radians(var_bindings["v1"]["latitude"])) - sin(radians(var_bindings["v3"]["latitude"])) * cos(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v1"]["longitude"] - var_bindings["v3"]["longitude"]))) - atan2(sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v4"]["longitude"])) * cos(radians(var_bindings["v2"]["latitude"])), cos(radians(var_bindings["v4"]["latitude"])) * sin(radians(var_bindings["v2"]["latitude"])) - sin(radians(var_bindings["v4"]["latitude"])) * cos(radians(var_bindings["v2"]["latitude"])) * cos(radians(var_bindings["v2"]["longitude"] - var_bindings["v4"]["longitude"])))) <= _N_THRESHOLD_2

