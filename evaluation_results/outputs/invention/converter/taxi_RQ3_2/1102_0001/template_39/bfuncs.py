from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """When the speed value of v1 is zero, its direction value may be ignored or remain unchanged."""
    return (var_bindings["v1"]["speed"] == 0) or (var_bindings["v1"]["direction"] == _N_THRESHOLD_1)

