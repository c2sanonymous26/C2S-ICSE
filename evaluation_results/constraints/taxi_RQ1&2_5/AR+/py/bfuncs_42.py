from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['longitude'] <= ((0 if abs(var_bindings['v2']['longitude']) < 1/1000 else log(abs(var_bindings['v2']['longitude']))) * sqrt(abs(((0 if abs(var_bindings['v2']['longitude']) < 1/1000 else log(abs(var_bindings['v2']['longitude']))) * ((0 if abs(var_bindings['v2']['longitude']) < 1/1000 else log(abs(var_bindings['v2']['longitude']))) * sqrt(abs(((0 if abs(var_bindings['v2']['longitude']) < 1/1000 else log(abs(var_bindings['v2']['longitude']))) * sqrt(abs(-13730841/500))))))))))
