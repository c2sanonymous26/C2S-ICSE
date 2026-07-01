from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['ScRSRP'] is not None

def bfunc_1_c10(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] > var_bindings['v1']['ScRSRP'] + 39

def bfunc_1_c11(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] is not None

def bfunc_1_c12(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] > var_bindings['v1']['ScRSRP'] + 39

def bfunc_1_c13(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] is not None

def bfunc_1_c14(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] > var_bindings['v1']['ScRSRP'] + 39

def bfunc_1_c15(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] is not None

def bfunc_1_c16(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] > var_bindings['v1']['ScRSRP'] + 39

def bfunc_1_c17(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] is not None

def bfunc_1_c18(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] > var_bindings['v1']['ScRSRP'] + 39

def bfunc_1_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['ScRSRQ'] is not None

def bfunc_1_c3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] is not None

def bfunc_1_c4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] > var_bindings['v1']['ScRSRP'] + 39

def bfunc_1_c5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] is not None

def bfunc_1_c6(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] > var_bindings['v1']['ScRSRP'] + 39

def bfunc_1_c7(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] is not None

def bfunc_1_c8(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] > var_bindings['v1']['ScRSRP'] + 39

def bfunc_1_c9(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] is not None

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['ScRSRQ'] < 33

