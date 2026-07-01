from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return (0.000000000 <= var_bindings['v1']['direction'] <= 15.750000000)

def bfunc_1_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return (0.000000000 <= var_bindings['v1']['speed'] <= 5.700000000)

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['speed'] <= (1 if -1/1000 <= (var_bindings['v1']['timestamp']) <= 1/1000 else (sqrt(abs(sqrt(abs((0 if abs((0 if abs(var_bindings['v1']['timestamp']) < 1/1000 else log(abs(var_bindings['v1']['timestamp'])))) < 1/1000 else log(abs((0 if abs(var_bindings['v1']['timestamp']) < 1/1000 else log(abs(var_bindings['v1']['timestamp']))))))))))) / (var_bindings['v1']['timestamp']))
