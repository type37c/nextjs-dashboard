# Wrong history and generalization — frozen acquisition/analysis plan v1.0

2026-11-06. Local pre-acquisition specification, **no external preregistration**.
Supersedes the user's unfrozen v0.1 and working v0.2. Main evaluation not yet run
when this document and its source hashes are frozen.

## Questions and population

P1: does normal-minus-removal performance remain positive for new native T7
circuits under a repeatable ancestral recalibration procedure?
P2: can a matched other-history component replace one's own component, and how
does that intervention differ from removing the component?

Pilot circuits810000–810002 are excluded. Main circuits810100–810119 are fixed
before inspecting their parameters or performance. No replacement of weak circuits.
Their native parameters are drawn by original `core.network(seed)`. Equality of
that generator's native parameters and coupling with historical circuits200–204
was checked. Calibration is re-executed per new circuit as described below.
The inferential population is this generator plus this calibration/training
procedure, not arbitrary oscillators. Seeds represent independent pseudorandom
circuit draws; topology, update equations, and task family remain fixed.

## Interventions and policies

All arms share the computation and decision window before the first preparation.
Only P's subsequent phase calculation changes:

- B0: m.
- B2_once: m − h_own; boundary h_own=m−m_ref, then decay1−eps.
- Bswap: m − (h_own−h_donor); the difference decays1−eps. This ordering makes
  self-donor sham exactly equal to B0. Neither m nor phase/cd is transplanted.
- Bconst: m − h_own + c; h_own decays but c does not.

m_ref remains the median of128 training-derived quantile thresholds. Bconst c is
one signed mean of own boundary components over the readout training cohort and
both holds per circuit, fixed before arm training. Bconst changes time course as
well as variability, so its contrast is not a pure content manipulation.

Primary policy: per-arm StandardScaler + LogisticRegression(C=3,max_iter=8000),
520 original observed features. Eight training history groups, four rows/group,
two holds512/16384, seven decisions =448 rows per arm before swap-row filtering.
Random-candidate training behavior uses the same random stream across arms.
A single-class or empty selective-training set falls back to the training-selected
fixed candidate, as in the previous pilot. Report every fallback; do not exclude it.
No refitting/tuning on evaluation. Training source differs by arm, budget does not.

Secondary fixed policy: slot1 (the second candidate) in each circuit's freshly
calibrated pair. User explicitly selected this definition. The slot is fixed
across all arms/circuits; its physical operation may differ between circuits.
No oracle policy is added to the main performance table. Counterfactual candidate
outcomes are for training labels and offline diagnostics only.

## Donors and dependence

Randomly permute whole history groups with an independent fixed donor seed, then
pair adjacent groups and swap the matching A/current-B cell. No self donor; all
training/evaluation group counts are even. This pairing is shared across holds.
A donor's boundary component is simulated from its own M history with the
recipient's exact current B and amplitude. Only that computed component enters
the intervention; donor phase, refractory and receiver states never enter P.
The recipient's future input is unchanged. Outcomes and state distances never
enter matching. No eligible donor is an acquisition error, not a row exclusion.

Donors share A, so task memory is not erased. The intervention disrupts finer
individual history matching while preserving coarse task context and current
input. The pilot found high own/donor correlations, which must be reported.
Even equal marginal component distributions cannot rule out state-compatibility
or operating-point explanations.

For every circuit/hold, report signed and absolute distributions, mean absolute
and RMS displacement, correlation, KS distances, SD ratio, and normalized mean
difference. Prespecified magnitude diagnostic: both KS distances≤.15, SD ratio
in[.8,1.25], mean difference/own SD≤.2. These are descriptive engineering bounds,
not statistical equivalence tests. Any failing cell bars the phrase 'content-only
control'; it does not trigger exclusions or replacement donors.

## Structural calibration (separate from readout budget)

Run only ancestral stages that determine parameters used here; do not replay
obsolete test cohorts or unused intermediate readout studies:

1. Original OM-2H clocked output selection: original T7 reservoir and random fixed
   coupling;256 training/64 validation timing groups; original snapshot/C/leak/
   gain/threshold grid, original tie rule. This supplies R parameters.
2. Original OM-3Q135-candidate initialization/weight grid:128 training groups for
   diagnostics,32 validation groups, original two fit holds, worst truth-cell then
   mean balanced accuracy with stable candidate order. M recurrence remains the
   specified architecture(.72,.6), P is native unit2, M native units0/1.
3. Original E7-A calibration:128 groups split64/64, original delays8/16/32,
   two-candidate selection, slow/fast relay and gate grids. Pair and D are selected
   by the original algorithm; no old circuit's selected settings are copied.
4. E7-D threshold rule: first64 groups from that training cohort, four calibration
   holds1024/3072/8192/12288, random-policy decisions1..6, quantiles i/129.
   Random choices use an equivalent iid uniform two-candidate PRNG interface;
   the historical random-number stream itself is not reused.

Both arms' physical calibration is common, chosen before intervention-specific
readouts. Calibration error stops the acquisition and is retained. No circuit is
silently dropped. Unexpected calibration failure makes the planned complete-panel
analysis unavailable until a documented new design; it is not repaired based on
main outcomes. Main code forbids overwriting an existing acquisition.

## Sample size, frozen streams, and stopping

20 main circuits,64 evaluation history groups per circuit, four rows/group,
two holds.10,240 chains/cell, eight arm×policy cells =81,920 chains. Independent
inference unit: circuit. No claim that chains, rows or holds are independent.
20 circuits is the user's proposed feasible scale, informed by prior five-circuit
heterogeneity and the three-circuit training-only feasibility/cost pilot. Neither
pilot establishes power for P2 or makes±2-point equivalence easy to demonstrate.

