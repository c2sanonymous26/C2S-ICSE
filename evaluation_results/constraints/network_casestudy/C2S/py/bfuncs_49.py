from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Imei'] == var_bindings['v2']['Imei']

def bfunc_1_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Imsi'] == var_bindings['v2']['Imsi']

def bfunc_1_c3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['MmeGroupId'] == var_bindings['v2']['MmeGroupId']

def bfunc_1_c4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['MmeCode'] == var_bindings['v2']['MmeCode']

def bfunc_1_c5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['MmeUeS1apId'] == var_bindings['v2']['MmeUeS1apId']

def bfunc_1_c6(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Imei_Imsi_MmeGroupId_MmeCode_MmeUeS1apId_grpId'] == var_bindings['v1']['Imei_Imsi_MmeGroupId_MmeCode_MmeUeS1apId_grpId'] + 1

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['CellID'] is not None

def bfunc_2_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['CellID'] is not None

def bfunc_2_c3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['CellID'] == var_bindings['v2']['CellID']

def bfunc_3_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Time'] is not None

def bfunc_3_c10(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 6371000 * 2 * asin(sqrt(pow(sin(radians(var_bindings['v2']['Latitude'] - var_bindings['v1']['Latitude']) / 2), 2) + cos(radians(var_bindings['v1']['Latitude'])) * cos(radians(var_bindings['v2']['Latitude'])) * pow(sin(radians(var_bindings['v2']['Longitude'] - var_bindings['v1']['Longitude']) / 2), 2))) / ((var_bindings['v2']['Time'] - var_bindings['v1']['Time']) / 1000.0) * 3.6 < 1807100972507195/2251799813685248

def bfunc_3_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Time'] is not None

def bfunc_3_c3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Longitude'] is not None

def bfunc_3_c4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Latitude'] is not None

def bfunc_3_c5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Longitude'] is not None

def bfunc_3_c6(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Latitude'] is not None

def bfunc_3_c7(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['ScAOA'] is not None

def bfunc_3_c8(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['ScAOA'] is not None

def bfunc_3_c9(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Time'] > var_bindings['v1']['Time']

def bfunc_4_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['ScAOA'] - var_bindings['v2']['ScAOA']) < 1/1000000

