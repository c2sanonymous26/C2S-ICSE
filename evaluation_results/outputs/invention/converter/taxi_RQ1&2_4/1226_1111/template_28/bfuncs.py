from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the speed value of v1 is non-negative"""
    return var_bindings["v1"]["speed"] >= 0

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the speed value of v1 does not exceed a certain reasonable upper bound"""
    return var_bindings["v1"]["speed"] <= _N_THRESHOLD_1

