# Part 2 Rating Form

Please fill in A, B, or C in the Rating column, and record any concerns or explanations in the Notes column (optional).

## Method 1

| Constraint | Rating | Notes |
|------------|--------|-------|
| `3_constraint_19` |A | |
| `3_constraint_21` |A | |
| `3_constraint_22` |A | |
| `3_constraint_23` |A | |
| `3_constraint_24` |A | |
| `3_constraint_26` |C | |
| `3_constraint_28` |B |If v1's speed is above a threshold, requiring v2.grpid to equal v1.grpid + 1 has no logical connection, because the temporal order of v1 and v2 is not specified |
| `3_constraint_29` |A | |
| `3_constraint_30` |A | |
| `3_constraint_31` |B |For a vehicle moving at constant speed, requiring the timestamp difference between v1 and v2 to stay within a small reasonable range is partly unreasonable |
| `3_constraint_32` |B |If v1 has zero speed and v2 does not, that does not necessarily imply a small timestamp difference between them; it is possible in some cases, but not inevitable |
| `3_constraint_33` |B | |
| `3_constraint_34` |B | |
| `3_constraint_35` |A | |
| `3_constraint_36` |A | |
| `3_constraint_41` |A | |
| `3_constraint_42` |A | |
| `3_constraint_43` |B |The allowed range for the latitude/longitude differences between v1 and v2 in the code is too small |
| `3_constraint_44` |B |The assertion in bfunc4 has no clear physical meaning |
| `3_constraint_45` |B |Part of the constraint condition is unreasonable; v2 should not be required to have the same direction as v1 |
| `3_constraint_46` |B | |
| `3_constraint_48` |B |Part of the constraint condition is unreasonable; v2 should not be required to have the same direction as v1 |
| `3_constraint_50` |A | |
| `4_constraint_1` |A | |
| `4_constraint_4` |B | |
| `4_constraint_5` |B | |
| `4_constraint_6` |A | |
| `4_constraint_7` |A | |
| `4_constraint_8` |A | |
| `4_constraint_9` |B |The threshold range in bfunc_4_c1 is too small |
| `4_constraint_10` |A | |
| `4_constraint_11` |B |For two different vehicles, their speeds cannot be used to infer a valid range for the product of instantaneous speed difference and direction difference |
| `4_constraint_13` |A | |
| `4_constraint_15` |A | |
| `4_constraint_16` |A | |
| `4_constraint_18` |A | |
| `4_constraint_19` |A | |
| `4_constraint_22` |B | |
| `4_constraint_24` |B |The direction threshold in bfunc_3_c1 is set too high |
| `4_constraint_25` |A | |
| `4_constraint_27` |A | |
| `4_constraint_28` |A | |
| `4_constraint_31` |A | |
| `4_constraint_32` |A | |
| `4_constraint_36` |C |The timestamps and positional relationship of two different vehicles should not affect their direction difference |
| `4_constraint_38` |A | |
| `4_constraint_42` |A | |
| `4_constraint_43` |A | |
| `4_constraint_44` |A | |
| `5_constraint_1` |A | |
| `5_constraint_3` |A | |
| `5_constraint_4` |A | |
| `5_constraint_5` |A| |
| `5_constraint_6` |A | |
| `5_constraint_7` |B |The speed difference and direction difference between two different vehicles are not correlated |
| `5_constraint_9` |B | |
| `5_constraint_10` |B | |
| `5_constraint_11` |A | |
| `5_constraint_15` |B | |
| `5_constraint_19` |A | |
| `5_constraint_21` |B |The threshold setting in bfunc_3_c1 does not match the semantic description |
| `5_constraint_24` |B |The timestamps and direction difference of two different vehicles do not impose a constraint on their speeds |
| `5_constraint_26` |A | |
| `5_constraint_27` |A | |
| `5_constraint_28` |A | |
| `5_constraint_29` |C | |
| `5_constraint_30` |C | |
| `5_constraint_31` |A | |

## Method 2

| Constraint | Rating | Notes |
|------------|--------|-------|
| `3_constraint_23` |C | |
| `3_constraint_24` |C |This constraint always returns true |
| `3_constraint_25` |B | |
| `3_constraint_27` |C |This constraint always returns true |
| `3_constraint_28` |A | |
| `3_constraint_29` |C | |
| `3_constraint_32` |C | |
| `3_constraint_33` |C | |
| `3_constraint_34` |B | |
| `3_constraint_35` |C | |
| `3_constraint_36` |C | |
| `3_constraint_41` |C | |
| `3_constraint_43` |C | |
| `3_constraint_44` |B |Only some timestamps can satisfy this constraint |
| `3_constraint_45` |C | |
| `3_constraint_46` |C |This constraint always returns true |
| `3_constraint_47` |B | |
| `3_constraint_48` |C | |
| `3_constraint_50` |B | |
| `4_constraint_1` |B | |
| `4_constraint_2` |C |This constraint always returns true |
| `4_constraint_3` |C |This constraint always returns true |
| `4_constraint_4` |C | |
| `4_constraint_5` |C | |
| `4_constraint_6` |C | |
| `4_constraint_7` |C | |
| `4_constraint_8` |C | |
| `4_constraint_9` |C | |
| `4_constraint_10` |C |Speed cannot always be greater than this value |
| `4_constraint_11` |C |Speed cannot always be greater than this value |
| `4_constraint_14` |C | |
| `4_constraint_15` |C | |
| `4_constraint_16` |C | |
| `4_constraint_17` |C | |
| `4_constraint_18` |C | |
| `4_constraint_19` |C |This constraint always returns true |
| `4_constraint_20` |C | |
| `4_constraint_21` |C | |
| `4_constraint_22` |C | |
| `4_constraint_23` |C | |
| `4_constraint_25` |C | |
| `4_constraint_28` |C | |
| `4_constraint_30` |C | |
| `4_constraint_31` |B | |
| `4_constraint_32` |C | |
| `4_constraint_33` |C | |
| `4_constraint_34` |C | |
| `4_constraint_35` |C | |
| `4_constraint_36` |C | |
| `4_constraint_37` |C | |
| `4_constraint_38` |C | |
| `4_constraint_39` |C | |
| `4_constraint_40` |C | |
| `4_constraint_41` |C | |
| `4_constraint_43` |B | |
| `4_constraint_44` |C |This constraint always returns true |
| `4_constraint_45` |C | |
| `4_constraint_46` |C | |
| `4_constraint_48` |B | |
| `4_constraint_49` |C | |
| `4_constraint_50` |C | |
| `5_constraint_5` |B | |
| `5_constraint_6` |B | |
| `5_constraint_7` |C | |
| `5_constraint_8` |B | |
| `5_constraint_9` |C | |
| `5_constraint_11` |C | |
| `5_constraint_12` |C | |
| `5_constraint_13` |B | |
| `5_constraint_14` |C | |
| `5_constraint_15` |C | |
| `5_constraint_19` |B | |
| `5_constraint_20` |C | |
| `5_constraint_21` |C | |
| `5_constraint_23` |B | |
| `5_constraint_26` |C | |
| `5_constraint_27` |B | |
| `5_constraint_28` |B | |
| `5_constraint_30` |C | |
| `5_constraint_31` |B | |
| `5_constraint_32` |B | |
| `5_constraint_34` |C | |
| `5_constraint_36` |C | |
| `5_constraint_37` |C | |
| `5_constraint_39` |C | |
| `5_constraint_40` |A | |
| `5_constraint_42` |C | |
| `5_constraint_44` |C | |
| `5_constraint_45` |C | |
| `5_constraint_46` |C | |
| `5_constraint_50` |C | |
