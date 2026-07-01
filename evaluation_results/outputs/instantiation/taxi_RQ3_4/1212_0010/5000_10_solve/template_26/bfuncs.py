from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['carid'] != var_bindings['v2']['carid']

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['timestamp'] - var_bindings['v2']['timestamp']) <= 60

def bfunc_3_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return pow(abs(var_bindings['v1']['latitude'] - var_bindings['v2']['latitude']), 2) + pow(abs(var_bindings['v1']['longitude'] - var_bindings['v2']['longitude']), 2) <= 7233337286182989/73786976294838206464

def bfunc_4_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(atan2(sin(var_bindings['v1']['direction'] - var_bindings['v2']['direction']), cos(var_bindings['v1']['direction'] - var_bindings['v2']['direction']))) <= 3437494630899519/1125899906842624

