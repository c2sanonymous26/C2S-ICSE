from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the timestamp value of v1 is greater than or equal to 0"""
    return var_bindings["v1"]["timestamp"] >= 0

