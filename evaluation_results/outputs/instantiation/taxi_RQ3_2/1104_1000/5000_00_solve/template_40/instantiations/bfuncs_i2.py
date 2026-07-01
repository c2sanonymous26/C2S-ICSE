from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['speed'] > 229/2

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['carid'] == var_bindings['v1']['carid']

def bfunc_2_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['grpid'] == var_bindings['v1']['grpid'] - 1

def bfunc_3_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(atan2(sin(radians(var_bindings['v1']['longitude'] - var_bindings['v2']['longitude'])) * cos(radians(var_bindings['v1']['latitude'])), cos(radians(var_bindings['v2']['latitude'])) * sin(radians(var_bindings['v1']['latitude'])) - sin(radians(var_bindings['v2']['latitude'])) * cos(radians(var_bindings['v1']['latitude'])) * cos(radians(var_bindings['v1']['longitude'] - var_bindings['v2']['longitude']))) - var_bindings['v1']['direction']) <= -1/2

def bfunc_4_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['speed'] - var_bindings['v2']['speed']) <= -1/2

