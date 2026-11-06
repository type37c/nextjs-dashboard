# 4. Wall I — Retained history may be unreadable or unusable

English manuscript draft, 6 November 2026. This section integrates the evidence
identified in the revised outline. References below identify primary experimental
records; they are not a substitute for the paper's pending literature review.

Retaining a distinction from the past is not sufficient to make that distinction
useful in a subsequent computation. A receiver must obtain an informative signal,
a readout must preserve what the task requires, and a policy must have an action
that can succeed from the resulting state. We separate these requirements because
their failures imply different interventions. Improving a decoder will not solve
a shortage of feasible actions, while increasing internal memory may not help a
receiver that cannot use its output. The studies below illustrate these distinctions
in particular simulated systems; they do not establish a universal architecture
for intelligence.

## 4.1 Retention, expression, and transmission do not guarantee use

The MC-4X exploration provides a small example of a mismatch between an available
signal and downstream use. It evaluated five circuits on a task distinguishing
both distant and recent input histories. Its main measure, *both*, was the smaller
of the two discrimination accuracies, rather than overall task accuracy. For a
mixed oscillator population, the output oscillator achieved 0.531. An external
classifier using an integration timescale matched to the receiver achieved 0.546;
allowing a longer integration window yielded 0.698. These results motivate asking
which temporal features a receiver can exploit, rather than treating the arrival
of spikes as evidence of successful information use. [MC4X]

The adverse comparisons matter to this interpretation. With longer integration,
a fast population and a control without memory–motion coupling performed
comparably to the mixed population. This exploration therefore did not establish
an advantage for mixed timescales or for the coupling itself. The receiver,
observation window and training procedure are part of the explanation of the
measured outcome. A failure of one readout does not show that the source contains
no information; success with a different readout does not show that the original
receiver can use it.

## 4.2 Reading without damage requires a preservation target

Readout accuracy and readout disturbance are separate quantities. A perturbation
may preserve a memory variable while changing phase, refractoriness, spike timing
or subsequent task performance. Accordingly, a claim of nondestructive reading
must specify both the object to preserve and a tolerance.

In E7-D, the processor P is accompanied by a system that maintains a copy of its
memory and reads that copy through perturbations. The direct readout kick does
not reach P. The relevant claim is therefore that the mechanism avoids directly
kicking the original processor; it is not that every state of the full system
returns to its initial value. Copy fidelity, readout error, latency and subsequent
computation remain separate evaluation targets. [E7D]

This distinction also makes the method portable. A reader applying the framework
to another substrate can compare reading with an equal-duration no-read control,
measure the changes in specified state variables, and then assess the same
downstream task. If a copy is used, its creation and maintenance belong in the
cost and error accounting. Appendix A gives that procedure without assuming that
all systems permit exact state duplication.

## 4.3 Accurate reading does not ensure a successful preparation

E7-D connects readout to a restricted preparation decision. In its fixed-five-
circuit confirmation, using previously unused inputs and four hold conditions,
the 64-unit readout condition achieved 57.8% success on all seven subsequent
computations, compared with 48.5% for the frozen E7 reference. The reported paired
difference was +9.3 percentage points, with a 95% interval of [+8.7, +9.9]. This
was an evaluation of new inputs to known circuits, not inference over a population
of new circuits. Readout weights were learned externally. [E7D] [E7PLAN]

Its failure decomposition is as informative as the success rate. Of 107,520
subsequent decisions under the 64-unit condition, 11,194 failed. At 10,148 of those
failures—90.7% of failures—neither of the two available preparation candidates
could succeed from the reached state. This is a property of the specified
candidate set, task and time limit. It neither describes 90.7% of all states nor
establishes impossibility over all conceivable controls. Counterfactual candidate
outcomes were an evaluation diagnostic, not information supplied to the online
selector. [E7RESULTS]

Larger readouts also did not translate directly into larger task gains: the
reported seven-step difference between the 16- and 64-unit conditions had an
interval containing zero. The lesson is to measure reading, selection and
candidate availability separately. Because different policies reach different
states, their failure compositions should not be interpreted as a same-state
causal decomposition.

## 4.4 History and preparation policy must be evaluated together

The history-contribution studies ask a complementary question: does the retained
history contribution help the computation performed by a particular policy? The
task requires the output to represent A AND B, where A is a retained binary
condition and B varies between computations. Silence is correct for A=0, whereas
for A=1 the required response depends on B. That asymmetry is a task definition,
not an established explanation of the observed effects.

At the first preparation boundary, the removal intervention defines

```text
h_own = m − m_ref
h_own(t+1) = (1 − epsilon) h_own(t)
effective phase contribution = m − h_own
```

The processor's memory m is not reset; subsequent inputs continue to enter it.
Phase, refractory state and other retained states are also preserved at the
intervention boundary. Removing this component is a model-internal counterfactual
that changes effective phase velocity. It is neither removal of every influence
of the past nor a demonstrated physical control operation. [HCPLAN] [WHPLAN]

