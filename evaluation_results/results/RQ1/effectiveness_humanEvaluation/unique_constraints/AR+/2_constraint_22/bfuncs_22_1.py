from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['direction'] < (max(max(sqrt(abs(var_bindings['v1']['timestamp'])), min(var_bindings['v1']['timestamp'], var_bindings['v1']['longitude'])), sin((-507876/125 * var_bindings['v1']['latitude']))) * max((abs(var_bindings['v1']['longitude']) * sqrt(abs(-13987173/250))), cos(min(var_bindings['v1']['timestamp'], -19905311/500))))
