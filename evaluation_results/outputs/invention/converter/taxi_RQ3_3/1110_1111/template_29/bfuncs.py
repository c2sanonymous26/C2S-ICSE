from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle."""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The time difference between v1 and v2 is smaller than a certain threshold."""
    return (var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"] >= _N_THRESHOLD_1) and (var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"] <= _N_THRESHOLD_2)

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The ratio between the absolute speed difference of v1 and v2 and the timestamp difference between them does not exceed a certain reasonable upper bound on acceleration."""
    return abs(var_bindings["v1"]["speed"] - var_bindings["v2"]["speed"]) / (var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"]) <= _N_THRESHOLD_3

