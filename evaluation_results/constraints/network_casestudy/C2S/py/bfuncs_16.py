from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] == (var_bindings['v1']['Nc1Cellid'] is not None) + (var_bindings['v1']['Nc2Cellid'] is not None) + (var_bindings['v1']['Nc3Cellid'] is not None) + (var_bindings['v1']['Nc4Cellid'] is not None) + (var_bindings['v1']['Nc5Cellid'] is not None) + (var_bindings['v1']['Nc6Cellid'] is not None) + (var_bindings['v1']['Nc7Cellid'] is not None) + (var_bindings['v1']['Nc8Cellid'] is not None)

