from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['carid'] != var_bindings['v2']['carid']

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['timestamp'] - var_bindings['v2']['timestamp']) <= 59

def bfunc_3_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return pow(abs(var_bindings['v1']['latitude'] - var_bindings['v2']['latitude']), 2) + pow(abs(var_bindings['v1']['longitude'] - var_bindings['v2']['longitude']), 2) <= -1/1000000

def bfunc_4_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(degrees(atan2(sin(radians(var_bindings['v1']['direction'] - var_bindings['v2']['direction'])), cos(radians(var_bindings['v1']['direction'] - var_bindings['v2']['direction'])))) - degrees(atan2(var_bindings['v2']['latitude'] - var_bindings['v1']['latitude'], var_bindings['v2']['longitude'] - var_bindings['v1']['longitude']))) <= 686543686500655/35184372088832

