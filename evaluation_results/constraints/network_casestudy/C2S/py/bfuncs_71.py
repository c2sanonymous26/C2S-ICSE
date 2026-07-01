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

def bfunc_2_c10(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRQ'] is not None

def bfunc_2_c100(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRP'] is not None

def bfunc_2_c101(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRQ'] is not None

def bfunc_2_c102(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRQ'] is not None

def bfunc_2_c103(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRP'] - var_bindings['v1']['Nc1RSRP'] > 12

def bfunc_2_c104(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRQ'] >= var_bindings['v1']['Nc1RSRQ'] - 6

def bfunc_2_c105(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c106(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c107(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 2 <= var_bindings['v1']['NcSize']

def bfunc_2_c108(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 1 <= var_bindings['v2']['NcSize']

def bfunc_2_c109(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is not None

def bfunc_2_c11(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRQ'] is not None

def bfunc_2_c110(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1Cellid'] is not None

def bfunc_2_c111(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] == var_bindings['v2']['Nc1Cellid']

def bfunc_2_c112(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] is not None

def bfunc_2_c113(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRP'] is not None

def bfunc_2_c114(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRQ'] is not None

def bfunc_2_c115(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRQ'] is not None

def bfunc_2_c116(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRP'] - var_bindings['v1']['Nc2RSRP'] > 12

def bfunc_2_c117(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRQ'] >= var_bindings['v1']['Nc2RSRQ'] - 6

def bfunc_2_c118(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c119(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c12(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRP'] - var_bindings['v1']['Nc1RSRP'] > 12

def bfunc_2_c120(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 2 <= var_bindings['v1']['NcSize']

def bfunc_2_c121(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 2 <= var_bindings['v2']['NcSize']

def bfunc_2_c122(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is not None

def bfunc_2_c123(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2Cellid'] is not None

def bfunc_2_c124(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] == var_bindings['v2']['Nc2Cellid']

def bfunc_2_c125(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] is not None

def bfunc_2_c126(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRP'] is not None

def bfunc_2_c127(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRQ'] is not None

def bfunc_2_c128(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRQ'] is not None

def bfunc_2_c129(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRP'] - var_bindings['v1']['Nc2RSRP'] > 12

def bfunc_2_c13(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRQ'] >= var_bindings['v1']['Nc1RSRQ'] - 6

def bfunc_2_c130(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRQ'] >= var_bindings['v1']['Nc2RSRQ'] - 6

def bfunc_2_c131(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c132(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c133(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 2 <= var_bindings['v1']['NcSize']

def bfunc_2_c134(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 3 <= var_bindings['v2']['NcSize']

def bfunc_2_c135(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is not None

def bfunc_2_c136(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3Cellid'] is not None

def bfunc_2_c137(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] == var_bindings['v2']['Nc3Cellid']

def bfunc_2_c138(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] is not None

def bfunc_2_c139(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRP'] is not None

def bfunc_2_c14(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c140(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRQ'] is not None

def bfunc_2_c141(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRQ'] is not None

def bfunc_2_c142(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRP'] - var_bindings['v1']['Nc2RSRP'] > 12

def bfunc_2_c143(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRQ'] >= var_bindings['v1']['Nc2RSRQ'] - 6

def bfunc_2_c144(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c145(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c146(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 2 <= var_bindings['v1']['NcSize']

def bfunc_2_c147(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 4 <= var_bindings['v2']['NcSize']

def bfunc_2_c148(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is not None

def bfunc_2_c149(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4Cellid'] is not None

def bfunc_2_c15(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c150(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] == var_bindings['v2']['Nc4Cellid']

def bfunc_2_c151(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] is not None

def bfunc_2_c152(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRP'] is not None

def bfunc_2_c153(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRQ'] is not None

def bfunc_2_c154(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRQ'] is not None

def bfunc_2_c155(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRP'] - var_bindings['v1']['Nc2RSRP'] > 12

def bfunc_2_c156(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRQ'] >= var_bindings['v1']['Nc2RSRQ'] - 6

def bfunc_2_c157(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c158(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c159(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 2 <= var_bindings['v1']['NcSize']

def bfunc_2_c16(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 1 <= var_bindings['v1']['NcSize']

def bfunc_2_c160(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 5 <= var_bindings['v2']['NcSize']

def bfunc_2_c161(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is not None

def bfunc_2_c162(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5Cellid'] is not None

def bfunc_2_c163(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] == var_bindings['v2']['Nc5Cellid']

def bfunc_2_c164(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] is not None

def bfunc_2_c165(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRP'] is not None

def bfunc_2_c166(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRQ'] is not None

def bfunc_2_c167(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRQ'] is not None

def bfunc_2_c168(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRP'] - var_bindings['v1']['Nc2RSRP'] > 12

def bfunc_2_c169(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRQ'] >= var_bindings['v1']['Nc2RSRQ'] - 6

def bfunc_2_c17(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 2 <= var_bindings['v2']['NcSize']

def bfunc_2_c170(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c171(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c172(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 2 <= var_bindings['v1']['NcSize']

def bfunc_2_c173(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 6 <= var_bindings['v2']['NcSize']

def bfunc_2_c174(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is not None

def bfunc_2_c175(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6Cellid'] is not None

def bfunc_2_c176(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] == var_bindings['v2']['Nc6Cellid']

def bfunc_2_c177(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] is not None

def bfunc_2_c178(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRP'] is not None

def bfunc_2_c179(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRQ'] is not None

def bfunc_2_c18(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] is not None

def bfunc_2_c180(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRQ'] is not None

def bfunc_2_c181(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRP'] - var_bindings['v1']['Nc2RSRP'] > 12

def bfunc_2_c182(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRQ'] >= var_bindings['v1']['Nc2RSRQ'] - 6

def bfunc_2_c183(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c184(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c185(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 2 <= var_bindings['v1']['NcSize']

def bfunc_2_c186(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 7 <= var_bindings['v2']['NcSize']

def bfunc_2_c187(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is not None

def bfunc_2_c188(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7Cellid'] is not None

def bfunc_2_c189(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] == var_bindings['v2']['Nc7Cellid']

def bfunc_2_c19(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2Cellid'] is not None

def bfunc_2_c190(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] is not None

def bfunc_2_c191(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRP'] is not None

def bfunc_2_c192(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRQ'] is not None

def bfunc_2_c193(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRQ'] is not None

def bfunc_2_c194(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRP'] - var_bindings['v1']['Nc2RSRP'] > 12

def bfunc_2_c195(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRQ'] >= var_bindings['v1']['Nc2RSRQ'] - 6

def bfunc_2_c196(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c197(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c198(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 2 <= var_bindings['v1']['NcSize']

def bfunc_2_c199(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 8 <= var_bindings['v2']['NcSize']

def bfunc_2_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c20(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] == var_bindings['v2']['Nc2Cellid']

def bfunc_2_c200(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] is not None

def bfunc_2_c201(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8Cellid'] is not None

def bfunc_2_c202(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2Cellid'] == var_bindings['v2']['Nc8Cellid']

def bfunc_2_c203(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRP'] is not None

def bfunc_2_c204(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRP'] is not None

def bfunc_2_c205(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc2RSRQ'] is not None

def bfunc_2_c206(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRQ'] is not None

def bfunc_2_c207(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRP'] - var_bindings['v1']['Nc2RSRP'] > 12

def bfunc_2_c208(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRQ'] >= var_bindings['v1']['Nc2RSRQ'] - 6

def bfunc_2_c209(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c21(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] is not None

def bfunc_2_c210(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c211(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 3 <= var_bindings['v1']['NcSize']

def bfunc_2_c212(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 1 <= var_bindings['v2']['NcSize']

def bfunc_2_c213(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is not None

def bfunc_2_c214(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1Cellid'] is not None

def bfunc_2_c215(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] == var_bindings['v2']['Nc1Cellid']

def bfunc_2_c216(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] is not None

def bfunc_2_c217(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRP'] is not None

def bfunc_2_c218(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRQ'] is not None

def bfunc_2_c219(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRQ'] is not None

def bfunc_2_c22(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRP'] is not None

def bfunc_2_c220(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRP'] - var_bindings['v1']['Nc3RSRP'] > 12

def bfunc_2_c221(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRQ'] >= var_bindings['v1']['Nc3RSRQ'] - 6

def bfunc_2_c222(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c223(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c224(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 3 <= var_bindings['v1']['NcSize']

def bfunc_2_c225(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 2 <= var_bindings['v2']['NcSize']

def bfunc_2_c226(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is not None

def bfunc_2_c227(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2Cellid'] is not None

def bfunc_2_c228(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] == var_bindings['v2']['Nc2Cellid']

def bfunc_2_c229(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] is not None

def bfunc_2_c23(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRQ'] is not None

def bfunc_2_c230(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRP'] is not None

def bfunc_2_c231(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRQ'] is not None

def bfunc_2_c232(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRQ'] is not None

def bfunc_2_c233(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRP'] - var_bindings['v1']['Nc3RSRP'] > 12

def bfunc_2_c234(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRQ'] >= var_bindings['v1']['Nc3RSRQ'] - 6

def bfunc_2_c235(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c236(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c237(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 3 <= var_bindings['v1']['NcSize']

def bfunc_2_c238(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 3 <= var_bindings['v2']['NcSize']

def bfunc_2_c239(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is not None

def bfunc_2_c24(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRQ'] is not None

def bfunc_2_c240(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3Cellid'] is not None

def bfunc_2_c241(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] == var_bindings['v2']['Nc3Cellid']

def bfunc_2_c242(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] is not None

def bfunc_2_c243(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRP'] is not None

def bfunc_2_c244(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRQ'] is not None

def bfunc_2_c245(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRQ'] is not None

def bfunc_2_c246(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRP'] - var_bindings['v1']['Nc3RSRP'] > 12

def bfunc_2_c247(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRQ'] >= var_bindings['v1']['Nc3RSRQ'] - 6

def bfunc_2_c248(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c249(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c25(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRP'] - var_bindings['v1']['Nc1RSRP'] > 12

def bfunc_2_c250(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 3 <= var_bindings['v1']['NcSize']

def bfunc_2_c251(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 4 <= var_bindings['v2']['NcSize']

def bfunc_2_c252(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is not None

def bfunc_2_c253(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4Cellid'] is not None

def bfunc_2_c254(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] == var_bindings['v2']['Nc4Cellid']

def bfunc_2_c255(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] is not None

def bfunc_2_c256(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRP'] is not None

def bfunc_2_c257(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRQ'] is not None

def bfunc_2_c258(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRQ'] is not None

def bfunc_2_c259(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRP'] - var_bindings['v1']['Nc3RSRP'] > 12

def bfunc_2_c26(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRQ'] >= var_bindings['v1']['Nc1RSRQ'] - 6

def bfunc_2_c260(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRQ'] >= var_bindings['v1']['Nc3RSRQ'] - 6

def bfunc_2_c261(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c262(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c263(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 3 <= var_bindings['v1']['NcSize']

def bfunc_2_c264(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 5 <= var_bindings['v2']['NcSize']

def bfunc_2_c265(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is not None

def bfunc_2_c266(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5Cellid'] is not None

def bfunc_2_c267(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] == var_bindings['v2']['Nc5Cellid']

def bfunc_2_c268(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] is not None

def bfunc_2_c269(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRP'] is not None

def bfunc_2_c27(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c270(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRQ'] is not None

def bfunc_2_c271(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRQ'] is not None

def bfunc_2_c272(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRP'] - var_bindings['v1']['Nc3RSRP'] > 12

def bfunc_2_c273(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRQ'] >= var_bindings['v1']['Nc3RSRQ'] - 6

def bfunc_2_c274(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c275(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c276(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 3 <= var_bindings['v1']['NcSize']

def bfunc_2_c277(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 6 <= var_bindings['v2']['NcSize']

def bfunc_2_c278(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is not None

def bfunc_2_c279(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6Cellid'] is not None

def bfunc_2_c28(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c280(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] == var_bindings['v2']['Nc6Cellid']

def bfunc_2_c281(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] is not None

def bfunc_2_c282(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRP'] is not None

def bfunc_2_c283(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRQ'] is not None

def bfunc_2_c284(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRQ'] is not None

def bfunc_2_c285(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRP'] - var_bindings['v1']['Nc3RSRP'] > 12

def bfunc_2_c286(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRQ'] >= var_bindings['v1']['Nc3RSRQ'] - 6

def bfunc_2_c287(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c288(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c289(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 3 <= var_bindings['v1']['NcSize']

def bfunc_2_c29(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 1 <= var_bindings['v1']['NcSize']

def bfunc_2_c290(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 7 <= var_bindings['v2']['NcSize']

def bfunc_2_c291(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is not None

def bfunc_2_c292(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7Cellid'] is not None

def bfunc_2_c293(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] == var_bindings['v2']['Nc7Cellid']

def bfunc_2_c294(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] is not None

def bfunc_2_c295(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRP'] is not None

def bfunc_2_c296(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRQ'] is not None

def bfunc_2_c297(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRQ'] is not None

def bfunc_2_c298(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRP'] - var_bindings['v1']['Nc3RSRP'] > 12

def bfunc_2_c299(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRQ'] >= var_bindings['v1']['Nc3RSRQ'] - 6

def bfunc_2_c3(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 1 <= var_bindings['v1']['NcSize']

def bfunc_2_c30(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 3 <= var_bindings['v2']['NcSize']

def bfunc_2_c300(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c301(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c302(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 3 <= var_bindings['v1']['NcSize']

def bfunc_2_c303(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 8 <= var_bindings['v2']['NcSize']

def bfunc_2_c304(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] is not None

def bfunc_2_c305(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8Cellid'] is not None

def bfunc_2_c306(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3Cellid'] == var_bindings['v2']['Nc8Cellid']

def bfunc_2_c307(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRP'] is not None

def bfunc_2_c308(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRP'] is not None

def bfunc_2_c309(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc3RSRQ'] is not None

def bfunc_2_c31(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] is not None

def bfunc_2_c310(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRQ'] is not None

def bfunc_2_c311(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRP'] - var_bindings['v1']['Nc3RSRP'] > 12

def bfunc_2_c312(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRQ'] >= var_bindings['v1']['Nc3RSRQ'] - 6

def bfunc_2_c313(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c314(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c315(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 4 <= var_bindings['v1']['NcSize']

def bfunc_2_c316(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 1 <= var_bindings['v2']['NcSize']

def bfunc_2_c317(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is not None

def bfunc_2_c318(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1Cellid'] is not None

def bfunc_2_c319(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] == var_bindings['v2']['Nc1Cellid']

def bfunc_2_c32(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3Cellid'] is not None

def bfunc_2_c320(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] is not None

def bfunc_2_c321(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRP'] is not None

def bfunc_2_c322(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRQ'] is not None

def bfunc_2_c323(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRQ'] is not None

def bfunc_2_c324(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRP'] - var_bindings['v1']['Nc4RSRP'] > 12

def bfunc_2_c325(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRQ'] >= var_bindings['v1']['Nc4RSRQ'] - 6

def bfunc_2_c326(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c327(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c328(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 4 <= var_bindings['v1']['NcSize']

def bfunc_2_c329(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 2 <= var_bindings['v2']['NcSize']

def bfunc_2_c33(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] == var_bindings['v2']['Nc3Cellid']

def bfunc_2_c330(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is not None

def bfunc_2_c331(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2Cellid'] is not None

def bfunc_2_c332(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] == var_bindings['v2']['Nc2Cellid']

def bfunc_2_c333(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] is not None

def bfunc_2_c334(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRP'] is not None

def bfunc_2_c335(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRQ'] is not None

def bfunc_2_c336(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRQ'] is not None

def bfunc_2_c337(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRP'] - var_bindings['v1']['Nc4RSRP'] > 12

def bfunc_2_c338(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRQ'] >= var_bindings['v1']['Nc4RSRQ'] - 6

def bfunc_2_c339(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c34(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] is not None

def bfunc_2_c340(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c341(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 4 <= var_bindings['v1']['NcSize']

def bfunc_2_c342(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 3 <= var_bindings['v2']['NcSize']

def bfunc_2_c343(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is not None

def bfunc_2_c344(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3Cellid'] is not None

def bfunc_2_c345(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] == var_bindings['v2']['Nc3Cellid']

def bfunc_2_c346(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] is not None

def bfunc_2_c347(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRP'] is not None

def bfunc_2_c348(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRQ'] is not None

def bfunc_2_c349(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRQ'] is not None

def bfunc_2_c35(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRP'] is not None

def bfunc_2_c350(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRP'] - var_bindings['v1']['Nc4RSRP'] > 12

def bfunc_2_c351(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRQ'] >= var_bindings['v1']['Nc4RSRQ'] - 6

def bfunc_2_c352(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c353(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c354(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 4 <= var_bindings['v1']['NcSize']

def bfunc_2_c355(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 4 <= var_bindings['v2']['NcSize']

def bfunc_2_c356(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is not None

def bfunc_2_c357(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4Cellid'] is not None

def bfunc_2_c358(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] == var_bindings['v2']['Nc4Cellid']

def bfunc_2_c359(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] is not None

def bfunc_2_c36(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRQ'] is not None

def bfunc_2_c360(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRP'] is not None

def bfunc_2_c361(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRQ'] is not None

def bfunc_2_c362(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRQ'] is not None

def bfunc_2_c363(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRP'] - var_bindings['v1']['Nc4RSRP'] > 12

def bfunc_2_c364(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRQ'] >= var_bindings['v1']['Nc4RSRQ'] - 6

def bfunc_2_c365(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c366(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c367(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 4 <= var_bindings['v1']['NcSize']

def bfunc_2_c368(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 5 <= var_bindings['v2']['NcSize']

def bfunc_2_c369(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is not None

def bfunc_2_c37(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRQ'] is not None

def bfunc_2_c370(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5Cellid'] is not None

def bfunc_2_c371(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] == var_bindings['v2']['Nc5Cellid']

def bfunc_2_c372(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] is not None

def bfunc_2_c373(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRP'] is not None

def bfunc_2_c374(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRQ'] is not None

def bfunc_2_c375(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRQ'] is not None

def bfunc_2_c376(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRP'] - var_bindings['v1']['Nc4RSRP'] > 12

def bfunc_2_c377(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRQ'] >= var_bindings['v1']['Nc4RSRQ'] - 6

def bfunc_2_c378(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c379(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c38(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRP'] - var_bindings['v1']['Nc1RSRP'] > 12

def bfunc_2_c380(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 4 <= var_bindings['v1']['NcSize']

def bfunc_2_c381(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 6 <= var_bindings['v2']['NcSize']

def bfunc_2_c382(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is not None

def bfunc_2_c383(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6Cellid'] is not None

def bfunc_2_c384(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] == var_bindings['v2']['Nc6Cellid']

def bfunc_2_c385(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] is not None

def bfunc_2_c386(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRP'] is not None

def bfunc_2_c387(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRQ'] is not None

def bfunc_2_c388(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRQ'] is not None

def bfunc_2_c389(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRP'] - var_bindings['v1']['Nc4RSRP'] > 12

def bfunc_2_c39(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRQ'] >= var_bindings['v1']['Nc1RSRQ'] - 6

def bfunc_2_c390(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRQ'] >= var_bindings['v1']['Nc4RSRQ'] - 6

def bfunc_2_c391(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c392(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c393(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 4 <= var_bindings['v1']['NcSize']

def bfunc_2_c394(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 7 <= var_bindings['v2']['NcSize']

def bfunc_2_c395(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is not None

def bfunc_2_c396(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7Cellid'] is not None

def bfunc_2_c397(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] == var_bindings['v2']['Nc7Cellid']

def bfunc_2_c398(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] is not None

def bfunc_2_c399(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRP'] is not None

def bfunc_2_c4(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 1 <= var_bindings['v2']['NcSize']

def bfunc_2_c40(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c400(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRQ'] is not None

def bfunc_2_c401(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRQ'] is not None

def bfunc_2_c402(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRP'] - var_bindings['v1']['Nc4RSRP'] > 12

def bfunc_2_c403(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRQ'] >= var_bindings['v1']['Nc4RSRQ'] - 6

def bfunc_2_c404(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c405(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c406(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 4 <= var_bindings['v1']['NcSize']

def bfunc_2_c407(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 8 <= var_bindings['v2']['NcSize']

def bfunc_2_c408(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] is not None

def bfunc_2_c409(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8Cellid'] is not None

def bfunc_2_c41(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c410(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4Cellid'] == var_bindings['v2']['Nc8Cellid']

def bfunc_2_c411(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRP'] is not None

def bfunc_2_c412(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRP'] is not None

def bfunc_2_c413(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc4RSRQ'] is not None

def bfunc_2_c414(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRQ'] is not None

def bfunc_2_c415(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRP'] - var_bindings['v1']['Nc4RSRP'] > 12

def bfunc_2_c416(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRQ'] >= var_bindings['v1']['Nc4RSRQ'] - 6

def bfunc_2_c417(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c418(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c419(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 5 <= var_bindings['v1']['NcSize']

def bfunc_2_c42(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 1 <= var_bindings['v1']['NcSize']

def bfunc_2_c420(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 1 <= var_bindings['v2']['NcSize']

def bfunc_2_c421(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is not None

def bfunc_2_c422(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1Cellid'] is not None

def bfunc_2_c423(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] == var_bindings['v2']['Nc1Cellid']

def bfunc_2_c424(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] is not None

def bfunc_2_c425(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRP'] is not None

def bfunc_2_c426(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRQ'] is not None

def bfunc_2_c427(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRQ'] is not None

def bfunc_2_c428(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRP'] - var_bindings['v1']['Nc5RSRP'] > 12

def bfunc_2_c429(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRQ'] >= var_bindings['v1']['Nc5RSRQ'] - 6

def bfunc_2_c43(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 4 <= var_bindings['v2']['NcSize']

def bfunc_2_c430(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c431(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c432(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 5 <= var_bindings['v1']['NcSize']

def bfunc_2_c433(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 2 <= var_bindings['v2']['NcSize']

def bfunc_2_c434(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is not None

def bfunc_2_c435(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2Cellid'] is not None

def bfunc_2_c436(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] == var_bindings['v2']['Nc2Cellid']

def bfunc_2_c437(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] is not None

def bfunc_2_c438(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRP'] is not None

def bfunc_2_c439(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRQ'] is not None

def bfunc_2_c44(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] is not None

def bfunc_2_c440(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRQ'] is not None

def bfunc_2_c441(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRP'] - var_bindings['v1']['Nc5RSRP'] > 12

def bfunc_2_c442(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRQ'] >= var_bindings['v1']['Nc5RSRQ'] - 6

def bfunc_2_c443(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c444(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c445(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 5 <= var_bindings['v1']['NcSize']

def bfunc_2_c446(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 3 <= var_bindings['v2']['NcSize']

def bfunc_2_c447(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is not None

def bfunc_2_c448(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3Cellid'] is not None

def bfunc_2_c449(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] == var_bindings['v2']['Nc3Cellid']

def bfunc_2_c45(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4Cellid'] is not None

def bfunc_2_c450(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] is not None

def bfunc_2_c451(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRP'] is not None

def bfunc_2_c452(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRQ'] is not None

def bfunc_2_c453(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRQ'] is not None

def bfunc_2_c454(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRP'] - var_bindings['v1']['Nc5RSRP'] > 12

def bfunc_2_c455(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRQ'] >= var_bindings['v1']['Nc5RSRQ'] - 6

def bfunc_2_c456(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c457(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c458(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 5 <= var_bindings['v1']['NcSize']

def bfunc_2_c459(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 4 <= var_bindings['v2']['NcSize']

def bfunc_2_c46(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] == var_bindings['v2']['Nc4Cellid']

def bfunc_2_c460(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is not None

def bfunc_2_c461(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4Cellid'] is not None

def bfunc_2_c462(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] == var_bindings['v2']['Nc4Cellid']

def bfunc_2_c463(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] is not None

def bfunc_2_c464(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRP'] is not None

def bfunc_2_c465(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRQ'] is not None

def bfunc_2_c466(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRQ'] is not None

def bfunc_2_c467(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRP'] - var_bindings['v1']['Nc5RSRP'] > 12

def bfunc_2_c468(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRQ'] >= var_bindings['v1']['Nc5RSRQ'] - 6

def bfunc_2_c469(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c47(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] is not None

def bfunc_2_c470(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c471(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 5 <= var_bindings['v1']['NcSize']

def bfunc_2_c472(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 5 <= var_bindings['v2']['NcSize']

def bfunc_2_c473(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is not None

def bfunc_2_c474(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5Cellid'] is not None

def bfunc_2_c475(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] == var_bindings['v2']['Nc5Cellid']

def bfunc_2_c476(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] is not None

def bfunc_2_c477(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRP'] is not None

def bfunc_2_c478(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRQ'] is not None

def bfunc_2_c479(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRQ'] is not None

def bfunc_2_c48(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRP'] is not None

def bfunc_2_c480(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRP'] - var_bindings['v1']['Nc5RSRP'] > 12

def bfunc_2_c481(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRQ'] >= var_bindings['v1']['Nc5RSRQ'] - 6

def bfunc_2_c482(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c483(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c484(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 5 <= var_bindings['v1']['NcSize']

def bfunc_2_c485(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 6 <= var_bindings['v2']['NcSize']

def bfunc_2_c486(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is not None

def bfunc_2_c487(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6Cellid'] is not None

def bfunc_2_c488(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] == var_bindings['v2']['Nc6Cellid']

def bfunc_2_c489(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] is not None

def bfunc_2_c49(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRQ'] is not None

def bfunc_2_c490(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRP'] is not None

def bfunc_2_c491(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRQ'] is not None

def bfunc_2_c492(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRQ'] is not None

def bfunc_2_c493(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRP'] - var_bindings['v1']['Nc5RSRP'] > 12

def bfunc_2_c494(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRQ'] >= var_bindings['v1']['Nc5RSRQ'] - 6

def bfunc_2_c495(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c496(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c497(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 5 <= var_bindings['v1']['NcSize']

def bfunc_2_c498(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 7 <= var_bindings['v2']['NcSize']

def bfunc_2_c499(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is not None

def bfunc_2_c5(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] is not None

def bfunc_2_c50(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRQ'] is not None

def bfunc_2_c500(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7Cellid'] is not None

def bfunc_2_c501(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] == var_bindings['v2']['Nc7Cellid']

def bfunc_2_c502(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] is not None

def bfunc_2_c503(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRP'] is not None

def bfunc_2_c504(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRQ'] is not None

def bfunc_2_c505(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRQ'] is not None

def bfunc_2_c506(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRP'] - var_bindings['v1']['Nc5RSRP'] > 12

def bfunc_2_c507(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRQ'] >= var_bindings['v1']['Nc5RSRQ'] - 6

def bfunc_2_c508(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c509(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c51(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRP'] - var_bindings['v1']['Nc1RSRP'] > 12

def bfunc_2_c510(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 5 <= var_bindings['v1']['NcSize']

def bfunc_2_c511(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 8 <= var_bindings['v2']['NcSize']

def bfunc_2_c512(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] is not None

def bfunc_2_c513(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8Cellid'] is not None

def bfunc_2_c514(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5Cellid'] == var_bindings['v2']['Nc8Cellid']

def bfunc_2_c515(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRP'] is not None

def bfunc_2_c516(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRP'] is not None

def bfunc_2_c517(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc5RSRQ'] is not None

def bfunc_2_c518(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRQ'] is not None

def bfunc_2_c519(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRP'] - var_bindings['v1']['Nc5RSRP'] > 12

def bfunc_2_c52(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRQ'] >= var_bindings['v1']['Nc1RSRQ'] - 6

def bfunc_2_c520(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRQ'] >= var_bindings['v1']['Nc5RSRQ'] - 6

def bfunc_2_c521(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c522(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c523(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 6 <= var_bindings['v1']['NcSize']

def bfunc_2_c524(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 1 <= var_bindings['v2']['NcSize']

def bfunc_2_c525(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is not None

def bfunc_2_c526(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1Cellid'] is not None

def bfunc_2_c527(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] == var_bindings['v2']['Nc1Cellid']

def bfunc_2_c528(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] is not None

def bfunc_2_c529(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRP'] is not None

def bfunc_2_c53(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c530(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRQ'] is not None

def bfunc_2_c531(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRQ'] is not None

def bfunc_2_c532(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRP'] - var_bindings['v1']['Nc6RSRP'] > 12

def bfunc_2_c533(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRQ'] >= var_bindings['v1']['Nc6RSRQ'] - 6

def bfunc_2_c534(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c535(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c536(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 6 <= var_bindings['v1']['NcSize']

def bfunc_2_c537(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 2 <= var_bindings['v2']['NcSize']

def bfunc_2_c538(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is not None

def bfunc_2_c539(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2Cellid'] is not None

def bfunc_2_c54(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c540(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] == var_bindings['v2']['Nc2Cellid']

def bfunc_2_c541(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] is not None

def bfunc_2_c542(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRP'] is not None

def bfunc_2_c543(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRQ'] is not None

def bfunc_2_c544(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRQ'] is not None

def bfunc_2_c545(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRP'] - var_bindings['v1']['Nc6RSRP'] > 12

def bfunc_2_c546(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRQ'] >= var_bindings['v1']['Nc6RSRQ'] - 6

def bfunc_2_c547(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c548(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c549(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 6 <= var_bindings['v1']['NcSize']

def bfunc_2_c55(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 1 <= var_bindings['v1']['NcSize']

def bfunc_2_c550(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 3 <= var_bindings['v2']['NcSize']

def bfunc_2_c551(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is not None

def bfunc_2_c552(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3Cellid'] is not None

def bfunc_2_c553(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] == var_bindings['v2']['Nc3Cellid']

def bfunc_2_c554(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] is not None

def bfunc_2_c555(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRP'] is not None

def bfunc_2_c556(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRQ'] is not None

def bfunc_2_c557(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRQ'] is not None

def bfunc_2_c558(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRP'] - var_bindings['v1']['Nc6RSRP'] > 12

def bfunc_2_c559(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRQ'] >= var_bindings['v1']['Nc6RSRQ'] - 6

def bfunc_2_c56(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 5 <= var_bindings['v2']['NcSize']

def bfunc_2_c560(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c561(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c562(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 6 <= var_bindings['v1']['NcSize']

def bfunc_2_c563(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 4 <= var_bindings['v2']['NcSize']

def bfunc_2_c564(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is not None

def bfunc_2_c565(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4Cellid'] is not None

def bfunc_2_c566(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] == var_bindings['v2']['Nc4Cellid']

def bfunc_2_c567(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] is not None

def bfunc_2_c568(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRP'] is not None

def bfunc_2_c569(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRQ'] is not None

def bfunc_2_c57(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] is not None

def bfunc_2_c570(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRQ'] is not None

def bfunc_2_c571(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRP'] - var_bindings['v1']['Nc6RSRP'] > 12

def bfunc_2_c572(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRQ'] >= var_bindings['v1']['Nc6RSRQ'] - 6

def bfunc_2_c573(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c574(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c575(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 6 <= var_bindings['v1']['NcSize']

def bfunc_2_c576(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 5 <= var_bindings['v2']['NcSize']

def bfunc_2_c577(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is not None

def bfunc_2_c578(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5Cellid'] is not None

def bfunc_2_c579(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] == var_bindings['v2']['Nc5Cellid']

def bfunc_2_c58(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5Cellid'] is not None

def bfunc_2_c580(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] is not None

def bfunc_2_c581(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRP'] is not None

def bfunc_2_c582(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRQ'] is not None

def bfunc_2_c583(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRQ'] is not None

def bfunc_2_c584(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRP'] - var_bindings['v1']['Nc6RSRP'] > 12

def bfunc_2_c585(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRQ'] >= var_bindings['v1']['Nc6RSRQ'] - 6

def bfunc_2_c586(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c587(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c588(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 6 <= var_bindings['v1']['NcSize']

def bfunc_2_c589(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 6 <= var_bindings['v2']['NcSize']

def bfunc_2_c59(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] == var_bindings['v2']['Nc5Cellid']

def bfunc_2_c590(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is not None

def bfunc_2_c591(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6Cellid'] is not None

def bfunc_2_c592(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] == var_bindings['v2']['Nc6Cellid']

def bfunc_2_c593(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] is not None

def bfunc_2_c594(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRP'] is not None

def bfunc_2_c595(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRQ'] is not None

def bfunc_2_c596(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRQ'] is not None

def bfunc_2_c597(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRP'] - var_bindings['v1']['Nc6RSRP'] > 12

def bfunc_2_c598(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRQ'] >= var_bindings['v1']['Nc6RSRQ'] - 6

def bfunc_2_c599(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c6(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1Cellid'] is not None

def bfunc_2_c60(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] is not None

def bfunc_2_c600(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c601(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 6 <= var_bindings['v1']['NcSize']

def bfunc_2_c602(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 7 <= var_bindings['v2']['NcSize']

def bfunc_2_c603(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is not None

def bfunc_2_c604(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7Cellid'] is not None

def bfunc_2_c605(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] == var_bindings['v2']['Nc7Cellid']

def bfunc_2_c606(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] is not None

def bfunc_2_c607(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRP'] is not None

def bfunc_2_c608(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRQ'] is not None

def bfunc_2_c609(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRQ'] is not None

def bfunc_2_c61(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRP'] is not None

def bfunc_2_c610(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRP'] - var_bindings['v1']['Nc6RSRP'] > 12

def bfunc_2_c611(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRQ'] >= var_bindings['v1']['Nc6RSRQ'] - 6

def bfunc_2_c612(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c613(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c614(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 6 <= var_bindings['v1']['NcSize']

def bfunc_2_c615(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 8 <= var_bindings['v2']['NcSize']

def bfunc_2_c616(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] is not None

def bfunc_2_c617(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8Cellid'] is not None

def bfunc_2_c618(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6Cellid'] == var_bindings['v2']['Nc8Cellid']

def bfunc_2_c619(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRP'] is not None

def bfunc_2_c62(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRQ'] is not None

def bfunc_2_c620(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRP'] is not None

def bfunc_2_c621(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc6RSRQ'] is not None

def bfunc_2_c622(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRQ'] is not None

def bfunc_2_c623(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRP'] - var_bindings['v1']['Nc6RSRP'] > 12

def bfunc_2_c624(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRQ'] >= var_bindings['v1']['Nc6RSRQ'] - 6

def bfunc_2_c625(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c626(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c627(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 7 <= var_bindings['v1']['NcSize']

def bfunc_2_c628(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 1 <= var_bindings['v2']['NcSize']

def bfunc_2_c629(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is not None

def bfunc_2_c63(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRQ'] is not None

def bfunc_2_c630(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1Cellid'] is not None

def bfunc_2_c631(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] == var_bindings['v2']['Nc1Cellid']

def bfunc_2_c632(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] is not None

def bfunc_2_c633(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRP'] is not None

def bfunc_2_c634(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRQ'] is not None

def bfunc_2_c635(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRQ'] is not None

def bfunc_2_c636(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRP'] - var_bindings['v1']['Nc7RSRP'] > 12

def bfunc_2_c637(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRQ'] >= var_bindings['v1']['Nc7RSRQ'] - 6

def bfunc_2_c638(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c639(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c64(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRP'] - var_bindings['v1']['Nc1RSRP'] > 12

def bfunc_2_c640(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 7 <= var_bindings['v1']['NcSize']

def bfunc_2_c641(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 2 <= var_bindings['v2']['NcSize']

def bfunc_2_c642(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is not None

def bfunc_2_c643(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2Cellid'] is not None

def bfunc_2_c644(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] == var_bindings['v2']['Nc2Cellid']

def bfunc_2_c645(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] is not None

def bfunc_2_c646(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRP'] is not None

def bfunc_2_c647(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRQ'] is not None

def bfunc_2_c648(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRQ'] is not None

def bfunc_2_c649(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRP'] - var_bindings['v1']['Nc7RSRP'] > 12

def bfunc_2_c65(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRQ'] >= var_bindings['v1']['Nc1RSRQ'] - 6

def bfunc_2_c650(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRQ'] >= var_bindings['v1']['Nc7RSRQ'] - 6

def bfunc_2_c651(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c652(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c653(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 7 <= var_bindings['v1']['NcSize']

def bfunc_2_c654(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 3 <= var_bindings['v2']['NcSize']

def bfunc_2_c655(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is not None

def bfunc_2_c656(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3Cellid'] is not None

def bfunc_2_c657(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] == var_bindings['v2']['Nc3Cellid']

def bfunc_2_c658(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] is not None

def bfunc_2_c659(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRP'] is not None

def bfunc_2_c66(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c660(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRQ'] is not None

def bfunc_2_c661(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRQ'] is not None

def bfunc_2_c662(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRP'] - var_bindings['v1']['Nc7RSRP'] > 12

def bfunc_2_c663(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRQ'] >= var_bindings['v1']['Nc7RSRQ'] - 6

def bfunc_2_c664(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c665(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c666(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 7 <= var_bindings['v1']['NcSize']

def bfunc_2_c667(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 4 <= var_bindings['v2']['NcSize']

def bfunc_2_c668(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is not None

def bfunc_2_c669(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4Cellid'] is not None

def bfunc_2_c67(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c670(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] == var_bindings['v2']['Nc4Cellid']

def bfunc_2_c671(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] is not None

def bfunc_2_c672(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRP'] is not None

def bfunc_2_c673(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRQ'] is not None

def bfunc_2_c674(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRQ'] is not None

def bfunc_2_c675(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRP'] - var_bindings['v1']['Nc7RSRP'] > 12

def bfunc_2_c676(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRQ'] >= var_bindings['v1']['Nc7RSRQ'] - 6

def bfunc_2_c677(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c678(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c679(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 7 <= var_bindings['v1']['NcSize']

def bfunc_2_c68(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 1 <= var_bindings['v1']['NcSize']

def bfunc_2_c680(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 5 <= var_bindings['v2']['NcSize']

def bfunc_2_c681(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is not None

def bfunc_2_c682(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5Cellid'] is not None

def bfunc_2_c683(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] == var_bindings['v2']['Nc5Cellid']

def bfunc_2_c684(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] is not None

def bfunc_2_c685(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRP'] is not None

def bfunc_2_c686(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRQ'] is not None

def bfunc_2_c687(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRQ'] is not None

def bfunc_2_c688(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRP'] - var_bindings['v1']['Nc7RSRP'] > 12

def bfunc_2_c689(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRQ'] >= var_bindings['v1']['Nc7RSRQ'] - 6

def bfunc_2_c69(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 6 <= var_bindings['v2']['NcSize']

def bfunc_2_c690(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c691(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c692(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 7 <= var_bindings['v1']['NcSize']

def bfunc_2_c693(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 6 <= var_bindings['v2']['NcSize']

def bfunc_2_c694(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is not None

def bfunc_2_c695(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6Cellid'] is not None

def bfunc_2_c696(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] == var_bindings['v2']['Nc6Cellid']

def bfunc_2_c697(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] is not None

def bfunc_2_c698(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRP'] is not None

def bfunc_2_c699(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRQ'] is not None

def bfunc_2_c7(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] == var_bindings['v2']['Nc1Cellid']

def bfunc_2_c70(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] is not None

def bfunc_2_c700(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRQ'] is not None

def bfunc_2_c701(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRP'] - var_bindings['v1']['Nc7RSRP'] > 12

def bfunc_2_c702(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRQ'] >= var_bindings['v1']['Nc7RSRQ'] - 6

def bfunc_2_c703(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c704(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c705(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 7 <= var_bindings['v1']['NcSize']

def bfunc_2_c706(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 7 <= var_bindings['v2']['NcSize']

def bfunc_2_c707(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is not None

def bfunc_2_c708(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7Cellid'] is not None

def bfunc_2_c709(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] == var_bindings['v2']['Nc7Cellid']

def bfunc_2_c71(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6Cellid'] is not None

def bfunc_2_c710(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] is not None

def bfunc_2_c711(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRP'] is not None

def bfunc_2_c712(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRQ'] is not None

def bfunc_2_c713(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRQ'] is not None

def bfunc_2_c714(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRP'] - var_bindings['v1']['Nc7RSRP'] > 12

def bfunc_2_c715(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRQ'] >= var_bindings['v1']['Nc7RSRQ'] - 6

def bfunc_2_c716(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c717(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c718(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 7 <= var_bindings['v1']['NcSize']

def bfunc_2_c719(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 8 <= var_bindings['v2']['NcSize']

def bfunc_2_c72(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] == var_bindings['v2']['Nc6Cellid']

def bfunc_2_c720(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] is not None

def bfunc_2_c721(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8Cellid'] is not None

def bfunc_2_c722(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7Cellid'] == var_bindings['v2']['Nc8Cellid']

def bfunc_2_c723(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRP'] is not None

def bfunc_2_c724(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRP'] is not None

def bfunc_2_c725(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc7RSRQ'] is not None

def bfunc_2_c726(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRQ'] is not None

def bfunc_2_c727(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRP'] - var_bindings['v1']['Nc7RSRP'] > 12

def bfunc_2_c728(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRQ'] >= var_bindings['v1']['Nc7RSRQ'] - 6

def bfunc_2_c729(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c73(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] is not None

def bfunc_2_c730(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c731(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 8 <= var_bindings['v1']['NcSize']

def bfunc_2_c732(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 1 <= var_bindings['v2']['NcSize']

def bfunc_2_c733(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is not None

def bfunc_2_c734(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1Cellid'] is not None

def bfunc_2_c735(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] == var_bindings['v2']['Nc1Cellid']

def bfunc_2_c736(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] is not None

def bfunc_2_c737(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRP'] is not None

def bfunc_2_c738(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRQ'] is not None

def bfunc_2_c739(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRQ'] is not None

def bfunc_2_c74(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRP'] is not None

def bfunc_2_c740(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRP'] - var_bindings['v1']['Nc8RSRP'] > 12

def bfunc_2_c741(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRQ'] >= var_bindings['v1']['Nc8RSRQ'] - 6

def bfunc_2_c742(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c743(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c744(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 8 <= var_bindings['v1']['NcSize']

def bfunc_2_c745(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 2 <= var_bindings['v2']['NcSize']

def bfunc_2_c746(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is not None

def bfunc_2_c747(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2Cellid'] is not None

def bfunc_2_c748(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] == var_bindings['v2']['Nc2Cellid']

def bfunc_2_c749(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] is not None

def bfunc_2_c75(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRQ'] is not None

def bfunc_2_c750(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRP'] is not None

def bfunc_2_c751(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRQ'] is not None

def bfunc_2_c752(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRQ'] is not None

def bfunc_2_c753(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRP'] - var_bindings['v1']['Nc8RSRP'] > 12

def bfunc_2_c754(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc2RSRQ'] >= var_bindings['v1']['Nc8RSRQ'] - 6

def bfunc_2_c755(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c756(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c757(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 8 <= var_bindings['v1']['NcSize']

def bfunc_2_c758(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 3 <= var_bindings['v2']['NcSize']

def bfunc_2_c759(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is not None

def bfunc_2_c76(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRQ'] is not None

def bfunc_2_c760(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3Cellid'] is not None

def bfunc_2_c761(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] == var_bindings['v2']['Nc3Cellid']

def bfunc_2_c762(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] is not None

def bfunc_2_c763(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRP'] is not None

def bfunc_2_c764(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRQ'] is not None

def bfunc_2_c765(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRQ'] is not None

def bfunc_2_c766(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRP'] - var_bindings['v1']['Nc8RSRP'] > 12

def bfunc_2_c767(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc3RSRQ'] >= var_bindings['v1']['Nc8RSRQ'] - 6

def bfunc_2_c768(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c769(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c77(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRP'] - var_bindings['v1']['Nc1RSRP'] > 12

def bfunc_2_c770(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 8 <= var_bindings['v1']['NcSize']

def bfunc_2_c771(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 4 <= var_bindings['v2']['NcSize']

def bfunc_2_c772(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is not None

def bfunc_2_c773(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4Cellid'] is not None

def bfunc_2_c774(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] == var_bindings['v2']['Nc4Cellid']

def bfunc_2_c775(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] is not None

def bfunc_2_c776(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRP'] is not None

def bfunc_2_c777(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRQ'] is not None

def bfunc_2_c778(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRQ'] is not None

def bfunc_2_c779(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRP'] - var_bindings['v1']['Nc8RSRP'] > 12

def bfunc_2_c78(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRQ'] >= var_bindings['v1']['Nc1RSRQ'] - 6

def bfunc_2_c780(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc4RSRQ'] >= var_bindings['v1']['Nc8RSRQ'] - 6

def bfunc_2_c781(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c782(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c783(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 8 <= var_bindings['v1']['NcSize']

def bfunc_2_c784(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 5 <= var_bindings['v2']['NcSize']

def bfunc_2_c785(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is not None

def bfunc_2_c786(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5Cellid'] is not None

def bfunc_2_c787(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] == var_bindings['v2']['Nc5Cellid']

def bfunc_2_c788(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] is not None

def bfunc_2_c789(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRP'] is not None

def bfunc_2_c79(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c790(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRQ'] is not None

def bfunc_2_c791(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRQ'] is not None

def bfunc_2_c792(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRP'] - var_bindings['v1']['Nc8RSRP'] > 12

def bfunc_2_c793(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc5RSRQ'] >= var_bindings['v1']['Nc8RSRQ'] - 6

def bfunc_2_c794(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c795(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c796(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 8 <= var_bindings['v1']['NcSize']

def bfunc_2_c797(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 6 <= var_bindings['v2']['NcSize']

def bfunc_2_c798(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is not None

def bfunc_2_c799(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6Cellid'] is not None

def bfunc_2_c8(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] is not None

def bfunc_2_c80(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c800(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] == var_bindings['v2']['Nc6Cellid']

def bfunc_2_c801(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] is not None

def bfunc_2_c802(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRP'] is not None

def bfunc_2_c803(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRQ'] is not None

def bfunc_2_c804(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRQ'] is not None

def bfunc_2_c805(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRP'] - var_bindings['v1']['Nc8RSRP'] > 12

def bfunc_2_c806(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc6RSRQ'] >= var_bindings['v1']['Nc8RSRQ'] - 6

def bfunc_2_c807(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c808(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c809(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 8 <= var_bindings['v1']['NcSize']

def bfunc_2_c81(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 1 <= var_bindings['v1']['NcSize']

def bfunc_2_c810(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 7 <= var_bindings['v2']['NcSize']

def bfunc_2_c811(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is not None

def bfunc_2_c812(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7Cellid'] is not None

def bfunc_2_c813(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] == var_bindings['v2']['Nc7Cellid']

def bfunc_2_c814(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] is not None

def bfunc_2_c815(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRP'] is not None

def bfunc_2_c816(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRQ'] is not None

def bfunc_2_c817(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRQ'] is not None

def bfunc_2_c818(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRP'] - var_bindings['v1']['Nc8RSRP'] > 12

def bfunc_2_c819(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRQ'] >= var_bindings['v1']['Nc8RSRQ'] - 6

def bfunc_2_c82(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 7 <= var_bindings['v2']['NcSize']

def bfunc_2_c820(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c821(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c822(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 8 <= var_bindings['v1']['NcSize']

def bfunc_2_c823(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 8 <= var_bindings['v2']['NcSize']

def bfunc_2_c824(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] is not None

def bfunc_2_c825(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8Cellid'] is not None

def bfunc_2_c826(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8Cellid'] == var_bindings['v2']['Nc8Cellid']

def bfunc_2_c827(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRP'] is not None

def bfunc_2_c828(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRP'] is not None

def bfunc_2_c829(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc8RSRQ'] is not None

def bfunc_2_c83(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] is not None

def bfunc_2_c830(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRQ'] is not None

def bfunc_2_c831(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRP'] - var_bindings['v1']['Nc8RSRP'] > 12

def bfunc_2_c832(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8RSRQ'] >= var_bindings['v1']['Nc8RSRQ'] - 6

def bfunc_2_c84(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7Cellid'] is not None

def bfunc_2_c85(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] == var_bindings['v2']['Nc7Cellid']

def bfunc_2_c86(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] is not None

def bfunc_2_c87(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRP'] is not None

def bfunc_2_c88(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRQ'] is not None

def bfunc_2_c89(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRQ'] is not None

def bfunc_2_c9(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc1RSRP'] is not None

def bfunc_2_c90(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRP'] - var_bindings['v1']['Nc1RSRP'] > 12

def bfunc_2_c91(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc7RSRQ'] >= var_bindings['v1']['Nc1RSRQ'] - 6

def bfunc_2_c92(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['NcSize'] is not None

def bfunc_2_c93(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['NcSize'] is not None

def bfunc_2_c94(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 1 <= var_bindings['v1']['NcSize']

def bfunc_2_c95(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 8 <= var_bindings['v2']['NcSize']

def bfunc_2_c96(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] is not None

def bfunc_2_c97(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['Nc8Cellid'] is not None

def bfunc_2_c98(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1Cellid'] == var_bindings['v2']['Nc8Cellid']

def bfunc_2_c99(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['Nc1RSRP'] is not None

