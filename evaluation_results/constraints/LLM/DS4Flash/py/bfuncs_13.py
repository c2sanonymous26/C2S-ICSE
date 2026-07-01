from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """v1's GPS location (latitude and longitude) is within the city boundary"""
    return (var_bindings["v1"]["latitude"] >= 22.542) and ((var_bindings["v1"]["latitude"] <= 22.764) and ((var_bindings["v1"]["longitude"] >= 113.814) and (var_bindings["v1"]["longitude"] <= 114.34)))

