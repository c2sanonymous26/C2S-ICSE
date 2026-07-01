from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1, v2, and v3 belong to the same vehicle."""
    return (var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]) and (var_bindings["v2"]["carid"] == var_bindings["v3"]["carid"])

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1, v2, and v3 are consecutive in grpid order."""
    return (var_bindings["v1"]["grpid"] + 1 == var_bindings["v2"]["grpid"]) and (var_bindings["v2"]["grpid"] + 1 == var_bindings["v3"]["grpid"])

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The angle between the displacement direction computed from v1 and v2 and that computed from v2 and v3."""
    return abs(atan2(sin(degrees(var_bindings["v2"]["direction"] - var_bindings["v1"]["direction"])), cos(degrees(var_bindings["v2"]["direction"] - var_bindings["v1"]["direction"]))) - atan2(sin(degrees(var_bindings["v3"]["direction"] - var_bindings["v2"]["direction"])), cos(degrees(var_bindings["v3"]["direction"] - var_bindings["v2"]["direction"])))) <= _N_THRESHOLD_1

def bfunc_4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The rate of change of that angle, computed based on the time difference, does not exceed a certain reasonable upper bound."""
    return (abs(atan2(sin(degrees(var_bindings["v2"]["direction"] - var_bindings["v1"]["direction"])), cos(degrees(var_bindings["v2"]["direction"] - var_bindings["v1"]["direction"]))) - atan2(sin(degrees(var_bindings["v3"]["direction"] - var_bindings["v2"]["direction"])), cos(degrees(var_bindings["v3"]["direction"] - var_bindings["v2"]["direction"])))) / abs(var_bindings["v3"]["timestamp"] - var_bindings["v1"]["timestamp"])) <= _N_THRESHOLD_2

