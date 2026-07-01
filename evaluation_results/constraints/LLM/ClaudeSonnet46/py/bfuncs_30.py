from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle, and v2 is the consecutive next record after v1 for that vehicle"""
    return (var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]) and (var_bindings["v2"]["grpid"] == var_bindings["v1"]["grpid"] + 1)

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the time difference from v1 to v2 is sufficiently small and positive"""
    return (var_bindings["v2"]["timestamp"] > var_bindings["v1"]["timestamp"]) and (var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"] <= 20.0)

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the speed recorded in v1 is sufficiently large"""
    return var_bindings["v1"]["speed"] >= 50.0

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the direction recorded in v1 is within a certain range of due west"""
    return abs(var_bindings["v1"]["direction"] - 270) <= 0.0

def bfunc_5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the longitude recorded in v2 is less than the longitude recorded in v1 by at least a certain small amount"""
    return var_bindings["v1"]["longitude"] - var_bindings["v2"]["longitude"] >= 0.0003

