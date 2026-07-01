from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The speed value of v1 lies within a certain reasonable range."""
    return (var_bindings["v1"]["speed"] >= _N_THRESHOLD_1) and (var_bindings["v1"]["speed"] <= _N_THRESHOLD_2)

