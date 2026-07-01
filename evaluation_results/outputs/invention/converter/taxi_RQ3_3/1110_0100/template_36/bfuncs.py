from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle."""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 are two adjacent contexts of that vehicle."""
    return abs(var_bindings["v1"]["grpid"] - var_bindings["v2"]["grpid"]) == 1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The ratio between the absolute direction-angle difference of v1 and v2 and the timestamp difference between them does not exceed a certain reasonable upper bound on turning rate."""
    return abs(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"]) / (var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"]) <= _N_THRESHOLD_1

