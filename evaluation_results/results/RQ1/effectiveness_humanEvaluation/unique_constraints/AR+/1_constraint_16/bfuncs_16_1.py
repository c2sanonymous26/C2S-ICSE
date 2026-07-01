from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['timestamp'] >= ((-17631239/500 + var_bindings['v2']['timestamp']) + var_bindings['v2']['longitude'])
