from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle"""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v2 occurs after v1 in time"""
    return var_bindings["v2"]["timestamp"] > var_bindings["v1"]["timestamp"]

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the group sequence number of v2 is larger than the group sequence number of v1"""
    return var_bindings["v2"]["grpid"] > var_bindings["v1"]["grpid"]

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """the timestamp difference between v2 and v1 divided by the group sequence-number difference is within a certain expected sampling interval range"""
    return ((var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"]) / (var_bindings["v2"]["grpid"] - var_bindings["v1"]["grpid"]) >= 1.0) and ((var_bindings["v2"]["timestamp"] - var_bindings["v1"]["timestamp"]) / (var_bindings["v2"]["grpid"] - var_bindings["v1"]["grpid"]) <= 180.0)

