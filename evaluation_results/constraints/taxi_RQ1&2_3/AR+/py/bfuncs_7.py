from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['latitude'] < (0 if abs((cos(sin(sin(var_bindings['v1']['longitude']))) - abs(abs((var_bindings['v1']['timestamp'] * 11803291/1000))))) < 1/1000 else log(abs((cos(sin(sin(var_bindings['v1']['longitude']))) - abs(abs((var_bindings['v1']['timestamp'] * 11803291/1000)))))))
