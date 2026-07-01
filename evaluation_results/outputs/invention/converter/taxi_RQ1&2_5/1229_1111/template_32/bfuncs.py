from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the direction value of v1 is between 0 degrees and 360 degrees"""
    return (var_bindings["v1"]["direction"] >= 0) and (var_bindings["v1"]["direction"] <= 360)

