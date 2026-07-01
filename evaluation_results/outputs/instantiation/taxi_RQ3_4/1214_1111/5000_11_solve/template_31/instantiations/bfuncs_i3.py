from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['carid'] != var_bindings['v2']['carid']

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['timestamp'] - var_bindings['v2']['timestamp']) <= 26

def bfunc_3_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return sqrt(pow(var_bindings['v1']['latitude'] - var_bindings['v2']['latitude'], 2) + pow(var_bindings['v1']['longitude'] - var_bindings['v2']['longitude'], 2)) <= 8224517738751551/73786976294838206464

def bfunc_4_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(degrees(atan2(var_bindings['v2']['latitude'] - var_bindings['v1']['latitude'], var_bindings['v2']['longitude'] - var_bindings['v1']['longitude'])) - degrees(atan2(var_bindings['v1']['speed'] - var_bindings['v2']['speed'], 1.0))) <= 6335458287508093/35184372088832

