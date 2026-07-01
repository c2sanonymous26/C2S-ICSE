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
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_3_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] >= 1

def bfunc_3_c10(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is None

def bfunc_3_c100(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRP'] < 93000001/1000000

def bfunc_3_c101(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] >= 6

def bfunc_3_c102(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6Cellid'] is not None

def bfunc_3_c103(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRP'] is not None

def bfunc_3_c104(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] is None

def bfunc_3_c105(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] != var_bindings['v2']['Nc6Cellid']

def bfunc_3_c106(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is None

def bfunc_3_c107(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] != var_bindings['v2']['Nc6Cellid']

def bfunc_3_c108(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is None

def bfunc_3_c109(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] != var_bindings['v2']['Nc6Cellid']

def bfunc_3_c11(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] != var_bindings['v2']['Nc1Cellid']

def bfunc_3_c110(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is None

def bfunc_3_c111(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] != var_bindings['v2']['Nc6Cellid']

def bfunc_3_c112(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is None

def bfunc_3_c113(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] != var_bindings['v2']['Nc6Cellid']

def bfunc_3_c114(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is None

def bfunc_3_c115(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] != var_bindings['v2']['Nc6Cellid']

def bfunc_3_c116(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is None

def bfunc_3_c117(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] != var_bindings['v2']['Nc6Cellid']

def bfunc_3_c118(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is None

def bfunc_3_c119(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] != var_bindings['v2']['Nc6Cellid']

def bfunc_3_c12(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is None

def bfunc_3_c120(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRP'] < 93000001/1000000

def bfunc_3_c121(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] >= 7

def bfunc_3_c122(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7Cellid'] is not None

def bfunc_3_c123(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRP'] is not None

def bfunc_3_c124(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] is None

def bfunc_3_c125(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] != var_bindings['v2']['Nc7Cellid']

def bfunc_3_c126(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is None

def bfunc_3_c127(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] != var_bindings['v2']['Nc7Cellid']

def bfunc_3_c128(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is None

def bfunc_3_c129(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] != var_bindings['v2']['Nc7Cellid']

def bfunc_3_c13(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] != var_bindings['v2']['Nc1Cellid']

def bfunc_3_c130(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is None

def bfunc_3_c131(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] != var_bindings['v2']['Nc7Cellid']

def bfunc_3_c132(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is None

def bfunc_3_c133(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] != var_bindings['v2']['Nc7Cellid']

def bfunc_3_c134(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is None

def bfunc_3_c135(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] != var_bindings['v2']['Nc7Cellid']

def bfunc_3_c136(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is None

def bfunc_3_c137(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] != var_bindings['v2']['Nc7Cellid']

def bfunc_3_c138(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is None

def bfunc_3_c139(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] != var_bindings['v2']['Nc7Cellid']

def bfunc_3_c14(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is None

def bfunc_3_c140(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRP'] < 93000001/1000000

def bfunc_3_c141(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] >= 8

def bfunc_3_c142(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8Cellid'] is not None

def bfunc_3_c143(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRP'] is not None

def bfunc_3_c144(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] is None

def bfunc_3_c145(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] != var_bindings['v2']['Nc8Cellid']

def bfunc_3_c146(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is None

def bfunc_3_c147(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] != var_bindings['v2']['Nc8Cellid']

def bfunc_3_c148(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is None

def bfunc_3_c149(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] != var_bindings['v2']['Nc8Cellid']

def bfunc_3_c15(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] != var_bindings['v2']['Nc1Cellid']

def bfunc_3_c150(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is None

def bfunc_3_c151(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] != var_bindings['v2']['Nc8Cellid']

def bfunc_3_c152(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is None

def bfunc_3_c153(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] != var_bindings['v2']['Nc8Cellid']

def bfunc_3_c154(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is None

def bfunc_3_c155(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] != var_bindings['v2']['Nc8Cellid']

def bfunc_3_c156(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is None

def bfunc_3_c157(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] != var_bindings['v2']['Nc8Cellid']

def bfunc_3_c158(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is None

def bfunc_3_c159(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] != var_bindings['v2']['Nc8Cellid']

def bfunc_3_c16(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is None

def bfunc_3_c160(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRP'] < 93000001/1000000

def bfunc_3_c17(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] != var_bindings['v2']['Nc1Cellid']

def bfunc_3_c18(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is None

def bfunc_3_c19(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] != var_bindings['v2']['Nc1Cellid']

def bfunc_3_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1Cellid'] is not None

def bfunc_3_c20(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRP'] < 93000001/1000000

def bfunc_3_c21(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] >= 2

def bfunc_3_c22(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2Cellid'] is not None

def bfunc_3_c23(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRP'] is not None

def bfunc_3_c24(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] is None

def bfunc_3_c25(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] != var_bindings['v2']['Nc2Cellid']

def bfunc_3_c26(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is None

def bfunc_3_c27(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] != var_bindings['v2']['Nc2Cellid']

def bfunc_3_c28(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is None

def bfunc_3_c29(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] != var_bindings['v2']['Nc2Cellid']

def bfunc_3_c3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRP'] is not None

def bfunc_3_c30(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is None

def bfunc_3_c31(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] != var_bindings['v2']['Nc2Cellid']

def bfunc_3_c32(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is None

def bfunc_3_c33(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] != var_bindings['v2']['Nc2Cellid']

def bfunc_3_c34(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is None

def bfunc_3_c35(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] != var_bindings['v2']['Nc2Cellid']

def bfunc_3_c36(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is None

def bfunc_3_c37(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] != var_bindings['v2']['Nc2Cellid']

def bfunc_3_c38(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is None

def bfunc_3_c39(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] != var_bindings['v2']['Nc2Cellid']

def bfunc_3_c4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] is None

def bfunc_3_c40(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRP'] < 93000001/1000000

def bfunc_3_c41(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] >= 3

def bfunc_3_c42(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3Cellid'] is not None

def bfunc_3_c43(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRP'] is not None

def bfunc_3_c44(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] is None

def bfunc_3_c45(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] != var_bindings['v2']['Nc3Cellid']

def bfunc_3_c46(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is None

def bfunc_3_c47(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] != var_bindings['v2']['Nc3Cellid']

def bfunc_3_c48(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is None

def bfunc_3_c49(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] != var_bindings['v2']['Nc3Cellid']

def bfunc_3_c5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] != var_bindings['v2']['Nc1Cellid']

def bfunc_3_c50(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is None

def bfunc_3_c51(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] != var_bindings['v2']['Nc3Cellid']

def bfunc_3_c52(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is None

def bfunc_3_c53(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] != var_bindings['v2']['Nc3Cellid']

def bfunc_3_c54(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is None

def bfunc_3_c55(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] != var_bindings['v2']['Nc3Cellid']

def bfunc_3_c56(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is None

def bfunc_3_c57(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] != var_bindings['v2']['Nc3Cellid']

def bfunc_3_c58(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is None

def bfunc_3_c59(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] != var_bindings['v2']['Nc3Cellid']

def bfunc_3_c6(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is None

def bfunc_3_c60(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRP'] < 93000001/1000000

def bfunc_3_c61(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] >= 4

def bfunc_3_c62(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4Cellid'] is not None

def bfunc_3_c63(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRP'] is not None

def bfunc_3_c64(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] is None

def bfunc_3_c65(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] != var_bindings['v2']['Nc4Cellid']

def bfunc_3_c66(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is None

def bfunc_3_c67(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] != var_bindings['v2']['Nc4Cellid']

def bfunc_3_c68(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is None

def bfunc_3_c69(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] != var_bindings['v2']['Nc4Cellid']

def bfunc_3_c7(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] != var_bindings['v2']['Nc1Cellid']

def bfunc_3_c70(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is None

def bfunc_3_c71(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] != var_bindings['v2']['Nc4Cellid']

def bfunc_3_c72(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is None

def bfunc_3_c73(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] != var_bindings['v2']['Nc4Cellid']

def bfunc_3_c74(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is None

def bfunc_3_c75(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] != var_bindings['v2']['Nc4Cellid']

def bfunc_3_c76(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is None

def bfunc_3_c77(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] != var_bindings['v2']['Nc4Cellid']

def bfunc_3_c78(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is None

def bfunc_3_c79(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] != var_bindings['v2']['Nc4Cellid']

def bfunc_3_c8(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is None

def bfunc_3_c80(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRP'] < 93000001/1000000

def bfunc_3_c81(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] >= 5

def bfunc_3_c82(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5Cellid'] is not None

def bfunc_3_c83(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRP'] is not None

def bfunc_3_c84(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] is None

def bfunc_3_c85(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] != var_bindings['v2']['Nc5Cellid']

def bfunc_3_c86(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is None

def bfunc_3_c87(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] != var_bindings['v2']['Nc5Cellid']

def bfunc_3_c88(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is None

def bfunc_3_c89(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] != var_bindings['v2']['Nc5Cellid']

def bfunc_3_c9(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] != var_bindings['v2']['Nc1Cellid']

def bfunc_3_c90(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is None

def bfunc_3_c91(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] != var_bindings['v2']['Nc5Cellid']

def bfunc_3_c92(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is None

def bfunc_3_c93(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] != var_bindings['v2']['Nc5Cellid']

def bfunc_3_c94(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is None

def bfunc_3_c95(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] != var_bindings['v2']['Nc5Cellid']

def bfunc_3_c96(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is None

def bfunc_3_c97(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] != var_bindings['v2']['Nc5Cellid']

def bfunc_3_c98(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is None

def bfunc_3_c99(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] != var_bindings['v2']['Nc5Cellid']

