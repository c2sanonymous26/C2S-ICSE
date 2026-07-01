from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['carid'] != var_bindings['v2']['carid']

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['latitude'] >= tan(min(abs(max(cos(var_bindings['v2']['timestamp']), sqrt(abs(var_bindings['v2']['longitude'])))), (cos(tan(var_bindings['v1']['latitude'])) * (1 if -1/1000 <= ((var_bindings['v1']['latitude'] - 2333289/40)) <= 1/1000 else ((0 if abs(var_bindings['v2']['longitude']) < 1/1000 else log(abs(var_bindings['v2']['longitude'])))) / ((var_bindings['v1']['latitude'] - 2333289/40))))))
