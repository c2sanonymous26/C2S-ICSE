# Aggregated Ratings

## Method 1

| Constraint | Final Rating | Votes | Notes |
|------------|--------------|-------|-------|
| `1_constraint_1` | A | reviewer1:A, reviewer2:A, reviewer3:A (unanimous) |  |
| `2_constraint_43` | A | same as `1_constraint_1` |  |
| `3_constraint_11` | A | same as `1_constraint_1` |  |
| `4_constraint_29` | A | same as `1_constraint_1` |  |
| `5_constraint_32` | A | same as `1_constraint_1` |  |
| `1_constraint_2` | A | reviewer1:A, reviewer2:B, reviewer3:A (2:1) |  |
| `2_constraint_44` | A | same as `1_constraint_2` |  |
| `3_constraint_12` | A | same as `1_constraint_2` |  |
| `5_constraint_33` | A | same as `1_constraint_2` |  |
| `1_constraint_3` | A | reviewer1:A, reviewer2:B, reviewer3:A (2:1) |  |
| `2_constraint_45` | A | same as `1_constraint_3` |  |
| `3_constraint_14` | A | same as `1_constraint_3` |  |
| `4_constraint_30` | A | same as `1_constraint_3` |  |
| `5_constraint_34` | A | same as `1_constraint_3` |  |
| `1_constraint_5` | A | reviewer1:A, reviewer2:A, reviewer3:B (2:1) | reviewer3: Does not seem meaningful in practice |
| `2_constraint_46` | A | same as `1_constraint_5` |  |
| `1_constraint_6` | A | reviewer1:A, reviewer2:B, reviewer3:A (2:1) |  |
| `1_constraint_7` | A | reviewer1:B, reviewer2:A, reviewer3:A (2:1) | reviewer1: Does not account for the fact that 0 and 359 degrees are actually only 1 degree apart |
| `2_constraint_37` | A | same as `1_constraint_7` |  |
| `3_constraint_4` | A | same as `1_constraint_7` |  |
| `1_constraint_8` | A | reviewer1:A, reviewer2:A, reviewer3:A (unanimous) |  |
| `2_constraint_35` | A | same as `1_constraint_8` |  |
| `4_constraint_39` | A | same as `1_constraint_8` |  |
| `1_constraint_9` | B | reviewer1:B, reviewer2:B, reviewer3:A (2:1) | reviewer1: The generated constraint logic does not match its description |
| `2_constraint_39` | B | same as `1_constraint_9` |  |
| `1_constraint_10` | A | reviewer1:A, reviewer2:A, reviewer3:A (unanimous) |  |
| `2_constraint_38` | A | same as `1_constraint_10` |  |
| `3_constraint_3` | A | same as `1_constraint_10` |  |
| `4_constraint_41` | A | same as `1_constraint_10` |  |
| `1_constraint_12` | B | reviewer1:B, reviewer2:B, reviewer3:C (2:1) | reviewer1: On a two-way road, one side can be congested while the other remains smooth |
| `4_constraint_35` | B | same as `1_constraint_12` |  |
| `1_constraint_13` | A | reviewer1:A, reviewer2:B, reviewer3:A (2:1) |  |
| `1_constraint_14` | C | reviewer1:B, reviewer2:C, reviewer3:C (2:1) | reviewer1: The generated constraint logic does not match its description |
| `1_constraint_16` | A | reviewer1:A, reviewer2:A, reviewer3:B (2:1) | reviewer3: The meaning of the product is unclear |
| `2_constraint_5` | A | same as `1_constraint_16` |  |
| `1_constraint_17` | C | reviewer1:B, reviewer2:A, reviewer3:C (1:1:1) | reviewer1: Does not account for the fact that 0 and 359 degrees are actually only 1 degree apart |
| `1_constraint_18` | B | reviewer1:B, reviewer2:A, reviewer3:B (2:1) | reviewer1: Does not account for the fact that 0 and 359 degrees are actually only 1 degree apart; reviewer3: At low speed, a larger direction change seems possible |
| `1_constraint_19` | A | reviewer1:A, reviewer2:A, reviewer3:A (unanimous) |  |
| `1_constraint_21` | B | reviewer1:B, reviewer2:A, reviewer3:B (2:1) | reviewer1: The derived threshold seems somewhat too loose; reviewer3: The lower bound seems meaningless |
| `1_constraint_22` | B | reviewer1:B, reviewer2:B, reviewer3:A (2:1) | reviewer1: The real-world meaning of distance multiplied by speed is questionable; reviewer2: Distance divided by speed would be more reasonable |
| `1_constraint_24` | A | reviewer1:A, reviewer2:A, reviewer3:A (unanimous) |  |
| `3_constraint_7` | A | same as `1_constraint_24` |  |
| `1_constraint_25` | B | reviewer1:A, reviewer2:B, reviewer3:B (2:1) | reviewer3: The meaning of the product is unclear |
| `1_constraint_27` | C | reviewer1:B, reviewer2:A, reviewer3:C (1:1:1) | reviewer1: Does not account for the fact that 0 and 359 degrees are actually only 1 degree apart |
| `1_constraint_29` | A | reviewer1:B, reviewer2:A, reviewer3:A (2:1) | reviewer1: Does not account for the fact that 0 and 359 degrees are actually only 1 degree apart |
| `1_constraint_31` | B | reviewer1:B, reviewer2:B, reviewer3:B (unanimous) | reviewer1: Does not account for the fact that 0 and 359 degrees are actually only 1 degree apart; reviewer2: Intuitively, direction changes are more likely at low speed |
| `1_constraint_32` | B | reviewer1:B, reviewer2:B, reviewer3:B (unanimous) | reviewer1: Does not account for the fact that 0 and 359 degrees are actually only 1 degree apart, and the derived threshold seems somewhat too loose |
| `1_constraint_33` | A | reviewer1:A, reviewer2:A, reviewer3:A (unanimous) |  |
| `1_constraint_34` | A | reviewer1:A, reviewer2:A, reviewer3:A (unanimous) |  |
| `1_constraint_35` | A | reviewer1:B, reviewer2:A, reviewer3:A (2:1) | reviewer1: The derived threshold seems somewhat too loose |
| `1_constraint_36` | A | reviewer1:B, reviewer2:A, reviewer3:A (2:1) | reviewer1: Does not account for the fact that 0 and 359 degrees are actually only 1 degree apart |
| `1_constraint_38` | A | reviewer1:B, reviewer2:A, reviewer3:A (2:1) | reviewer1: Does not account for location constraints |
| `1_constraint_39` | B | reviewer1:B, reviewer2:B, reviewer3:A (2:1) | reviewer1: Two-way road; reviewer2: Different vehicles should not be related |
| `1_constraint_41` | B | reviewer1:A, reviewer2:B, reviewer3:B (2:1) |  |
| `1_constraint_43` | A | reviewer1:A, reviewer2:B, reviewer3:A (2:1) |  |
| `1_constraint_46` | B | reviewer1:B, reviewer2:B, reviewer3:B (unanimous) | reviewer1: Does not account for the fact that 0 and 359 degrees are actually only 1 degree apart |
| `1_constraint_47` | A | reviewer1:A, reviewer2:A, reviewer3:A (unanimous) |  |
| `2_constraint_1` | A | reviewer1:A, reviewer2:A, reviewer3:A (unanimous) |  |
| `2_constraint_2` | B | reviewer1:B, reviewer2:A, reviewer3:B (2:1) | reviewer1: The generated constraint logic does not match its description; reviewer3: The lower bound does not seem meaningful |
| `2_constraint_3` | B | reviewer1:B, reviewer2:B, reviewer3:B (unanimous) | reviewer1: The derived threshold seems somewhat too loose, and its real-world meaning is questionable; reviewer2: Negative speed is meaningless |
| `2_constraint_4` | B | reviewer1:B, reviewer2:B, reviewer3:C (2:1) | reviewer1: Does not account for the fact that 0 and 359 degrees are actually only 1 degree apart |
| `4_constraint_14` | B | same as `2_constraint_4` |  |
| `2_constraint_7` | A | reviewer1:B, reviewer2:A, reviewer3:A (2:1) | reviewer1: The derived threshold seems somewhat too loose |
| `2_constraint_8` | A | reviewer1:A, reviewer2:A, reviewer3:A (unanimous) |  |
| `2_constraint_9` | B | reviewer1:B, reviewer2:B, reviewer3:A (2:1) | reviewer1: Does not account for the fact that 0 and 359 degrees are actually only 1 degree apart |
| `2_constraint_10` | A | reviewer1:B, reviewer2:A, reviewer3:A (2:1) | reviewer1: Does not account for the fact that 0 and 359 degrees are actually only 1 degree apart |
| `2_constraint_11` | B | reviewer1:B, reviewer2:B, reviewer3:B (unanimous) | reviewer1: Does not account for the fact that 0 and 359 degrees are actually only 1 degree apart |
| `2_constraint_12` | B | reviewer1:B, reviewer2:B, reviewer3:B (unanimous) | reviewer1: Does not account for the fact that 0 and 359 degrees are actually only 1 degree apart |
| `2_constraint_13` | A | reviewer1:A, reviewer2:A, reviewer3:A (unanimous) |  |
| `2_constraint_14` | A | reviewer1:B, reviewer2:A, reviewer3:A (2:1) | reviewer1: The derived threshold seems somewhat too loose |
| `2_constraint_15` | B | reviewer1:B, reviewer2:B, reviewer3:B (unanimous) | reviewer1: Does not account for the fact that 0 and 359 degrees are actually only 1 degree apart |
| `2_constraint_19` | A | reviewer1:A, reviewer2:B, reviewer3:A (2:1) |  |
| `2_constraint_22` | B | reviewer1:B, reviewer2:B, reviewer3:A (2:1) | reviewer1: The derived threshold seems somewhat too loose |
| `2_constraint_24` | B | reviewer1:B, reviewer2:A, reviewer3:B (2:1) | reviewer1: Does not account for the fact that 0 and 359 degrees are actually only 1 degree apart |
| `2_constraint_29` | A | reviewer1:A, reviewer2:A, reviewer3:A (unanimous) |  |
| `2_constraint_30` | A | reviewer1:B, reviewer2:A, reviewer3:A (2:1) | reviewer1: Does not account for the fact that 0 and 359 degrees are actually only 1 degree apart, and the derived threshold seems somewhat too loose |
| `2_constraint_32` | A | reviewer1:A, reviewer2:A, reviewer3:A (unanimous) |  |
| `2_constraint_34` | B | reviewer1:B, reviewer2:B, reviewer3:A (2:1) | reviewer1: The derived threshold seems somewhat too loose |
| `2_constraint_36` | A | reviewer1:A, reviewer2:A, reviewer3:A (unanimous) |  |
| `2_constraint_40` | B | reviewer1:B, reviewer2:B, reviewer3:C (2:1) | reviewer1: The derived threshold seems somewhat too loose; reviewer3: A negative lower bound is not very meaningful |
| `2_constraint_41` | B | reviewer1:C, reviewer2:A, reviewer3:B (1:1:1) |  |
| `2_constraint_42` | B | reviewer1:B, reviewer2:A, reviewer3:B (2:1) | reviewer1: Does not account for the fact that 0 and 359 degrees are actually only 1 degree apart |
| `3_constraint_10` | B | same as `2_constraint_42` |  |
| `4_constraint_45` | B | same as `2_constraint_42` |  |
| `2_constraint_47` | A | reviewer1:A, reviewer2:A, reviewer3:C (2:1) | reviewer3: Not very meaningful |
| `3_constraint_15` | A | same as `2_constraint_47` |  |
| `5_constraint_35` | A | same as `2_constraint_47` |  |
| `3_constraint_1` | A | reviewer1:A, reviewer2:A, reviewer3:A (unanimous) |  |
| `3_constraint_2` | A | reviewer1:A, reviewer2:A, reviewer3:A (unanimous) |  |
| `3_constraint_5` | B | reviewer1:B, reviewer2:B, reviewer3:A (2:1) | reviewer1: The derived threshold seems somewhat too loose |
| `3_constraint_6` | A | reviewer1:A, reviewer2:A, reviewer3:B (2:1) |  |
| `3_constraint_8` | B | reviewer1:B, reviewer2:A, reviewer3:B (2:1) | reviewer1: Does not account for the fact that 0 and 359 degrees are actually only 1 degree apart |
| `3_constraint_9` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `3_constraint_13` | A | reviewer1:A, reviewer2:A, reviewer3:C (2:1) | reviewer3: Not very meaningful |
| `5_constraint_36` | A | same as `3_constraint_13` |  |
| `3_constraint_16` | A | reviewer1:A, reviewer2:A, reviewer3:A (unanimous) |  |
| `3_constraint_18` | B | reviewer1:B, reviewer2:B, reviewer3:A (2:1) | reviewer1: Does not account for the fact that 0 and 359 degrees are actually only 1 degree apart, and the derived threshold seems somewhat too loose |

