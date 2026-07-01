from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle (v1.carid = v2.carid)"""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 are consecutive records of that vehicle (v2.grpid - v1.grpid = 1)"""
    return var_bindings["v2"]["grpid"] - var_bindings["v1"]["grpid"] == 1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the product of the speed recorded in v1 and the absolute circular heading difference between v1 and v2 divided by the absolute time difference between v2 and v1 does not exceed a certain upper bound"""
    return (var_bindings["v1"]["speed"] * degrees(abs(atan2(sin(radians(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"])), cos(radians(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"])))))) / abs(var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"]) <= 3105.0

