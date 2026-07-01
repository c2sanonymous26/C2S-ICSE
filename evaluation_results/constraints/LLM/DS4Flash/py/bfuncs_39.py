from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the speed recorded in v1 does not exceed a certain maximum speed threshold"""
    return var_bindings["v1"]["speed"] <= 114.0

