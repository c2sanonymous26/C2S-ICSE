from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The speed of v1 is 0 and this state persists for longer than a certain reasonable time threshold."""
    return var_bindings["v1"]["speed"] == 0

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v2 is the previous context of v1."""
    return (var_bindings["v2"]["carid"] == var_bindings["v1"]["carid"]) and (var_bindings["v2"]["grpid"] == var_bindings["v1"]["grpid"] - 1)

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v3 is the previous context of v2."""
    return (var_bindings["v3"]["carid"] == var_bindings["v2"]["carid"]) and (var_bindings["v3"]["grpid"] == var_bindings["v2"]["grpid"] - 1)

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The standard deviation of the direction-angle changes among v1, v2, and v3 does not exceed a certain reasonable stationary heading fluctuation range."""
    return sqrt(pow(abs(var_bindings["v1"]["direction"] - var_bindings["v2"]["direction"]), 2) + pow(abs(var_bindings["v2"]["direction"] - var_bindings["v3"]["direction"]), 2)) / 2 <= _N_THRESHOLD_1

