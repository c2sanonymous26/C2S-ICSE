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
    return var_bindings['v2']['ScPci'] is not None

def bfunc_3_c10(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Earfcn'] is not None

def bfunc_3_c11(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is not None

def bfunc_3_c12(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] == var_bindings['v2']['CellID']

def bfunc_3_c13(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Pci'] is not None

def bfunc_3_c14(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Earfcn'] is not None

def bfunc_3_c15(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is not None

def bfunc_3_c16(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] == var_bindings['v2']['CellID']

def bfunc_3_c17(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Pci'] is not None

def bfunc_3_c18(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Earfcn'] is not None

def bfunc_3_c19(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is not None

def bfunc_3_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['ScEarfcn'] is not None

def bfunc_3_c20(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] == var_bindings['v2']['CellID']

def bfunc_3_c21(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Pci'] is not None

def bfunc_3_c22(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Earfcn'] is not None

def bfunc_3_c23(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is not None

def bfunc_3_c24(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] == var_bindings['v2']['CellID']

def bfunc_3_c25(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Pci'] is not None

def bfunc_3_c26(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Earfcn'] is not None

def bfunc_3_c27(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is not None

def bfunc_3_c28(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] == var_bindings['v2']['CellID']

def bfunc_3_c29(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Pci'] is not None

def bfunc_3_c3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] is not None

def bfunc_3_c30(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Earfcn'] is not None

def bfunc_3_c31(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is not None

def bfunc_3_c32(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] == var_bindings['v2']['CellID']

def bfunc_3_c33(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Pci'] is not None

def bfunc_3_c34(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Earfcn'] is not None

def bfunc_3_c4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] == var_bindings['v2']['CellID']

def bfunc_3_c5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Pci'] is not None

def bfunc_3_c6(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Earfcn'] is not None

def bfunc_3_c7(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is not None

def bfunc_3_c8(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] == var_bindings['v2']['CellID']

def bfunc_3_c9(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Pci'] is not None

def bfunc_4_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] is not None

def bfunc_4_c10(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] == var_bindings['v2']['CellID']

def bfunc_4_c11(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['ScPci'] == var_bindings['v1']['Nc3Pci']

def bfunc_4_c12(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['ScEarfcn'] == var_bindings['v1']['Nc3Earfcn']

def bfunc_4_c13(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is not None

def bfunc_4_c14(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] == var_bindings['v2']['CellID']

def bfunc_4_c15(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['ScPci'] == var_bindings['v1']['Nc4Pci']

def bfunc_4_c16(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['ScEarfcn'] == var_bindings['v1']['Nc4Earfcn']

def bfunc_4_c17(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is not None

def bfunc_4_c18(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] == var_bindings['v2']['CellID']

def bfunc_4_c19(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['ScPci'] == var_bindings['v1']['Nc5Pci']

def bfunc_4_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] == var_bindings['v2']['CellID']

def bfunc_4_c20(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['ScEarfcn'] == var_bindings['v1']['Nc5Earfcn']

def bfunc_4_c21(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is not None

def bfunc_4_c22(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] == var_bindings['v2']['CellID']

def bfunc_4_c23(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['ScPci'] == var_bindings['v1']['Nc6Pci']

def bfunc_4_c24(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['ScEarfcn'] == var_bindings['v1']['Nc6Earfcn']

def bfunc_4_c25(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is not None

def bfunc_4_c26(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] == var_bindings['v2']['CellID']

def bfunc_4_c27(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['ScPci'] == var_bindings['v1']['Nc7Pci']

def bfunc_4_c28(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['ScEarfcn'] == var_bindings['v1']['Nc7Earfcn']

def bfunc_4_c29(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is not None

def bfunc_4_c3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['ScPci'] == var_bindings['v1']['Nc1Pci']

def bfunc_4_c30(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] == var_bindings['v2']['CellID']

def bfunc_4_c31(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['ScPci'] == var_bindings['v1']['Nc8Pci']

def bfunc_4_c32(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['ScEarfcn'] == var_bindings['v1']['Nc8Earfcn']

def bfunc_4_c4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['ScEarfcn'] == var_bindings['v1']['Nc1Earfcn']

def bfunc_4_c5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is not None

def bfunc_4_c6(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] == var_bindings['v2']['CellID']

def bfunc_4_c7(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['ScPci'] == var_bindings['v1']['Nc2Pci']

def bfunc_4_c8(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['ScEarfcn'] == var_bindings['v1']['Nc2Earfcn']

def bfunc_4_c9(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is not None

