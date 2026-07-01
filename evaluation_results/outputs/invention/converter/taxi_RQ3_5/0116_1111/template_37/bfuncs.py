from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle."""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The grpid value of v1 is 3 greater than that of v2."""
    return var_bindings["v1"]["grpid"] == var_bindings["v2"]["grpid"] + 3

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The ratio between the position change of v1 and v2 computed from coordinates and their direction difference does not exceed a certain reasonable range."""
    return (sqrt(pow(var_bindings["v1"]["latitude"] - var_bindings["v2"]["latitude"], 2) + pow(var_bindings["v1"]["longitude"] - var_bindings["v2"]["longitude"], 2)) / abs(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"])) <= _N_THRESHOLD_1

