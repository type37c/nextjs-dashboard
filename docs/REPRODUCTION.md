# Reproduction levels

1. **Replot:** `python scripts/plot_results.py` aggregates original trial records, asserts 128 conditions per group and correct new-context learning, and writes PNG/SVG figures.
2. **Saved-data audit:** `python experiments/otb21_readiness_history_validation/independent_audit.py` verifies 1,152 scores, 64 previous queries, input generation, source snapshots, saved state recurrences and two radial traces. It writes `audit_independent.json`; running it may change that generated file's byte formatting.
3. **Fresh simulation:** `python experiments/otb21_readiness_history_validation/run.py --name reproduction_01` runs the original frozen acquisition on the bundled eight learned memory states. Use a unique alphanumeric/underscore name. It creates records, summary, snapshots and selected traces. It checks the prior source hashes before proceeding.

Use Python 3.12 and the pinned requirements. Run from the repository root. Keep the original `history_20261105` acquisition unchanged. The frozen scripts use the historical directory layout deliberately, including a local Numba cache ignored by Git.

The eight OTB15 learned memory inputs are data dependencies. Re-training OTB15 is outside this focused release. The OTB19 runner is included as an imported helper; OTB19's complete experiment is outside this release. Original Japanese archive documents may mention sibling studies that are not bundled.

A new simulation is not a fresh scientific confirmation: it reuses the same memories, phase RNG, task family, and policy choices. For new evidence, preregister new conditions and comparisons before running them.

## Release validation (2026-11-05)

A fresh full acquisition completed in the release workspace using the pinned environment. All 1,152 record dictionaries and 64 old-query dictionaries matched the original exactly. Arrays in `states.npz`, `old_states.npz`, `inputs.npz`, and both retained trace files matched within rtol=atol=2e-12; they were not all bitwise identical. The machine-readable report records maximum absolute errors. The saved-data audit also passed. See [machine-readable validation](RELEASE_VALIDATION.json). This is same-input reproduction, not confirmation on new scientific conditions.
