from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['carid'] != var_bindings['v2']['carid']

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['timestamp'] - var_bindings['v2']['timestamp']) <= 2

def bfunc_3_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return sqrt(pow(var_bindings['v1']['latitude'] - var_bindings['v2']['latitude'], 2) + pow(var_bindings['v1']['longitude'] - var_bindings['v2']['longitude'], 2)) <= 2882279838395897/288230376151711744

def bfunc_4_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(atan2(sin(var_bindings['v1']['direction'] - var_bindings['v2']['direction']), cos(var_bindings['v1']['direction'] - var_bindings['v2']['direction'])) - atan2(var_bindings['v2']['latitude'] - var_bindings['v1']['latitude'], var_bindings['v2']['longitude'] - var_bindings['v1']['longitude'])) <= 6952801925861889/1125899906842624

