from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle."""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 are two adjacent contexts of that vehicle."""
    return abs(var_bindings["v1"]["grpid"] - var_bindings["v2"]["grpid"]) == 1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The absolute differences in longitude and latitude between v1 and v2 do not exceed a certain range."""
    return (abs(var_bindings["v1"]["longitude"] - var_bindings["v2"]["longitude"]) <= _N_THRESHOLD_1) and (abs(var_bindings["v1"]["latitude"] - var_bindings["v2"]["latitude"]) <= _N_THRESHOLD_2)

