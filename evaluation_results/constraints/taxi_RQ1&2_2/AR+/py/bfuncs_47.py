from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['carid'] != var_bindings['v2']['carid']

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['speed'] < ((sqrt(abs(abs((-var_bindings['v1']['longitude'])))) - (abs(abs(61240201/1000)) - (min(var_bindings['v1']['speed'], var_bindings['v1']['direction']) + (1 if -1/1000 <= (var_bindings['v1']['latitude']) <= 1/1000 else (var_bindings['v2']['timestamp']) / (var_bindings['v1']['latitude']))))) * sqrt(abs(((tan(var_bindings['v2']['latitude']) * min(var_bindings['v1']['longitude'], var_bindings['v1']['speed'])) - max(abs(9619071/250), cos(var_bindings['v1']['direction']))))))
