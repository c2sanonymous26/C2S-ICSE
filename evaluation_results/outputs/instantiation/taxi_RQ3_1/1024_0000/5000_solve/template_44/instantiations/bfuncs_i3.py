from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['latitude'] >= -1/2

def bfunc_1_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['latitude'] <= 6548304226940879/281474976710656

def bfunc_1_c3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['longitude'] >= 1/2

def bfunc_1_c4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['longitude'] <= 4086800277950379/35184372088832

