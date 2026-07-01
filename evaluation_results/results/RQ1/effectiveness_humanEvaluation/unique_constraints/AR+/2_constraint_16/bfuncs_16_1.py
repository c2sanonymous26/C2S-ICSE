from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['timestamp'] <= (abs((((0 if abs(var_bindings['v1']['speed']) < 1/1000 else log(abs(var_bindings['v1']['speed']))) - max(var_bindings['v1']['direction'], 27122143/1000)) - sin((1 if -1/1000 <= (var_bindings['v1']['speed']) <= 1/1000 else (-7597243/125) / (var_bindings['v1']['speed']))))) * 7784713/125)
