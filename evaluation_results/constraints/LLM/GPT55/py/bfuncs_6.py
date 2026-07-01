from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle."""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The grpid of v2 immediately follows the grpid of v1."""
    return var_bindings["v2"]["grpid"] == var_bindings["v1"]["grpid"] + 1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The timestamp recorded in v2 is greater than the timestamp recorded in v1."""
    return var_bindings["v2"]["timestamp"] > var_bindings["v1"]["timestamp"]

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The timestamp difference between v2 and v1 is within a reliable comparison range."""
    return (var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"] >= 5.0) and (var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"] <= 60.0)

def bfunc_5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The GPS displacement from the location of v1 to the location of v2 is sufficiently large."""
    return 6371.0 * 2 * atan2(sqrt(sin(radians(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) * sin(radians(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) + cos(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v2"]["latitude"])) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) / 2) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) / 2)), sqrt(1 - (sin(radians(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) * sin(radians(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) + cos(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v2"]["latitude"])) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) / 2) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) / 2)))) >= 0.1

def bfunc_6(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The direction recorded in v2 is close to the geographic bearing from the location of v1 to the location of v2 within a certain angular tolerance."""
    return abs(((var_bindings["v2"]["direction"] - degrees(atan2(sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"])) * cos(radians(var_bindings["v2"]["latitude"])), cos(radians(var_bindings["v1"]["latitude"])) * sin(radians(var_bindings["v2"]["latitude"])) - sin(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v2"]["latitude"])) * cos(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"])))) + 180) % 360) - 180) <= 45.0

