from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['carid'] == var_bindings['v2']['carid']

def bfunc_1_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['carid'] == var_bindings['v3']['carid']

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['grpid'] + 1 == var_bindings['v2']['grpid']

def bfunc_2_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['grpid'] + 1 == var_bindings['v3']['grpid']

def bfunc_3_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(atan2(sin(degrees(var_bindings['v2']['direction'] - var_bindings['v1']['direction'])), cos(degrees(var_bindings['v2']['direction'] - var_bindings['v1']['direction']))) - atan2(sin(degrees(var_bindings['v3']['direction'] - var_bindings['v2']['direction'])), cos(degrees(var_bindings['v3']['direction'] - var_bindings['v2']['direction'])))) <= _N_THRESHOLD_1

def bfunc_4_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(atan2(sin(degrees(var_bindings['v2']['direction'] - var_bindings['v1']['direction'])), cos(degrees(var_bindings['v2']['direction'] - var_bindings['v1']['direction']))) - atan2(sin(degrees(var_bindings['v3']['direction'] - var_bindings['v2']['direction'])), cos(degrees(var_bindings['v3']['direction'] - var_bindings['v2']['direction'])))) / abs(var_bindings['v3']['timestamp'] - var_bindings['v1']['timestamp']) <= _N_THRESHOLD_2

