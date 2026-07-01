from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['timestamp'] <= ((4916988/125 + var_bindings['v1']['speed']) * max(var_bindings['v1']['longitude'], 4410372/125))
