# Examples

The following examples illustrate possible cases for Level A, Level B, and Level C. They are provided for reference.

---

## A-1

**`constraint.json`**

```json
{
  "semantics": "For any two vehicle records v1 and v2, if they belong to the same vehicle and are adjacent records of that vehicle, then the ratio between their geographic displacement, computed using the Haversine distance, and their timestamp difference should not exceed a reasonable speed upper bound.",
  "structure": "forall v1 in dataset (forall v2 in dataset (bfunc1(v1, v2) and bfunc2(v1, v2) implies bfunc3(v1, v2)))",
  "bfuncs": [
    {
      "id": "bfunc1",
      "parameters": ["v1", "v2"],
      "semantics": "v1 and v2 belong to the same vehicle",
      "implementation": "v1.carid == v2.carid",
      "restrictions": []
    },
    {
      "id": "bfunc2",
      "parameters": ["v1", "v2"],
      "semantics": "v1 and v2 are adjacent records of that vehicle",
      "implementation": "abs(v1.grpid - v2.grpid) == 1",
      "restrictions": []
    },
    {
      "id": "bfunc3",
      "parameters": ["v1", "v2"],
      "semantics": "the ratio between the Haversine displacement of v1 and v2 and their timestamp difference does not exceed a reasonable speed upper bound",
      "implementation": "(6371.0 × 2 × atan2(sqrt(sin(radians(v2.latitude - v1.latitude) ÷ 2) × sin(radians(v2.latitude - v1.latitude) ÷ 2) + cos(radians(v1.latitude)) × cos(radians(v2.latitude)) × sin(radians(v2.longitude - v1.longitude) ÷ 2) × sin(radians(v2.longitude - v1.longitude) ÷ 2)), sqrt(1 - (sin(radians(v2.latitude - v1.latitude) ÷ 2) × sin(radians(v2.latitude - v1.latitude) ÷ 2) + cos(radians(v1.latitude)) × cos(radians(v2.latitude)) × sin(radians(v2.longitude - v1.longitude) ÷ 2) × sin(radians(v2.longitude - v1.longitude) ÷ 2))))) ÷ (v2.timestamp - v1.timestamp) × 3600 <= NTHRESHOLD1",
      "restrictions": []
    }
  ]
}
```

**`bfuncs_*.py`**

```python
from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['carid'] == var_bindings['v2']['carid']

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['grpid'] - var_bindings['v2']['grpid']) == 1

def bfunc_3_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return 6371.0 * 2 * atan2(sqrt(sin(radians(var_bindings['v2']['latitude'] - var_bindings['v1']['latitude']) / 2) * sin(radians(var_bindings['v2']['latitude'] - var_bindings['v1']['latitude']) / 2) + cos(radians(var_bindings['v1']['latitude'])) * cos(radians(var_bindings['v2']['latitude'])) * sin(radians(var_bindings['v2']['longitude'] - var_bindings['v1']['longitude']) / 2) * sin(radians(var_bindings['v2']['longitude'] - var_bindings['v1']['longitude']) / 2)), sqrt(1 - (sin(radians(var_bindings['v2']['latitude'] - var_bindings['v1']['latitude']) / 2) * sin(radians(var_bindings['v2']['latitude'] - var_bindings['v1']['latitude']) / 2) + cos(radians(var_bindings['v1']['latitude'])) * cos(radians(var_bindings['v2']['latitude'])) * sin(radians(var_bindings['v2']['longitude'] - var_bindings['v1']['longitude']) / 2) * sin(radians(var_bindings['v2']['longitude'] - var_bindings['v1']['longitude']) / 2)))) / (var_bindings['v2']['timestamp'] - var_bindings['v1']['timestamp']) * 3600 <= 2916311760943289/8796093022208
```

**Level**: A

> This constraint is interpretable: it checks adjacent records from the same vehicle, computes the GPS-implied speed from geographic displacement and timestamp difference, and requires that speed to stay below an upper bound. It also expresses a substantive environmental condition because it captures whether consecutive taxi positions are physically consistent. The condition is physically plausible in the current scenario, since abnormal position jumps would imply unrealistically high movement speed. Therefore, it is assigned Level A.

---

## B-1

**`constraint.json`**

