from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['timestamp'] <= ((((var_bindings['v2']['speed'] + var_bindings['v2']['timestamp']) - (1 if -1/1000 <= (var_bindings['v2']['longitude']) <= 1/1000 else (var_bindings['v2']['latitude']) / (var_bindings['v2']['longitude']))) - abs(max(-20974037/1000, var_bindings['v1']['direction']))) - min(sin(max(var_bindings['v1']['latitude'], var_bindings['v1']['speed'])), (-(59485027/1000 - var_bindings['v2']['longitude']))))
