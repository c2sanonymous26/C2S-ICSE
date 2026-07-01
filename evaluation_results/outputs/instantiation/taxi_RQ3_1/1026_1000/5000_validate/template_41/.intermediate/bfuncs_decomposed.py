from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['carid'] == var_bindings['v2']['carid']

def bfunc_1_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['grpid'] - var_bindings['v2']['grpid']) == 1

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['direction'] >= 0

def bfunc_2_c10(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['direction'] < 270

def bfunc_2_c11(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['direction'] >= 180

def bfunc_2_c12(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['direction'] < 270

def bfunc_2_c13(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['direction'] >= 270

def bfunc_2_c14(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['direction'] < 360

def bfunc_2_c15(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['direction'] >= 270

def bfunc_2_c16(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['direction'] < 360

def bfunc_2_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['direction'] < 90

def bfunc_2_c3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['direction'] >= 0

def bfunc_2_c4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['direction'] < 90

def bfunc_2_c5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['direction'] >= 90

def bfunc_2_c6(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['direction'] < 180

def bfunc_2_c7(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['direction'] >= 90

def bfunc_2_c8(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['direction'] < 180

def bfunc_2_c9(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['direction'] >= 180

def bfunc_3_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['longitude'] - var_bindings['v2']['longitude'] > 0

def bfunc_3_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['latitude'] - var_bindings['v2']['latitude'] > 0

def bfunc_3_c3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['longitude'] - var_bindings['v2']['longitude'] < 0

def bfunc_3_c4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['latitude'] - var_bindings['v2']['latitude'] < 0

