from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['carid'] == var_bindings['v2']['carid']

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['latitude'] > min(cos(max((var_bindings['v1']['longitude'] * 50428911/1000), min(var_bindings['v2']['timestamp'], -1636811/250))), (-(-(1 if -1/1000 <= (var_bindings['v2']['longitude']) <= 1/1000 else (var_bindings['v1']['longitude']) / (var_bindings['v2']['longitude'])))))
