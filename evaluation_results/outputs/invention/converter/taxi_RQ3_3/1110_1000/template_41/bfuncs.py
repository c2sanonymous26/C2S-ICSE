from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The speed of v1 is zero and remains so beyond a certain time threshold, meaning that the timestamp difference between v1 and its next context v2 exceeds a certain value."""
    return (var_bindings["v1"]["speed"] == 0) and ((var_bindings["v1"]["timestamp"] < var_bindings["v2"]["timestamp"]) and (var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"] > _N_THRESHOLD_1))

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v2 is the next context of v1."""
    return (var_bindings["v2"]["grpid"] == var_bindings["v1"]["grpid"] + 1) and (var_bindings["v2"]["carid"] == var_bindings["v1"]["carid"])

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The absolute difference between the direction angle of v1 and that of v2 does not exceed a certain reasonable angular range."""
    return abs(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"]) <= _N_THRESHOLD_2

