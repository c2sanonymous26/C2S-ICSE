from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle."""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 are two adjacent contexts of that vehicle."""
    return abs(var_bindings["v1"]["grpid"] - var_bindings["v2"]["grpid"]) == 1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The ratio between the direction-angle change rate computed from the direction-angle difference and timestamp difference of v1 and v2 and the speed-change rate computed from the speed difference and timestamp difference of v1 and v2 does not exceed a certain reasonable range."""
    return abs(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"]) / abs(var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"]) / abs(var_bindings["v1"]["speed"] - var_bindings["v2"]["speed"]) / abs(var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"]) <= _N_THRESHOLD_1

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The product of that ratio and the average speed of v1 and v2 does not exceed a certain reasonable turning-radius limit."""
    return (abs(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"]) / abs(var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"]) / abs(var_bindings["v1"]["speed"] - var_bindings["v2"]["speed"]) / abs(var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"])) * ((var_bindings["v1"]["speed"] + var_bindings["v2"]["speed"]) / 2) <= _N_THRESHOLD_2

