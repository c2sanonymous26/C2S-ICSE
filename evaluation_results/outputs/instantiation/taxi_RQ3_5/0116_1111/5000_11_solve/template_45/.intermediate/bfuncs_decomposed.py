from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['carid'] != var_bindings['v2']['carid']

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['timestamp'] - var_bindings['v2']['timestamp']) <= _N_THRESHOLD_1

def bfunc_3_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v3']['carid'] == var_bindings['v1']['carid']

def bfunc_3_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v3']['grpid'] == var_bindings['v1']['grpid'] - 1

def bfunc_3_c3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v4']['carid'] == var_bindings['v1']['carid']

def bfunc_3_c4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v4']['grpid'] == var_bindings['v1']['grpid'] + 1

def bfunc_4_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v5']['carid'] == var_bindings['v2']['carid']

def bfunc_4_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v5']['grpid'] == var_bindings['v2']['grpid'] - 1

def bfunc_4_c3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v6']['carid'] == var_bindings['v2']['carid']

def bfunc_4_c4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v6']['grpid'] == var_bindings['v2']['grpid'] + 1

def bfunc_5_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs((atan2(sin(radians(var_bindings['v1']['direction'] - var_bindings['v3']['direction'])), cos(radians(var_bindings['v1']['direction'] - var_bindings['v3']['direction']))) - atan2(sin(radians(var_bindings['v2']['direction'] - var_bindings['v5']['direction'])), cos(radians(var_bindings['v2']['direction'] - var_bindings['v5']['direction'])))) / (var_bindings['v1']['timestamp'] - var_bindings['v2']['timestamp'])) <= _N_THRESHOLD_2

