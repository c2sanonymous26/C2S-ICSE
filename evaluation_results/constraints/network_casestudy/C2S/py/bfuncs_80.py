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

def bfunc_3_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Time'] is not None

def bfunc_3_c3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Longitude'] is not None

def bfunc_3_c4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Longitude'] is not None

def bfunc_3_c5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Latitude'] is not None

def bfunc_3_c6(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Latitude'] is not None

def bfunc_3_c7(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_3_c8(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_3_c9(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Time'] > var_bindings['v1']['Time']

def bfunc_4_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 6371000 * 2 * asin(sqrt(pow(sin(radians(var_bindings['v2']['Latitude'] - var_bindings['v1']['Latitude']) / 2), 2) + cos(radians(var_bindings['v1']['Latitude'])) * cos(radians(var_bindings['v2']['Latitude'])) * pow(sin(radians(var_bindings['v2']['Longitude'] - var_bindings['v1']['Longitude']) / 2), 2))) / ((var_bindings['v2']['Time'] - var_bindings['v1']['Time']) / 1000.0) < 160763/62500

def bfunc_5_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] >= 1

def bfunc_5_c10(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] < 60000001/1000000

def bfunc_5_c11(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] >= 3

def bfunc_5_c12(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is not None

def bfunc_5_c13(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] is not None

def bfunc_5_c14(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return (var_bindings['v2']['NcSize'] >= 1 and (var_bindings['v2']['Nc1Cellid'] is not None and var_bindings['v2']['Nc1Cellid'] == var_bindings['v1']['Nc3Cellid'])) + (var_bindings['v2']['NcSize'] >= 2 and (var_bindings['v2']['Nc2Cellid'] is not None and var_bindings['v2']['Nc2Cellid'] == var_bindings['v1']['Nc3Cellid'])) + (var_bindings['v2']['NcSize'] >= 3 and (var_bindings['v2']['Nc3Cellid'] is not None and var_bindings['v2']['Nc3Cellid'] == var_bindings['v1']['Nc3Cellid'])) + (var_bindings['v2']['NcSize'] >= 4 and (var_bindings['v2']['Nc4Cellid'] is not None and var_bindings['v2']['Nc4Cellid'] == var_bindings['v1']['Nc3Cellid'])) + (var_bindings['v2']['NcSize'] >= 5 and (var_bindings['v2']['Nc5Cellid'] is not None and var_bindings['v2']['Nc5Cellid'] == var_bindings['v1']['Nc3Cellid'])) + (var_bindings['v2']['NcSize'] >= 6 and (var_bindings['v2']['Nc6Cellid'] is not None and var_bindings['v2']['Nc6Cellid'] == var_bindings['v1']['Nc3Cellid'])) + (var_bindings['v2']['NcSize'] >= 7 and (var_bindings['v2']['Nc7Cellid'] is not None and var_bindings['v2']['Nc7Cellid'] == var_bindings['v1']['Nc3Cellid'])) + (var_bindings['v2']['NcSize'] >= 8 and (var_bindings['v2']['Nc8Cellid'] is not None and var_bindings['v2']['Nc8Cellid'] == var_bindings['v1']['Nc3Cellid'])) == 0

def bfunc_5_c15(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] < 60000001/1000000

def bfunc_5_c16(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] >= 4

def bfunc_5_c17(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is not None

def bfunc_5_c18(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] is not None

def bfunc_5_c19(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return (var_bindings['v2']['NcSize'] >= 1 and (var_bindings['v2']['Nc1Cellid'] is not None and var_bindings['v2']['Nc1Cellid'] == var_bindings['v1']['Nc4Cellid'])) + (var_bindings['v2']['NcSize'] >= 2 and (var_bindings['v2']['Nc2Cellid'] is not None and var_bindings['v2']['Nc2Cellid'] == var_bindings['v1']['Nc4Cellid'])) + (var_bindings['v2']['NcSize'] >= 3 and (var_bindings['v2']['Nc3Cellid'] is not None and var_bindings['v2']['Nc3Cellid'] == var_bindings['v1']['Nc4Cellid'])) + (var_bindings['v2']['NcSize'] >= 4 and (var_bindings['v2']['Nc4Cellid'] is not None and var_bindings['v2']['Nc4Cellid'] == var_bindings['v1']['Nc4Cellid'])) + (var_bindings['v2']['NcSize'] >= 5 and (var_bindings['v2']['Nc5Cellid'] is not None and var_bindings['v2']['Nc5Cellid'] == var_bindings['v1']['Nc4Cellid'])) + (var_bindings['v2']['NcSize'] >= 6 and (var_bindings['v2']['Nc6Cellid'] is not None and var_bindings['v2']['Nc6Cellid'] == var_bindings['v1']['Nc4Cellid'])) + (var_bindings['v2']['NcSize'] >= 7 and (var_bindings['v2']['Nc7Cellid'] is not None and var_bindings['v2']['Nc7Cellid'] == var_bindings['v1']['Nc4Cellid'])) + (var_bindings['v2']['NcSize'] >= 8 and (var_bindings['v2']['Nc8Cellid'] is not None and var_bindings['v2']['Nc8Cellid'] == var_bindings['v1']['Nc4Cellid'])) == 0

def bfunc_5_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] is not None

def bfunc_5_c20(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] < 60000001/1000000

def bfunc_5_c21(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] >= 5

def bfunc_5_c22(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is not None

def bfunc_5_c23(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] is not None

def bfunc_5_c24(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return (var_bindings['v2']['NcSize'] >= 1 and (var_bindings['v2']['Nc1Cellid'] is not None and var_bindings['v2']['Nc1Cellid'] == var_bindings['v1']['Nc5Cellid'])) + (var_bindings['v2']['NcSize'] >= 2 and (var_bindings['v2']['Nc2Cellid'] is not None and var_bindings['v2']['Nc2Cellid'] == var_bindings['v1']['Nc5Cellid'])) + (var_bindings['v2']['NcSize'] >= 3 and (var_bindings['v2']['Nc3Cellid'] is not None and var_bindings['v2']['Nc3Cellid'] == var_bindings['v1']['Nc5Cellid'])) + (var_bindings['v2']['NcSize'] >= 4 and (var_bindings['v2']['Nc4Cellid'] is not None and var_bindings['v2']['Nc4Cellid'] == var_bindings['v1']['Nc5Cellid'])) + (var_bindings['v2']['NcSize'] >= 5 and (var_bindings['v2']['Nc5Cellid'] is not None and var_bindings['v2']['Nc5Cellid'] == var_bindings['v1']['Nc5Cellid'])) + (var_bindings['v2']['NcSize'] >= 6 and (var_bindings['v2']['Nc6Cellid'] is not None and var_bindings['v2']['Nc6Cellid'] == var_bindings['v1']['Nc5Cellid'])) + (var_bindings['v2']['NcSize'] >= 7 and (var_bindings['v2']['Nc7Cellid'] is not None and var_bindings['v2']['Nc7Cellid'] == var_bindings['v1']['Nc5Cellid'])) + (var_bindings['v2']['NcSize'] >= 8 and (var_bindings['v2']['Nc8Cellid'] is not None and var_bindings['v2']['Nc8Cellid'] == var_bindings['v1']['Nc5Cellid'])) == 0

def bfunc_5_c25(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] < 60000001/1000000

def bfunc_5_c26(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] >= 6

def bfunc_5_c27(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is not None

def bfunc_5_c28(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] is not None

def bfunc_5_c29(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return (var_bindings['v2']['NcSize'] >= 1 and (var_bindings['v2']['Nc1Cellid'] is not None and var_bindings['v2']['Nc1Cellid'] == var_bindings['v1']['Nc6Cellid'])) + (var_bindings['v2']['NcSize'] >= 2 and (var_bindings['v2']['Nc2Cellid'] is not None and var_bindings['v2']['Nc2Cellid'] == var_bindings['v1']['Nc6Cellid'])) + (var_bindings['v2']['NcSize'] >= 3 and (var_bindings['v2']['Nc3Cellid'] is not None and var_bindings['v2']['Nc3Cellid'] == var_bindings['v1']['Nc6Cellid'])) + (var_bindings['v2']['NcSize'] >= 4 and (var_bindings['v2']['Nc4Cellid'] is not None and var_bindings['v2']['Nc4Cellid'] == var_bindings['v1']['Nc6Cellid'])) + (var_bindings['v2']['NcSize'] >= 5 and (var_bindings['v2']['Nc5Cellid'] is not None and var_bindings['v2']['Nc5Cellid'] == var_bindings['v1']['Nc6Cellid'])) + (var_bindings['v2']['NcSize'] >= 6 and (var_bindings['v2']['Nc6Cellid'] is not None and var_bindings['v2']['Nc6Cellid'] == var_bindings['v1']['Nc6Cellid'])) + (var_bindings['v2']['NcSize'] >= 7 and (var_bindings['v2']['Nc7Cellid'] is not None and var_bindings['v2']['Nc7Cellid'] == var_bindings['v1']['Nc6Cellid'])) + (var_bindings['v2']['NcSize'] >= 8 and (var_bindings['v2']['Nc8Cellid'] is not None and var_bindings['v2']['Nc8Cellid'] == var_bindings['v1']['Nc6Cellid'])) == 0

def bfunc_5_c3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] is not None

def bfunc_5_c30(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] < 60000001/1000000

def bfunc_5_c31(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] >= 7

def bfunc_5_c32(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is not None

def bfunc_5_c33(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] is not None

def bfunc_5_c34(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return (var_bindings['v2']['NcSize'] >= 1 and (var_bindings['v2']['Nc1Cellid'] is not None and var_bindings['v2']['Nc1Cellid'] == var_bindings['v1']['Nc7Cellid'])) + (var_bindings['v2']['NcSize'] >= 2 and (var_bindings['v2']['Nc2Cellid'] is not None and var_bindings['v2']['Nc2Cellid'] == var_bindings['v1']['Nc7Cellid'])) + (var_bindings['v2']['NcSize'] >= 3 and (var_bindings['v2']['Nc3Cellid'] is not None and var_bindings['v2']['Nc3Cellid'] == var_bindings['v1']['Nc7Cellid'])) + (var_bindings['v2']['NcSize'] >= 4 and (var_bindings['v2']['Nc4Cellid'] is not None and var_bindings['v2']['Nc4Cellid'] == var_bindings['v1']['Nc7Cellid'])) + (var_bindings['v2']['NcSize'] >= 5 and (var_bindings['v2']['Nc5Cellid'] is not None and var_bindings['v2']['Nc5Cellid'] == var_bindings['v1']['Nc7Cellid'])) + (var_bindings['v2']['NcSize'] >= 6 and (var_bindings['v2']['Nc6Cellid'] is not None and var_bindings['v2']['Nc6Cellid'] == var_bindings['v1']['Nc7Cellid'])) + (var_bindings['v2']['NcSize'] >= 7 and (var_bindings['v2']['Nc7Cellid'] is not None and var_bindings['v2']['Nc7Cellid'] == var_bindings['v1']['Nc7Cellid'])) + (var_bindings['v2']['NcSize'] >= 8 and (var_bindings['v2']['Nc8Cellid'] is not None and var_bindings['v2']['Nc8Cellid'] == var_bindings['v1']['Nc7Cellid'])) == 0

def bfunc_5_c35(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] < 60000001/1000000

def bfunc_5_c36(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] >= 8

def bfunc_5_c37(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is not None

def bfunc_5_c38(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] is not None

def bfunc_5_c39(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return (var_bindings['v2']['NcSize'] >= 1 and (var_bindings['v2']['Nc1Cellid'] is not None and var_bindings['v2']['Nc1Cellid'] == var_bindings['v1']['Nc8Cellid'])) + (var_bindings['v2']['NcSize'] >= 2 and (var_bindings['v2']['Nc2Cellid'] is not None and var_bindings['v2']['Nc2Cellid'] == var_bindings['v1']['Nc8Cellid'])) + (var_bindings['v2']['NcSize'] >= 3 and (var_bindings['v2']['Nc3Cellid'] is not None and var_bindings['v2']['Nc3Cellid'] == var_bindings['v1']['Nc8Cellid'])) + (var_bindings['v2']['NcSize'] >= 4 and (var_bindings['v2']['Nc4Cellid'] is not None and var_bindings['v2']['Nc4Cellid'] == var_bindings['v1']['Nc8Cellid'])) + (var_bindings['v2']['NcSize'] >= 5 and (var_bindings['v2']['Nc5Cellid'] is not None and var_bindings['v2']['Nc5Cellid'] == var_bindings['v1']['Nc8Cellid'])) + (var_bindings['v2']['NcSize'] >= 6 and (var_bindings['v2']['Nc6Cellid'] is not None and var_bindings['v2']['Nc6Cellid'] == var_bindings['v1']['Nc8Cellid'])) + (var_bindings['v2']['NcSize'] >= 7 and (var_bindings['v2']['Nc7Cellid'] is not None and var_bindings['v2']['Nc7Cellid'] == var_bindings['v1']['Nc8Cellid'])) + (var_bindings['v2']['NcSize'] >= 8 and (var_bindings['v2']['Nc8Cellid'] is not None and var_bindings['v2']['Nc8Cellid'] == var_bindings['v1']['Nc8Cellid'])) == 0

def bfunc_5_c4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return (var_bindings['v2']['NcSize'] >= 1 and (var_bindings['v2']['Nc1Cellid'] is not None and var_bindings['v2']['Nc1Cellid'] == var_bindings['v1']['Nc1Cellid'])) + (var_bindings['v2']['NcSize'] >= 2 and (var_bindings['v2']['Nc2Cellid'] is not None and var_bindings['v2']['Nc2Cellid'] == var_bindings['v1']['Nc1Cellid'])) + (var_bindings['v2']['NcSize'] >= 3 and (var_bindings['v2']['Nc3Cellid'] is not None and var_bindings['v2']['Nc3Cellid'] == var_bindings['v1']['Nc1Cellid'])) + (var_bindings['v2']['NcSize'] >= 4 and (var_bindings['v2']['Nc4Cellid'] is not None and var_bindings['v2']['Nc4Cellid'] == var_bindings['v1']['Nc1Cellid'])) + (var_bindings['v2']['NcSize'] >= 5 and (var_bindings['v2']['Nc5Cellid'] is not None and var_bindings['v2']['Nc5Cellid'] == var_bindings['v1']['Nc1Cellid'])) + (var_bindings['v2']['NcSize'] >= 6 and (var_bindings['v2']['Nc6Cellid'] is not None and var_bindings['v2']['Nc6Cellid'] == var_bindings['v1']['Nc1Cellid'])) + (var_bindings['v2']['NcSize'] >= 7 and (var_bindings['v2']['Nc7Cellid'] is not None and var_bindings['v2']['Nc7Cellid'] == var_bindings['v1']['Nc1Cellid'])) + (var_bindings['v2']['NcSize'] >= 8 and (var_bindings['v2']['Nc8Cellid'] is not None and var_bindings['v2']['Nc8Cellid'] == var_bindings['v1']['Nc1Cellid'])) == 0

def bfunc_5_c40(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] < 60000001/1000000

def bfunc_5_c5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] < 60000001/1000000

def bfunc_5_c6(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] >= 2

def bfunc_5_c7(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is not None

def bfunc_5_c8(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] is not None

def bfunc_5_c9(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return (var_bindings['v2']['NcSize'] >= 1 and (var_bindings['v2']['Nc1Cellid'] is not None and var_bindings['v2']['Nc1Cellid'] == var_bindings['v1']['Nc2Cellid'])) + (var_bindings['v2']['NcSize'] >= 2 and (var_bindings['v2']['Nc2Cellid'] is not None and var_bindings['v2']['Nc2Cellid'] == var_bindings['v1']['Nc2Cellid'])) + (var_bindings['v2']['NcSize'] >= 3 and (var_bindings['v2']['Nc3Cellid'] is not None and var_bindings['v2']['Nc3Cellid'] == var_bindings['v1']['Nc2Cellid'])) + (var_bindings['v2']['NcSize'] >= 4 and (var_bindings['v2']['Nc4Cellid'] is not None and var_bindings['v2']['Nc4Cellid'] == var_bindings['v1']['Nc2Cellid'])) + (var_bindings['v2']['NcSize'] >= 5 and (var_bindings['v2']['Nc5Cellid'] is not None and var_bindings['v2']['Nc5Cellid'] == var_bindings['v1']['Nc2Cellid'])) + (var_bindings['v2']['NcSize'] >= 6 and (var_bindings['v2']['Nc6Cellid'] is not None and var_bindings['v2']['Nc6Cellid'] == var_bindings['v1']['Nc2Cellid'])) + (var_bindings['v2']['NcSize'] >= 7 and (var_bindings['v2']['Nc7Cellid'] is not None and var_bindings['v2']['Nc7Cellid'] == var_bindings['v1']['Nc2Cellid'])) + (var_bindings['v2']['NcSize'] >= 8 and (var_bindings['v2']['Nc8Cellid'] is not None and var_bindings['v2']['Nc8Cellid'] == var_bindings['v1']['Nc2Cellid'])) == 0

