from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle"""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v2 is the consecutive next record after v1 for that vehicle"""
    return var_bindings["v2"]["grpid"] - var_bindings["v1"]["grpid"] == 1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the time difference from v1 to v2 is sufficiently small and positive"""
    return (var_bindings["v2"]["timestamp"] > var_bindings["v1"]["timestamp"]) and (var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"] <= 40.0)

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the direction recorded in v1 is within a certain range of due east"""
    return abs(var_bindings["v1"]["direction"] - 90) <= 0.0

def bfunc_5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the direction recorded in v2 is within a certain range of due east and at least one of the speeds recorded in v1 and v2 is sufficiently large"""
    return (abs(var_bindings["v2"]["direction"] - 90) <= 0.0) and (((var_bindings["v1"]["speed"] >= 40.0) or (var_bindings["v2"]["speed"] >= 40.0)))

def bfunc_6(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the absolute difference between the latitudes recorded in v1 and v2 is within a certain small range"""
    return abs(var_bindings["v1"]["latitude"] - var_bindings["v2"]["latitude"]) <= 0.007

