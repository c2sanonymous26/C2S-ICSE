from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle and are consecutive contexts."""
    return (var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]) and (var_bindings["v1"]["grpid"] + 1 == var_bindings["v2"]["grpid"])

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The speed-change rate between v1 and v2 lies within a reasonable range, and the direction-change rate between v1 and v2 also lies within a reasonable range."""
    return (abs(var_bindings["v2"]["speed"] - var_bindings["v1"]["speed"]) <= _N_THRESHOLD_1) and (min(abs(var_bindings["v2"]["direction"] - var_bindings["v1"]["direction"]), 360 - abs(var_bindings["v2"]["direction"] - var_bindings["v1"]["direction"])) <= _N_THRESHOLD_2)

