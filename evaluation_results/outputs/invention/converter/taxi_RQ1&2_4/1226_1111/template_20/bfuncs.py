from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1's speed is zero"""
    return var_bindings["v1"]["speed"] == 0

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v2 is the next context of v1"""
    return (var_bindings["v2"]["carid"] == var_bindings["v1"]["carid"]) and (var_bindings["v2"]["grpid"] == var_bindings["v1"]["grpid"] + 1)

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v2's speed is zero and the timestamp difference does not exceed the threshold"""
    return (var_bindings["v2"]["speed"] == 0) and (abs(var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"]) <= _N_THRESHOLD_1)