```json
{
  "semantics": "For any vehicle record v1, if the speed of v1 is significantly lower than a threshold, then the absolute direction difference between v1 and its next record v2 should not exceed a reasonable range, and the timestamp difference between v1 and v2 should not exceed a reasonable time range.",
  "structure": "forall v1 in dataset (bfunc1(v1) implies (exists v2 in dataset (bfunc2(v1, v2) and bfunc3(v1, v2) and bfunc4(v1, v2))))",
  "bfuncs": [
    {
      "id": "bfunc1",
      "parameters": ["v1"],
      "semantics": "the speed of v1 is significantly lower than a threshold",
      "implementation": "v1.speed < NTHRESHOLD1",
      "restrictions": ["NTHRESHOLD1 <= 30"]
    },
    {
      "id": "bfunc2",
      "parameters": ["v1", "v2"],
      "semantics": "v2 is the next record of v1",
      "implementation": "v2.grpid == v1.grpid + 1 && v2.carid == v1.carid",
      "restrictions": []
    },
    {
      "id": "bfunc3",
      "parameters": ["v1", "v2"],
      "semantics": "the absolute direction difference between v1 and v2 does not exceed a reasonable range",
      "implementation": "abs(v1.direction - v2.direction) <= NTHRESHOLD2",
      "restrictions": []
    },
    {
      "id": "bfunc4",
      "parameters": ["v1", "v2"],
      "semantics": "the timestamp difference between v1 and v2 does not exceed a reasonable time range",
      "implementation": "v2.timestamp - v1.timestamp <= NTHRESHOLD3",
      "restrictions": []
    }
  ]
}
```

**`bfuncs_*.py`**

```python
from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['speed'] < 0

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['grpid'] == var_bindings['v1']['grpid'] + 1

def bfunc_2_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['carid'] == var_bindings['v1']['carid']

def bfunc_3_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['direction'] - var_bindings['v2']['direction']) <= 45

def bfunc_4_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['timestamp'] - var_bindings['v1']['timestamp'] <= 281
```

**Level**: B

> The intended condition is interpretable and substantive: for a low-speed vehicle, the direction change and time interval between adjacent records should remain within reasonable ranges. This idea is physically plausible in the taxi scenario. However, `bfuncs_*.py` shows that the precondition is implemented as `v1.speed < 0`, meaning that the threshold was instantiated as 0. Since the speed field ranges from 0.0 to 250.0, this condition never holds in the data, so the implication becomes vacuously true. The constraint therefore has a reasonable intended meaning but a clear implementation issue that weakens the expressed condition. It is assigned Level B.

---

## B-2

**`constraint.json`**

```json
{
  "semantics": "For any record v1 in the dataset, v1.longitude is smaller than sqrt(abs(13250.688)).",
  "structure": "forall v1 in dataset (bfunc1(v1))",
  "bfuncs": [
    {
      "id": "bfunc1",
      "parameters": ["v1"],
      "semantics": "v1.longitude is smaller than sqrt(abs(13250.688))",
      "implementation": "var_bindings['v1']['longitude'] < sqrt(abs(abs(1656336/125)))"
    }
  ]
}
```

**`bfuncs_*.py`**

```python
from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['longitude'] < sqrt(abs(abs(1656336/125)))
```

**Level**: B

> This constraint is interpretable as a longitude upper-bound check, and such a bound can express a substantive geographic condition for taxi records. Since `sqrt(13250.688)` is approximately 115.1 degrees, the resulting value can be physically plausible for taxi data from a Chinese city. However, expressing a simple geographic threshold as `sqrt(abs(13250.688))` is indirect and makes the condition less transparent. The constraint mostly satisfies the two questions, but the expression introduces uncertainty about the intended environmental meaning. It is assigned Level B.

---

## C-1

**`constraint.json`**

```json
{
  "semantics": "For any record v1 in the dataset, v1.latitude is greater than abs(abs(add(div(v1.speed, v1.speed), log(v1.timestamp)))).",
  "structure": "forall v1 in dataset (bfunc1(v1))",
  "bfuncs": [
    {
      "id": "bfunc1",
      "parameters": ["v1"],
      "semantics": "v1.latitude is greater than abs(abs(add(div(v1.speed, v1.speed), log(v1.timestamp))))",
      "implementation": "var_bindings['v1']['latitude'] > abs(abs(((1 if -1/1000 <= (var_bindings['v1']['speed']) <= 1/1000 else (var_bindings['v1']['speed']) / (var_bindings['v1']['speed'])) + (0 if abs(var_bindings['v1']['timestamp']) < 1/1000 else log(abs(var_bindings['v1']['timestamp']))))))"
    }
  ]
}
```

**`bfuncs_*.py`**

```python
from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['latitude'] > abs(abs(((1 if -1/1000 <= (var_bindings['v1']['speed']) <= 1/1000 else (var_bindings['v1']['speed']) / (var_bindings['v1']['speed'])) + (0 if abs(var_bindings['v1']['timestamp']) < 1/1000 else log(abs(var_bindings['v1']['timestamp']))))))
```

