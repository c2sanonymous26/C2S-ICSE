from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The speed recorded in context v1 is sufficiently high."""
    return var_bindings["v1"]["speed"] > 70.0

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """Contexts v1 and v2 belong to different vehicles."""
    return var_bindings["v1"]["carid"] != var_bindings["v2"]["carid"]

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The timestamps of v1 and v2 are within the same short time period."""
    return abs(var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"]) <= 2.0

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The GPS locations of v1 and v2 are within a certain traffic-neighborhood distance."""
    return 6371.0 * 2 * atan2(sqrt(sin(radians(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) * sin(radians(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) + cos(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v2"]["latitude"])) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) / 2) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) / 2)), sqrt(1 - (sin(radians(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) * sin(radians(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) + cos(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v2"]["latitude"])) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) / 2) * sin(radians(var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]) / 2)))) <= 1.5

def bfunc_5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The absolute normalized difference between the directions recorded in v1 and v2 does not exceed a certain angular bound."""
    return abs((var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"] + 540) % 360 - 180) <= 45.0

