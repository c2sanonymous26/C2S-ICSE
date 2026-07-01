from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['carid'] != var_bindings['v2']['carid']

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['timestamp'] > (((0 if abs(sin((var_bindings['v2']['timestamp'] - var_bindings['v1']['latitude']))) < 1/1000 else log(abs(sin((var_bindings['v2']['timestamp'] - var_bindings['v1']['latitude']))))) + cos((1 if -1/1000 <= (sqrt(abs(var_bindings['v1']['longitude']))) <= 1/1000 else ((var_bindings['v1']['speed'] * var_bindings['v2']['longitude'])) / (sqrt(abs(var_bindings['v1']['longitude'])))))) + (((sqrt(abs(var_bindings['v1']['speed'])) - (-var_bindings['v2']['timestamp'])) + (-(0 if abs(var_bindings['v2']['speed']) < 1/1000 else log(abs(var_bindings['v2']['speed']))))) - (max(abs(var_bindings['v1']['direction']), var_bindings['v1']['longitude']) * max(max(var_bindings['v2']['latitude'], var_bindings['v1']['speed']), max(var_bindings['v1']['speed'], var_bindings['v1']['latitude'])))))
