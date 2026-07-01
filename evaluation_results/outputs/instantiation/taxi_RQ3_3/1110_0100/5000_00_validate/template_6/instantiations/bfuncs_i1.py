from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['speed'] - 0) <= 120

def bfunc_1_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['direction'] - 0) <= 360

