from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['longitude'] < (-(cos(var_bindings['v1']['timestamp']) - sqrt(abs(17846543/1000))))
