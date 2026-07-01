from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle."""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The time difference between v1 and v2 is smaller than a certain threshold."""
    return (var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"] >= _N_THRESHOLD_1) and (var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"] <= _N_THRESHOLD_2)

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The ratio between the distance between the coordinates of v1 and v2 computed using the Euclidean distance formula and the timestamp difference between them does not exceed a certain reasonable upper bound on speed."""
    return sqrt(pow(var_bindings["v1"]["latitude"] - var_bindings["v2"]["latitude"], 2) + pow(var_bindings["v1"]["longitude"] - var_bindings["v2"]["longitude"], 2)) / (var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"]) <= _N_THRESHOLD_3

