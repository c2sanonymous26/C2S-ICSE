from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v3 belong to the same taxi (same carid)."""
    return var_bindings["v1"]["carid"] == var_bindings["v3"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v3 is the second consecutive record after v1 (grpid of v3 equals grpid of v1 plus 2)."""
    return var_bindings["v3"]["grpid"] - var_bindings["v1"]["grpid"] == 2

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The haversine distance between the GPS locations (longitude, latitude) of v1 and v3 is within a certain tolerance of the sum of the haversine distances from v1 to the context with grpid = v1.grpid+1 and same carid, and from that context to v3."""
    return abs((6371.0 * 2 * atan2(sqrt(sin(radians(var_bindings["v3"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) * sin(radians(var_bindings["v3"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) + cos(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v3"]["latitude"])) * sin(radians(var_bindings["v3"]["longitude"] - var_bindings["v1"]["longitude"]) / 2) * sin(radians(var_bindings["v3"]["longitude"] - var_bindings["v1"]["longitude"]) / 2)), sqrt(1 - (sin(radians(var_bindings["v3"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) * sin(radians(var_bindings["v3"]["latitude"] - var_bindings["v1"]["latitude"]) / 2) + cos(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v3"]["latitude"])) * sin(radians(var_bindings["v3"]["longitude"] - var_bindings["v1"]["longitude"]) / 2) * sin(radians(var_bindings["v3"]["longitude"] - var_bindings["v1"]["longitude"]) / 2)))) * 3600 / (var_bindings["v3"]["timestamp"] - var_bindings["v1"]["timestamp"])) - var_bindings["v1"]["speed"]) <= 50.0

