from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['carid'] != var_bindings['v2']['carid']

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['timestamp'] >= (var_bindings['v1']['latitude'] - min(((max(abs(var_bindings['v1']['latitude']), tan(var_bindings['v2']['longitude'])) + sqrt(abs(abs(var_bindings['v1']['latitude'])))) - (abs(max(var_bindings['v1']['latitude'], var_bindings['v2']['speed'])) + tan((var_bindings['v2']['direction'] - var_bindings['v1']['longitude'])))), (min((0 if abs(min(var_bindings['v1']['timestamp'], var_bindings['v2']['latitude'])) < 1/1000 else log(abs(min(var_bindings['v1']['timestamp'], var_bindings['v2']['latitude'])))), (0 if abs((1 if -1/1000 <= (var_bindings['v2']['speed']) <= 1/1000 else (var_bindings['v1']['speed']) / (var_bindings['v2']['speed']))) < 1/1000 else log(abs((1 if -1/1000 <= (var_bindings['v2']['speed']) <= 1/1000 else (var_bindings['v1']['speed']) / (var_bindings['v2']['speed'])))))) - max(max(min(var_bindings['v2']['speed'], var_bindings['v1']['direction']), (-10267543/250 + var_bindings['v1']['timestamp'])), max(abs(var_bindings['v1']['direction']), (-var_bindings['v2']['speed']))))))