## Method 2

| Constraint | Final Rating | Votes | Notes |
|------------|--------------|-------|-------|
| `1_constraint_1` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `1_constraint_2` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `1_constraint_3` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `1_constraint_4` | C | reviewer1:C, reviewer2:C, reviewer3:B (2:1) |  |
| `1_constraint_5` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `1_constraint_6` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `1_constraint_8` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `1_constraint_9` | C | reviewer1:C, reviewer2:C, reviewer3:B (2:1) |  |
| `1_constraint_10` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `1_constraint_11` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `1_constraint_12` | A | reviewer1:A, reviewer2:B, reviewer3:A (2:1) |  |
| `1_constraint_13` | B | reviewer1:B, reviewer2:B, reviewer3:C (2:1) |  |
| `1_constraint_16` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `1_constraint_17` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `1_constraint_18` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `1_constraint_19` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `1_constraint_20` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `1_constraint_22` | C | reviewer1:C, reviewer2:C, reviewer3:B (2:1) |  |
| `1_constraint_23` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `1_constraint_24` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `1_constraint_26` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `1_constraint_27` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `1_constraint_28` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `1_constraint_30` | B | reviewer1:C, reviewer2:B, reviewer3:B (2:1) |  |
| `1_constraint_34` | C | reviewer1:C, reviewer2:C, reviewer3:B (2:1) |  |
| `1_constraint_36` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `1_constraint_37` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `1_constraint_40` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `1_constraint_41` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `1_constraint_45` | B | reviewer1:B, reviewer2:B, reviewer3:C (2:1) |  |
| `1_constraint_46` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `1_constraint_47` | A | reviewer1:C, reviewer2:A, reviewer3:A (2:1) |  |
| `1_constraint_48` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `1_constraint_50` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `2_constraint_1` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `2_constraint_2` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `2_constraint_3` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `2_constraint_4` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `2_constraint_5` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `2_constraint_7` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `2_constraint_8` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `2_constraint_9` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `2_constraint_10` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `2_constraint_13` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `2_constraint_14` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `2_constraint_15` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `2_constraint_16` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `2_constraint_17` | C | reviewer1:C, reviewer2:C, reviewer3:B (2:1) |  |
| `2_constraint_19` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `2_constraint_20` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `2_constraint_21` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `2_constraint_22` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `2_constraint_23` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `2_constraint_24` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `2_constraint_25` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `2_constraint_27` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `2_constraint_29` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `2_constraint_30` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `2_constraint_31` | C | reviewer1:C, reviewer2:C, reviewer3:B (2:1) |  |
| `2_constraint_32` | C | reviewer1:C, reviewer2:C, reviewer3:B (2:1) |  |
| `2_constraint_33` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `2_constraint_34` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `2_constraint_36` | C | reviewer1:C, reviewer2:B, reviewer3:C (2:1) |  |
| `2_constraint_38` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `2_constraint_39` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `2_constraint_40` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `2_constraint_41` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `2_constraint_42` | C | reviewer1:C, reviewer2:B, reviewer3:C (2:1) |  |
| `2_constraint_43` | C | reviewer1:C, reviewer2:B, reviewer3:C (2:1) |  |
| `2_constraint_44` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `2_constraint_46` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `2_constraint_47` | C | reviewer1:C, reviewer2:C, reviewer3:B (2:1) |  |
| `2_constraint_48` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `2_constraint_49` | C | reviewer1:C, reviewer2:B, reviewer3:C (2:1) |  |
| `2_constraint_50` | C | reviewer1:B, reviewer2:C, reviewer3:C (2:1) |  |
| `3_constraint_1` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `3_constraint_2` | B | reviewer1:B, reviewer2:C, reviewer3:B (2:1) |  |
| `3_constraint_3` | A | reviewer1:A, reviewer2:C, reviewer3:A (2:1) |  |
| `3_constraint_4` | B | reviewer1:B, reviewer2:C, reviewer3:B (2:1) |  |
| `3_constraint_6` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `3_constraint_7` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `3_constraint_8` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `3_constraint_9` | C | reviewer1:C, reviewer2:C, reviewer3:B (2:1) |  |
| `3_constraint_10` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `3_constraint_12` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `3_constraint_13` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `3_constraint_18` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `3_constraint_19` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `3_constraint_20` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `3_constraint_21` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
| `3_constraint_22` | C | reviewer1:C, reviewer2:C, reviewer3:C (unanimous) |  |
