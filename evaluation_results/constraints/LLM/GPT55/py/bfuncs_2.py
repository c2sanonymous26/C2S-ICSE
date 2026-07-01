from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The speed recorded in context v1 is nonnegative and does not exceed a certain reasonable upper bound."""
    return (var_bindings["v1"]["speed"] >= 0) and (var_bindings["v1"]["speed"] <= 80.0)
