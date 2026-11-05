# OTB21 reproduction and saved-data audit

The preserved acquisition is in
`results/otb21_readiness_history_validation/history_20261105/`.
See [the report](../../results/otb21_readiness_history_validation/REPORT.md)
for results and limitations, and [DESIGN.md](DESIGN.md) for frozen conditions.

Run from the repository root with Python, NumPy and Numba installed. The saved
run used Python 3.12.14, NumPy 2.3.5 and Numba 0.68.1. If using this workspace's
optional package cache, add `.cache/oscillator-night-pydeps` to `PYTHONPATH`.

Audit the preserved data without importing the acquisition or dynamics modules:

```text
python experiments/otb21_readiness_history_validation/independent_audit.py
```

The audit currently targets the preserved `history_20261105` directory. It
reconstructs all 1,152 scores, input RNG, eligibility/error-state boundaries,
guard conditions and summaries. It also checks hashes and the two retained
traces using independently written e/s and radial RK4 equations. It does not
replay every T7/work trajectory or certify arbitrary integration step sizes.

For fresh acquisition, use a new output name:

```text
python experiments/otb21_readiness_history_validation/run.py --name reproduction_01
```

Existing output directories are refused. The run reads the unchanged OTB15
memory inputs and OTB19/20 policy provenance, snapshots and hashes them before
acquisition, and records every declared condition. Do not overwrite preserved
data to make a reproduction match. A new run is separate from the saved-data
audit above; that audit is not parameterized for arbitrary output names.

Generate the integration figures from saved summaries with Matplotlib installed:

```text
python scripts/plot_learning_readiness_integration.py
```

The histories and deadlines vary within the existing four-context binary task.
These data do not establish new semantic rules, a fully oscillator-based
controller, or an advantage over an optimized longer fixed wait.
