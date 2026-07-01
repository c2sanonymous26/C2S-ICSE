from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['carid'] == var_bindings['v2']['carid']

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['speed'] >= ((max(((var_bindings['v2']['latitude'] + var_bindings['v2']['timestamp']) - min(var_bindings['v2']['speed'], var_bindings['v2']['timestamp'])), abs((var_bindings['v2']['speed'] + var_bindings['v1']['timestamp']))) * (1 if -1/1000 <= (sqrt(abs((0 if abs(var_bindings['v2']['timestamp']) < 1/1000 else log(abs(var_bindings['v2']['timestamp'])))))) <= 1/1000 else ((-(0 if abs(var_bindings['v1']['longitude']) < 1/1000 else log(abs(var_bindings['v1']['longitude']))))) / (sqrt(abs((0 if abs(var_bindings['v2']['timestamp']) < 1/1000 else log(abs(var_bindings['v2']['timestamp'])))))))) + ((0 if abs((1 if -1/1000 <= ((0 if abs(var_bindings['v2']['speed']) < 1/1000 else log(abs(var_bindings['v2']['speed'])))) <= 1/1000 else (sqrt(abs(var_bindings['v1']['longitude']))) / ((0 if abs(var_bindings['v2']['speed']) < 1/1000 else log(abs(var_bindings['v2']['speed'])))))) < 1/1000 else log(abs((1 if -1/1000 <= ((0 if abs(var_bindings['v2']['speed']) < 1/1000 else log(abs(var_bindings['v2']['speed'])))) <= 1/1000 else (sqrt(abs(var_bindings['v1']['longitude']))) / ((0 if abs(var_bindings['v2']['speed']) < 1/1000 else log(abs(var_bindings['v2']['speed'])))))))) * abs(sqrt(abs((var_bindings['v1']['longitude'] * var_bindings['v1']['longitude']))))))