The exploratory pilot found that normal dynamics performed better than removal
with separately fitted readouts, but worse under fixed preparation. A subsequent
evaluation used five existing circuits and ten frozen pilot-trained readouts on
a new cohort, with 5,120 chains per cell. Its normal-minus-removal difference was
+4.0820 points, with a 95% paired-group bootstrap interval of [+2.9883, +5.1563].
The prespecified criterion required the lower bound to exceed three points and
was not met. Section 2.3 retains that decision. The fixed-policy contrast had the
opposite sign. [HCPILOT] [HCREPORT]

The comparison evaluates substrate–policy combinations under a matched training
budget. It does not identify the best attainable policy for either substrate or
the effect of changing the substrate while keeping one controller fixed. Even so,
the reversal gives a concrete reason to ask how retained history is used, rather
than assigning it an intrinsic positive value.

## 4.5 What generalized beyond the original five circuits?

A separate study tested generalization under the original circuit generator and
calibration procedure. A training-only feasibility pilot used three new circuits;
none entered the main panel. The protocol, code, circuit IDs, streams and analysis
were then fixed locally before acquiring 20 further circuits. Physical weights,
preparation candidates and timing were recalibrated for each circuit. Each
intervention received its own readout fitted with the same feature class and
training budget. The secondary fixed policy always selected the second slot of
that circuit's calibrated pair, so its physical action could vary across circuits.
[WHPLAN] [WHPILOT]

Each circuit contributed 64 evaluation history groups, four rows per group and
two holds. This yielded 10,240 chains per arm–policy cell and 81,920 across four
arms and two policies. The primary inference unit was a circuit, not a chain.
Five prespecified claims, including two equivalence claims, formed one Holm
family. Ordinary 95% Student-t intervals across circuits describe uncertainty;
they are not multiplicity-adjusted decision intervals. Equivalence used TOST with
a prespecified ±2-point margin. The protocol was locally fixed before acquisition,
without external preregistration. [WHPLAN]

| Refitted-readout comparison | Difference, percentage points | Ordinary 95% interval | Prespecified conclusion |
|---|---:|---:|---|
| Normal − removal | +4.0723 | [+2.4333, +5.7113] | Positive difference supported; Holm p=0.0002546 |
| Normal − matched donor | +2.5879 | [+1.4132, +3.7626] | Own-component advantage supported; Holm p=0.0007626 |
| Matched donor − removal | +1.4844 | [−0.2171, +3.1858] | Donor harm and equivalence to removal not established |

Normal dynamics achieved 55.6348% seven-step success, versus 51.5625% after
removal. The difference was positive in 16 circuits, negative in three and zero
in one. Thus a positive average difference extended beyond the original five
circuits under this generator, calibration and training procedure. The evidence
does not establish a uniform circuit-wise advantage or transfer to arbitrary
topologies, tasks or training procedures. [WHDATA]

The new study did not add observations to the previous sample to obtain a passing
three-point result. It tested a distinct zero-based generalization claim using a
different inference unit. The previous minimum-effect decision remains unmet;
the new interval also includes values below three points.

## 4.6 Own history versus a matched foreign contribution

The donor arm addressed an ambiguity in removal: losing performance might reflect
a change in operating point rather than the identity of a history contribution.
It used m − h_own + h_donor in phase evolution, with both auxiliary components
decaying at the prescribed memory rate. Donor histories came from different
history groups within the same circuit, hold, A and current-input condition. Their
boundary components were recomputed using the recipient's exact current input
amplitude. Donor selection did not use outcomes or state proximity; no donor
phase, refractory state or receiver state was transplanted. [WHPLAN]

Normal dynamics outperformed matched donor replacement by +2.5879 points after
the prespecified Holm correction. All 40 circuit–hold cells met the frozen
marginal-distribution diagnostic; donor/own standard-deviation ratios ranged
from 0.9928 to 1.0079. Thus matching marginal scale did not preserve performance.
However, this is not a complete separation of content from operating point or
state compatibility. Own/donor correlations ranged from 0.8952 to 0.9878, and
matching A and the current input preserves substantial shared task structure.
The intervention replaced a component associated with a different individual
history within that matching class; it did not erase all task-relevant content
or perform a statistical residualization. Marginal matching also does not match
the component's joint distribution with retained phase and other state. [WHDATA]

The donor-minus-removal estimate was +1.4844 points. Neither the prespecified
donor-harm claim nor equivalence to removal was supported. Donor–removal
equivalence had Holm-adjusted p=0.8002; donor–normal equivalence also failed
(adjusted p=1). These failures do not prove non-equivalence, and the positive
donor-minus-removal point estimate is not a confirmed donor benefit.

A secondary constant-offset arm achieved 48.5449%, the lowest point estimate
among the four refitted conditions. Donor minus constant was +4.5020 points, with
a descriptive 95% interval of [+2.5366, +6.4673]. This contrast changes the
temporal profile as well as the across-history value: the donor component decays,
whereas the constant persists. Consequently, it does not identify the benefit of
temporal variation alone. The ordering of the four point estimates should not
be presented as an established ranking of every pair. [WHDATA]

