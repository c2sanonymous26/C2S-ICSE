# Scenario Description

The target application scenario concerns taxi management, including the backend software platform and the surrounding taxi operation environment. Each taxi continuously reports its driving state to the backend platform through an onboard collector. A reported context records the status of a taxi at a specific moment, including its location, speed, direction, and related identifiers.

The backend platform aggregates these reported contexts into context sequences and uses them to support downstream services such as dispatching, abnormal-behavior analysis, and route planning. A useful constraint should therefore describe a reasonable property of individual taxi contexts or relationships among contexts in a context sequence.
