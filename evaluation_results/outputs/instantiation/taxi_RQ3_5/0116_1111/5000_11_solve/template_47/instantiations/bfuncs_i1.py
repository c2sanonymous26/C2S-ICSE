from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['speed'] > 112

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['carid'] == var_bindings['v2']['carid']

def bfunc_3_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['grpid'] == var_bindings['v1']['grpid'] - 2

def bfunc_4_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs((var_bindings['v1']['speed'] - var_bindings['v2']['speed']) / (var_bindings['v1']['timestamp'] - var_bindings['v2']['timestamp'])) <= 2476979795053773/2251799813685248

