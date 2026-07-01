from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['carid'] == var_bindings['v2']['carid']

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['longitude'] <= (sqrt(abs(-7690083/500)) - (0 if abs(var_bindings['v2']['latitude']) < 1/1000 else log(abs(var_bindings['v2']['latitude']))))
