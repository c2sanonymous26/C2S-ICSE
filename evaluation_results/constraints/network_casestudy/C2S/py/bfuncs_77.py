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

def bfunc_2_c10(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['ScRSRP'] is not None

def bfunc_2_c11(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['ScRSRP'] is not None

def bfunc_2_c12(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['ScRSRQ'] is not None

def bfunc_2_c13(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['ScRSRQ'] is not None

def bfunc_2_c14(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Time'] > var_bindings['v1']['Time']

def bfunc_2_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['CellID'] is not None

def bfunc_2_c3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['CellID'] == var_bindings['v2']['CellID']

def bfunc_2_c4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Time'] is not None

def bfunc_2_c5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Time'] is not None

def bfunc_2_c6(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Longitude'] is not None

def bfunc_2_c7(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Longitude'] is not None

def bfunc_2_c8(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Latitude'] is not None

def bfunc_2_c9(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Latitude'] is not None

def bfunc_3_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 6371000 * 2 * asin(sqrt(pow(sin(radians(var_bindings['v2']['Latitude'] - var_bindings['v1']['Latitude']) / 2), 2) + cos(radians(var_bindings['v1']['Latitude'])) * cos(radians(var_bindings['v2']['Latitude'])) * pow(sin(radians(var_bindings['v2']['Longitude'] - var_bindings['v1']['Longitude']) / 2), 2))) / ((var_bindings['v2']['Time'] - var_bindings['v1']['Time']) / 1000.0) * 3.6 < 1610388221865281/562949953421312

def bfunc_4_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['ScRSRP'] - var_bindings['v2']['ScRSRP']) < 29000001/1000000

def bfunc_5_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['ScRSRQ'] - var_bindings['v2']['ScRSRQ'] > 3

def bfunc_6_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1Cellid'] is not None

def bfunc_6_c10(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is not None

def bfunc_6_c100(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] == var_bindings['v2']['Nc6Cellid']

def bfunc_6_c101(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is not None

def bfunc_6_c102(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] == var_bindings['v2']['Nc6Cellid']

def bfunc_6_c103(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7Cellid'] is not None

def bfunc_6_c104(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] is not None

def bfunc_6_c105(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] == var_bindings['v2']['Nc7Cellid']

def bfunc_6_c106(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is not None

def bfunc_6_c107(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] == var_bindings['v2']['Nc7Cellid']

def bfunc_6_c108(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is not None

def bfunc_6_c109(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] == var_bindings['v2']['Nc7Cellid']

def bfunc_6_c11(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] == var_bindings['v2']['Nc1Cellid']

def bfunc_6_c110(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is not None

def bfunc_6_c111(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] == var_bindings['v2']['Nc7Cellid']

def bfunc_6_c112(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is not None

def bfunc_6_c113(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] == var_bindings['v2']['Nc7Cellid']

def bfunc_6_c114(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is not None

def bfunc_6_c115(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] == var_bindings['v2']['Nc7Cellid']

def bfunc_6_c116(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is not None

def bfunc_6_c117(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] == var_bindings['v2']['Nc7Cellid']

def bfunc_6_c118(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is not None

def bfunc_6_c119(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] == var_bindings['v2']['Nc7Cellid']

def bfunc_6_c12(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is not None

def bfunc_6_c120(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8Cellid'] is not None

def bfunc_6_c121(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] is not None

def bfunc_6_c122(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] == var_bindings['v2']['Nc8Cellid']

def bfunc_6_c123(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is not None

def bfunc_6_c124(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] == var_bindings['v2']['Nc8Cellid']

def bfunc_6_c125(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is not None

def bfunc_6_c126(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] == var_bindings['v2']['Nc8Cellid']

def bfunc_6_c127(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is not None

def bfunc_6_c128(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] == var_bindings['v2']['Nc8Cellid']

def bfunc_6_c129(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is not None

def bfunc_6_c13(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] == var_bindings['v2']['Nc1Cellid']

def bfunc_6_c130(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] == var_bindings['v2']['Nc8Cellid']

def bfunc_6_c131(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is not None

def bfunc_6_c132(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] == var_bindings['v2']['Nc8Cellid']

def bfunc_6_c133(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is not None

def bfunc_6_c134(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] == var_bindings['v2']['Nc8Cellid']

def bfunc_6_c135(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is not None

def bfunc_6_c136(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] == var_bindings['v2']['Nc8Cellid']

def bfunc_6_c14(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is not None

def bfunc_6_c15(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] == var_bindings['v2']['Nc1Cellid']

def bfunc_6_c16(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is not None

def bfunc_6_c17(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] == var_bindings['v2']['Nc1Cellid']

def bfunc_6_c18(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2Cellid'] is not None

def bfunc_6_c19(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] is not None

def bfunc_6_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] is not None

def bfunc_6_c20(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] == var_bindings['v2']['Nc2Cellid']

def bfunc_6_c21(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is not None

def bfunc_6_c22(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] == var_bindings['v2']['Nc2Cellid']

def bfunc_6_c23(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is not None

def bfunc_6_c24(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] == var_bindings['v2']['Nc2Cellid']

def bfunc_6_c25(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is not None

def bfunc_6_c26(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] == var_bindings['v2']['Nc2Cellid']

def bfunc_6_c27(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is not None

def bfunc_6_c28(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] == var_bindings['v2']['Nc2Cellid']

def bfunc_6_c29(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is not None

def bfunc_6_c3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] == var_bindings['v2']['Nc1Cellid']

def bfunc_6_c30(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] == var_bindings['v2']['Nc2Cellid']

def bfunc_6_c31(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is not None

def bfunc_6_c32(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] == var_bindings['v2']['Nc2Cellid']

def bfunc_6_c33(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is not None

def bfunc_6_c34(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] == var_bindings['v2']['Nc2Cellid']

def bfunc_6_c35(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3Cellid'] is not None

def bfunc_6_c36(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] is not None

def bfunc_6_c37(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] == var_bindings['v2']['Nc3Cellid']

def bfunc_6_c38(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is not None

def bfunc_6_c39(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] == var_bindings['v2']['Nc3Cellid']

def bfunc_6_c4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is not None

def bfunc_6_c40(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is not None

def bfunc_6_c41(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] == var_bindings['v2']['Nc3Cellid']

def bfunc_6_c42(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is not None

def bfunc_6_c43(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] == var_bindings['v2']['Nc3Cellid']

def bfunc_6_c44(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is not None

def bfunc_6_c45(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] == var_bindings['v2']['Nc3Cellid']

def bfunc_6_c46(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is not None

def bfunc_6_c47(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] == var_bindings['v2']['Nc3Cellid']

def bfunc_6_c48(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is not None

def bfunc_6_c49(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] == var_bindings['v2']['Nc3Cellid']

def bfunc_6_c5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] == var_bindings['v2']['Nc1Cellid']

def bfunc_6_c50(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is not None

def bfunc_6_c51(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] == var_bindings['v2']['Nc3Cellid']

def bfunc_6_c52(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4Cellid'] is not None

def bfunc_6_c53(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] is not None

def bfunc_6_c54(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] == var_bindings['v2']['Nc4Cellid']

def bfunc_6_c55(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is not None

def bfunc_6_c56(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] == var_bindings['v2']['Nc4Cellid']

def bfunc_6_c57(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is not None

def bfunc_6_c58(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] == var_bindings['v2']['Nc4Cellid']

def bfunc_6_c59(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is not None

def bfunc_6_c6(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is not None

def bfunc_6_c60(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] == var_bindings['v2']['Nc4Cellid']

def bfunc_6_c61(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is not None

def bfunc_6_c62(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] == var_bindings['v2']['Nc4Cellid']

def bfunc_6_c63(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is not None

def bfunc_6_c64(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] == var_bindings['v2']['Nc4Cellid']

def bfunc_6_c65(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is not None

def bfunc_6_c66(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] == var_bindings['v2']['Nc4Cellid']

def bfunc_6_c67(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is not None

def bfunc_6_c68(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] == var_bindings['v2']['Nc4Cellid']

def bfunc_6_c69(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5Cellid'] is not None

def bfunc_6_c7(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] == var_bindings['v2']['Nc1Cellid']

def bfunc_6_c70(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] is not None

def bfunc_6_c71(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] == var_bindings['v2']['Nc5Cellid']

def bfunc_6_c72(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is not None

def bfunc_6_c73(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] == var_bindings['v2']['Nc5Cellid']

def bfunc_6_c74(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is not None

def bfunc_6_c75(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] == var_bindings['v2']['Nc5Cellid']

def bfunc_6_c76(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is not None

def bfunc_6_c77(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] == var_bindings['v2']['Nc5Cellid']

def bfunc_6_c78(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is not None

def bfunc_6_c79(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] == var_bindings['v2']['Nc5Cellid']

def bfunc_6_c8(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is not None

def bfunc_6_c80(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is not None

def bfunc_6_c81(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] == var_bindings['v2']['Nc5Cellid']

def bfunc_6_c82(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is not None

def bfunc_6_c83(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] == var_bindings['v2']['Nc5Cellid']

def bfunc_6_c84(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is not None

def bfunc_6_c85(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] == var_bindings['v2']['Nc5Cellid']

def bfunc_6_c86(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6Cellid'] is not None

def bfunc_6_c87(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] is not None

def bfunc_6_c88(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] == var_bindings['v2']['Nc6Cellid']

def bfunc_6_c89(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is not None

def bfunc_6_c9(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] == var_bindings['v2']['Nc1Cellid']

def bfunc_6_c90(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] == var_bindings['v2']['Nc6Cellid']

def bfunc_6_c91(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is not None

def bfunc_6_c92(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] == var_bindings['v2']['Nc6Cellid']

def bfunc_6_c93(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is not None

def bfunc_6_c94(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] == var_bindings['v2']['Nc6Cellid']

def bfunc_6_c95(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is not None

def bfunc_6_c96(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] == var_bindings['v2']['Nc6Cellid']

def bfunc_6_c97(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is not None

def bfunc_6_c98(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] == var_bindings['v2']['Nc6Cellid']

def bfunc_6_c99(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is not None

