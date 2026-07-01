from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return (0.000000000 <= var_bindings['v1']['direction'] <= 15.750000000)

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['direction'] <= (1 if -1/1000 <= (var_bindings['v1']['timestamp']) <= 1/1000 else (((1 if -1/1000 <= (var_bindings['v1']['timestamp']) <= 1/1000 else (-4434349/125) / (var_bindings['v1']['timestamp'])) * -47343003/1000)) / (var_bindings['v1']['timestamp']))
