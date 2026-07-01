from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle."""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 are two adjacent contexts of that vehicle."""
    return abs(var_bindings["v1"]["grpid"] - var_bindings["v2"]["grpid"]) == 1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The absolute difference between the average instantaneous speed of v1 and v2 and the ratio between the straight-line distance computed from the coordinates of v1 and v2 and the timestamp difference of v1 and v2 does not exceed a certain reasonable range."""
    return abs(((var_bindings["v1"]["speed"] + var_bindings["v2"]["speed"]) / 2) - ((6371.0 * atan2(sqrt(pow(sin((radians(var_bindings["v2"]["latitude"]) - radians(var_bindings["v1"]["latitude"])) / 2), 2) + cos(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v2"]["latitude"])) * pow(sin((radians(var_bindings["v2"]["longitude"]) - radians(var_bindings["v1"]["longitude"])) / 2), 2)), sqrt(1 - (pow(sin((radians(var_bindings["v2"]["latitude"]) - radians(var_bindings["v1"]["latitude"])) / 2), 2) + cos(radians(var_bindings["v1"]["latitude"])) * cos(radians(var_bindings["v2"]["latitude"])) * pow(sin((radians(var_bindings["v2"]["longitude"]) - radians(var_bindings["v1"]["longitude"])) / 2), 2))))) / (abs(var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"]) / 3600))) <= _N_THRESHOLD_1

