from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to different vehicles."""
    return var_bindings["v1"]["carid"] != var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 are close in time and position, meaning that their absolute time difference does not exceed a certain value and their coordinate-based distance does not exceed a certain value."""
    return ((abs(var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"]) <= _N_THRESHOLD_1)) and ((sqrt(pow(var_bindings["v1"]["latitude"] - var_bindings["v2"]["latitude"], 2) + pow(var_bindings["v1"]["longitude"] - var_bindings["v2"]["longitude"], 2)) <= _N_THRESHOLD_2))

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The rate of change of the angle between the direction of the line connecting v1 and v2 and the direction of the line connecting v2 and v3 does not exceed a certain reasonable upper bound."""
    return abs(atan2(sin(radians(atan2(var_bindings["v3"]["latitude"] - var_bindings["v2"]["latitude"], var_bindings["v3"]["longitude"] - var_bindings["v2"]["longitude"]) - atan2(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"], var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]))), cos(radians(atan2(var_bindings["v3"]["latitude"] - var_bindings["v2"]["latitude"], var_bindings["v3"]["longitude"] - var_bindings["v2"]["longitude"]) - atan2(var_bindings["v2"]["latitude"] - var_bindings["v1"]["latitude"], var_bindings["v2"]["longitude"] - var_bindings["v1"]["longitude"]))))) / abs(var_bindings["v3"]["timestamp"] - var_bindings["v1"]["timestamp"]) <= _N_THRESHOLD_3

