from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['timestamp'] < abs((var_bindings['v1']['timestamp'] + 25022633/1000))
