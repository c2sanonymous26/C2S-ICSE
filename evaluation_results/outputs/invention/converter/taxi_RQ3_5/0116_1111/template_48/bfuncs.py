from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The speed of v1 is significantly higher than a certain threshold."""
    return var_bindings["v1"]["speed"] > _N_THRESHOLD_1

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v2 belongs to the same vehicle and the grpid value of v2 is 1 smaller than that of v1."""
    return (var_bindings["v2"]["carid"] == var_bindings["v1"]["carid"]) and (var_bindings["v2"]["grpid"] == var_bindings["v1"]["grpid"] - 1)

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v3 belongs to the same vehicle and the grpid value of v3 is 1 greater than that of v1."""
    return (var_bindings["v3"]["carid"] == var_bindings["v1"]["carid"]) and (var_bindings["v3"]["grpid"] == var_bindings["v1"]["grpid"] + 1)

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The absolute difference between the speed-change rate between v1 and v2 and the speed-change rate between v1 and v3 does not exceed a certain reasonable range."""
    return abs(((var_bindings["v1"]["speed"] - var_bindings["v2"]["speed"]) / (var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"])) - ((var_bindings["v3"]["speed"] - var_bindings["v1"]["speed"]) / (var_bindings["v3"]["timestamp"] - var_bindings["v1"]["timestamp"]))) <= _N_THRESHOLD_2

