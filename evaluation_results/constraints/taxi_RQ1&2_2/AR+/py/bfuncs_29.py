from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['carid'] != var_bindings['v2']['carid']

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['timestamp'] <= max(max(((var_bindings['v1']['timestamp'] + 55248019/1000) - (-var_bindings['v2']['direction'])), (max(var_bindings['v1']['latitude'], 53975227/1000) - sin(var_bindings['v1']['direction']))), cos(((0 if abs(var_bindings['v1']['timestamp']) < 1/1000 else log(abs(var_bindings['v1']['timestamp']))) - (var_bindings['v2']['direction'] - var_bindings['v1']['speed']))))
