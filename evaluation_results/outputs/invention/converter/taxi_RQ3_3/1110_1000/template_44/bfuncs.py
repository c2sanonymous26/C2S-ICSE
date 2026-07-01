from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The speed of v1 is zero."""
    return var_bindings["v1"]["speed"] == 0

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v2 is the previous context of v1, and the timestamp difference between v1 and v2 does not exceed a certain reasonable upper bound on stationary time."""
    return (var_bindings["v2"]["grpid"] == var_bindings["v1"]["grpid"] - 1) and ((var_bindings["v2"]["carid"] == var_bindings["v1"]["carid"]) and ((var_bindings["v1"]["timestamp"] - var_bindings["v2"]["timestamp"]) <= _N_THRESHOLD_1))

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v3 is the next context of v1, and the timestamp difference between v1 and v3 does not exceed a certain reasonable upper bound on stationary time."""
    return (var_bindings["v3"]["grpid"] == var_bindings["v1"]["grpid"] + 1) and ((var_bindings["v3"]["carid"] == var_bindings["v1"]["carid"]) and ((var_bindings["v3"]["timestamp"] - var_bindings["v1"]["timestamp"]) <= _N_THRESHOLD_2))

