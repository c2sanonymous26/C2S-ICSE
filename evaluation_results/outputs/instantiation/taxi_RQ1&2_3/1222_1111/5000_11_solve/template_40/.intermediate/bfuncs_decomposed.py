from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['carid'] == var_bindings['v2']['carid']

def bfunc_1_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['carid'] == var_bindings['v3']['carid']

def bfunc_1_c3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['grpid'] - var_bindings['v1']['grpid'] == 1

def bfunc_1_c4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v3']['grpid'] - var_bindings['v2']['grpid'] == 1

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['speed'] > _N_THRESHOLD_1

def bfunc_2_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v3']['speed'] > _N_THRESHOLD_1

def bfunc_3_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['speed'] < _N_THRESHOLD_2

def bfunc_4_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(degrees(atan2(sin(radians(var_bindings['v3']['longitude'] - var_bindings['v1']['longitude'])) * cos(radians(var_bindings['v3']['latitude'])), cos(radians(var_bindings['v1']['latitude'])) * sin(radians(var_bindings['v3']['latitude'])) - sin(radians(var_bindings['v1']['latitude'])) * cos(radians(var_bindings['v3']['latitude'])) * cos(radians(var_bindings['v3']['longitude'] - var_bindings['v1']['longitude'])))) - var_bindings['v2']['direction']) <= _N_THRESHOLD_3

