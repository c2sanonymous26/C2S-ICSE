from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the instantaneous speed recorded in v1 does not exceed a certain upper bound for plausible city taxi operation"""
    return var_bindings["v1"]["speed"] <= 100.0

