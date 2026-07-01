from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['latitude'] > cos((0 if abs((var_bindings['v2']['longitude'] - var_bindings['v2']['direction'])) < 1/1000 else log(abs((var_bindings['v2']['longitude'] - var_bindings['v2']['direction'])))))
