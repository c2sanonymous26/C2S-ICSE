from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle."""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 are two consecutive contexts of that vehicle."""
    return abs(var_bindings["v1"]["grpid"] - var_bindings["v2"]["grpid"]) == 1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The product of the absolute difference in direction angle between v1 and v2 and the average of their speed values does not exceed a certain reasonable upper bound."""
    return abs(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"]) * ((var_bindings["v1"]["speed"] + var_bindings["v2"]["speed"]) / 2) <= _N_THRESHOLD_1

