from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v0 belongs to the same vehicle as v1 and the grpid of v0 is smaller than the grpid of v1."""
    return (var_bindings["v0"]["carid"] == var_bindings["v1"]["carid"]) and (var_bindings["v0"]["grpid"] < var_bindings["v1"]["grpid"])

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v2 belongs to the same vehicle as v1 and the grpid of v2 immediately precedes the grpid of v1."""
    return (var_bindings["v2"]["carid"] == var_bindings["v1"]["carid"]) and (var_bindings["v2"]["grpid"] == var_bindings["v1"]["grpid"] - 1)

