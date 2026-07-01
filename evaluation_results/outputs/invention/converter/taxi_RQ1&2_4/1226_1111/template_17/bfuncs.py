from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1's speed is zero"""
    return var_bindings["v1"]["speed"] == 0

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v2 is the next context of v1"""
    return (var_bindings["v2"]["grpid"] == var_bindings["v1"]["grpid"] + 1) and (var_bindings["v2"]["carid"] == var_bindings["v1"]["carid"])

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v3 is the next context of v2"""
    return (var_bindings["v3"]["grpid"] == var_bindings["v2"]["grpid"] + 1) and (var_bindings["v3"]["carid"] == var_bindings["v2"]["carid"])

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the Haversine displacement between v1 and v2, and between v2 and v3, does not exceed a negligibly small range"""
    return ((6371.0 * 2 * atan2(sqrt(sin(radians(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) * sin(radians(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) + cos(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v2"]["latitude"])) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) / 2) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) / 2)), sqrt(1 - (sin(radians(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) * sin(radians(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) + cos(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v2"]["latitude"])) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) / 2) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) / 2))))) <= _N_THRESHOLD_1) and ((6371.0 * 2 * atan2(sqrt(sin(radians(var_bindings["v3"]["latitude"] - var_bindings["v2"]["latitude"]) / 2) * sin(radians(var_bindings["v3"]["latitude"] - var_bindings["v2"]["latitude"]) / 2) + cos(radians(var_bindings["v2"]["latitude"])) * cos(radians(var_bindings["v3"]["latitude"])) * sin(radians(var_bindings["v3"]["longitude"] - var_bindings["v2"]["longitude"]) / 2) * sin(radians(var_bindings["v3"]["longitude"] - var_bindings["v2"]["longitude"]) / 2)), sqrt(1 - (sin(radians(var_bindings["v3"]["latitude"] - var_bindings["v2"]["latitude"]) / 2) * sin(radians(var_bindings["v3"]["latitude"] - var_bindings["v2"]["latitude"]) / 2) + cos(radians(var_bindings["v2"]["latitude"])) * cos(radians(var_bindings["v3"]["latitude"])) * sin(radians(var_bindings["v3"]["longitude"] - var_bindings["v2"]["longitude"]) / 2) * sin(radians(var_bindings["v3"]["longitude"] - var_bindings["v2"]["longitude"]) / 2))))) <= _N_THRESHOLD_1)

