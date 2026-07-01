from math import *
from typing import Any

def bfunc_1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    """The grpid value of v1 is greater than or equal to 1."""
    return var_bindings["v1"]["grpid"] >= 1

