from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to different vehicles."""
    return var_bindings["v1"]["carid"] != var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The timestamps of v1 and v2 are close, and their absolute time difference does not exceed a certain value."""
    return abs(var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"]) <= _N_THRESHOLD_1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The absolute difference between the coordinate-change directions of v1 and v2 computed from their respective surrounding records does not exceed a certain reasonable range."""
    return abs(degrees(atan2(sin(radians(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"])), cos(radians(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"]))))) <= _N_THRESHOLD_2

