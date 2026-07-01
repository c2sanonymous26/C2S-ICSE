from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle (v1.carid = v2.carid)"""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 are consecutive records of that vehicle (v2.grpid - v1.grpid = 1)"""
    return var_bindings["v2"]["grpid"] - var_bindings["v1"]["grpid"] == 1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the absolute difference between the timestamps of v1 and v2 is within a certain range (neither too small nor too large)"""
    return (abs(var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"]) >= 3.0) and (abs(var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"]) <= 26.0)

