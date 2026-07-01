from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['longitude'] > (abs(((0 if abs(var_bindings['v2']['timestamp']) < 1/1000 else log(abs(var_bindings['v2']['timestamp']))) - var_bindings['v1']['longitude'])) - (var_bindings['v2']['latitude'] * sin(cos(var_bindings['v2']['latitude']))))
