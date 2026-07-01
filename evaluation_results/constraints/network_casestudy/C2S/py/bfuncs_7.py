from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['ScPci'] is not None

def bfunc_1_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['ScAOA'] is not None

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['ScPci'] % 3 == 0

def bfunc_2_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['ScAOA'] >= 0

def bfunc_2_c3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['ScAOA'] <= 719

def bfunc_2_c4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['ScPci'] % 3 == 1

def bfunc_2_c5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['ScAOA'] >= 0

def bfunc_2_c6(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['ScAOA'] <= 719

def bfunc_2_c7(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['ScPci'] % 3 == 2

def bfunc_2_c8(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['ScAOA'] >= 0

def bfunc_2_c9(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['ScAOA'] <= 719

