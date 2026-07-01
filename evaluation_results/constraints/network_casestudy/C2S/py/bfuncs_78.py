from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Imei'] == var_bindings['v2']['Imei']

def bfunc_1_c10(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_1_c11(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] > 0

def bfunc_1_c12(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_1_c13(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] == 0

def bfunc_1_c14(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['ScRSRP'] is not None

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

def bfunc_1_c7(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['CellID'] is not None

def bfunc_1_c8(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['CellID'] is not None

def bfunc_1_c9(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['CellID'] == var_bindings['v2']['CellID']

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['ScRSRP'] > 85999999/1000000

def bfunc_3_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['ScRSRP'] < 86

