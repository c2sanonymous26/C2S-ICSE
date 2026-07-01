from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle, and v2 is the consecutive next record after v1 for that vehicle"""
    return (var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]) and (var_bindings["v2"]["grpid"] == var_bindings["v1"]["grpid"] + 1)

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the time difference from v1 to v2 is sufficiently small and positive"""
    return (var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"] > 0) and (var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"] <= 1.0)

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the longitude recorded in v1 equals the longitude recorded in v2"""
    return var_bindings["v1"]["longitude"] == var_bindings["v2"]["longitude"]

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the latitude recorded in v1 equals the latitude recorded in v2"""
    return var_bindings["v1"]["latitude"] == var_bindings["v2"]["latitude"]

def bfunc_5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the speed recorded in v1 is sufficiently low and the speed recorded in v2 is sufficiently low"""
    return (var_bindings["v1"]["speed"] <= 9.0) and (var_bindings["v2"]["speed"] <= 9.0)

