from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Longitude'] is not None

def bfunc_1_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Latitude'] is not None

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Longitude'] >= 261806250806999/2199023255552

def bfunc_3_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Longitude'] <= 8425378937406021/70368744177664

def bfunc_4_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Latitude'] >= 1134680553925485/35184372088832

def bfunc_5_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Latitude'] <= 4683196565848079/140737488355328

