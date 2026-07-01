from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle."""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 are two adjacent contexts of that vehicle."""
    return abs(var_bindings["v1"]["grpid"] - var_bindings["v2"]["grpid"]) == 1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The ratio between the timestamp difference of v1 and v2 and the grpid difference of v1 and v2 lies within a certain reasonable range."""
    return ((var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"]) / abs(var_bindings["v2"]["grpid"] - var_bindings["v1"]["grpid"]) >= _N_THRESHOLD_1) and ((var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"]) / abs(var_bindings["v2"]["grpid"] - var_bindings["v1"]["grpid"]) <= _N_THRESHOLD_2)

