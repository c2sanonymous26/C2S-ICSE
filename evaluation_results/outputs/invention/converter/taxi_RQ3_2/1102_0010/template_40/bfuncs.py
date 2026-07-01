from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The speed value of v1 is zero."""
    return var_bindings["v1"]["speed"] == 0

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The grpid of v2 differs from that of v1 by 1, and the longitude and latitude values of v1 are the same as those of v2."""
    return ((abs(var_bindings["v2"]["grpid"] - var_bindings["v1"]["grpid"]) == 1)) and (((var_bindings["v1"]["latitude"] == var_bindings["v2"]["latitude"])) and ((var_bindings["v1"]["longitude"] == var_bindings["v2"]["longitude"])))

