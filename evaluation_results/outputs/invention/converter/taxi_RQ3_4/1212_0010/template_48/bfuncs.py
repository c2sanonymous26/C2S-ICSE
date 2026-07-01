from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The speed value of v1 is significantly higher than a certain threshold."""
    return var_bindings["v1"]["speed"] > 50

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The direction value of v1 does not change drastically within a short time."""
    return abs(var_bindings["v1"]["direction"] - 180) < 30

