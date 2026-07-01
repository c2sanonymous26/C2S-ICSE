from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle (v1.carid = v2.carid)"""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 are consecutive records of that vehicle (v2.grpid - v1.grpid = 1)"""
    return var_bindings["v2"]["grpid"] - var_bindings["v1"]["grpid"] == 1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the absolute circular heading difference between v1 and v2 (the smallest angular difference modulo 360) exceeds a certain threshold"""
    return min(abs(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"]), 360 - abs(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"])) > 135.0

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the speed recorded in v1 is below a certain upper bound and the speed recorded in v2 is below a certain upper bound"""
    return (var_bindings["v1"]["speed"] <= 30.0) and (var_bindings["v2"]["speed"] <= 30.0)

