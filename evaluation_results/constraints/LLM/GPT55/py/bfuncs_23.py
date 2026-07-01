from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The GPS location recorded in context v1, determined by its latitude and longitude, lies within the expected SmartCity taxi service area."""
    return (var_bindings["v1"]["latitude"] >= 22.505028) and ((var_bindings["v1"]["latitude"] <= 22.76425) and ((var_bindings["v1"]["longitude"] >= 113.79545) and (var_bindings["v1"]["longitude"] <= 114.33787)))

