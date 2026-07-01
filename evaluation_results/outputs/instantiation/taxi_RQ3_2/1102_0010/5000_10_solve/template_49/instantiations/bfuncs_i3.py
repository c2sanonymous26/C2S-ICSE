from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['carid'] != var_bindings['v2']['carid']

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['timestamp'] - var_bindings['v2']['timestamp']) <= 0

def bfunc_3_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['speed'] - var_bindings['v2']['speed']) / sqrt(pow(var_bindings['v1']['latitude'] - var_bindings['v2']['latitude'], 2) + pow(var_bindings['v1']['longitude'] - var_bindings['v2']['longitude'], 2)) == 3140272735338119/562949953421312

def bfunc_4_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['speed'] - var_bindings['v2']['speed']) / sqrt(pow(var_bindings['v1']['latitude'] - var_bindings['v2']['latitude'], 2) + pow(var_bindings['v1']['longitude'] - var_bindings['v2']['longitude'], 2)) >= 9999783/1000000

def bfunc_4_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['speed'] - var_bindings['v2']['speed']) / sqrt(pow(var_bindings['v1']['latitude'] - var_bindings['v2']['latitude'], 2) + pow(var_bindings['v1']['longitude'] - var_bindings['v2']['longitude'], 2)) <= 5938872146635715/2251799813685248

