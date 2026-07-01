from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The speed of v1 is significantly higher than a certain threshold."""
    return var_bindings["v1"]["speed"] > _N_THRESHOLD_1

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The absolute difference between the coordinate-change direction of v1 and the direction of v1 does not exceed a certain reasonable range."""
    return abs(var_bindings["v1"]["direction"] - degrees(atan2(sin(radians(var_bindings["v1"]["longitude"] - var_bindings["v1"]["longitude"])), cos(radians(var_bindings["v1"]["latitude"])) - sin(radians(var_bindings["v1"]["latitude"])) * tan(radians(var_bindings["v1"]["direction"]))))) <= _N_THRESHOLD_2

