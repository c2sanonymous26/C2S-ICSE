from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return (var_bindings['v1']['Nc1RSRP'] is not None and var_bindings['v1']['Nc1RSRP'] > var_bindings['v1']['ScRSRP']) + (var_bindings['v1']['Nc2RSRP'] is not None and var_bindings['v1']['Nc2RSRP'] > var_bindings['v1']['ScRSRP']) + (var_bindings['v1']['Nc3RSRP'] is not None and var_bindings['v1']['Nc3RSRP'] > var_bindings['v1']['ScRSRP']) + (var_bindings['v1']['Nc4RSRP'] is not None and var_bindings['v1']['Nc4RSRP'] > var_bindings['v1']['ScRSRP']) + (var_bindings['v1']['Nc5RSRP'] is not None and var_bindings['v1']['Nc5RSRP'] > var_bindings['v1']['ScRSRP']) + (var_bindings['v1']['Nc6RSRP'] is not None and var_bindings['v1']['Nc6RSRP'] > var_bindings['v1']['ScRSRP']) + (var_bindings['v1']['Nc7RSRP'] is not None and var_bindings['v1']['Nc7RSRP'] > var_bindings['v1']['ScRSRP']) + (var_bindings['v1']['Nc8RSRP'] is not None and var_bindings['v1']['Nc8RSRP'] > var_bindings['v1']['ScRSRP']) <= 8

