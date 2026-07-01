from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to different vehicles (v1.carid != v2.carid)"""
    return var_bindings["v1"]["carid"] != var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the absolute time difference between v1 and v2 is within a certain range (|v1.timestamp - v2.timestamp| <= T)"""
    return abs(var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"]) <= 1.0

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the distance between the GPS locations of v1 and v2 is within a certain distance (d <= D)"""
    return pow(abs(var_bindings["v1"]["latitude"] - var_bindings["v2"]["latitude"]), 2) + pow(abs(var_bindings["v1"]["longitude"] - var_bindings["v2"]["longitude"]), 2) <= 8e-05

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the absolute speed difference between v1 and v2 does not exceed a certain bound (|v1.speed - v2.speed| <= S)"""
    return abs(var_bindings["v1"]["speed"] - var_bindings["v2"]["speed"]) <= 24.0

