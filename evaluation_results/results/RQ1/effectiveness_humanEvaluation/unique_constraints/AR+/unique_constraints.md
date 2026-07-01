# Unique Constraints (AR+ RQ1)

There are **182** unique constraints collected from 5 experiments.

| # | Constraints (Representative / Duplicates) | Semantics |
|---|-------------------------------------------|-----------|
| 1 | `1_constraint_1` | For any record v1 in the dataset, v1.latitude is greater than abs(abs(add(div(v1.speed, v1.speed), log(v1.timestamp)))). |
| 2 | `1_constraint_2` | For any two records v1 and v2 that belong to the same vehicle (same carid), v1.speed is greater than or equal to div(cos(cos(tan(tan(sin(-43399.820))))), v2.timestamp). |
| 3 | `1_constraint_3` | For any two records v1 and v2 in the dataset, v1.timestamp is less than or equal to sub(sub(sub(add(v2.speed, v2.timestamp), div(v2.latitude, v2.longitude)), abs(max(-20974.037, v1.direction))), min(sin(max(v1.latitude, v1.speed)), neg(sub(59485.027, v2.longitude)))). |
| 4 | `1_constraint_4` | For any two records v1 and v2 in the dataset, v1.longitude is greater than or equal to mul(v2.latitude, sqrt(neg(neg(v2.latitude)))). |
| 5 | `1_constraint_5` | For any two records v1 and v2 in the dataset, v1.latitude is greater than log(v1.timestamp). |
| 6 | `1_constraint_6` | For any two records v1 and v2 that belong to the same vehicle (same carid), v2.timestamp is greater than or equal to sub(add(-41897.049, v1.timestamp), neg(v1.speed)). |
| 7 | `1_constraint_8` | For any record v1 in the dataset, v1.longitude is less than or equal to max(sin(v1.speed), sqrt(-13228.913)). |
| 8 | `1_constraint_9` | For any two records v1 and v2 that belong to the same vehicle (same carid), v2.direction is equal to div(div(v1.latitude, v2.longitude), v1.timestamp). |
| 9 | `1_constraint_10` | For any record v1 in the dataset, v1.timestamp is less than or equal to mul(add(39335.904, v1.speed), max(v1.longitude, 35282.976)). |
| 10 | `1_constraint_11` | For any two records v1 and v2 that belong to different vehicles (different carid values), v1.longitude is greater than or equal to sqrt(add(-11868.862, v2.speed)). |
| 11 | `1_constraint_12` | For any record v1 in the dataset, v1.longitude is less than sqrt(abs(13250.688)). |
| 12 | `1_constraint_13` | For any two records v1 and v2 that belong to different vehicles (different carid values), v2.latitude is less than or equal to add(cos(49981.560), v1.latitude). |
| 13 | `1_constraint_16` | For any two records v1 and v2 in the dataset, v1.timestamp is greater than or equal to add(add(-35262.478, v2.timestamp), v2.longitude). |
| 14 | `1_constraint_17` | For any record v1 in the dataset, v1.latitude is less than min(sqrt(div(neg(sub(-62823.006, v1.speed)), abs(v1.longitude))), max(v1.longitude, sin(sqrt(sub(v1.longitude, v1.timestamp))))). |
| 15 | `1_constraint_18` | For any two records v1 and v2 that belong to the same vehicle (same carid), v2.latitude is greater than or equal to max(add(log(v1.timestamp), sin(sub(cos(v2.direction), abs(v2.speed)))), tan(tan(min(v2.longitude, cos(neg(v2.longitude)))))). |
| 16 | `1_constraint_19` | For any two records v1 and v2 that belong to the same vehicle (same carid), v2.direction is less than or equal to div(log(sqrt(sqrt(v1.longitude))), v1.timestamp). |
| 17 | `1_constraint_20` | For any record v1 in the dataset, v1.direction is less than or equal to div(sqrt(tan(log(v1.timestamp))), v1.timestamp). |
| 18 | `1_constraint_22` | For any two records v1 and v2 that belong to the same vehicle (same carid), v2.direction is equal to div(div(v1.longitude, mul(tan(div(v1.timestamp, v2.timestamp)), v1.timestamp)), v1.longitude). |
| 19 | `1_constraint_23` | For any record v1 in the dataset, v1.longitude is less than abs(sqrt(abs(add(abs(-13462.654), add(v1.speed, v1.speed))))). |
| 20 | `1_constraint_24` | For any two records v1 and v2 in the dataset, v2.latitude is greater than log(max(v1.timestamp, v2.timestamp)). |
| 21 | `1_constraint_26` | For any two records v1 and v2 that belong to the same vehicle (same carid), v2.timestamp is less than or equal to abs(add(max(max(v2.direction, v1.speed), v1.timestamp), 53832.797)). |
| 22 | `1_constraint_27` | For any two records v1 and v2 that belong to different vehicles (different carid values), v1.timestamp is greater than add(add(log(sin(sub(v2.timestamp, v1.latitude))), cos(div(mul(v1.speed, v2.longitude), sqrt(v1.longitude)))), sub(add(sub(sqrt(v1.speed), neg(v2.timestamp)), neg(log(v2.speed))), mul(max(abs(v1.direction), v1.longitude), max(max(v2.latitude, v1.speed), max(v1.speed, v1.latitude))))). |
| 23 | `1_constraint_28` | For any record v1 in the dataset, v1.speed is greater than div(sin(-13888.256), v1.timestamp). |
| 24 | `1_constraint_30` | For any two records v1 and v2 that belong to the same vehicle (same carid), v2.longitude is greater than or equal to mul(abs(abs(v2.latitude)), sqrt(abs(v2.latitude))). |
| 25 | `1_constraint_34` | For any two records v1 and v2 in the dataset, v2.longitude is greater than sub(abs(sub(log(v2.timestamp), v1.longitude)), mul(v2.latitude, sin(cos(v2.latitude)))). |
| 26 | `1_constraint_36` | For any record v1 in the dataset, v1.speed is less than div(sqrt(sqrt(tan(-52460.223))), v1.timestamp). |
| 27 | `1_constraint_37` | For any record v1 in the dataset, v1.direction is less than or equal to div(tan(-48875.972), v1.timestamp). |
| 28 | `1_constraint_40` | For any two records v1 and v2 in the dataset, v2.latitude is less than or equal to sub(v1.latitude, sin(sqrt(v1.latitude))). |
| 29 | `1_constraint_41` | For any record v1 in the dataset, v1.direction is less than div(log(sqrt(tan(25505.093))), v1.timestamp). |
| 30 | `1_constraint_45` | For any two records v1 and v2 that belong to different vehicles (different carid values), v1.longitude is less than or equal to add(v2.longitude, sqrt(v2.latitude)). |
| 31 | `1_constraint_46` | For any two records v1 and v2 in the dataset, v1.longitude is greater than add(v1.latitude, mul(add(log(v1.latitude), add(log(v1.latitude), abs(v1.latitude))), log(v2.latitude))). |
| 32 | `1_constraint_47` | For any two records v1 and v2 in the dataset, v2.timestamp is less than abs(add(v1.timestamp, 25022.633)). |
| 33 | `1_constraint_48` | For any record v1 in the dataset, v1.latitude is greater than or equal to add(abs(log(v1.timestamp)), sqrt(sin(-41164.717))). |
| 34 | `1_constraint_50` | For any record v1 in the dataset, v1.direction is greater than or equal to div(sqrt(tan(15867.784)), v1.timestamp). |
| 35 | `2_constraint_1` | For any two records v1 and v2 that belong to different vehicles (different carid values), v1.longitude is greater than min(neg(sub(add(v1.speed, v2.latitude), log(v2.timestamp))), abs(tan(sqrt(v2.longitude)))). |
| 36 | `2_constraint_2` | For any two records v1 and v2 in the dataset, v2.latitude is less than sqrt(abs(mul(neg(tan(v1.latitude)), add(add(v2.timestamp, v1.latitude), add(v1.timestamp, v2.timestamp))))). |
| 37 | `2_constraint_3` | For any two records v1 and v2 that belong to different vehicles (different carid values), v2.latitude is greater than or equal to sin(v2.speed). |
| 38 | `2_constraint_4` | For any two records v1 and v2 that belong to different vehicles (different carid values), v2.longitude is greater than or equal to cos(v1.direction). |
| 39 | `2_constraint_5` | For any two records v1 and v2 that belong to the same vehicle (same carid), v2.direction is greater than add(cos(v1.longitude), neg(v2.latitude)). |
| 40 | `2_constraint_7` | For any two records v1 and v2 that belong to the same vehicle (same carid), v1.speed is less than or equal to sub(mul(abs(cos(v1.timestamp)), abs(mul(v2.latitude, v1.timestamp))), tan(sin(neg(v2.speed)))). |
| 41 | `2_constraint_8` | For any two records v1 and v2 in the dataset, v2.timestamp is greater than or equal to neg(log(tan(add(-24318.082, v1.longitude)))). |
| 42 | `2_constraint_9` | For any record v1 in the dataset, v1.timestamp is less than mul(add(cos(cos(sin(v1.longitude))), max(abs(add(v1.latitude, 47225.525)), max(cos(21518.318), cos(v1.longitude)))), add(sin(log(mul(42094.010, v1.latitude))), abs(sub(max(56641.424, v1.latitude), max(v1.latitude, 2615.879))))). |
| 43 | `2_constraint_10` | For any two records v1 and v2 that belong to different vehicles (different carid values), v2.longitude is greater than or equal to cos(log(div(v1.speed, v2.direction))). |
| 44 | `2_constraint_13` | For any record v1 in the dataset, v1.timestamp is less than or equal to add(mul(mul(-34115.753, abs(42127.481)), sub(cos(v1.speed), v1.latitude)), abs(log(tan(v1.longitude)))). |
| 45 | `2_constraint_14` | For any two records v1 and v2 that belong to the same vehicle (same carid), v1.latitude is greater than min(cos(max(mul(v1.longitude, 50428.911), min(v2.timestamp, -6547.244))), neg(neg(div(v1.longitude, v2.longitude)))). |
| 46 | `2_constraint_15` | For any record v1 in the dataset, v1.speed is greater than mul(max(v1.timestamp, v1.latitude), add(-61079.604, 2972.119)). |
| 47 | `2_constraint_16` | For any record v1 in the dataset, v1.timestamp is less than or equal to mul(abs(sub(sub(log(v1.speed), max(v1.direction, 27122.143)), sin(div(-60777.944, v1.speed)))), 62277.704). |
| 48 | `2_constraint_17` | For any two records v1 and v2 that belong to different vehicles (different carid values), v1.longitude is less than or equal to sub(v2.latitude, mul(v1.latitude, min(neg(v2.timestamp), max(mul(v2.timestamp, -56770.299), add(v1.direction, v2.direction))))). |
| 49 | `2_constraint_19` | For any record v1 in the dataset, v1.timestamp is greater than min(log(sqrt(abs(add(neg(v1.speed), mul(-11189.766, 2442.834))))), cos(v1.direction)). |
| 50 | `2_constraint_20` | For any record v1 in the dataset, v1.latitude is less than or equal to min(max(v1.timestamp, sub(v1.timestamp, v1.speed)), add(tan(v1.timestamp), sqrt(v1.timestamp))). |
| 51 | `2_constraint_21` | For any record v1 in the dataset, v1.latitude is less than or equal to add(v1.timestamp, v1.timestamp). |
| 52 | `2_constraint_22` | For any record v1 in the dataset, v1.direction is less than mul(max(max(sqrt(v1.timestamp), min(v1.timestamp, v1.longitude)), sin(mul(-4063.008, v1.latitude))), max(mul(abs(v1.longitude), sqrt(-55948.692)), cos(min(v1.timestamp, -39810.622)))). |
| 53 | `2_constraint_23` | For any record v1 in the dataset, v1.latitude is less than add(tan(mul(min(sub(v1.timestamp, v1.longitude), log(v1.timestamp)), abs(v1.speed))), v1.timestamp). |
| 54 | `2_constraint_24` | For any two records v1 and v2 that belong to different vehicles (different carid values), v2.latitude is greater than or equal to tan(min(abs(max(cos(v2.timestamp), sqrt(v2.longitude))), mul(cos(tan(v1.latitude)), div(log(v2.longitude), sub(v1.latitude, 58332.225))))). |
| 55 | `2_constraint_25` | For any two records v1 and v2 in the dataset, v2.timestamp is greater than max(sin(max(33240.487, v1.timestamp)), tan(div(v1.longitude, v1.direction))). |
| 56 | `2_constraint_27` | For any two records v1 and v2 that belong to different vehicles (different carid values), v1.speed is less than mul(abs(v1.timestamp), abs(v2.timestamp)). |
| 57 | `2_constraint_29` | For any two records v1 and v2 that belong to different vehicles (different carid values), v2.timestamp is less than or equal to max(max(sub(add(v1.timestamp, 55248.019), neg(v2.direction)), sub(max(v1.latitude, 53975.227), sin(v1.direction))), cos(sub(log(v1.timestamp), sub(v2.direction, v1.speed)))). |
| 58 | `2_constraint_30` | For any two records v1 and v2 that belong to the same vehicle (same carid), v2.direction is less than or equal to add(v2.timestamp, v1.direction). |
| 59 | `2_constraint_31` | For any record v1 in the dataset, v1.latitude is less than min(div(abs(abs(max(v1.longitude, v1.timestamp))), sqrt(max(min(v1.direction, 62173.505), max(v1.longitude, v1.direction)))), add(neg(abs(sin(v1.direction))), v1.timestamp)). |
| 60 | `2_constraint_32` | For any two records v1 and v2 that belong to the same vehicle (same carid), v1.latitude is less than add(min(v2.latitude, add(v1.direction, add(v2.longitude, v1.speed))), v1.timestamp). |
| 61 | `2_constraint_33` | For any two records v1 and v2 in the dataset, v1.latitude is greater than min(log(neg(v2.direction)), add(v2.direction, v2.speed)). |
| 62 | `2_constraint_34` | For any record v1 in the dataset, v1.longitude is greater than or equal to log(mul(log(mul(v1.direction, v1.direction)), sqrt(abs(v1.timestamp)))). |
| 63 | `2_constraint_36` | For any record v1 in the dataset, v1.timestamp is greater than sqrt(abs(v1.latitude)). |
| 64 | `2_constraint_38` | For any two records v1 and v2 in the dataset, v2.latitude is greater than cos(log(sub(v2.longitude, v2.direction))). |
| 65 | `2_constraint_39` | For any two records v1 and v2 in the dataset, v1.latitude is less than or equal to div(max(add(v2.direction, 40011.111), abs(v2.direction)), abs(sqrt(v2.longitude))). |
| 66 | `2_constraint_40` | For any two records v1 and v2 that belong to the same vehicle (same carid), v2.timestamp is less than or equal to max(cos(log(v2.direction)), mul(sqrt(v2.latitude), v1.timestamp)). |
| 67 | `2_constraint_41` | For any record v1 in the dataset, v1.latitude is greater than sin(cos(sub(add(v1.speed, -16583.383), sin(v1.longitude)))). |
| 68 | `2_constraint_42` | For any two records v1 and v2 that belong to the same vehicle (same carid), v2.speed is greater than or equal to neg(mul(v2.longitude, v2.timestamp)). |
| 69 | `2_constraint_43` | For any two records v1 and v2 that belong to different vehicles (different carid values), v2.latitude is greater than or equal to neg(v2.direction). |
| 70 | `2_constraint_44` | For any two records v1 and v2 in the dataset, v1.latitude is less than or equal to mul(log(abs(v2.latitude)), abs(mul(v1.longitude, v1.longitude))). |
| 71 | `2_constraint_46` | For any two records v1 and v2 that belong to different vehicles (different carid values), v2.speed is greater than max(cos(sqrt(-10647.349)), mul(tan(v1.latitude), sin(v1.latitude))). |
| 72 | `2_constraint_47` | For any two records v1 and v2 that belong to different vehicles (different carid values), v2.speed is less than mul(sub(sqrt(abs(neg(v1.longitude))), sub(abs(abs(61240.201)), add(min(v1.speed, v1.direction), div(v2.timestamp, v1.latitude)))), sqrt(sub(mul(tan(v2.latitude), min(v1.longitude, v1.speed)), max(abs(38476.284), cos(v1.direction))))). |
| 73 | `2_constraint_48` | For any two records v1 and v2 in the dataset, v2.speed is greater than or equal to sub(tan(log(v2.longitude)), sin(log(v2.timestamp))). |
| 74 | `2_constraint_49` | For any two records v1 and v2 that belong to the same vehicle (same carid), v2.direction is greater than neg(v1.timestamp). |
| 75 | `2_constraint_50` | For any two records v1 and v2 that belong to different vehicles (different carid values), v1.direction is greater than or equal to div(neg(19353.533), add(add(v1.speed, log(v2.timestamp)), sub(sub(v1.timestamp, v1.latitude), sqrt(v1.longitude)))). |
| 76 | `3_constraint_1` | For any record v1 in the dataset, v1.speed is greater than div(sin(cos(-51789.908)), v1.timestamp). |
| 77 | `3_constraint_2` | For any two records v1 and v2 that belong to the same vehicle (same carid), v1.longitude is less than add(v1.latitude, v2.longitude). |
| 78 | `3_constraint_3` | For any two records v1 and v2 that belong to different vehicles (different carid values), v1.timestamp is greater than or equal to add(v2.timestamp, -24021.441). |
| 79 | `3_constraint_4` | For any two records v1 and v2 that belong to different vehicles (different carid values), v2.longitude is less than add(v1.latitude, abs(v1.longitude)). |
| 80 | `3_constraint_6` | For any record v1 in the dataset, v1.latitude is greater than or equal to div(log(v1.timestamp), cos(-17618.185)). |
| 81 | `3_constraint_7` | For any record v1 in the dataset, v1.latitude is less than log(sub(cos(sin(sin(v1.longitude))), abs(abs(mul(v1.timestamp, 11803.291))))). |
| 82 | `3_constraint_8` | For any record v1 in the dataset, v1.direction is greater than or equal to div(cos(59174.124), v1.timestamp). |
| 83 | `3_constraint_9` | For any two records v1 and v2 that belong to different vehicles (different carid values), v2.timestamp is less than or equal to add(v1.timestamp, sqrt(v1.timestamp)). |
| 84 | `3_constraint_10` | For any record v1 in the dataset, v1.latitude is greater than or equal to add(div(v1.longitude, v1.longitude), log(v1.timestamp)). |
| 85 | `3_constraint_12` | For any two records v1 and v2 that belong to the same vehicle (same carid), v2.speed is greater than div(sin(sqrt(-11563.852)), sub(-11563.852, v1.timestamp)). |
| 86 | `3_constraint_13` | For any two records v1 and v2 that belong to the same vehicle (same carid), v1.speed is greater than div(cos(v2.latitude), v1.timestamp). |
| 87 | `3_constraint_18` | For any record v1 in the dataset, v1.longitude is less than sub(add(div(v1.latitude, v1.timestamp), sqrt(20062.754)), v1.latitude). |
| 88 | `3_constraint_19` | For any two records v1 and v2 that belong to the same vehicle (same carid), v2.direction is less than div(sqrt(log(sqrt(v1.latitude))), v1.timestamp). |
| 89 | `3_constraint_20` | For any record v1 in the dataset, v1.speed is greater than div(sin(sin(log(-27923.434))), v1.timestamp). |
| 90 | `3_constraint_21` | For any two records v1 and v2 that belong to the same vehicle (same carid), v2.direction is less than or equal to div(cos(div(cos(36216.286), v1.timestamp)), v1.timestamp). |
| 91 | `3_constraint_22` | For any record v1 in the dataset, v1.latitude is greater than or equal to log(sub(v1.timestamp, -36970.059)). |
| 92 | `3_constraint_23` | For any two records v1 and v2 in the dataset, v2.latitude is less than div(v1.longitude, log(max(v2.longitude, max(sin(mul(v1.direction, v1.timestamp)), log(sqrt(v1.latitude)))))). |
| 93 | `3_constraint_24` | For any two records v1 and v2 that belong to the same vehicle (same carid), v1.latitude is greater than add(log(v2.timestamp), tan(v2.latitude)). |
| 94 | `3_constraint_25` | For any two records v1 and v2 that belong to the same vehicle (same carid), v1.timestamp is greater than add(-5828.477, v2.timestamp). |
| 95 | `3_constraint_27` | For any two records v1 and v2 that belong to the same vehicle (same carid), v1.direction is greater than div(cos(v2.latitude), v1.timestamp). |
| 96 | `3_constraint_28` | For any record v1 in the dataset, v1.longitude is less than abs(sqrt(14453.193)). |
| 97 | `3_constraint_29` | For any two records v1 and v2 in the dataset, v2.timestamp is greater than mul(sin(v1.longitude), v1.timestamp). |
| 98 | `3_constraint_32` | For any two records v1 and v2 that belong to different vehicles (different carid values), v2.timestamp is less than or equal to add(sqrt(v1.timestamp), add(v1.timestamp, v2.latitude)). |
| 99 | `3_constraint_33` | For any record v1 in the dataset, v1.speed is less than or equal to div(tan(cos(cos(-15127.919))), v1.timestamp). |
| 100 | `3_constraint_34` | For any record v1 in the dataset, v1.timestamp is greater than add(max(-56888.107, -25871.755), max(min(v1.longitude, v1.latitude), mul(neg(-41147.911), 29409.390))). |
| 101 | `3_constraint_35` | For any two records v1 and v2 that belong to different vehicles (different carid values), v2.longitude is greater than or equal to add(abs(v1.latitude), add(abs(add(v2.latitude, log(19760.558))), v2.latitude)). |
| 102 | `3_constraint_36` | For any two records v1 and v2 in the dataset, v1.longitude is greater than div(log(v2.timestamp), max(div(v1.latitude, v2.longitude), neg(add(v1.latitude, v1.timestamp)))). |
| 103 | `3_constraint_41` | For any record v1 in the dataset, v1.longitude is less than neg(sub(cos(v1.timestamp), sqrt(17846.543))). |
| 104 | `3_constraint_43` | For any record v1 in the dataset, v1.latitude is greater than or equal to log(add(v1.timestamp, 38594.680)). |
| 105 | `3_constraint_44` | For any two records v1 and v2 that belong to different vehicles (different carid values), v2.timestamp is greater than or equal to sub(v1.timestamp, 49029.657). |
| 106 | `3_constraint_45` | For any record v1 in the dataset, v1.speed is equal to div(log(sqrt(log(sqrt(sqrt(mul(-52848.623, sqrt(sqrt(mul(-52848.623, sqrt(sqrt(mul(-52848.623, sqrt(sqrt(mul(-52848.623, v1.latitude))))))))))))))), v1.timestamp). |
| 107 | `3_constraint_46` | For any two records v1 and v2 that belong to different vehicles (different carid values), v1.latitude is greater than or equal to log(v1.timestamp). |
| 108 | `3_constraint_47` | For any two records v1 and v2 that belong to different vehicles (different carid values), v1.longitude is greater than or equal to sqrt(-11648.396). |
| 109 | `3_constraint_48` | For any record v1 in the dataset, v1.direction is greater than or equal to div(tan(tan(-39536.477)), v1.timestamp). |
| 110 | `3_constraint_50` | For any two records v1 and v2 that belong to different vehicles (different carid values), v1.longitude is greater than abs(div(-12236.040, v2.longitude)). |
| 111 | `4_constraint_1` | For any two records v1 and v2 in the dataset, v2.longitude is greater than sqrt(sqrt(abs(v1.longitude))). |
| 112 | `4_constraint_2` | For any record v1 in the dataset, v1.timestamp is greater than add(sqrt(v1.direction), min(v1.latitude, v1.latitude)). |
| 113 | `4_constraint_3` | For any two records v1 and v2 that belong to the same vehicle (same carid), v2.timestamp is greater than or equal to sqrt(v2.direction). |
| 114 | `4_constraint_4` | For any two records v1 and v2 that belong to the same vehicle (same carid), v1.longitude is greater than mul(add(div(sub(v1.direction, v1.timestamp), div(v2.timestamp, v2.speed)), mul(div(v2.direction, v1.timestamp), tan(v1.direction))), abs(min(sqrt(v1.speed), sqrt(v1.direction)))). |
| 115 | `4_constraint_5` | For any two records v1 and v2 that belong to the same vehicle (same carid), v2.direction is less than or equal to add(max(v1.timestamp, v2.longitude), sub(v1.latitude, v1.longitude)). |
| 116 | `4_constraint_6` | For any two records v1 and v2 in the dataset, v1.direction is greater than or equal to add(neg(min(tan(v2.latitude), mul(v2.timestamp, v2.speed))), log(min(cos(sub(sub(v1.latitude, v1.speed), div(v1.longitude, v1.longitude))), v1.speed))). |
| 117 | `4_constraint_7` | For any two records v1 and v2 in the dataset, v2.timestamp is greater than or equal to log(neg(div(tan(v1.timestamp), log(v1.speed)))). |
| 118 | `4_constraint_8` | For any two records v1 and v2 that belong to different vehicles (different carid values), v2.latitude is greater than or equal to tan(min(min(sqrt(v2.longitude), div(v2.direction, v2.timestamp)), log(add(v1.latitude, v2.speed)))). |
| 119 | `4_constraint_9` | For any two records v1 and v2 that belong to different vehicles (different carid values), v1.timestamp is less than or equal to mul(add(add(cos(v2.timestamp), add(v2.latitude, v2.timestamp)), min(log(v2.direction), sin(v1.latitude))), abs(sub(max(v1.longitude, v2.latitude), div(v1.speed, v2.direction)))). |
| 120 | `4_constraint_10` | For any record v1 in the dataset, v1.speed is greater than or equal to cos(log(v1.timestamp)). |
| 121 | `4_constraint_11` | For any two records v1 and v2 that belong to the same vehicle (same carid), v2.speed is greater than sin(sqrt(v2.latitude)). |
| 122 | `4_constraint_14` | For any record v1 in the dataset, v1.direction is less than or equal to sqrt(max(sub(v1.timestamp, v1.speed), mul(v1.latitude, v1.timestamp))). |
| 123 | `4_constraint_15` | For any two records v1 and v2 in the dataset, v1.speed is less than add(min(add(v2.speed, v2.timestamp), v1.longitude), mul(v1.latitude, div(v2.latitude, v2.latitude))). |
| 124 | `4_constraint_16` | For any record v1 in the dataset, v1.latitude is greater than or equal to sin(sub(sin(sin(v1.timestamp)), v1.direction)). |
| 125 | `4_constraint_17` | For any record v1 in the dataset, v1.speed is greater than neg(cos(log(v1.longitude))). |
| 126 | `4_constraint_18` | For any two records v1 and v2 that belong to the same vehicle (same carid), v2.latitude is greater than or equal to neg(max(sub(tan(min(v2.timestamp, v1.timestamp)), cos(log(v2.timestamp))), abs(abs(cos(v1.latitude))))). |
| 127 | `4_constraint_19` | For any two records v1 and v2 that belong to the same vehicle (same carid), v2.direction is greater than or equal to neg(add(v1.timestamp, -21731.675)). |
| 128 | `4_constraint_20` | For any two records v1 and v2 that belong to different vehicles (different carid values), v1.longitude is less than or equal to max(cos(neg(v2.timestamp)), max(abs(v2.direction), min(v2.timestamp, v1.timestamp))). |
| 129 | `4_constraint_21` | For any two records v1 and v2 that belong to the same vehicle (same carid), v2.latitude is less than max(sin(v2.speed), abs(v2.longitude)). |
| 130 | `4_constraint_22` | For any two records v1 and v2 that belong to different vehicles (different carid values), v1.longitude is less than abs(sub(v1.direction, -19711.637)). |
| 131 | `4_constraint_23` | For any two records v1 and v2 in the dataset, v2.direction is less than mul(v2.longitude, v1.longitude). |
| 132 | `4_constraint_25` | For any two records v1 and v2 that belong to different vehicles (different carid values), v1.timestamp is less than or equal to mul(sub(19025.060, v2.longitude), abs(v2.timestamp)). |
| 133 | `4_constraint_28` | For any two records v1 and v2 in the dataset, v2.latitude is less than div(abs(sqrt(div(max(v1.timestamp, v2.timestamp), log(v2.longitude)))), log(sqrt(neg(log(v2.longitude))))). |
| 134 | `4_constraint_30` | For any two records v1 and v2 in the dataset, v2.timestamp is greater than cos(div(tan(sin(v2.longitude)), tan(sqrt(v1.direction)))). |
| 135 | `4_constraint_31` | For any record v1 in the dataset, v1.latitude is greater than or equal to sin(sub(v1.timestamp, v1.speed)). |
| 136 | `4_constraint_32` | For any two records v1 and v2 that belong to different vehicles (different carid values), v2.latitude is less than or equal to add(max(v2.direction, v2.longitude), cos(-10577.597)). |
| 137 | `4_constraint_33` | For any two records v1 and v2 that belong to the same vehicle (same carid), v1.speed is greater than or equal to add(mul(max(sub(add(v2.latitude, v2.timestamp), min(v2.speed, v2.timestamp)), abs(add(v2.speed, v1.timestamp))), div(neg(log(v1.longitude)), sqrt(log(v2.timestamp)))), mul(log(div(sqrt(v1.longitude), log(v2.speed))), abs(sqrt(mul(v1.longitude, v1.longitude))))). |
| 138 | `4_constraint_34` | For any two records v1 and v2 in the dataset, v1.timestamp is less than or equal to sub(mul(v2.timestamp, v1.longitude), sin(v2.timestamp)). |
| 139 | `4_constraint_35` | For any record v1 in the dataset, v1.speed is greater than or equal to sub(div(v1.longitude, v1.direction), mul(v1.longitude, v1.latitude)). |
| 140 | `4_constraint_36` | For any record v1 in the dataset, v1.direction is less than or equal to max(neg(mul(sin(sqrt(v1.latitude)), mul(sub(neg(v1.timestamp), max(v1.speed, v1.longitude)), cos(div(v1.latitude, v1.longitude))))), max(v1.timestamp, v1.longitude)). |
| 141 | `4_constraint_37` | For any two records v1 and v2 that belong to the same vehicle (same carid), v2.direction is less than or equal to sub(min(v2.speed, sub(v2.latitude, sqrt(v2.longitude))), neg(max(v1.timestamp, v1.direction))). |
| 142 | `4_constraint_38` | For any two records v1 and v2 in the dataset, v1.speed is greater than or equal to cos(abs(v1.latitude)). |
| 143 | `4_constraint_39` | For any two records v1 and v2 in the dataset, v1.latitude is greater than sub(min(neg(v2.direction), min(v1.timestamp, v2.direction)), tan(mul(5169.952, -57090.012))). |
| 144 | `4_constraint_40` | For any record v1 in the dataset, v1.longitude is less than or equal to add(tan(v1.latitude), sqrt(v1.timestamp)). |
| 145 | `4_constraint_41` | For any record v1 in the dataset, v1.direction is equal to div(sin(-23107.089), v1.timestamp). |
| 146 | `4_constraint_43` | For any record v1 in the dataset, v1.latitude is greater than tan(sin(add(v1.direction, v1.timestamp))). |
| 147 | `4_constraint_44` | For any two records v1 and v2 in the dataset, v2.timestamp is greater than add(v2.speed, v2.latitude). |
| 148 | `4_constraint_45` | For any two records v1 and v2 that belong to different vehicles (different carid values), v1.speed is greater than or equal to abs(div(div(v2.direction, v1.timestamp), neg(v1.timestamp))). |
| 149 | `4_constraint_46` | For any record v1 in the dataset, v1.timestamp is greater than add(div(sqrt(add(v1.longitude, v1.longitude)), add(v1.speed, log(v1.longitude))), v1.latitude). |
| 150 | `4_constraint_48` | For any two records v1 and v2 that belong to different vehicles (different carid values), v1.latitude is greater than tan(v2.latitude). |
| 151 | `4_constraint_49` | For any record v1 in the dataset, v1.direction is greater than or equal to min(v1.speed, cos(add(max(v1.speed, v1.longitude), sqrt(v1.timestamp)))). |
| 152 | `4_constraint_50` | For any two records v1 and v2 that belong to different vehicles (different carid values), v1.direction is less than or equal to min(sub(v1.timestamp, log(v1.speed)), v1.timestamp). |
| 153 | `5_constraint_5` | For any record v1 in the dataset, v1.speed is greater than div(sin(cos(21302.372)), v1.timestamp). |
| 154 | `5_constraint_6` | For any record v1 in the dataset, v1.speed is equal to div(cos(cos(5780.161)), mul(v1.timestamp, cos(5780.161))). |
| 155 | `5_constraint_7` | For any two records v1 and v2 that belong to the same vehicle (same carid), v1.longitude is less than or equal to sub(sqrt(-15380.166), log(v2.latitude)). |
| 156 | `5_constraint_8` | For any two records v1 and v2 that belong to the same vehicle (same carid), v1.speed is greater than or equal to div(sin(40890.352), neg(v2.timestamp)). |
| 157 | `5_constraint_9` | For any two records v1 and v2 that belong to different vehicles (different carid values), v2.timestamp is greater than div(v1.timestamp, sqrt(sqrt(sqrt(sqrt(sqrt(sqrt(abs(log(v2.longitude))))))))). |
| 158 | `5_constraint_11` | For any two records v1 and v2 that belong to the same vehicle (same carid), v2.timestamp is greater than abs(neg(mul(sin(sqrt(30274.064)), add(v2.direction, v1.timestamp)))). |
| 159 | `5_constraint_12` | For any two records v1 and v2 that belong to different vehicles (different carid values), v1.latitude is greater than or equal to add(div(v2.longitude, v2.timestamp), log(v2.timestamp)). |
| 160 | `5_constraint_13` | For any two records v1 and v2 that belong to the same vehicle (same carid), v1.timestamp is greater than add(v2.timestamp, -52243.102). |
| 161 | `5_constraint_14` | For any record v1 in the dataset, v1.latitude is less than abs(sqrt(mul(min(abs(v1.longitude), log(v1.longitude)), abs(abs(v1.longitude))))). |
| 162 | `5_constraint_15` | For any two records v1 and v2 in the dataset, v2.latitude is less than add(log(abs(log(abs(log(mul(neg(v1.longitude), v1.longitude)))))), max(log(neg(v1.timestamp)), abs(abs(v1.latitude)))). |
| 163 | `5_constraint_19` | For any two records v1 and v2 in the dataset, v1.longitude is less than or equal to abs(abs(sub(tan(abs(-35078.421)), abs(v2.longitude)))). |
| 164 | `5_constraint_20` | For any record v1 in the dataset, v1.latitude is less than or equal to add(sqrt(sqrt(log(v1.timestamp))), log(neg(v1.timestamp))). |
| 165 | `5_constraint_21` | For any two records v1 and v2 that belong to different vehicles (different carid values), v2.timestamp is greater than add(sin(neg(mul(v2.speed, v2.latitude))), sub(max(sub(v1.timestamp, 17133.830), abs(v1.speed)), div(sin(v1.direction), sqrt(v2.latitude)))). |
| 166 | `5_constraint_23` | For any two records v1 and v2 that belong to different vehicles (different carid values), v2.timestamp is greater than div(v1.timestamp, min(v1.timestamp, sqrt(sqrt(sqrt(min(v1.timestamp, sqrt(sqrt(min(v1.timestamp, sqrt(sqrt(sqrt(sqrt(v2.latitude))))))))))))). |
| 167 | `5_constraint_26` | For any two records v1 and v2 that belong to different vehicles (different carid values), v2.timestamp is greater than or equal to sub(v1.latitude, min(sub(add(max(abs(v1.latitude), tan(v2.longitude)), sqrt(abs(v1.latitude))), add(abs(max(v1.latitude, v2.speed)), tan(sub(v2.direction, v1.longitude)))), sub(min(log(min(v1.timestamp, v2.latitude)), log(div(v1.speed, v2.speed))), max(max(min(v2.speed, v1.direction), add(-41070.172, v1.timestamp)), max(abs(v1.direction), neg(v2.speed)))))). |
| 168 | `5_constraint_27` | For any two records v1 and v2 in the dataset, v2.longitude is less than or equal to add(v1.longitude, sin(v1.longitude)). |
| 169 | `5_constraint_28` | For any record v1 in the dataset, v1.longitude is greater than or equal to mul(max(sqrt(v1.latitude), sqrt(v1.latitude)), max(v1.latitude, neg(v1.latitude))). |
| 170 | `5_constraint_30` | For any record v1 in the dataset, v1.speed is less than or equal to div(sqrt(sqrt(log(log(v1.timestamp)))), v1.timestamp). |
| 171 | `5_constraint_31` | For any two records v1 and v2 that belong to different vehicles (different carid values), v2.longitude is less than or equal to abs(add(sqrt(v2.latitude), v1.longitude)). |
| 172 | `5_constraint_32` | For any two records v1 and v2 that belong to different vehicles (different carid values), v1.longitude is greater than or equal to add(add(v2.latitude, add(abs(v1.latitude), add(v2.latitude, abs(v1.latitude)))), abs(v1.latitude)). |
| 173 | `5_constraint_34` | For any record v1 in the dataset, v1.latitude is greater than or equal to log(sub(tan(tan(v1.longitude)), neg(add(v1.timestamp, v1.direction)))). |
| 174 | `5_constraint_36` | For any two records v1 and v2 that belong to the same vehicle (same carid), v2.speed is greater than div(sin(sin(neg(sqrt(cos(sqrt(cos(cos(cos(v2.latitude))))))))), v2.timestamp). |
| 175 | `5_constraint_37` | For any record v1 in the dataset, v1.direction is equal to div(neg(tan(tan(log(tan(cos(log(v1.timestamp))))))), v1.timestamp). |
| 176 | `5_constraint_39` | For any record v1 in the dataset, v1.direction is less than or equal to div(mul(div(-35474.792, v1.timestamp), -47343.003), v1.timestamp). |
| 177 | `5_constraint_40` | For any two records v1 and v2 that belong to the same vehicle (same carid), v2.longitude is greater than or equal to sqrt(-12398.018). |
| 178 | `5_constraint_42` | For any two records v1 and v2 in the dataset, v1.longitude is less than or equal to mul(log(v2.longitude), sqrt(mul(log(v2.longitude), mul(log(v2.longitude), sqrt(mul(log(v2.longitude), sqrt(-27461.682))))))). |
| 179 | `5_constraint_44` | For any record v1 in the dataset, v1.timestamp is less than mul(abs(add(-54979.658, add(min(10994.281, v1.speed), neg(-28263.866)))), 52554.063). |
| 180 | `5_constraint_45` | For any record v1 in the dataset, v1.timestamp is greater than mul(add(-49899.432, add(-49899.432, neg(v1.direction))), -12619.258). |
| 181 | `5_constraint_46` | For any two records v1 and v2 that belong to the same vehicle (same carid), v2.speed is greater than or equal to div(div(v1.latitude, v1.timestamp), v2.longitude). |
| 182 | `5_constraint_50` | For any record v1 in the dataset, v1.timestamp is greater than or equal to neg(min(abs(add(sqrt(v1.direction), cos(neg(v1.direction)))), div(mul(add(-12824.157, min(-7019.369, v1.speed)), sub(max(62640.522, v1.longitude), sin(v1.latitude))), neg(sub(cos(-21835.810), sin(sin(10613.504))))))). |
