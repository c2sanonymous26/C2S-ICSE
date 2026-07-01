from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to different vehicles."""
    return var_bindings["v1"]["carid"] != var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The timestamps of v1 and v2 are close to each other, and their absolute time difference does not exceed a certain value."""
    return abs(var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"]) <= _N_THRESHOLD_1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The positions of v1 and v2 are close to each other, and the distance computed from their coordinates does not exceed a certain value."""
    return pow(abs(var_bindings["v1"]["latitude"] - var_bindings["v2"]["latitude"]), 2) + pow(abs(var_bindings["v1"]["longitude"] - var_bindings["v2"]["longitude"]), 2) <= _N_THRESHOLD_2

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The angle between the motion directions of v1 and v2 computed from direction does not exceed a certain value."""
    return (abs(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"]) <= _N_THRESHOLD_3) or (abs(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"]) >= 360 - _N_THRESHOLD_3)

