from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle."""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The grpid value of v1 is equal to the grpid value of v2 minus 1, and the speed of v1 is zero."""
    return (var_bindings["v1"]["grpid"] == var_bindings["v2"]["grpid"] - 1) and (var_bindings["v1"]["speed"] == 0)

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The speed of v2 is zero."""
    return var_bindings["v2"]["speed"] == 0

