from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['latitude'] < min(sqrt(abs((1 if -1/1000 <= (abs(var_bindings['v1']['longitude'])) <= 1/1000 else ((-(-31411503/500 - var_bindings['v1']['speed']))) / (abs(var_bindings['v1']['longitude']))))), max(var_bindings['v1']['longitude'], sin(sqrt(abs((var_bindings['v1']['longitude'] - var_bindings['v1']['timestamp']))))))
