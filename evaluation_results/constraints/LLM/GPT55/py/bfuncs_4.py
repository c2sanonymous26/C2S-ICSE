from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle"""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the grpid of v2 immediately follows the grpid of v1"""
    return var_bindings["v2"]["grpid"] - var_bindings["v1"]["grpid"] == 1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the timestamp of v2 is greater than the timestamp of v1"""
    return var_bindings["v2"]["timestamp"] > var_bindings["v1"]["timestamp"]

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the timestamp difference between v2 and v1 is within a reliable comparison range"""
    return (var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"] >= 1.0) and (var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"] <= 200.0)

def bfunc_5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the absolute normalized difference between the directions recorded in v1 and v2 is sufficiently large"""
    return min(abs(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"]), abs(360 - abs(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"]))) >= 90.0

def bfunc_6(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the speeds recorded in both v1 and v2 are not greater than a certain reasonable turning-speed threshold"""
    return (var_bindings["v1"]["speed"] <= 30.0) and (var_bindings["v2"]["speed"] <= 30.0)

