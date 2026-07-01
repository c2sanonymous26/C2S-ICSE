from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['direction'] >= min(var_bindings['v1']['speed'], cos((max(var_bindings['v1']['speed'], var_bindings['v1']['longitude']) + sqrt(abs(var_bindings['v1']['timestamp'])))))
