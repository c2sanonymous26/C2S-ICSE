from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['latitude'] > sin(cos(((var_bindings['v1']['speed'] + -16583383/1000) - sin(var_bindings['v1']['longitude']))))
