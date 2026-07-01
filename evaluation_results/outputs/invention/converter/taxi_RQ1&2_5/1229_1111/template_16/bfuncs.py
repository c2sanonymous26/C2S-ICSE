from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1, v2, and v3 belong to the same vehicle"""
    return (var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]) and (var_bindings["v1"]["carid"] == var_bindings["v3"]["carid"])

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the grpid of v1 is greater than that of v2 by 1"""
    return var_bindings["v1"]["grpid"] == var_bindings["v2"]["grpid"] + 1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the grpid of v2 is greater than that of v3 by 1"""
    return var_bindings["v2"]["grpid"] == var_bindings["v3"]["grpid"] + 1

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the ratio of the latitude-longitude distance between v1 and v2 to the latitude-longitude distance between v2 and v3 (i.e., the rate of position change) is significantly less than some upper bound"""
    return (6371.0 * 2 * atan2(sqrt(sin(radians(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) * sin(radians(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) + cos(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v2"]["latitude"])) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) / 2) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) / 2)), sqrt(1 - (sin(radians(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) * sin(radians(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) + cos(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v2"]["latitude"])) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) / 2) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) / 2))))) / (6371.0 * 2 * atan2(sqrt(sin(radians(var_bindings["v3"]["latitude"] - var_bindings["v2"]["latitude"]) / 2) * sin(radians(var_bindings["v3"]["latitude"] - var_bindings["v2"]["latitude"]) / 2) + cos(radians(var_bindings["v2"]["latitude"])) * cos(radians(var_bindings["v3"]["latitude"])) * sin(radians(var_bindings["v3"]["longitude"] - var_bindings["v2"]["longitude"]) / 2) * sin(radians(var_bindings["v3"]["longitude"] - var_bindings["v2"]["longitude"]) / 2)), sqrt(1 - (sin(radians(var_bindings["v3"]["latitude"] - var_bindings["v2"]["latitude"]) / 2) * sin(radians(var_bindings["v3"]["latitude"] - var_bindings["v2"]["latitude"]) / 2) + cos(radians(var_bindings["v2"]["latitude"])) * cos(radians(var_bindings["v3"]["latitude"])) * sin(radians(var_bindings["v3"]["longitude"] - var_bindings["v2"]["longitude"]) / 2) * sin(radians(var_bindings["v3"]["longitude"] - var_bindings["v2"]["longitude"]) / 2))))) <= _N_THRESHOLD_1

