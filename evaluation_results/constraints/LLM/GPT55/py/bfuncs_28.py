from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle."""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The grpid recorded in v2 is greater than the grpid recorded in v1."""
    return var_bindings["v2"]["grpid"] > var_bindings["v1"]["grpid"]

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The timestamp difference between v2 and v1 divided by the grpid difference between v2 and v1 lies within a certain reasonable per-record sampling interval range."""
    return ((var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"]) / (var_bindings["v2"]["grpid"] - var_bindings["v1"]["grpid"]) >= 1.0) and ((var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"]) / (var_bindings["v2"]["grpid"] - var_bindings["v1"]["grpid"]) <= 61.0)

