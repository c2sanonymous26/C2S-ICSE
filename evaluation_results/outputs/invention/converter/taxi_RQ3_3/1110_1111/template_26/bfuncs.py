from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle."""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The grpid value of v1 is smaller than that of v2."""
    return var_bindings["v1"]["grpid"] < var_bindings["v2"]["grpid"]

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The speed of v1 is greater than the speed of v2."""
    return var_bindings["v1"]["speed"] > var_bindings["v2"]["speed"]