Circuit seeds are specified above. Calibration base9270000000 plus phase offsets
100000/200000/300000/400000/500000/600000 and circuit seed, as defined in code.
Readout train/cohort, draw, donor bases9280000000/9280100000/9280200000.
Evaluation bases9290000000/9290100000/9290200000. Add circuit seed to each.
Secondary bootstrap seed9300000000,20,000 replicates. Random training choice
seed=circuit*100+hold. No interim aggregate success inspection or adaptive stopping.
Complete all20 planned circuits once; preserve every failed attempt.

## Primary inference and multiple comparisons

Average each circuit's all-seven success over its rows and both holds. Form
paired circuit-level differences. Report mean, SD/SE, individual circuits and
ordinary95% Student-t intervals(df19). These are approximate distributional
inferences across20 circuits, not exact finite-sample guarantees.

There are two scientific questions but **five inferential claims**. Use one Holm
family at alpha.05 over these five p-values; do not apply Holm only to two chosen
claims after looking at results:

1. P1: B0>B2. Two-sided paired-circuit t p-value, accepted only in positive direction.
2. P2-harm: Bswap<B2. Two-sided p-value, accepted only in negative direction.
3. P2-own: B0>Bswap. Two-sided p-value, accepted only in positive direction.
4. P2-eq-removal: Bswap equivalent to B2 within±.02 absolute success probability.
5. P2-eq-normal: Bswap equivalent to B0 within±.02.

For each equivalence claim use TOST on circuit differences, p=max(lower-bound
one-sided p, upper-bound one-sided p), then include that p in the Holm family.
Do not treat failure to reject equality as equivalence. The standard unadjusted
TOST corresponds to a90% interval, not a95% interval; ordinary95% descriptive
intervals are not Holm-adjusted decision intervals. All raw/adjusted p-values and
flags are saved. A zero-variance sample is flagged; conservative p=1 and no primary
claim, rather than inventing certainty. Holm tests are the primary decision rule.

Margin±2points is a substantive tolerance proposed in v0.1 and adopted before
main acquisition. It is roughly half the earlier4.08-point estimate and small
relative to substantial pilot cross-arm variation. This motivates a scale, not a
universal or statistically estimated equivalence threshold. Report the entire
interval so readers can judge the margin. Do not retune it to pass.

## Interpretation rules (corrected from v0.1)

- P1 not supported: generalization of positive advantage is not established;
  keep the previous claim conditional on five historical circuits. This is not
  proof of no effect. The previous three-point criterion remains unmet.
- Bswap≈B2: replacement did not recover a distinction from removal at this margin.
  This does **not** show a generic history-like bias is sufficient. Interpret
  alongside B0−Bswap and P1, without calling it content or operating-point proof.
- Bswap<B2: foreign contribution is harmful under this pairing. Content mismatch
  and compatibility with other retained states remain competing explanations.
- B0>Bswap: own component has a conditional advantage over this matched donor,
  not a demonstration of semantic content or intelligence.
- Bswap≈B0: donor replacement is tolerated within the chosen margin and matching
  class. Withdraw a claim that this individual's fine history is necessary here;
  do not say 'any past works', since A/current input remain matched.
- Both equivalences supported: the alternatives are not mechanistically separated
  at the chosen resolution. Multiple flags are reported; do not force mutually
  exclusive causal stories. No flag: unresolved.

## Secondary analyses

Bswap−Bconst; policy×B0/B2 interaction; A0/A1, hold and next-step contrasts;
actual-input candidate absence/selection failure and four-probe joint readiness
with separate denominators. All descriptive; no promotion after primary failure.
Within-circuit bootstrap resamples **two-group donor blocks**, not single groups,
conditional on frozen fitted models. This change from v0.1 preserves donor-induced
dependence. Do not compare per-policy failure compositions as a same-state causal
mediation analysis.

## Integrity and audits

NPZ input files and individual SHA256 sidecars are written immediately upon
creation, before corresponding simulations. Model/calibration hashes are sealed
per circuit before its evaluation cohort is generated. Full source/protocol/hash
freeze precedes any main-circuit calibration or outcome acquisition.
Available historical two-rail initial-phase records plus named generated cohorts
are inventoried. Rounded12-decimal phase-pair fingerprints are a broader duplicate
screen than complete history-token equality. Pilot phases are reserved too.
New canonical structural-training/readout-training/evaluation cohorts are checked
against that registry and each other under a file lock before simulation.
Unsupported record shapes and inaccessible/remote histories are explicit; no
claim that every past cohort in every branch was audited. Separate literal seed
and circuit-ID checks are recorded.

All rows: independent scoring from saved R event counts and A/B targets, agreement
with stored correct flags and actual-input counterfactual predictions, common
preintervention states, finite arrays, donor pairing, component equations,
constant persistence, fixed slot1, observed shadow reconstruction and hashes.
Separate scalar replay fixed before acquisition: circuits810100/810119, both holds,
all four arms, refit/fixed, decisions0/3/6, rows0/3:192 preparation/query trajectories.
Also replay128 own/donor first-boundary states. This is within-project numerical
checking, not an external independent replication.

## Scope and reporting

No B3, C3 rescue, continual learning/retention, LIF superiority, real hardware,
semantic-memory erasure or intelligence-seed identification is tested. Save pilot,
main, secondary and exploratory material separately. Report training fallback,
calibration feasibility, costs and non-identifiability alongside successes.
Only observed interpretation branches may enter the paper.