**Level**: C

> This constraint is not meaningfully interpretable as an environmental condition. It compares latitude with a complex expression involving speed and timestamp, but latitude, speed, and timestamp have different units and meanings and do not have a physically meaningful ordering of this form. As a result, the constraint does not express a substantive environmental condition and is not physically plausible in the current scenario. It is assigned Level C.

---

## A-2

**`constraint.json`**

```json
{
  "semantics": "For any two vehicle records v1 and v2, if they belong to the same vehicle, are adjacent records of that vehicle, and both have speeds significantly higher than a threshold, then their absolute direction difference should be smaller than a relatively small reasonable range.",
  "structure": "forall v1 in dataset (forall v2 in dataset (((bfunc1(v1, v2) and bfunc2(v1, v2)) and bfunc3(v1, v2)) implies bfunc4(v1, v2)))",
  "bfuncs": [
    {
      "id": "bfunc1",
      "parameters": [
        "v1",
        "v2"
      ],
      "semantics": "v1 and v2 belong to the same vehicle",
      "implementation": "v1.carid == v2.carid",
      "restrictions": []
    },
    {
      "id": "bfunc2",
      "parameters": [
        "v1",
        "v2"
      ],
      "semantics": "v1 and v2 are adjacent records of that vehicle",
      "implementation": "abs(v1.grpid - v2.grpid) == 1",
      "restrictions": []
    },
    {
      "id": "bfunc3",
      "parameters": [
        "v1",
        "v2"
      ],
      "semantics": "both v1 and v2 have speeds significantly higher than a threshold",
      "implementation": "v1.speed > NTHRESHOLD1 && v2.speed > NTHRESHOLD1",
      "restrictions": [
        "NTHRESHOLD1 >= 60"
      ]
    },
    {
      "id": "bfunc4",
      "parameters": [
        "v1",
        "v2"
      ],
      "semantics": "the absolute direction difference between v1 and v2 is smaller than a relatively small reasonable range",
      "implementation": "abs(v1.direction - v2.direction) <= NTHRESHOLD2",
      "restrictions": []
    }
  ]
}
```

**`bfuncs_*.py`**

```python
from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['carid'] == var_bindings['v2']['carid']

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['grpid'] - var_bindings['v2']['grpid']) == 1

def bfunc_3_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['speed'] > 93

def bfunc_3_c2(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['speed'] > 93

def bfunc_4_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return abs(var_bindings['v1']['direction'] - var_bindings['v2']['direction']) <= 45
```

**Level**: A

> This constraint is interpretable: for two adjacent records of the same vehicle, if both speeds are above 93 km/h, the direction change should not exceed 45 degrees. It expresses a substantive environmental condition about high-speed vehicle movement. The condition is physically plausible in the current scenario because sharp turns at high speed are unlikely and unsafe. The preconditions and conclusion are coherent, and the implementation matches the semantics. Therefore, it is assigned Level A.

---

## B-3

**`constraint.json`**

```json
{
  "semantics": "For any two records v1 and v2 from the same vehicle, v1.timestamp is greater than add(-5828.477, v2.timestamp).",
  "structure": "forall v1 in dataset (forall v2 in dataset ((bfunc1(v1, v2) implies bfunc2(v1, v2))))",
  "bfuncs": [
    {
      "id": "bfunc1",
      "parameters": [
        "v1",
        "v2"
      ],
      "semantics": "v1 and v2 belong to the same vehicle, i.e., they have the same carid",
      "implementation": "var_bindings['v1']['carid'] == var_bindings['v2']['carid']"
    },
    {
      "id": "bfunc2",
      "parameters": [
        "v1",
        "v2"
      ],
      "semantics": "v1.timestamp is greater than add(-5828.477, v2.timestamp)",
      "implementation": "var_bindings['v1']['timestamp'] > (-5828477/1000 + var_bindings['v2']['timestamp'])"
    }
  ]
}
```

**`bfuncs_*.py`**

```python
from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['carid'] == var_bindings['v2']['carid']

def bfunc_2_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v1']['timestamp'] > (-5828477/1000 + var_bindings['v2']['timestamp'])
```

**Level**: B

> This constraint is interpretable as a timestamp-gap condition between records of the same vehicle. Bounding time gaps can be a substantive environmental condition in some taxi-record settings. However, this constraint applies to all pairs of records from the same vehicle rather than adjacent records, which effectively implies that all records of the same vehicle should fall within about 97 minutes. That condition may be too strict for a taxi operating over a long period. Therefore, the constraint has a plausible idea but a clear concern about physical plausibility in the current scenario. It is assigned Level B.

