from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['carid'] != var_bindings['v2']['carid']

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['timestamp'] - var_bindings['v2']['timestamp']) <= _N_THRESHOLD_1

def bfunc_3_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return degrees(atan2(var_bindings['v2']['longitude'] - var_bindings['v1']['longitude'], var_bindings['v2']['latitude'] - var_bindings['v1']['latitude'])) <= _N_THRESHOLD_2

def bfunc_4_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(abs(var_bindings['v1']['direction'] - degrees(atan2(var_bindings['v2']['longitude'] - var_bindings['v1']['longitude'], var_bindings['v2']['latitude'] - var_bindings['v1']['latitude']))) % 360) <= _N_THRESHOLD_3

def bfunc_4_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(abs(var_bindings['v1']['direction'] - degrees(atan2(var_bindings['v2']['longitude'] - var_bindings['v1']['longitude'], var_bindings['v2']['latitude'] - var_bindings['v1']['latitude']))) % 360 - 360) <= _N_THRESHOLD_3

