from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to different vehicles."""
    return var_bindings["v1"]["carid"] != var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The timestamps of v1 and v2 are close, and their absolute time difference does not exceed a certain value."""
    return abs(var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"]) <= _N_THRESHOLD_1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v3 and v4 are the previous and next contexts of v1."""
    return (var_bindings["v3"]["carid"] == var_bindings["v1"]["carid"]) and ((var_bindings["v3"]["grpid"] == var_bindings["v1"]["grpid"] - 1) and ((var_bindings["v4"]["carid"] == var_bindings["v1"]["carid"]) and (var_bindings["v4"]["grpid"] == var_bindings["v1"]["grpid"] + 1)))

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v5 and v6 are the previous and next contexts of v2."""
    return (var_bindings["v5"]["carid"] == var_bindings["v2"]["carid"]) and ((var_bindings["v5"]["grpid"] == var_bindings["v2"]["grpid"] - 1) and ((var_bindings["v6"]["carid"] == var_bindings["v2"]["carid"]) and (var_bindings["v6"]["grpid"] == var_bindings["v2"]["grpid"] + 1)))

def bfunc_5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The absolute difference between the direction-change rates of v1 and v2 does not exceed a certain reasonable range."""
    return abs((atan2(sin(radians(var_bindings["v1"]["direction"] - var_bindings["v3"]["direction"])), cos(radians(var_bindings["v1"]["direction"] - var_bindings["v3"]["direction"]))) - atan2(sin(radians(var_bindings["v2"]["direction"] - var_bindings["v5"]["direction"])), cos(radians(var_bindings["v2"]["direction"] - var_bindings["v5"]["direction"])))) / (var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"])) <= _N_THRESHOLD_2