The supported conclusion is narrower: within this procedure, an own boundary
component was more useful than this matched replacement under refitted policies.
Whether that advantage is best explained by content, compatibility with other
state, or a combination remains unresolved.

## 4.7 Conditional effects and the limits of a trajectory interpretation

The new panel again showed a reversal under fixed preparation. Normal dynamics
achieved 37.9590%, versus 47.0605% after removal. The descriptive policy-by-
intervention contrast was +13.1738 points, with an ordinary 95% interval of
[+9.8774, +16.4702]. Re-observing this pattern on new circuits strengthens the
case for evaluating history together with policy. It does not make the pattern
a universal property of memory-dependent systems. [WHDATA]

Other patterns did not extend as clearly. The normal-minus-removal difference
was +8.5742 points for A=1, with a descriptive interval of [+5.8256, +11.3229],
and −0.4297 for A=0, with an interval of [−2.6592, +1.7998]. The A=1 positive
difference was observed again, but the negative A=0 difference was not established
in this panel. Different significance outcomes within subgroups do not by
themselves demonstrate a subgroup difference or an effect exclusive to A=1.
The hold-specific differences were +5.4297 points at 512 steps and +2.7148 at
16,384 steps, reversing the ordering in the previous five-circuit evaluation.
Neither study establishes a monotonic retention law.

The immediately following computation had a normal-minus-removal estimate of
−0.0195 points, with a descriptive interval of [−2.9814, +2.9423], while all-seven
success showed the positive primary difference. This motivates assessing
continued computation in addition to the next response. It does not establish
that the immediate effect is zero: equivalence at that endpoint was not tested.
Nor do the two aggregate endpoints identify a trajectory-mediated mechanism.
Equal aggregate next-step accuracy can conceal different successful rows,
different later states, and different dependencies among subsequent failures.
Trajectory shaping is an interpretation to investigate, not a mechanism
demonstrated by this comparison. [WHDATA]

Adverse evidence remains part of the account. The pilot's C3 transplantation
diagnostic did not show a rescue when exact-memory features were updated after
transplantation; its small perturbation limited interpretation of that negative
finding. The new panel did not retest C3. The MC relay disadvantages discussed in
Section 7 likewise remain relevant to the division of roles. A useful memory
substrate need not be the best relay, and a successful diagnostic need not be an
optimal controller. [HCPILOT]

The new evaluation's 320 saved outcome files passed separate scoring from event
counts and task inputs. A separate scalar implementation reproduced 192
predetermined preparation/query trajectories and 128 own/donor boundary states.
These were within-project numerical checks, not external replication. The
protocol and evidence map specify the scope of historical-cohort checks and the
limits of the numerical evidence. [WHAUDIT] [WHDYNAMICS]

Together, these studies give the first wall an operational meaning: retained
history must become observable and actionable under specified constraints before
its value can be assessed. The evidence supports conditional questions about
usable memory. It does not establish that an explicit management layer is
universally necessary, or that memory-dependent units are generally superior to
other substrates. The next wall concerns a different demand: making a new
experience learnable without corrupting what is already retained.

## Figure 3 caption draft

**Own history, matched donor history, and new circuits.** Twenty circuits were
generated and individually recalibrated before evaluating four phase-contribution
conditions. (A) All-seven success under arm-specific refitted readouts and a fixed
choice of the second calibrated candidate. (B) Circuit-level normal-minus-removal
point estimates under refitted readouts. (C) Paired circuit-level mean differences
and ordinary 95% Student-t intervals. The shaded ±2-point range is the P2
equivalence margin, not the P1 threshold; Holm decisions use the prespecified
five-test family. Donors match A and current input. Removal and replacement act
on the pre-boundary contribution to phase, leaving m itself intact. Each cell
contains 10,240 chains. The figure reports this procedure's outcomes, not a
content-only intervention or hardware-efficiency comparison.

## Primary experimental records

[MC4X]: sources/MC4X_REPORT.md
[E7D]: sources/E7D_REPORT.md
[E7PLAN]: sources/E7D_PLAN.md
[E7RESULTS]: sources/E7D_results.json
[HCPLAN]: sources/HISTORY_COUPLING_CONFIRMATION_PROTOCOL.ja.md
[HCPILOT]: sources/HISTORY_COUPLING_PILOT_REPORT.ja.md
[HCREPORT]: sources/HISTORY_COUPLING_CONFIRMATION_REPORT.ja.md
[WHPLAN]: sources/WH_PLAN.md
[WHPILOT]: sources/WH_PILOT_REPORT.md
[WHDATA]: sources/WH_analysis.json
[WHAUDIT]: sources/WH_saved_data_audit.json
[WHDYNAMICS]: sources/WH_dynamics_audit.json
