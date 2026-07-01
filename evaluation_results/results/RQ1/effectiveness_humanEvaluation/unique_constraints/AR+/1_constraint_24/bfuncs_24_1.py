from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['latitude'] > (0 if abs(max(var_bindings['v1']['timestamp'], var_bindings['v2']['timestamp'])) < 1/1000 else log(abs(max(var_bindings['v1']['timestamp'], var_bindings['v2']['timestamp']))))
