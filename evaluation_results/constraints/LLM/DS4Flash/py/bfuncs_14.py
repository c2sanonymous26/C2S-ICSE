from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle (v1.carid = v2.carid)"""
    return var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1.grpid is less than v2.grpid"""
    return var_bindings["v1"]["grpid"] < var_bindings["v2"]["grpid"]

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1.timestamp is less than v2.timestamp"""
    return var_bindings["v1"]["timestamp"] < var_bindings["v2"]["timestamp"]

