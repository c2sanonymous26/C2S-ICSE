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
    return var_bindings['v1']['Nc1Cellid'] is not None

def bfunc_3_c10(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] is not None

def bfunc_3_c100(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] is not None

def bfunc_3_c101(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRP'] is not None

def bfunc_3_c102(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc3RSRP'] - var_bindings['v2']['Nc1RSRP']) < 61000001/1000000

def bfunc_3_c103(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is not None

def bfunc_3_c104(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2Cellid'] is not None

def bfunc_3_c105(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] == var_bindings['v2']['Nc2Cellid']

def bfunc_3_c106(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] is not None

def bfunc_3_c107(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRP'] is not None

def bfunc_3_c108(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc3RSRP'] - var_bindings['v2']['Nc2RSRP']) < 61000001/1000000

def bfunc_3_c109(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is not None

def bfunc_3_c11(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRP'] is not None

def bfunc_3_c110(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3Cellid'] is not None

def bfunc_3_c111(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] == var_bindings['v2']['Nc3Cellid']

def bfunc_3_c112(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] is not None

def bfunc_3_c113(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRP'] is not None

def bfunc_3_c114(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc3RSRP'] - var_bindings['v2']['Nc3RSRP']) < 61000001/1000000

def bfunc_3_c115(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is not None

def bfunc_3_c116(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4Cellid'] is not None

def bfunc_3_c117(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] == var_bindings['v2']['Nc4Cellid']

def bfunc_3_c118(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] is not None

def bfunc_3_c119(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRP'] is not None

def bfunc_3_c12(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc1RSRP'] - var_bindings['v2']['Nc2RSRP']) < 61000001/1000000

def bfunc_3_c120(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc3RSRP'] - var_bindings['v2']['Nc4RSRP']) < 61000001/1000000

def bfunc_3_c121(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is not None

def bfunc_3_c122(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5Cellid'] is not None

def bfunc_3_c123(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] == var_bindings['v2']['Nc5Cellid']

def bfunc_3_c124(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] is not None

def bfunc_3_c125(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRP'] is not None

def bfunc_3_c126(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc3RSRP'] - var_bindings['v2']['Nc5RSRP']) < 61000001/1000000

def bfunc_3_c127(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is not None

def bfunc_3_c128(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6Cellid'] is not None

def bfunc_3_c129(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] == var_bindings['v2']['Nc6Cellid']

def bfunc_3_c13(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] is not None

def bfunc_3_c130(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] is not None

def bfunc_3_c131(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRP'] is not None

def bfunc_3_c132(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc3RSRP'] - var_bindings['v2']['Nc6RSRP']) < 61000001/1000000

def bfunc_3_c133(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is not None

def bfunc_3_c134(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7Cellid'] is not None

def bfunc_3_c135(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] == var_bindings['v2']['Nc7Cellid']

def bfunc_3_c136(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] is not None

def bfunc_3_c137(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRP'] is not None

def bfunc_3_c138(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc3RSRP'] - var_bindings['v2']['Nc7RSRP']) < 61000001/1000000

def bfunc_3_c139(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is not None

def bfunc_3_c14(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3Cellid'] is not None

def bfunc_3_c140(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8Cellid'] is not None

def bfunc_3_c141(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] == var_bindings['v2']['Nc8Cellid']

def bfunc_3_c142(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] is not None

def bfunc_3_c143(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRP'] is not None

def bfunc_3_c144(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc3RSRP'] - var_bindings['v2']['Nc8RSRP']) < 61000001/1000000

def bfunc_3_c145(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is not None

def bfunc_3_c146(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1Cellid'] is not None

def bfunc_3_c147(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] == var_bindings['v2']['Nc1Cellid']

def bfunc_3_c148(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] is not None

def bfunc_3_c149(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRP'] is not None

def bfunc_3_c15(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] == var_bindings['v2']['Nc3Cellid']

def bfunc_3_c150(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc4RSRP'] - var_bindings['v2']['Nc1RSRP']) < 61000001/1000000

def bfunc_3_c151(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is not None

def bfunc_3_c152(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2Cellid'] is not None

def bfunc_3_c153(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] == var_bindings['v2']['Nc2Cellid']

def bfunc_3_c154(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] is not None

def bfunc_3_c155(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRP'] is not None

def bfunc_3_c156(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc4RSRP'] - var_bindings['v2']['Nc2RSRP']) < 61000001/1000000

def bfunc_3_c157(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is not None

def bfunc_3_c158(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3Cellid'] is not None

def bfunc_3_c159(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] == var_bindings['v2']['Nc3Cellid']

def bfunc_3_c16(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] is not None

def bfunc_3_c160(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] is not None

def bfunc_3_c161(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRP'] is not None

def bfunc_3_c162(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc4RSRP'] - var_bindings['v2']['Nc3RSRP']) < 61000001/1000000

def bfunc_3_c163(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is not None

def bfunc_3_c164(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4Cellid'] is not None

def bfunc_3_c165(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] == var_bindings['v2']['Nc4Cellid']

def bfunc_3_c166(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] is not None

def bfunc_3_c167(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRP'] is not None

def bfunc_3_c168(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc4RSRP'] - var_bindings['v2']['Nc4RSRP']) < 61000001/1000000

def bfunc_3_c169(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is not None

def bfunc_3_c17(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRP'] is not None

def bfunc_3_c170(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5Cellid'] is not None

def bfunc_3_c171(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] == var_bindings['v2']['Nc5Cellid']

def bfunc_3_c172(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] is not None

def bfunc_3_c173(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRP'] is not None

def bfunc_3_c174(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc4RSRP'] - var_bindings['v2']['Nc5RSRP']) < 61000001/1000000

def bfunc_3_c175(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is not None

def bfunc_3_c176(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6Cellid'] is not None

def bfunc_3_c177(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] == var_bindings['v2']['Nc6Cellid']

def bfunc_3_c178(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] is not None

def bfunc_3_c179(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRP'] is not None

def bfunc_3_c18(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc1RSRP'] - var_bindings['v2']['Nc3RSRP']) < 61000001/1000000

def bfunc_3_c180(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc4RSRP'] - var_bindings['v2']['Nc6RSRP']) < 61000001/1000000

def bfunc_3_c181(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is not None

def bfunc_3_c182(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7Cellid'] is not None

def bfunc_3_c183(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] == var_bindings['v2']['Nc7Cellid']

def bfunc_3_c184(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] is not None

def bfunc_3_c185(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRP'] is not None

def bfunc_3_c186(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc4RSRP'] - var_bindings['v2']['Nc7RSRP']) < 61000001/1000000

def bfunc_3_c187(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is not None

def bfunc_3_c188(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8Cellid'] is not None

def bfunc_3_c189(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] == var_bindings['v2']['Nc8Cellid']

def bfunc_3_c19(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] is not None

def bfunc_3_c190(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] is not None

def bfunc_3_c191(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRP'] is not None

def bfunc_3_c192(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc4RSRP'] - var_bindings['v2']['Nc8RSRP']) < 61000001/1000000

def bfunc_3_c193(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is not None

def bfunc_3_c194(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1Cellid'] is not None

def bfunc_3_c195(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] == var_bindings['v2']['Nc1Cellid']

def bfunc_3_c196(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] is not None

def bfunc_3_c197(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRP'] is not None

def bfunc_3_c198(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc5RSRP'] - var_bindings['v2']['Nc1RSRP']) < 61000001/1000000

def bfunc_3_c199(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is not None

def bfunc_3_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1Cellid'] is not None

def bfunc_3_c20(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4Cellid'] is not None

def bfunc_3_c200(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2Cellid'] is not None

def bfunc_3_c201(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] == var_bindings['v2']['Nc2Cellid']

def bfunc_3_c202(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] is not None

def bfunc_3_c203(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRP'] is not None

def bfunc_3_c204(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc5RSRP'] - var_bindings['v2']['Nc2RSRP']) < 61000001/1000000

def bfunc_3_c205(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is not None

def bfunc_3_c206(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3Cellid'] is not None

def bfunc_3_c207(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] == var_bindings['v2']['Nc3Cellid']

def bfunc_3_c208(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] is not None

def bfunc_3_c209(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRP'] is not None

def bfunc_3_c21(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] == var_bindings['v2']['Nc4Cellid']

def bfunc_3_c210(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc5RSRP'] - var_bindings['v2']['Nc3RSRP']) < 61000001/1000000

def bfunc_3_c211(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is not None

def bfunc_3_c212(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4Cellid'] is not None

def bfunc_3_c213(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] == var_bindings['v2']['Nc4Cellid']

def bfunc_3_c214(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] is not None

def bfunc_3_c215(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRP'] is not None

def bfunc_3_c216(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc5RSRP'] - var_bindings['v2']['Nc4RSRP']) < 61000001/1000000

def bfunc_3_c217(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is not None

def bfunc_3_c218(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5Cellid'] is not None

def bfunc_3_c219(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] == var_bindings['v2']['Nc5Cellid']

def bfunc_3_c22(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] is not None

def bfunc_3_c220(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] is not None

def bfunc_3_c221(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRP'] is not None

def bfunc_3_c222(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc5RSRP'] - var_bindings['v2']['Nc5RSRP']) < 61000001/1000000

def bfunc_3_c223(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is not None

def bfunc_3_c224(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6Cellid'] is not None

def bfunc_3_c225(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] == var_bindings['v2']['Nc6Cellid']

def bfunc_3_c226(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] is not None

def bfunc_3_c227(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRP'] is not None

def bfunc_3_c228(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc5RSRP'] - var_bindings['v2']['Nc6RSRP']) < 61000001/1000000

def bfunc_3_c229(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is not None

def bfunc_3_c23(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRP'] is not None

def bfunc_3_c230(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7Cellid'] is not None

def bfunc_3_c231(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] == var_bindings['v2']['Nc7Cellid']

def bfunc_3_c232(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] is not None

def bfunc_3_c233(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRP'] is not None

def bfunc_3_c234(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc5RSRP'] - var_bindings['v2']['Nc7RSRP']) < 61000001/1000000

def bfunc_3_c235(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is not None

def bfunc_3_c236(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8Cellid'] is not None

def bfunc_3_c237(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] == var_bindings['v2']['Nc8Cellid']

def bfunc_3_c238(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] is not None

def bfunc_3_c239(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRP'] is not None

def bfunc_3_c24(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc1RSRP'] - var_bindings['v2']['Nc4RSRP']) < 61000001/1000000

def bfunc_3_c240(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc5RSRP'] - var_bindings['v2']['Nc8RSRP']) < 61000001/1000000

def bfunc_3_c241(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is not None

def bfunc_3_c242(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1Cellid'] is not None

def bfunc_3_c243(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] == var_bindings['v2']['Nc1Cellid']

def bfunc_3_c244(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] is not None

def bfunc_3_c245(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRP'] is not None

def bfunc_3_c246(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc6RSRP'] - var_bindings['v2']['Nc1RSRP']) < 61000001/1000000

def bfunc_3_c247(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is not None

def bfunc_3_c248(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2Cellid'] is not None

def bfunc_3_c249(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] == var_bindings['v2']['Nc2Cellid']

def bfunc_3_c25(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] is not None

def bfunc_3_c250(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] is not None

def bfunc_3_c251(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRP'] is not None

def bfunc_3_c252(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc6RSRP'] - var_bindings['v2']['Nc2RSRP']) < 61000001/1000000

def bfunc_3_c253(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is not None

def bfunc_3_c254(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3Cellid'] is not None

def bfunc_3_c255(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] == var_bindings['v2']['Nc3Cellid']

def bfunc_3_c256(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] is not None

def bfunc_3_c257(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRP'] is not None

def bfunc_3_c258(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc6RSRP'] - var_bindings['v2']['Nc3RSRP']) < 61000001/1000000

def bfunc_3_c259(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is not None

def bfunc_3_c26(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5Cellid'] is not None

def bfunc_3_c260(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4Cellid'] is not None

def bfunc_3_c261(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] == var_bindings['v2']['Nc4Cellid']

def bfunc_3_c262(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] is not None

def bfunc_3_c263(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRP'] is not None

def bfunc_3_c264(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc6RSRP'] - var_bindings['v2']['Nc4RSRP']) < 61000001/1000000

def bfunc_3_c265(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is not None

def bfunc_3_c266(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5Cellid'] is not None

def bfunc_3_c267(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] == var_bindings['v2']['Nc5Cellid']

def bfunc_3_c268(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] is not None

def bfunc_3_c269(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRP'] is not None

def bfunc_3_c27(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] == var_bindings['v2']['Nc5Cellid']

def bfunc_3_c270(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc6RSRP'] - var_bindings['v2']['Nc5RSRP']) < 61000001/1000000

def bfunc_3_c271(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is not None

def bfunc_3_c272(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6Cellid'] is not None

def bfunc_3_c273(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] == var_bindings['v2']['Nc6Cellid']

def bfunc_3_c274(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] is not None

def bfunc_3_c275(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRP'] is not None

def bfunc_3_c276(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc6RSRP'] - var_bindings['v2']['Nc6RSRP']) < 61000001/1000000

def bfunc_3_c277(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is not None

def bfunc_3_c278(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7Cellid'] is not None

def bfunc_3_c279(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] == var_bindings['v2']['Nc7Cellid']

def bfunc_3_c28(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] is not None

def bfunc_3_c280(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] is not None

def bfunc_3_c281(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRP'] is not None

def bfunc_3_c282(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc6RSRP'] - var_bindings['v2']['Nc7RSRP']) < 61000001/1000000

def bfunc_3_c283(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is not None

def bfunc_3_c284(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8Cellid'] is not None

def bfunc_3_c285(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] == var_bindings['v2']['Nc8Cellid']

def bfunc_3_c286(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] is not None

def bfunc_3_c287(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRP'] is not None

def bfunc_3_c288(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc6RSRP'] - var_bindings['v2']['Nc8RSRP']) < 61000001/1000000

def bfunc_3_c289(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is not None

def bfunc_3_c29(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRP'] is not None

def bfunc_3_c290(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1Cellid'] is not None

def bfunc_3_c291(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] == var_bindings['v2']['Nc1Cellid']

def bfunc_3_c292(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] is not None

def bfunc_3_c293(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRP'] is not None

def bfunc_3_c294(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc7RSRP'] - var_bindings['v2']['Nc1RSRP']) < 61000001/1000000

def bfunc_3_c295(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is not None

def bfunc_3_c296(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2Cellid'] is not None

def bfunc_3_c297(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] == var_bindings['v2']['Nc2Cellid']

def bfunc_3_c298(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] is not None

def bfunc_3_c299(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRP'] is not None

def bfunc_3_c3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] == var_bindings['v2']['Nc1Cellid']

def bfunc_3_c30(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc1RSRP'] - var_bindings['v2']['Nc5RSRP']) < 61000001/1000000

def bfunc_3_c300(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc7RSRP'] - var_bindings['v2']['Nc2RSRP']) < 61000001/1000000

def bfunc_3_c301(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is not None

def bfunc_3_c302(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3Cellid'] is not None

def bfunc_3_c303(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] == var_bindings['v2']['Nc3Cellid']

def bfunc_3_c304(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] is not None

def bfunc_3_c305(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRP'] is not None

def bfunc_3_c306(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc7RSRP'] - var_bindings['v2']['Nc3RSRP']) < 61000001/1000000

def bfunc_3_c307(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is not None

def bfunc_3_c308(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4Cellid'] is not None

def bfunc_3_c309(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] == var_bindings['v2']['Nc4Cellid']

def bfunc_3_c31(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] is not None

def bfunc_3_c310(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] is not None

def bfunc_3_c311(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRP'] is not None

def bfunc_3_c312(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc7RSRP'] - var_bindings['v2']['Nc4RSRP']) < 61000001/1000000

def bfunc_3_c313(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is not None

def bfunc_3_c314(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5Cellid'] is not None

def bfunc_3_c315(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] == var_bindings['v2']['Nc5Cellid']

def bfunc_3_c316(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] is not None

def bfunc_3_c317(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRP'] is not None

def bfunc_3_c318(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc7RSRP'] - var_bindings['v2']['Nc5RSRP']) < 61000001/1000000

def bfunc_3_c319(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is not None

def bfunc_3_c32(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6Cellid'] is not None

def bfunc_3_c320(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6Cellid'] is not None

def bfunc_3_c321(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] == var_bindings['v2']['Nc6Cellid']

def bfunc_3_c322(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] is not None

def bfunc_3_c323(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRP'] is not None

def bfunc_3_c324(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc7RSRP'] - var_bindings['v2']['Nc6RSRP']) < 61000001/1000000

def bfunc_3_c325(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is not None

def bfunc_3_c326(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7Cellid'] is not None

def bfunc_3_c327(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] == var_bindings['v2']['Nc7Cellid']

def bfunc_3_c328(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] is not None

def bfunc_3_c329(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRP'] is not None

def bfunc_3_c33(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] == var_bindings['v2']['Nc6Cellid']

def bfunc_3_c330(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc7RSRP'] - var_bindings['v2']['Nc7RSRP']) < 61000001/1000000

def bfunc_3_c331(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is not None

def bfunc_3_c332(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8Cellid'] is not None

def bfunc_3_c333(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] == var_bindings['v2']['Nc8Cellid']

def bfunc_3_c334(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] is not None

def bfunc_3_c335(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRP'] is not None

def bfunc_3_c336(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc7RSRP'] - var_bindings['v2']['Nc8RSRP']) < 61000001/1000000

def bfunc_3_c337(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is not None

def bfunc_3_c338(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1Cellid'] is not None

def bfunc_3_c339(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] == var_bindings['v2']['Nc1Cellid']

def bfunc_3_c34(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] is not None

def bfunc_3_c340(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] is not None

def bfunc_3_c341(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRP'] is not None

def bfunc_3_c342(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc8RSRP'] - var_bindings['v2']['Nc1RSRP']) < 61000001/1000000

def bfunc_3_c343(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is not None

def bfunc_3_c344(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2Cellid'] is not None

def bfunc_3_c345(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] == var_bindings['v2']['Nc2Cellid']

def bfunc_3_c346(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] is not None

def bfunc_3_c347(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRP'] is not None

def bfunc_3_c348(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc8RSRP'] - var_bindings['v2']['Nc2RSRP']) < 61000001/1000000

def bfunc_3_c349(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is not None

def bfunc_3_c35(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRP'] is not None

def bfunc_3_c350(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3Cellid'] is not None

def bfunc_3_c351(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] == var_bindings['v2']['Nc3Cellid']

def bfunc_3_c352(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] is not None

def bfunc_3_c353(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRP'] is not None

def bfunc_3_c354(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc8RSRP'] - var_bindings['v2']['Nc3RSRP']) < 61000001/1000000

def bfunc_3_c355(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is not None

def bfunc_3_c356(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4Cellid'] is not None

def bfunc_3_c357(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] == var_bindings['v2']['Nc4Cellid']

def bfunc_3_c358(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] is not None

def bfunc_3_c359(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRP'] is not None

def bfunc_3_c36(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc1RSRP'] - var_bindings['v2']['Nc6RSRP']) < 61000001/1000000

def bfunc_3_c360(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc8RSRP'] - var_bindings['v2']['Nc4RSRP']) < 61000001/1000000

def bfunc_3_c361(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is not None

def bfunc_3_c362(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5Cellid'] is not None

def bfunc_3_c363(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] == var_bindings['v2']['Nc5Cellid']

def bfunc_3_c364(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] is not None

def bfunc_3_c365(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRP'] is not None

def bfunc_3_c366(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc8RSRP'] - var_bindings['v2']['Nc5RSRP']) < 61000001/1000000

def bfunc_3_c367(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is not None

def bfunc_3_c368(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6Cellid'] is not None

def bfunc_3_c369(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] == var_bindings['v2']['Nc6Cellid']

def bfunc_3_c37(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] is not None

def bfunc_3_c370(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] is not None

def bfunc_3_c371(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRP'] is not None

def bfunc_3_c372(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc8RSRP'] - var_bindings['v2']['Nc6RSRP']) < 61000001/1000000

def bfunc_3_c373(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is not None

def bfunc_3_c374(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7Cellid'] is not None

def bfunc_3_c375(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] == var_bindings['v2']['Nc7Cellid']

def bfunc_3_c376(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] is not None

def bfunc_3_c377(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRP'] is not None

def bfunc_3_c378(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc8RSRP'] - var_bindings['v2']['Nc7RSRP']) < 61000001/1000000

def bfunc_3_c379(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is not None

def bfunc_3_c38(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7Cellid'] is not None

def bfunc_3_c380(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8Cellid'] is not None

def bfunc_3_c381(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] == var_bindings['v2']['Nc8Cellid']

def bfunc_3_c382(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] is not None

def bfunc_3_c383(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRP'] is not None

def bfunc_3_c384(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc8RSRP'] - var_bindings['v2']['Nc8RSRP']) < 61000001/1000000

def bfunc_3_c39(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] == var_bindings['v2']['Nc7Cellid']

def bfunc_3_c4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] is not None

def bfunc_3_c40(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] is not None

def bfunc_3_c41(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRP'] is not None

def bfunc_3_c42(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc1RSRP'] - var_bindings['v2']['Nc7RSRP']) < 61000001/1000000

def bfunc_3_c43(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] is not None

def bfunc_3_c44(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8Cellid'] is not None

def bfunc_3_c45(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] == var_bindings['v2']['Nc8Cellid']

def bfunc_3_c46(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] is not None

def bfunc_3_c47(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRP'] is not None

def bfunc_3_c48(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc1RSRP'] - var_bindings['v2']['Nc8RSRP']) < 61000001/1000000

def bfunc_3_c49(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is not None

def bfunc_3_c5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRP'] is not None

def bfunc_3_c50(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1Cellid'] is not None

def bfunc_3_c51(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] == var_bindings['v2']['Nc1Cellid']

def bfunc_3_c52(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] is not None

def bfunc_3_c53(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRP'] is not None

def bfunc_3_c54(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc2RSRP'] - var_bindings['v2']['Nc1RSRP']) < 61000001/1000000

def bfunc_3_c55(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is not None

def bfunc_3_c56(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2Cellid'] is not None

def bfunc_3_c57(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] == var_bindings['v2']['Nc2Cellid']

def bfunc_3_c58(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] is not None

def bfunc_3_c59(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRP'] is not None

def bfunc_3_c6(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc1RSRP'] - var_bindings['v2']['Nc1RSRP']) < 61000001/1000000

def bfunc_3_c60(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc2RSRP'] - var_bindings['v2']['Nc2RSRP']) < 61000001/1000000

def bfunc_3_c61(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is not None

def bfunc_3_c62(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3Cellid'] is not None

def bfunc_3_c63(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] == var_bindings['v2']['Nc3Cellid']

def bfunc_3_c64(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] is not None

def bfunc_3_c65(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRP'] is not None

def bfunc_3_c66(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc2RSRP'] - var_bindings['v2']['Nc3RSRP']) < 61000001/1000000

def bfunc_3_c67(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is not None

def bfunc_3_c68(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4Cellid'] is not None

def bfunc_3_c69(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] == var_bindings['v2']['Nc4Cellid']

def bfunc_3_c7(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] is not None

def bfunc_3_c70(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] is not None

def bfunc_3_c71(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRP'] is not None

def bfunc_3_c72(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc2RSRP'] - var_bindings['v2']['Nc4RSRP']) < 61000001/1000000

def bfunc_3_c73(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is not None

def bfunc_3_c74(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5Cellid'] is not None

def bfunc_3_c75(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] == var_bindings['v2']['Nc5Cellid']

def bfunc_3_c76(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] is not None

def bfunc_3_c77(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRP'] is not None

def bfunc_3_c78(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc2RSRP'] - var_bindings['v2']['Nc5RSRP']) < 61000001/1000000

def bfunc_3_c79(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is not None

def bfunc_3_c8(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2Cellid'] is not None

def bfunc_3_c80(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6Cellid'] is not None

def bfunc_3_c81(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] == var_bindings['v2']['Nc6Cellid']

def bfunc_3_c82(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] is not None

def bfunc_3_c83(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRP'] is not None

def bfunc_3_c84(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc2RSRP'] - var_bindings['v2']['Nc6RSRP']) < 61000001/1000000

def bfunc_3_c85(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is not None

def bfunc_3_c86(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7Cellid'] is not None

def bfunc_3_c87(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] == var_bindings['v2']['Nc7Cellid']

def bfunc_3_c88(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] is not None

def bfunc_3_c89(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRP'] is not None

def bfunc_3_c9(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] == var_bindings['v2']['Nc2Cellid']

def bfunc_3_c90(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc2RSRP'] - var_bindings['v2']['Nc7RSRP']) < 61000001/1000000

def bfunc_3_c91(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is not None

def bfunc_3_c92(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8Cellid'] is not None

def bfunc_3_c93(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] == var_bindings['v2']['Nc8Cellid']

def bfunc_3_c94(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] is not None

def bfunc_3_c95(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRP'] is not None

def bfunc_3_c96(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['Nc2RSRP'] - var_bindings['v2']['Nc8RSRP']) < 61000001/1000000

def bfunc_3_c97(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is not None

def bfunc_3_c98(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1Cellid'] is not None

def bfunc_3_c99(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] == var_bindings['v2']['Nc1Cellid']

