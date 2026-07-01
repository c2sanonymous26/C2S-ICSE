from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['speed'] > 114

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['grpid'] == var_bindings['v1']['grpid'] + 1

def bfunc_2_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['carid'] == var_bindings['v1']['carid']

def bfunc_3_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 6371.0 * 1000 * 2 * atan2(sqrt(sin(radians(var_bindings['v2']['latitude'] - var_bindings['v1']['latitude']) / 2) * sin(radians(var_bindings['v2']['latitude'] - var_bindings['v1']['latitude']) / 2) + cos(radians(var_bindings['v1']['latitude'])) * cos(radians(var_bindings['v2']['latitude'])) * sin(radians(var_bindings['v2']['longitude'] - var_bindings['v1']['longitude']) / 2) * sin(radians(var_bindings['v2']['longitude'] - var_bindings['v1']['longitude']) / 2)), sqrt(1 - (sin(radians(var_bindings['v2']['latitude'] - var_bindings['v1']['latitude']) / 2) * sin(radians(var_bindings['v2']['latitude'] - var_bindings['v1']['latitude']) / 2) + cos(radians(var_bindings['v1']['latitude'])) * cos(radians(var_bindings['v2']['latitude'])) * sin(radians(var_bindings['v2']['longitude'] - var_bindings['v1']['longitude']) / 2) * sin(radians(var_bindings['v2']['longitude'] - var_bindings['v1']['longitude']) / 2)))) / (var_bindings['v2']['timestamp'] - var_bindings['v1']['timestamp']) <= 2660846312611289/1125899906842624

