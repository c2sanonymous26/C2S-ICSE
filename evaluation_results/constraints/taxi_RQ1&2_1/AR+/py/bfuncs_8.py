from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['longitude'] <= max(sin(var_bindings['v1']['speed']), sqrt(abs(-13228913/1000)))
