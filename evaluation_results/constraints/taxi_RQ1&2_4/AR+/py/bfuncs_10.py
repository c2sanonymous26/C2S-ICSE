from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['speed'] >= cos((0 if abs(var_bindings['v1']['timestamp']) < 1/1000 else log(abs(var_bindings['v1']['timestamp']))))
