from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle."""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The grpid of v2 immediately follows the grpid of v1."""
    return var_bindings["v2"]["grpid"] == var_bindings["v1"]["grpid"] + 1

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The timestamp of v2 is greater than the timestamp of v1."""
    return var_bindings["v2"]["timestamp"] > var_bindings["v1"]["timestamp"]

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The timestamp difference between v1 and v2 is within a reliable comparison range."""
    return var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"] <= 21.0

def bfunc_5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The speeds recorded in both v1 and v2 are sufficiently high for direction comparison."""
    return (var_bindings["v1"]["speed"] >= 20.0) and (var_bindings["v2"]["speed"] >= 20.0)

def bfunc_6(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The absolute normalized heading difference between v1 and v2 divided by their timestamp difference does not exceed a certain reasonable upper bound."""
    return min(abs(var_bindings["v2"]["direction"] - var_bindings["v1"]["direction"]), 360 - abs(var_bindings["v2"]["direction"] - var_bindings["v1"]["direction"])) / (var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"]) <= 5.0

