from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle (v1.carid = v2.carid)"""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 are consecutive records of that vehicle (v2.grpid - v1.grpid = 1)"""
    return var_bindings["v2"]["grpid"] - var_bindings["v1"]["grpid"] == 1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the speed recorded in v1 is significantly higher than a certain threshold"""
    return var_bindings["v1"]["speed"] > 80.0

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the distance between the GPS locations of v1 and v2 is above a certain lower bound"""
    return pow(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"], 2) + pow(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"], 2) > 5e-06

