from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['longitude'] > (1 if -1/1000 <= (max((1 if -1/1000 <= (var_bindings['v2']['longitude']) <= 1/1000 else (var_bindings['v1']['latitude']) / (var_bindings['v2']['longitude'])), (-(var_bindings['v1']['latitude'] + var_bindings['v1']['timestamp'])))) <= 1/1000 else ((0 if abs(var_bindings['v2']['timestamp']) < 1/1000 else log(abs(var_bindings['v2']['timestamp'])))) / (max((1 if -1/1000 <= (var_bindings['v2']['longitude']) <= 1/1000 else (var_bindings['v1']['latitude']) / (var_bindings['v2']['longitude'])), (-(var_bindings['v1']['latitude'] + var_bindings['v1']['timestamp'])))))
