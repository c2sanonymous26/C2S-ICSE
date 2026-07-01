from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['carid'] != var_bindings['v2']['carid']

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['longitude'] <= (var_bindings['v2']['latitude'] - (var_bindings['v1']['latitude'] * min((-var_bindings['v2']['timestamp']), max((var_bindings['v2']['timestamp'] * -56770299/1000), (var_bindings['v1']['direction'] + var_bindings['v2']['direction'])))))
