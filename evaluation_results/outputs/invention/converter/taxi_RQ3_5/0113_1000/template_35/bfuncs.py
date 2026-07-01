from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to different vehicles."""
    return var_bindings["v1"]["carid"] != var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The timestamps of v1 and v2 are close, and their absolute time difference does not exceed a certain value."""
    return abs(var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"]) <= _N_THRESHOLD_1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The absolute difference between the angles formed by the direction of the line connecting the positions of v1 and v2 and their respective travel directions does not exceed a certain reasonable range."""
    return abs(atan2(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"], var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) - ((var_bindings["v1"]["direction"] + var_bindings["v2"]["direction"]) * 0.5)) <= _N_THRESHOLD_2

