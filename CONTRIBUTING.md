# Collaborating on Oscillator Mind

Reproductions, counterexamples, comparative models and clearer explanations are welcome. Start with the [research map](docs/RESEARCH_MAP.md); OTB21 is the currently runnable study.

## Questions by research direction

- **Individual dynamics:** characterize how m-to-phase coupling and the refractory rule change observability and response. Compare matched history-dependent alternatives before attributing an effect specifically to T7.
- **Network computation:** identify where distinctions are lost between retained state, firing and receiver response. Keep information preservation separate from downstream task success.
- **Continual computation and learning:** compare OTB21 against an equally slow optimized fixed wait; tighten finite-time retention bounds; test longer mixed-context streams. Measure target learning and non-target retention separately.
- **Experience sharing:** package a reproducible minimal sharing example, test conflicting testimony and communication delays, and distinguish joint use from recipient learning. The included OTB22 report is a starting point, not a complete public code package.

## A useful first experiment

Calibrate fixed waits on separate streams and compare them against the OTB21 guard on held-out histories at matched total time. A longer fixed wait may explain the entire benefit. Preserve that result if it occurs.

Before collecting evaluation data, record the question, settings, split unit, baseline, success rule and compute budget. Do not count repeated phases as independent worlds. Put new experiments in new directories and retain original source snapshots. State which code and reasoning used AI assistance and how they were checked.

For bug reports, include dependency versions, exact command, expected versus actual behavior and a minimal reproduction. Hosted CI currently cannot start because of an account-level restriction; [local validation and CI status](docs/CI_STATUS.md) are documented separately.

The reuse license remains pending author selection. Discuss proposed reuse with the author until a license is added; no permissive grant is implied by this contribution guide.
