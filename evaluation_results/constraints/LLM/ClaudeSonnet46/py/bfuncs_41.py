from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle"""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v2 is the consecutive next record after v1 for that vehicle"""
    return var_bindings["v2"]["grpid"] == var_bindings["v1"]["grpid"] + 1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the time difference from v1 to v2 is sufficiently small and positive"""
    return (var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"] > 0) and (var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"] <= 30.0)

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the geographic displacement between the locations in v1 and v2 is within a certain small range"""
    return pow(abs(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]), 2) + pow(abs(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]), 2) <= 1e-07

def bfunc_5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the speed recorded in v2 is sufficiently larger than the speed recorded in v1"""
    return var_bindings["v2"]["speed"] - var_bindings["v1"]["speed"] >= 15.0