---

## C-2

**`constraint.json`**

```json
{
  "semantics": "For any two records v1 and v2 in the dataset, v2.latitude is smaller than div(v1.longitude, log(max(v2.longitude, max(sin(mul(v1.direction, v1.timestamp)), log(sqrt(v1.latitude)))))).",
  "structure": "forall v1 in dataset (forall v2 in dataset (bfunc1(v1, v2)))",
  "bfuncs": [
    {
      "id": "bfunc1",
      "parameters": [
        "v1",
        "v2"
      ],
      "semantics": "v2.latitude is smaller than div(v1.longitude, log(max(v2.longitude, max(sin(mul(v1.direction, v1.timestamp)), log(sqrt(v1.latitude))))))",
      "implementation": "var_bindings['v2']['latitude'] < (1 if -1/1000 <= ((0 if abs(max(var_bindings['v2']['longitude'], max(sin((var_bindings['v1']['direction'] * var_bindings['v1']['timestamp'])), (0 if abs(sqrt(abs(var_bindings['v1']['latitude']))) < 1/1000 else log(abs(sqrt(abs(var_bindings['v1']['latitude'])))))))) < 1/1000 else log(abs(max(var_bindings['v2']['longitude'], max(sin((var_bindings['v1']['direction'] * var_bindings['v1']['timestamp'])), (0 if abs(sqrt(abs(var_bindings['v1']['latitude']))) < 1/1000 else log(abs(sqrt(abs(var_bindings['v1']['latitude']))))))))))) <= 1/1000 else (var_bindings['v1']['longitude']) / ((0 if abs(max(var_bindings['v2']['longitude'], max(sin((var_bindings['v1']['direction'] * var_bindings['v1']['timestamp'])), (0 if abs(sqrt(abs(var_bindings['v1']['latitude']))) < 1/1000 else log(abs(sqrt(abs(var_bindings['v1']['latitude'])))))))) < 1/1000 else log(abs(max(var_bindings['v2']['longitude'], max(sin((var_bindings['v1']['direction'] * var_bindings['v1']['timestamp'])), (0 if abs(sqrt(abs(var_bindings['v1']['latitude']))) < 1/1000 else log(abs(sqrt(abs(var_bindings['v1']['latitude']))))))))))))"
    }
  ]
}
```

**`bfuncs_*.py`**

```python
from math import *
from typing import Any

def bfunc_1_c1(var_bindings: dict[str, dict[str, Any]]) -> bool:
    return var_bindings['v2']['latitude'] < (1 if -1/1000 <= ((0 if abs(max(var_bindings['v2']['longitude'], max(sin((var_bindings['v1']['direction'] * var_bindings['v1']['timestamp'])), (0 if abs(sqrt(abs(var_bindings['v1']['latitude']))) < 1/1000 else log(abs(sqrt(abs(var_bindings['v1']['latitude'])))))))) < 1/1000 else log(abs(max(var_bindings['v2']['longitude'], max(sin((var_bindings['v1']['direction'] * var_bindings['v1']['timestamp'])), (0 if abs(sqrt(abs(var_bindings['v1']['latitude']))) < 1/1000 else log(abs(sqrt(abs(var_bindings['v1']['latitude']))))))))))) <= 1/1000 else (var_bindings['v1']['longitude']) / ((0 if abs(max(var_bindings['v2']['longitude'], max(sin((var_bindings['v1']['direction'] * var_bindings['v1']['timestamp'])), (0 if abs(sqrt(abs(var_bindings['v1']['latitude']))) < 1/1000 else log(abs(sqrt(abs(var_bindings['v1']['latitude'])))))))) < 1/1000 else log(abs(max(var_bindings['v2']['longitude'], max(sin((var_bindings['v1']['direction'] * var_bindings['v1']['timestamp'])), (0 if abs(sqrt(abs(var_bindings['v1']['latitude']))) < 1/1000 else log(abs(sqrt(abs(var_bindings['v1']['latitude']))))))))))))
```

**Level**: C

> This constraint is not meaningfully interpretable as an environmental condition. It compares the latitude of v2 with a complex expression that mixes longitude, direction, timestamp, and latitude from different records. These fields represent different physical quantities, including geographic coordinates, heading angle, and time. Combining them through these operations and comparing the result with latitude does not express a substantive environmental condition and is not physically plausible in the current scenario. It is assigned Level C.
