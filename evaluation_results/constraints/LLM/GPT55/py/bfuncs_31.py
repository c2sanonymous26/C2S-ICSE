from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle"""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the absolute difference between the timestamps recorded in v1 and v2 is within a very short time window"""
    return abs(var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"]) <= 2.0

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the speeds recorded in both v1 and v2 are sufficiently high for direction readings to be reliable"""
    return (var_bindings["v1"]["speed"] >= 30.0) and (var_bindings["v2"]["speed"] >= 30.0)

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the absolute normalized difference between the directions recorded in v1 and v2 does not exceed a certain reasonable angular bound"""
    return min(abs(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"]), 360 - abs(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"])) <= 45.0

