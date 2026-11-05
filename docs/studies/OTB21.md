# OTB21 — Learning readiness

**Place in the program:** continual computation and learning. This experiment asks when a system whose state contains previous query activity should accept the next learning signal.

A query leaves eligibility on its route. A later label for a different query can update both the intended memory and an unrelated older route. Waiting before the new query reduces the old trace while allowing the current input to create a fresh one.

The comparison uses immediate updating, a fixed 4,096-step wait, and a state-based retention condition. There are 1,152 paired conditions. For query durations 1,536 and 2,048, old-relation retention is 64/128 with either immediate updating or the fixed wait, versus 128/128 with the guard. At duration 4,096, the fixed wait also achieves 128/128. Every group learns the changed relation in 128/128 conditions.

The guard's mean waiting cost is 15,408.25 steps. For the shortest query the total time rises from 14,632 to 30,040.25 steps. This motivates matched-time fixed controls rather than a claim of general adaptive superiority.

- [Mechanism and sufficient condition](../METHOD.md)
- [Exact original design](../../experiments/otb21_readiness_history_validation/DESIGN.md)
- [Original report](../../results/otb21_readiness_history_validation/REPORT.md)
- [Reproduction commands and scope](../REPRODUCTION.md)
- [Recorded release reproduction](../RELEASE_VALIDATION.json)

All formulas and scientific source snapshots remain unchanged in the public presentation update. The study is a finite binary task with supplied feature routing, an external teaching signal, and externally evaluated preparation control.
