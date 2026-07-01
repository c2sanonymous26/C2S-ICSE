from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['latitude'] <= (1 if -1/1000 <= (abs(sqrt(abs(var_bindings['v2']['longitude'])))) <= 1/1000 else (max((var_bindings['v2']['direction'] + 40011111/1000), abs(var_bindings['v2']['direction']))) / (abs(sqrt(abs(var_bindings['v2']['longitude'])))))
