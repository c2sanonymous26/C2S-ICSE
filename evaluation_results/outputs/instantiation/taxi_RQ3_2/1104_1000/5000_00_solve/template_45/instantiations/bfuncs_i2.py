from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['speed'] > 4205862801940628247359/36893488147419103232

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['carid'] == var_bindings['v1']['carid']

def bfunc_2_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['grpid'] == var_bindings['v1']['grpid'] - 1

def bfunc_3_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return sqrt(pow(var_bindings['v1']['latitude'] - var_bindings['v2']['latitude'], 2) + pow(var_bindings['v1']['longitude'] - var_bindings['v2']['longitude'], 2)) / (var_bindings['v1']['timestamp'] - var_bindings['v2']['timestamp']) >= 16753517435183753/36893488147419103232

def bfunc_3_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return sqrt(pow(var_bindings['v1']['latitude'] - var_bindings['v2']['latitude'], 2) + pow(var_bindings['v1']['longitude'] - var_bindings['v2']['longitude'], 2)) / (var_bindings['v1']['timestamp'] - var_bindings['v2']['timestamp']) <= 5153134850478911/36893488147419103232

def bfunc_4_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['timestamp'] - var_bindings['v2']['timestamp'] >= 1438861497153896462781/36893488147419103232

def bfunc_4_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['timestamp'] - var_bindings['v2']['timestamp'] <= -5153134850478911/36893488147419103232

