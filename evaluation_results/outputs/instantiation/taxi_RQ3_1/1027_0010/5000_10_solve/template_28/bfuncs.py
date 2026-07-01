from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['carid'] != var_bindings['v2']['carid']

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['timestamp'] - var_bindings['v2']['timestamp']) <= 20

def bfunc_3_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 6371 * 2 * asin(sqrt(pow(sin((radians(var_bindings['v1']['latitude']) - radians(var_bindings['v2']['latitude'])) / 2), 2) + cos(radians(var_bindings['v1']['latitude'])) * cos(radians(var_bindings['v2']['latitude'])) * pow(sin((radians(var_bindings['v1']['longitude']) - radians(var_bindings['v2']['longitude'])) / 2), 2))) <= 8404984244630085/4503599627370496

def bfunc_4_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['speed'] - var_bindings['v2']['speed']) <= 114

