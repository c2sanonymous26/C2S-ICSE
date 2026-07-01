from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['direction'] >= ((-min(tan(var_bindings['v2']['latitude']), (var_bindings['v2']['timestamp'] * var_bindings['v2']['speed']))) + (0 if abs(min(cos(((var_bindings['v1']['latitude'] - var_bindings['v1']['speed']) - (1 if -1/1000 <= (var_bindings['v1']['longitude']) <= 1/1000 else (var_bindings['v1']['longitude']) / (var_bindings['v1']['longitude'])))), var_bindings['v1']['speed'])) < 1/1000 else log(abs(min(cos(((var_bindings['v1']['latitude'] - var_bindings['v1']['speed']) - (1 if -1/1000 <= (var_bindings['v1']['longitude']) <= 1/1000 else (var_bindings['v1']['longitude']) / (var_bindings['v1']['longitude'])))), var_bindings['v1']['speed'])))))
