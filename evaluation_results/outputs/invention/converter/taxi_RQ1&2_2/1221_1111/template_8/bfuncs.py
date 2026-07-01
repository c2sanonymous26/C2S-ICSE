from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle"""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v2 is the next consecutive context after v1 (same vehicle)"""
    return (var_bindings["v1"]["grpid"] + 1 == var_bindings["v2"]["grpid"]) and (var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"])

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the ratio of the absolute speed difference between v1 and v2 to their timestamp difference does not exceed a certain reasonable upper bound"""
    return abs(var_bindings["v1"]["speed"] - var_bindings["v2"]["speed"]) / abs(var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"]) <= _N_THRESHOLD_1

