from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['carid'] == var_bindings['v2']['carid']

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['grpid'] == var_bindings['v2']['grpid'] + 1

def bfunc_3_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 6371.0 * 2 * atan2(sqrt(sin(radians(var_bindings['v2']['latitude'] - var_bindings['v1']['latitude']) / 2) * sin(radians(var_bindings['v2']['latitude'] - var_bindings['v1']['latitude']) / 2) + cos(radians(var_bindings['v1']['latitude'])) * cos(radians(var_bindings['v2']['latitude'])) * sin(radians(var_bindings['v2']['longitude'] - var_bindings['v1']['longitude']) / 2) * sin(radians(var_bindings['v2']['longitude'] - var_bindings['v1']['longitude']) / 2)), sqrt(1 - (sin(radians(var_bindings['v2']['latitude'] - var_bindings['v1']['latitude']) / 2) * sin(radians(var_bindings['v2']['latitude'] - var_bindings['v1']['latitude']) / 2) + cos(radians(var_bindings['v1']['latitude'])) * cos(radians(var_bindings['v2']['latitude'])) * sin(radians(var_bindings['v2']['longitude'] - var_bindings['v1']['longitude']) / 2) * sin(radians(var_bindings['v2']['longitude'] - var_bindings['v1']['longitude']) / 2)))) / abs(var_bindings['v1']['timestamp'] - var_bindings['v2']['timestamp']) >= -1/2

def bfunc_3_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 6371.0 * 2 * atan2(sqrt(sin(radians(var_bindings['v2']['latitude'] - var_bindings['v1']['latitude']) / 2) * sin(radians(var_bindings['v2']['latitude'] - var_bindings['v1']['latitude']) / 2) + cos(radians(var_bindings['v1']['latitude'])) * cos(radians(var_bindings['v2']['latitude'])) * sin(radians(var_bindings['v2']['longitude'] - var_bindings['v1']['longitude']) / 2) * sin(radians(var_bindings['v2']['longitude'] - var_bindings['v1']['longitude']) / 2)), sqrt(1 - (sin(radians(var_bindings['v2']['latitude'] - var_bindings['v1']['latitude']) / 2) * sin(radians(var_bindings['v2']['latitude'] - var_bindings['v1']['latitude']) / 2) + cos(radians(var_bindings['v1']['latitude'])) * cos(radians(var_bindings['v2']['latitude'])) * sin(radians(var_bindings['v2']['longitude'] - var_bindings['v1']['longitude']) / 2) * sin(radians(var_bindings['v2']['longitude'] - var_bindings['v1']['longitude']) / 2)))) / abs(var_bindings['v1']['timestamp'] - var_bindings['v2']['timestamp']) <= 57361310248003109/36028797018963968

def bfunc_4_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(6371.0 * 2 * atan2(sqrt(sin(radians(var_bindings['v2']['latitude'] - var_bindings['v1']['latitude']) / 2) * sin(radians(var_bindings['v2']['latitude'] - var_bindings['v1']['latitude']) / 2) + cos(radians(var_bindings['v1']['latitude'])) * cos(radians(var_bindings['v2']['latitude'])) * sin(radians(var_bindings['v2']['longitude'] - var_bindings['v1']['longitude']) / 2) * sin(radians(var_bindings['v2']['longitude'] - var_bindings['v1']['longitude']) / 2)), sqrt(1 - (sin(radians(var_bindings['v2']['latitude'] - var_bindings['v1']['latitude']) / 2) * sin(radians(var_bindings['v2']['latitude'] - var_bindings['v1']['latitude']) / 2) + cos(radians(var_bindings['v1']['latitude'])) * cos(radians(var_bindings['v2']['latitude'])) * sin(radians(var_bindings['v2']['longitude'] - var_bindings['v1']['longitude']) / 2) * sin(radians(var_bindings['v2']['longitude'] - var_bindings['v1']['longitude']) / 2)))) / abs(var_bindings['v1']['timestamp'] - var_bindings['v2']['timestamp']) - var_bindings['v1']['speed']) <= 4062755829896563/35184372088832

