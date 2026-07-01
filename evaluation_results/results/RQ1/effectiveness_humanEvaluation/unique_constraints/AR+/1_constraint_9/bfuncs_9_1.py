from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['carid'] == var_bindings['v2']['carid']

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return (0.000000000 <= var_bindings['v2']['direction'] <= 31.500000000)

def bfunc_3_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['direction'] == (1 if -1/1000 <= (var_bindings['v1']['timestamp']) <= 1/1000 else ((1 if -1/1000 <= (var_bindings['v2']['longitude']) <= 1/1000 else (var_bindings['v1']['latitude']) / (var_bindings['v2']['longitude']))) / (var_bindings['v1']['timestamp']))
