from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['carid'] == var_bindings['v2']['carid']

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['timestamp'] - var_bindings['v2']['timestamp']) <= -3/2

def bfunc_3_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return (var_bindings['v2']['speed'] - var_bindings['v1']['speed']) / (var_bindings['v2']['timestamp'] - var_bindings['v1']['timestamp']) * (abs(var_bindings['v2']['direction'] - var_bindings['v1']['direction']) / (var_bindings['v2']['timestamp'] - var_bindings['v1']['timestamp'])) <= -17147362014427305/18014398509481984

