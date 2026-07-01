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
    return var_bindings['v1']['CellID'] != var_bindings['v2']['CellID']

def bfunc_3_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['ScRSRP'] is not None

def bfunc_4_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['ScRSRP'] < 85000001/1000000

