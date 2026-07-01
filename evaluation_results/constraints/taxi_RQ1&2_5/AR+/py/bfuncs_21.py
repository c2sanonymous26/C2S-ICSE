from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['carid'] != var_bindings['v2']['carid']

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['timestamp'] > (sin((-(var_bindings['v2']['speed'] * var_bindings['v2']['latitude']))) + (max((var_bindings['v1']['timestamp'] - 1713383/100), abs(var_bindings['v1']['speed'])) - (1 if -1/1000 <= (sqrt(abs(var_bindings['v2']['latitude']))) <= 1/1000 else (sin(var_bindings['v1']['direction'])) / (sqrt(abs(var_bindings['v2']['latitude']))))))
