from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['carid'] != var_bindings['v2']['carid']

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['timestamp'] - var_bindings['v2']['timestamp']) <= -1/1000000

def bfunc_3_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['direction'] - var_bindings['v2']['direction']) <= 0

def bfunc_4_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 6371 * acos(sin(radians(var_bindings['v1']['latitude'])) * sin(radians(var_bindings['v2']['latitude'])) + cos(radians(var_bindings['v1']['latitude'])) * cos(radians(var_bindings['v2']['latitude'])) * cos(radians(var_bindings['v1']['longitude'] - var_bindings['v2']['longitude']))) < 45101043/500000

