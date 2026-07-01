from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['latitude'] < min((1 if -1/1000 <= (sqrt(abs(max(min(var_bindings['v1']['direction'], 12434701/200), max(var_bindings['v1']['longitude'], var_bindings['v1']['direction']))))) <= 1/1000 else (abs(abs(max(var_bindings['v1']['longitude'], var_bindings['v1']['timestamp'])))) / (sqrt(abs(max(min(var_bindings['v1']['direction'], 12434701/200), max(var_bindings['v1']['longitude'], var_bindings['v1']['direction'])))))), ((-abs(sin(var_bindings['v1']['direction']))) + var_bindings['v1']['timestamp']))
