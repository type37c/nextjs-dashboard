# Own history, matched donor history, and new circuits

Evidence addendum, 6 November 2026. This extends the earlier five-circuit case
study without changing its unmet three-point minimum-effect decision. It is an
insertion draft, not an introduction or a completed submission.

## Design and inferential scope

We addressed two remaining questions: whether the positive normal-minus-removal
difference extends to new circuits, and whether a matched foreign history
component can replace the processor's own component. Three new circuits were
used for a training-only feasibility pilot. We then fixed the protocol, source
hashes, circuit IDs, streams, sample size and analysis before acquiring a separate
set of 20 circuits. This was local pre-acquisition specification, not external
preregistration. We completed the fixed panel once without outcome-based circuit
replacement or additional acquisition.

Each new circuit was drawn from the original native generator and underwent the
ancestral calibration procedure, including physical weights, preparation
candidates and timing. Each intervention received a separately fitted readout
with the same training budget and feature class. The secondary fixed policy used
the second slot of each circuit's calibrated candidate pair; its physical action
could differ between circuits. Thus the target population is a particular
generator, calibration and training procedure, not arbitrary oscillator networks.

There were 64 evaluation history groups per circuit, four rows per group and two
holds, giving 10,240 chains per arm–policy cell. The primary endpoint was success
on all seven computations after the initial computation. Circuits, rather than
chains, were the primary inference units. We report ordinary 95% Student-t
intervals over 20 paired circuit differences; these are approximate and are not
the multiplicity-adjusted decision intervals. One Holm family covered five
prespecified claims: normal greater than removal, donor worse than removal,
normal greater than donor, and two equivalence tests comparing donor with removal
and with normal. Equivalence used TOST with a fixed ±2-point margin.

At the first preparation boundary, h_own = m − m_ref. Removal used m − h_own in
phase evolution, while h_own decayed with the memory decay coefficient. The donor
arm used m − h_own + h_donor. Donor histories were paired within circuit, hold,
retained task bit A and current input condition; their boundary components were
recomputed with the recipient's exact current input amplitude. No phase,
refractory state or receiver state was transplanted, and outcomes were not used
to choose donors. The processor's m itself was not overwritten. These remain
model-internal interventions, not demonstrated physical operations.

## Primary results

| Refitted-readout comparison | Difference, percentage points | Ordinary 95% interval | Prespecified decision |
|---|---:|---:|---|
| Normal − removal | +4.0723 | [+2.4333, +5.7113] | Positive difference supported; Holm p=0.0002546 |
| Donor − removal | +1.4844 | [−0.2171, +3.1858] | Neither donor harm nor ±2-point equivalence established |
| Normal − donor | +2.5879 | [+1.4132, +3.7626] | Own-component advantage supported; Holm p=0.0007626 |

Seven-step success was 55.6348% for normal dynamics, 51.5625% for removal and
53.0469% for matched donor replacement. Donor–removal equivalence had adjusted
p=0.8002; donor–normal equivalence had adjusted p=1. Failure to establish either
equivalence is not proof of non-equivalence. Nor is the positive point estimate
for donor minus removal evidence of a confirmed donor benefit.

The new-circuit result supports a positive average contribution under this
procedure. It does not retroactively satisfy the prior three-point criterion:
the earlier decision remains unmet, and the new generalization test used zero
as its directional null. Circuit-level normal-minus-removal estimates were
positive in 16 circuits, negative in three and zero in one. The result is not a
uniform advantage across circuits.

The normal–donor contrast narrows an operating-point-only account: replacing the
own component with a matched foreign component did not preserve performance.
However, it does not isolate semantic content from compatibility with retained
phase, refractory and other states. All 40 circuit–hold cells met the frozen
marginal-scale diagnostic; donor/own standard-deviation ratios ranged from
0.9928 to 1.0079. Own/donor correlations nevertheless ranged from 0.8952 to
0.9878. Matching A and the current input preserves substantial shared structure.
The supported claim is an advantage of the own component over this particular
matched replacement under refitted policies, not that any wrong memory is worse
than no memory, or that a seed of intelligence has been identified.

## Secondary observations and adverse evidence

The fixed-policy reversal appeared again in the new panel: normal dynamics
achieved 37.9590%, versus 47.0605% for removal. The descriptive policy-by-
intervention contrast was +13.1738 points, with an ordinary circuit-level 95%
interval of [+9.8774, +16.4702]. This supports examining how history is used by a
policy, but does not establish that the fitted policy is optimal or that a
management layer is universally necessary.

The refitted normal-minus-removal difference was +8.5742 points for A=1 and
−0.4297 for A=0; the A=0 interval included zero. A strict input-wise sign reversal
was therefore not established in this panel. Differences were +5.4297 points at
hold 512 and +2.7148 at hold 16,384, the reverse ordering of the previous
five-circuit evaluation. These descriptive estimates do not support a stable
claim that longer retention increases the contribution. No monotonic retention
law follows from either two-hold comparison.

The secondary constant-bias arm achieved 48.5449% with a refitted readout. Donor
minus constant was +4.5020 points, with a descriptive interval of [+2.5366,
+6.4673]. The constant arm changes temporal decay as well as variability, so this
does not isolate information content either. Secondary observations do not
replace the primary decisions. Earlier adverse MC evidence and the unconfirmed
C3 transplantation rescue remain unchanged and were not retested here.

## Integrity and availability

All 320 saved evaluation files passed independent scoring from saved output event
counts and task inputs, along with hash, donor, preintervention-state and numerical
checks. A separate scalar implementation reproduced 192 predetermined
preparation/query trajectories and 128 own/donor boundary states, with zero
maximum absolute discrepancy in the comparisons made. These are within-project
checks, not external replication. Input files received individual hashes at
generation, and each circuit's fitted models were sealed before its evaluation
cohort was generated. Historical overlap checks have the explicitly limited local
record coverage documented in the protocol.

Sources: [fixed plan](../../experiments/wrong_history_generalization/PLAN.md),
[source freeze](../../experiments/wrong_history_generalization/FREEZE.json),
[pilot](../../experiments/wrong_history_generalization/PILOT_REPORT.md),
[machine-readable analysis](../../results/wrong_history_generalization/main/analysis.json),
[full report](../../results/wrong_history_generalization/main/REPORT.ja.md),
[figure](../../results/wrong_history_generalization/main/wrong_history_generalization.pdf).
These are local versioned artifacts, not yet public evidence links.
