from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['speed'] > 66

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['direction'] - degrees(atan2(sin(radians(var_bindings['v1']['longitude'] - var_bindings['v1']['longitude'])), cos(radians(var_bindings['v1']['latitude'])) - sin(radians(var_bindings['v1']['latitude'])) * tan(radians(var_bindings['v1']['direction']))))) <= 315

