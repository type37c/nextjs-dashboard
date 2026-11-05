# Learning Readiness

Research code and data, hosted at [`type37c/nextjs-dashboard`](https://github.com/type37c/nextjs-dashboard). The repository URL retains the name of an archived tutorial; the current project is Learning Readiness.

**When should a memory system accept its next learning signal?**

A small, reproducible numerical study of interference in an oscillator-coupled memory system. Residual activity from an earlier query can route a later teaching signal into an unrelated memory. Waiting for a state-based retention condition before the next query preserves old relations while allowing the new relation to be learned.

This repository packages the OTB21 experiment from Keisuke Ohtani's oscillator research. It is an exploratory mechanism study with deliberately simple binary tasks, designed to make its assumptions, failures, and computational costs inspectable.

![Retention and time cost](figures/retention-cost.png)

## Main result

Each cell below contains 128 paired conditions (eight saved memories × four initial phases × two previous contexts × two current contexts). These are **not 128 independent tasks or worlds**.

| Query duration | Immediate update: old relation retained | Fixed 4,096-step wait | State-based wait |
|---:|---:|---:|---:|
| 1,536 | 64/128 | 64/128 | 128/128 |
| 2,048 | 64/128 | 64/128 | 128/128 |
| 4,096 | 64/128 | 128/128 | 128/128 |

The new relation was learned in **128/128 conditions for every policy and duration**. For the shortest query, average total time was 14,632 / 18,728 / 30,040.25 simulation steps, respectively. The state-based policy buys retention with additional time. An optimized longer fixed wait has not been ruled out.

## Run it

Python 3.12; CPU only. No API key, GPU, private repository access, or model download is required.

```bash
git clone https://github.com/type37c/nextjs-dashboard.git learning-readiness
cd learning-readiness
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/plot_results.py
python experiments/otb21_readiness_history_validation/independent_audit.py
```

The plot is recalculated from the saved trial records. The audit checks all 1,152 trial scores, the input RNG, saved eligibility/error-state boundaries, source hashes, guard conditions, and two retained radial traces. It does **not** independently rerun every T7 trajectory.

For a fresh simulation, use a new output directory name:

```bash
python experiments/otb21_readiness_history_validation/run.py --name reproduction_01
```

The first run includes Numba compilation. Existing output directories are refused. Fresh acquisition starts from the eight included learned memory states; it does not repeat their earlier OTB15 training. The original audit targets the preserved run, not arbitrary new output directories. See [reproduction](docs/REPRODUCTION.md).

## Mechanism

1. A query produces T7 firing and leaves a decaying eligibility trace `e` on the used memory route.
2. A later teaching error enters an error accumulator `s`, weighted by that trace.
3. The accumulator tilts a bistable amplitude memory, changing later T7 responses.
4. Residual traces from previous queries can therefore modify unrelated memories.
5. Before the next query, the guard waits until non-target traces satisfy a sufficient retention bound. The new query then establishes its own fresh trace.

The T7 dynamics, bistable memory, and learning rule are fixed across the three policies. Preparation timing changes. [Model and assumptions](docs/METHOD.md).

## What this establishes—and what remains open

- In this constructed task, a state-based waiting condition preserves existing relations across the tested phase/duration changes while learning a changed relation.
- The mechanism includes externally computed teaching errors, routing, and preparation control. It is not a fully oscillator-implemented autonomous learner.
- Feature relevance and context routing are supplied. No semantic concepts or unknown causal structures are discovered.
- This release does not establish oscillator superiority, hardware efficiency, large-scale continual learning, or a general solution to forgetting.
- The study used pilot-informed choices and locally frozen hashes. It was not externally preregistered or independently certified.

## Collaborate

Useful next experiments are concrete: compare against an equally slow optimized fixed wait; find a tighter finite-time retention condition; test longer mixed-context streams; compare against a matched non-oscillatory memory. See [contribution guide](CONTRIBUTING.md) for proposed experiments and reporting requirements.

## Evidence and provenance

- [English method](docs/METHOD.md) and [Japanese overview](docs/README.ja.md)
- [Original Japanese report](results/otb21_readiness_history_validation/REPORT.md) and [frozen design](experiments/otb21_readiness_history_validation/DESIGN.md)
- Original records, boundary states, two traces, and source snapshots are included under `results/`.
- [Source provenance and AI assistance](docs/PROVENANCE.md). Original internal study labels are retained so source hashes remain auditable.

This is an independent research project. No institutional endorsement is implied.

## Rights

No open-source license has yet been selected by the author. Public visibility alone does not grant a general redistribution or modification license. License selection remains a release decision; do not assume MIT or Apache terms.
