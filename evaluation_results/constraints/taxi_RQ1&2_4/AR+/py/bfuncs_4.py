from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['carid'] == var_bindings['v2']['carid']

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['longitude'] > (((1 if -1/1000 <= ((1 if -1/1000 <= (var_bindings['v2']['speed']) <= 1/1000 else (var_bindings['v2']['timestamp']) / (var_bindings['v2']['speed']))) <= 1/1000 else ((var_bindings['v1']['direction'] - var_bindings['v1']['timestamp'])) / ((1 if -1/1000 <= (var_bindings['v2']['speed']) <= 1/1000 else (var_bindings['v2']['timestamp']) / (var_bindings['v2']['speed'])))) + ((1 if -1/1000 <= (var_bindings['v1']['timestamp']) <= 1/1000 else (var_bindings['v2']['direction']) / (var_bindings['v1']['timestamp'])) * tan(var_bindings['v1']['direction']))) * abs(min(sqrt(abs(var_bindings['v1']['speed'])), sqrt(abs(var_bindings['v1']['direction'])))))
