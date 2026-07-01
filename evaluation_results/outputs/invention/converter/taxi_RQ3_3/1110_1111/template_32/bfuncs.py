from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle."""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The grpid value of v1 is equal to the grpid value of v2 minus 3."""
    return var_bindings["v1"]["grpid"] == var_bindings["v2"]["grpid"] - 3

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The acceleration computed from v1 and v2 does not exceed a certain reasonable upper bound on acceleration."""
    return abs(var_bindings["v1"]["speed"] - var_bindings["v2"]["speed"]) / (var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"]) <= _N_THRESHOLD_1

