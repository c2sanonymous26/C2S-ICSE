from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to different vehicles."""
    return var_bindings["v1"]["carid"] != var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The timestamps of v1 and v2 are close to each other, with the difference not exceeding a certain value."""
    return abs(var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"]) <= _N_THRESHOLD_1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The product of the absolute speed difference between v1 and v2 and the cosine of their direction-angle difference lies within a certain reasonable range."""
    return abs(var_bindings["v1"]["speed"] - var_bindings["v2"]["speed"]) * cos(radians(abs(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"]))) <= _N_THRESHOLD_2

