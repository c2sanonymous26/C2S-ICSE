from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the speed recorded in v1 is non-negative and does not exceed a certain upper bound"""
    return (var_bindings["v1"]["speed"] >= 0) and (var_bindings["v1"]["speed"] <= 114.0)

