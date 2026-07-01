from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The speed value of v1 is non-negative."""
    return var_bindings["v1"]["speed"] >= 0

