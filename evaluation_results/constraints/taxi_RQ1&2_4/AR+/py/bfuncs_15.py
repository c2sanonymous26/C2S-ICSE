from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['speed'] < (min((var_bindings['v2']['speed'] + var_bindings['v2']['timestamp']), var_bindings['v1']['longitude']) + (var_bindings['v1']['latitude'] * (1 if -1/1000 <= (var_bindings['v2']['latitude']) <= 1/1000 else (var_bindings['v2']['latitude']) / (var_bindings['v2']['latitude']))))
