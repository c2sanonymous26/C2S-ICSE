from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to different vehicles"""
    return var_bindings["v1"]["carid"] != var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the timestamp difference between v1 and v2 is within a certain reasonable time range"""
    return abs(var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"]) <= _N_THRESHOLD_1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the ratio of the haversine GPS distance between v1 and v2 to their timestamp difference does not exceed a certain reasonable speed upper bound"""
    return (sqrt(pow(sin(radians((var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) * 0.5)), 2) + cos(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v2"]["latitude"])) * pow(sin(radians((var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) * 0.5)), 2)) * 2 * 6371) / (abs(var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"]) / 3600) <= _N_THRESHOLD_2

