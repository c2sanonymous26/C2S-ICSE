from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1 and v2 belong to the same vehicle and are consecutive contexts."""
    return (var_bindings["v1"]["carid"] == var_bindings["v2"]["carid"]) and (abs(var_bindings["v1"]["grpid"] - var_bindings["v2"]["grpid"]) == 1)

def bfunc_2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The travel directions of v1 and v2 lie in the same quadrant."""
    return (((var_bindings["v1"]["direction"] >= 0) and ((var_bindings["v1"]["direction"] < 90) and ((var_bindings["v2"]["direction"] >= 0) and (var_bindings["v2"]["direction"] < 90))))) or ((((var_bindings["v1"]["direction"] >= 90) and ((var_bindings["v1"]["direction"] < 180) and ((var_bindings["v2"]["direction"] >= 90) and (var_bindings["v2"]["direction"] < 180))))) or ((((var_bindings["v1"]["direction"] >= 180) and ((var_bindings["v1"]["direction"] < 270) and ((var_bindings["v2"]["direction"] >= 180) and (var_bindings["v2"]["direction"] < 270))))) or (((var_bindings["v1"]["direction"] >= 270) and ((var_bindings["v1"]["direction"] < 360) and ((var_bindings["v2"]["direction"] >= 270) and (var_bindings["v2"]["direction"] < 360)))))))

def bfunc_3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The longitude difference and latitude difference between v1 and v2 have the same sign."""
    return (((var_bindings["v1"]["longitude"] - var_bindings["v2"]["longitude"] > 0) and (var_bindings["v1"]["latitude"] - var_bindings["v2"]["latitude"] > 0))) or (((var_bindings["v1"]["longitude"] - var_bindings["v2"]["longitude"] < 0) and (var_bindings["v1"]["latitude"] - var_bindings["v2"]["latitude"] < 0)))

