from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The speed value of v1 is significantly higher than a certain threshold."""
    return var_bindings["v1"]["speed"] > _N_THRESHOLD_1

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v2 is the previous context of v1."""
    return (var_bindings["v2"]["grpid"] == var_bindings["v1"]["grpid"] - 1) and (var_bindings["v2"]["carid"] == var_bindings["v1"]["carid"])

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The ratio between the squared Euclidean distance of the coordinates of v1 and v2 and the timestamp difference does not exceed a certain reasonable multiple of the speed value of v1."""
    return (pow(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"], 2) + pow(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"], 2)) / (var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"]) <= var_bindings["v1"]["speed"] * _N_THRESHOLD_2

