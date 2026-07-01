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
    return var_bindings['v1']['Nc1Cellid'] is not None

def bfunc_3_c10(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is not None

def bfunc_3_c11(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] == var_bindings['v2']['CellID']

def bfunc_3_c12(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] is not None

def bfunc_3_c13(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is not None

def bfunc_3_c14(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] == var_bindings['v2']['CellID']

def bfunc_3_c15(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] is not None

def bfunc_3_c16(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is not None

def bfunc_3_c17(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] == var_bindings['v2']['CellID']

def bfunc_3_c18(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] is not None

def bfunc_3_c19(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is not None

def bfunc_3_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] == var_bindings['v2']['CellID']

def bfunc_3_c20(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] == var_bindings['v2']['CellID']

def bfunc_3_c21(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] is not None

def bfunc_3_c22(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is not None

def bfunc_3_c23(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] == var_bindings['v2']['CellID']

def bfunc_3_c24(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] is not None

def bfunc_3_c3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] is not None

def bfunc_3_c4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is not None

def bfunc_3_c5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] == var_bindings['v2']['CellID']

def bfunc_3_c6(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] is not None

def bfunc_3_c7(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is not None

def bfunc_3_c8(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] == var_bindings['v2']['CellID']

def bfunc_3_c9(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] is not None

def bfunc_4_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] is not None

def bfunc_4_c10(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] >= var_bindings['v1']['Nc4RSRP']

def bfunc_4_c100(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] >= var_bindings['v1']['Nc4RSRP']

def bfunc_4_c101(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] is not None

def bfunc_4_c102(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] >= var_bindings['v1']['Nc5RSRP']

def bfunc_4_c103(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] is not None

def bfunc_4_c104(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] >= var_bindings['v1']['Nc6RSRP']

def bfunc_4_c105(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] is not None

def bfunc_4_c106(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] >= var_bindings['v1']['Nc7RSRP']

def bfunc_4_c107(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] is not None

def bfunc_4_c108(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] >= var_bindings['v1']['Nc8RSRP']

def bfunc_4_c109(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is not None

def bfunc_4_c11(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] is not None

def bfunc_4_c110(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] == var_bindings['v2']['CellID']

def bfunc_4_c111(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] is not None

def bfunc_4_c112(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] >= var_bindings['v1']['Nc1RSRP']

def bfunc_4_c113(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] is not None

def bfunc_4_c114(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] >= var_bindings['v1']['Nc2RSRP']

def bfunc_4_c115(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] is not None

def bfunc_4_c116(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] >= var_bindings['v1']['Nc3RSRP']

def bfunc_4_c117(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] is not None

def bfunc_4_c118(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] >= var_bindings['v1']['Nc4RSRP']

def bfunc_4_c119(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] is not None

def bfunc_4_c12(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] >= var_bindings['v1']['Nc5RSRP']

def bfunc_4_c120(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] >= var_bindings['v1']['Nc5RSRP']

def bfunc_4_c121(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] is not None

def bfunc_4_c122(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] >= var_bindings['v1']['Nc6RSRP']

def bfunc_4_c123(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] is not None

def bfunc_4_c124(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] >= var_bindings['v1']['Nc7RSRP']

def bfunc_4_c125(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] is not None

def bfunc_4_c126(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] >= var_bindings['v1']['Nc8RSRP']

def bfunc_4_c127(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is not None

def bfunc_4_c128(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] == var_bindings['v2']['CellID']

def bfunc_4_c129(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] is not None

def bfunc_4_c13(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] is not None

def bfunc_4_c130(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] >= var_bindings['v1']['Nc1RSRP']

def bfunc_4_c131(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] is not None

def bfunc_4_c132(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] >= var_bindings['v1']['Nc2RSRP']

def bfunc_4_c133(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] is not None

def bfunc_4_c134(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] >= var_bindings['v1']['Nc3RSRP']

def bfunc_4_c135(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] is not None

def bfunc_4_c136(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] >= var_bindings['v1']['Nc4RSRP']

def bfunc_4_c137(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] is not None

def bfunc_4_c138(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] >= var_bindings['v1']['Nc5RSRP']

def bfunc_4_c139(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] is not None

def bfunc_4_c14(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] >= var_bindings['v1']['Nc6RSRP']

def bfunc_4_c140(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] >= var_bindings['v1']['Nc6RSRP']

def bfunc_4_c141(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] is not None

def bfunc_4_c142(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] >= var_bindings['v1']['Nc7RSRP']

def bfunc_4_c143(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] is not None

def bfunc_4_c144(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] >= var_bindings['v1']['Nc8RSRP']

def bfunc_4_c15(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] is not None

def bfunc_4_c16(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] >= var_bindings['v1']['Nc7RSRP']

def bfunc_4_c17(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] is not None

def bfunc_4_c18(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] >= var_bindings['v1']['Nc8RSRP']

def bfunc_4_c19(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is not None

def bfunc_4_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] == var_bindings['v2']['CellID']

def bfunc_4_c20(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] == var_bindings['v2']['CellID']

def bfunc_4_c21(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] is not None

def bfunc_4_c22(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] >= var_bindings['v1']['Nc1RSRP']

def bfunc_4_c23(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] is not None

def bfunc_4_c24(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] >= var_bindings['v1']['Nc2RSRP']

def bfunc_4_c25(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] is not None

def bfunc_4_c26(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] >= var_bindings['v1']['Nc3RSRP']

def bfunc_4_c27(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] is not None

def bfunc_4_c28(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] >= var_bindings['v1']['Nc4RSRP']

def bfunc_4_c29(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] is not None

def bfunc_4_c3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] is not None

def bfunc_4_c30(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] >= var_bindings['v1']['Nc5RSRP']

def bfunc_4_c31(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] is not None

def bfunc_4_c32(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] >= var_bindings['v1']['Nc6RSRP']

def bfunc_4_c33(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] is not None

def bfunc_4_c34(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] >= var_bindings['v1']['Nc7RSRP']

def bfunc_4_c35(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] is not None

def bfunc_4_c36(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] >= var_bindings['v1']['Nc8RSRP']

def bfunc_4_c37(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is not None

def bfunc_4_c38(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] == var_bindings['v2']['CellID']

def bfunc_4_c39(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] is not None

def bfunc_4_c4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] >= var_bindings['v1']['Nc1RSRP']

def bfunc_4_c40(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] >= var_bindings['v1']['Nc1RSRP']

def bfunc_4_c41(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] is not None

def bfunc_4_c42(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] >= var_bindings['v1']['Nc2RSRP']

def bfunc_4_c43(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] is not None

def bfunc_4_c44(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] >= var_bindings['v1']['Nc3RSRP']

def bfunc_4_c45(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] is not None

def bfunc_4_c46(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] >= var_bindings['v1']['Nc4RSRP']

def bfunc_4_c47(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] is not None

def bfunc_4_c48(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] >= var_bindings['v1']['Nc5RSRP']

def bfunc_4_c49(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] is not None

def bfunc_4_c5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] is not None

def bfunc_4_c50(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] >= var_bindings['v1']['Nc6RSRP']

def bfunc_4_c51(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] is not None

def bfunc_4_c52(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] >= var_bindings['v1']['Nc7RSRP']

def bfunc_4_c53(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] is not None

def bfunc_4_c54(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] >= var_bindings['v1']['Nc8RSRP']

def bfunc_4_c55(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is not None

def bfunc_4_c56(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] == var_bindings['v2']['CellID']

def bfunc_4_c57(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] is not None

def bfunc_4_c58(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] >= var_bindings['v1']['Nc1RSRP']

def bfunc_4_c59(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] is not None

def bfunc_4_c6(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] >= var_bindings['v1']['Nc2RSRP']

def bfunc_4_c60(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] >= var_bindings['v1']['Nc2RSRP']

def bfunc_4_c61(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] is not None

def bfunc_4_c62(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] >= var_bindings['v1']['Nc3RSRP']

def bfunc_4_c63(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] is not None

def bfunc_4_c64(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] >= var_bindings['v1']['Nc4RSRP']

def bfunc_4_c65(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] is not None

def bfunc_4_c66(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] >= var_bindings['v1']['Nc5RSRP']

def bfunc_4_c67(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] is not None

def bfunc_4_c68(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] >= var_bindings['v1']['Nc6RSRP']

def bfunc_4_c69(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] is not None

def bfunc_4_c7(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] is not None

def bfunc_4_c70(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] >= var_bindings['v1']['Nc7RSRP']

def bfunc_4_c71(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] is not None

def bfunc_4_c72(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] >= var_bindings['v1']['Nc8RSRP']

def bfunc_4_c73(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is not None

def bfunc_4_c74(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] == var_bindings['v2']['CellID']

def bfunc_4_c75(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] is not None

def bfunc_4_c76(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] >= var_bindings['v1']['Nc1RSRP']

def bfunc_4_c77(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] is not None

def bfunc_4_c78(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] >= var_bindings['v1']['Nc2RSRP']

def bfunc_4_c79(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] is not None

def bfunc_4_c8(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] >= var_bindings['v1']['Nc3RSRP']

def bfunc_4_c80(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] >= var_bindings['v1']['Nc3RSRP']

def bfunc_4_c81(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] is not None

def bfunc_4_c82(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] >= var_bindings['v1']['Nc4RSRP']

def bfunc_4_c83(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] is not None

def bfunc_4_c84(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] >= var_bindings['v1']['Nc5RSRP']

def bfunc_4_c85(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] is not None

def bfunc_4_c86(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] >= var_bindings['v1']['Nc6RSRP']

def bfunc_4_c87(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] is not None

def bfunc_4_c88(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] >= var_bindings['v1']['Nc7RSRP']

def bfunc_4_c89(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] is not None

def bfunc_4_c9(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] is not None

def bfunc_4_c90(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] >= var_bindings['v1']['Nc8RSRP']

def bfunc_4_c91(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is not None

def bfunc_4_c92(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] == var_bindings['v2']['CellID']

def bfunc_4_c93(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] is not None

def bfunc_4_c94(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] >= var_bindings['v1']['Nc1RSRP']

def bfunc_4_c95(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] is not None

def bfunc_4_c96(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] >= var_bindings['v1']['Nc2RSRP']

def bfunc_4_c97(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] is not None

def bfunc_4_c98(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] >= var_bindings['v1']['Nc3RSRP']

def bfunc_4_c99(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] is not None

