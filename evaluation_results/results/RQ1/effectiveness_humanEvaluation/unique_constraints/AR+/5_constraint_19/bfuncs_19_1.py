from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['longitude'] <= abs(abs((tan(abs(-35078421/1000)) - abs(var_bindings['v2']['longitude']))))
