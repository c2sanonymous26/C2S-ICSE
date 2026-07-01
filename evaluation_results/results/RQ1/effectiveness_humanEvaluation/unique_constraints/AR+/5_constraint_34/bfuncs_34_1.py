from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['latitude'] >= (0 if abs((tan(tan(var_bindings['v1']['longitude'])) - (-(var_bindings['v1']['timestamp'] + var_bindings['v1']['direction'])))) < 1/1000 else log(abs((tan(tan(var_bindings['v1']['longitude'])) - (-(var_bindings['v1']['timestamp'] + var_bindings['v1']['direction']))))))
