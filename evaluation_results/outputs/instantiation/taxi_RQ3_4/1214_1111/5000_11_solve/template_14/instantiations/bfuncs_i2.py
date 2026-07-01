from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['carid'] == var_bindings['v2']['carid']

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['timestamp'] - var_bindings['v2']['timestamp']) <= 96

def bfunc_3_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return sqrt(pow(var_bindings['v1']['longitude'] - var_bindings['v2']['longitude'], 2) + pow(var_bindings['v1']['latitude'] - var_bindings['v2']['latitude'], 2)) <= 19208458707835/562949953421312

