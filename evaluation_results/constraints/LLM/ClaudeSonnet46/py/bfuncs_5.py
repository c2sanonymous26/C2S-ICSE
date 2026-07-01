from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle"""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v2 is the consecutive next context after v1 for that vehicle"""
    return var_bindings["v2"]["grpid"] == var_bindings["v1"]["grpid"] + 1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the time difference from v1 to v2 is sufficiently small"""
    return var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"] <= 45.0

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the speeds recorded in both v1 and v2 are sufficiently large"""
    return (var_bindings["v1"]["speed"] >= 40.0) and (var_bindings["v2"]["speed"] >= 40.0)

def bfunc_5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the change in direction between v1 and v2 is within a range that is close to an about-face"""
    return abs(min(abs(var_bindings["v2"]["direction"] - var_bindings["v1"]["direction"]), 360 - abs(var_bindings["v2"]["direction"] - var_bindings["v1"]["direction"])) - 180) <= 30.0

