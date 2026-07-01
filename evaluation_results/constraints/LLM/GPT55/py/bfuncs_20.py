from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle."""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The grpid of v2 immediately follows the grpid of v1."""
    return var_bindings["v2"]["grpid"] == var_bindings["v1"]["grpid"] + 1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The timestamp of v2 is greater than the timestamp of v1."""
    return var_bindings["v2"]["timestamp"] > var_bindings["v1"]["timestamp"]

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The timestamp difference between v1 and v2 is within a reliable comparison range."""
    return var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"] <= 20.0

def bfunc_5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The GPS displacement between v1 and v2 is sufficiently small."""
    return 6371.0 * 2 * atan2(sqrt(sin(radians(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) * sin(radians(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) + cos(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v2"]["latitude"])) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) / 2) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) / 2)), sqrt(1 - (sin(radians(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) * sin(radians(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) + cos(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v2"]["latitude"])) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) / 2) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) / 2)))) <= 0.005

def bfunc_6(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The speeds recorded in both v1 and v2 are sufficiently small."""
    return (var_bindings["v1"]["speed"] <= 12.0) and (var_bindings["v2"]["speed"] <= 12.0)

