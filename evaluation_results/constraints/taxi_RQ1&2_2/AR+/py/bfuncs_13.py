from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['timestamp'] <= (((-34115753/1000 * abs(42127481/1000)) * (cos(var_bindings['v1']['speed']) - var_bindings['v1']['latitude'])) + abs((0 if abs(tan(var_bindings['v1']['longitude'])) < 1/1000 else log(abs(tan(var_bindings['v1']['longitude']))))))
