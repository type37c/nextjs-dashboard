# Contributing

Reproductions, counterexamples, matched baselines, and narrower claims are welcome.

Useful first contributions:

- **Equal-time fixed baseline:** choose fixed waits on separate calibration streams, then compare against the guard on held-out histories at matched total time. A longer wait may explain the entire benefit.
- **Finite-time bound:** reduce unnecessary waiting while checking target learning and non-target retention separately.
- **Stream stress test:** vary context order, inter-query time, label delay and noise. Preserve failures and report every declared condition.
- **Matched non-oscillatory baseline:** retain equivalent memory and teaching information; report state count, update work and accuracy rather than inferring hardware power from Python runtime.

Before collecting evaluation data, record the question, frozen settings, split unit, baseline, success rule and compute budget. Do not count repeated phases as independent worlds. New experiments belong in new directories; do not overwrite preserved source snapshots or results. State which code and reasoning were produced with AI assistance and how they were checked.

For a bug report, include Python/dependency versions, the exact command, expected versus actual behavior and a minimal reproduction. Do not include credentials or private datasets.
