from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['carid'] == var_bindings['v2']['carid']

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['grpid'] - var_bindings['v2']['grpid']) == 1

def bfunc_3_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(atan2(var_bindings['v2']['latitude'] - var_bindings['v1']['latitude'], var_bindings['v2']['longitude'] - var_bindings['v1']['longitude']) - var_bindings['v1']['direction']) <= _N_THRESHOLD_1

