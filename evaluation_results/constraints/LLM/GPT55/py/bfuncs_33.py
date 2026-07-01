from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle."""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The grpid of v2 immediately follows the grpid of v1."""
    return var_bindings["v2"]["grpid"] - var_bindings["v1"]["grpid"] == 1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The timestamp recorded in v2 is greater than the timestamp recorded in v1."""
    return var_bindings["v2"]["timestamp"] > var_bindings["v1"]["timestamp"]

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The speed recorded in v1 is sufficiently high."""
    return var_bindings["v1"]["speed"] >= 70.0

def bfunc_5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The speed recorded in v2 is sufficiently high."""
    return var_bindings["v2"]["speed"] >= 70.0

def bfunc_6(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The timestamp difference between v2 and v1 is within a sufficiently short high-speed sampling interval."""
    return var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"] <= 21.0

