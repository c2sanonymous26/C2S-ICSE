from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle."""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 are two consecutive contexts."""
    return abs(var_bindings["v1"]["grpid"] - var_bindings["v2"]["grpid"]) == 1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The travel directions of v1 and v2 lie in opposite quadrants."""
    return ((((var_bindings["v1"]["direction"] >= 0) and ((var_bindings["v1"]["direction"] < 90) and ((var_bindings["v2"]["direction"] >= 180) and (var_bindings["v2"]["direction"] < 270))))) or ((((var_bindings["v1"]["direction"] >= 90) and ((var_bindings["v1"]["direction"] < 180) and ((var_bindings["v2"]["direction"] >= 270) and (var_bindings["v2"]["direction"] < 360))))) or ((((var_bindings["v1"]["direction"] >= 180) and ((var_bindings["v1"]["direction"] < 270) and ((var_bindings["v2"]["direction"] >= 0) and (var_bindings["v2"]["direction"] < 90))))) or (((var_bindings["v1"]["direction"] >= 270) and ((var_bindings["v1"]["direction"] < 360) and ((var_bindings["v2"]["direction"] >= 90) and (var_bindings["v2"]["direction"] < 180))))))))

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The ratio between the haversine distance computed from v1 and v2 and their timestamp difference is significantly lower than the larger of the instantaneous speeds of v1 and v2."""
    return (6371.0 * 2 * atan2(sqrt(sin(radians(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) * sin(radians(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) + cos(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v2"]["latitude"])) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) / 2) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) / 2)), sqrt(1 - (sin(radians(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) * sin(radians(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) + cos(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v2"]["latitude"])) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) / 2) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) / 2))))) / (abs(var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"]) / (60 * 60)) < max(var_bindings["v1"]["speed"], var_bindings["v2"]["speed"]) * _N_THRESHOLD_1

