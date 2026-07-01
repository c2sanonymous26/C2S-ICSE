from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to different vehicles"""
    return var_bindings["v1"]["carid"] != var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the timestamps of v1 and v2 are close (the absolute time difference does not exceed some value)"""
    return abs(var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"]) <= _N_THRESHOLD_1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the latitude-longitude distance between v1 and v2 is significantly less than some value (i.e., the two vehicles are close in position)"""
    return sqrt(pow(var_bindings["v1"]["latitude"] - var_bindings["v2"]["latitude"], 2) + pow(var_bindings["v1"]["longitude"] - var_bindings["v2"]["longitude"], 2)) <= _N_THRESHOLD_2

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the direction difference between v1 and v2 is significantly less than some value (i.e., the two vehicles are traveling in similar directions)"""
    return abs(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"]) <= _N_THRESHOLD_3

