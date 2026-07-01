# Dataset Fields

| Field | Type | Unit | Description |
|------|------|------|-------------|
| `id` | int | - | Unique identifier of a context record. |
| `grpid` | int | - | The sequence index of a record within the same taxi. Consecutive reports from the same taxi have consecutive `grpid` values. |
| `carid` | str | - | Unique identifier of a taxi. |
| `timestamp` | float | second (s) | UNIX timestamp of the record. |
| `longitude` | float | degree | Geographic longitude of the taxi. |
| `latitude` | float | degree | Geographic latitude of the taxi. |
| `speed` | float | kilometer/hour (km/h) | Instantaneous scalar speed of the taxi. |
| `direction` | float | degree | Heading angle of the taxi, with 0 degrees indicating north and values increasing clockwise. |
