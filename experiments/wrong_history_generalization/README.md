# Wrong history and generalization

This experiment tests an own-history contribution, a matched donor replacement,
and transfer to new native circuits. It does not identify a seed of intelligence.

- [Acquisition and analysis plan](PLAN.md): locally fixed before acquisition;
  no external registration.
- [Training-only pilot](PILOT_REPORT.md): three circuits, excluded from evaluation.
- [Source freeze](FREEZE.json): source commit `eb61938`, sealed in `0862365`.
- [Runtime](RUNTIME.json): Python and numerical package versions.
- Results: `../../results/wrong_history_generalization/main/`.

The primary inference unit is a circuit, not a chain. Twenty circuits are drawn
from the original generator and each undergoes the ancestral calibration process.
There are four arms and two policies. Fixed policy means the second slot of each
circuit's calibrated pair; the actual operation can vary across circuits.

Read `analysis.json` for primary tests and descriptive secondary results;
`saved_data_audit.json` and `dynamics_audit.json` document verification.
`chains.csv.gz` contains one row per chain; `decisions.csv.gz` contains each next
decision and both candidates' diagnostic outcomes. NPZ files preserve all saved
states/features/event counts. `evaluation_donors.npz` in each circuit directory
is the full donor correspondence, including groups and block identifiers. There
are no exclusions or donor substitutions based on outcomes.

## Reproduce

Use an isolated checkout of commit `0862365` (or the full commit carrying that
prefix). It contains pilot data and the frozen historical registry, but no main
acquisition. Do not overwrite an existing result directory. Install the versions
in `RUNTIME.json` under Python 3.12. The acquisition checks all frozen hashes and
refuses to run if the main output directory already exists.

```sh
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
python experiments/wrong_history_generalization/workflow.py main
python experiments/wrong_history_generalization/analyse.py
python experiments/wrong_history_generalization/audit_dynamics.py
```

The final results commit additionally supplies `publish.py` for presentation and
CSV export. This script is outside the pre-acquisition freeze and does not define
any inferential decision. Run it only after both audits pass:

```sh
python experiments/wrong_history_generalization/publish.py
```

Never rerun acquisition merely to improve a result. Report a failed run and design
a separately identified protocol if a technical error requires changes.

## What is and is not controlled

Donors match A, current B and exact current amplitude. Their P history component
is recomputed using the recipient's current input, with a paired derangement of
history groups. No phase, refractory state or receiver state is transplanted.
High own/donor correlations in the pilot limit the strength of a content claim.
Matching marginal scales does not establish equal compatibility with other state.

The literal seed check covers locally available tracked text. Phase fingerprint
checks cover compatible local two-rail records plus explicitly named cohorts;
unsupported shapes and unavailable remote histories are listed. This is not a
claim that every historical branch was audited. Scalar replay is a separate
implementation within this project, not an external independent replication.

Elapsed worker times include contention from four parallel processes. Structural
calibration, readout fitting and numerical query budgets should not be confused
with hardware efficiency. Old saved sklearn objects emit a version warning on
import; native-generator and parent-trajectory parity were checked, and new
readouts use the recorded runtime. No old circuit's fitted readout is used as the
main policy on a new circuit.
