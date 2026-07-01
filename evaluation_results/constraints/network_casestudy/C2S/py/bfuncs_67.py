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
    return var_bindings['v1']['Tac'] is not None

def bfunc_2_c4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Tac'] is not None

def bfunc_2_c5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['CellID'] != var_bindings['v2']['CellID']

def bfunc_2_c6(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Tac'] != var_bindings['v2']['Tac']

def bfunc_3_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] is not None

def bfunc_3_c10(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] == var_bindings['v2']['CellID']

def bfunc_3_c11(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3TAC'] is not None

def bfunc_3_c12(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3TAC'] == var_bindings['v2']['Tac']

def bfunc_3_c13(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is not None

def bfunc_3_c14(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] == var_bindings['v2']['CellID']

def bfunc_3_c15(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4TAC'] is not None

def bfunc_3_c16(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4TAC'] == var_bindings['v2']['Tac']

def bfunc_3_c17(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is not None

def bfunc_3_c18(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] == var_bindings['v2']['CellID']

def bfunc_3_c19(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5TAC'] is not None

def bfunc_3_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] == var_bindings['v2']['CellID']

def bfunc_3_c20(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5TAC'] == var_bindings['v2']['Tac']

def bfunc_3_c21(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is not None

def bfunc_3_c22(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] == var_bindings['v2']['CellID']

def bfunc_3_c23(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6TAC'] is not None

def bfunc_3_c24(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6TAC'] == var_bindings['v2']['Tac']

def bfunc_3_c25(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is not None

def bfunc_3_c26(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] == var_bindings['v2']['CellID']

def bfunc_3_c27(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7TAC'] is not None

def bfunc_3_c28(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7TAC'] == var_bindings['v2']['Tac']

def bfunc_3_c29(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is not None

def bfunc_3_c3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1TAC'] is not None

def bfunc_3_c30(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] == var_bindings['v2']['CellID']

def bfunc_3_c31(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8TAC'] is not None

def bfunc_3_c32(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8TAC'] == var_bindings['v2']['Tac']

def bfunc_3_c4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1TAC'] == var_bindings['v2']['Tac']

def bfunc_3_c5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is not None

def bfunc_3_c6(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] == var_bindings['v2']['CellID']

def bfunc_3_c7(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2TAC'] is not None

def bfunc_3_c8(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2TAC'] == var_bindings['v2']['Tac']

def bfunc_3_c9(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is not None

