# From Having Memory to Using It

Insertion draft for Sections 2.3 and 4.4 — 6 November 2026.
This is a case-study draft, not the introduction or a completed submission.

## 2.3 A positive difference that did not meet the minimum-effect criterion

An evaluation of memory-dependent computation should specify which claim an
unfavorable outcome would weaken. We used a history-coupling pilot to select a
comparison between normal T7 dynamics and an intervention removing the
pre-boundary memory contribution from phase evolution. Before acquiring a new
cohort, we fixed the sample size, analysis code, and decision rule: the lower bound
of a 95% paired group bootstrap interval for the normal-minus-intervention
difference in seven-step success had to exceed three percentage points. This
minimum effect was a design choice made with knowledge of the pilot, not an
independently established property of the task. The protocol was recorded locally;
there was no external preregistration.

The evaluation used five existing circuits, 128 history groups per circuit, and
two hold conditions. Each group contributed four rows under both holds, yielding
5,120 chains per cell. Readouts had been trained separately for the two substrates
with the same training budget during the pilot; those ten fitted models were
frozen for the new evaluation. Groups were resampled within circuit, preserving
pairing across rows, holds, and experimental conditions. Consequently, inference
is conditional on these circuits and fitted models, rather than on a population
of new circuits or training runs.

Normal T7 achieved 56.89% seven-step success, compared with 52.81% after the
intervention. The difference was +4.0820 percentage points, with a 95% interval of
[+2.9883, +5.1563]. The interval supported a positive conditional difference, but
its lower bound did not exceed three percentage points. We therefore did not
claim that the minimum-effect criterion was met. Nor did the interval exclude a
three-point effect or establish equivalence. We did not change the rule or acquire
additional samples to obtain a passing result. Circuit-level point estimates were
positive in four circuits and negative in circuit 203 (−1.9531 points), unlike the
uniform direction observed in the pilot.

There is no scientific discontinuity between 2.9883 and 3. The estimate, its
uncertainty, and the decision under the chosen rule convey different information.
Keeping them separate prevents a favorable secondary observation from replacing
an unmet primary criterion. Adherence to that rule is a reporting discipline, not
additional evidence for the proposed mechanism.

Sources: [protocol](sources/HISTORY_COUPLING_CONFIRMATION_PROTOCOL.ja.md),
[freeze record](sources/HISTORY_COUPLING_CONFIRMATION_FREEZE.json),
[results](sources/HISTORY_COUPLING_CONFIRMATION_summary.json).

## 4.4 Retained history can help or hinder under different preparation policies

The intervention used a decaying auxiliary component. At the first preparation
boundary, we set h = m − m_ref and subsequently decayed h at the same rate as m.
Only the processor's phase update used m − h; m itself was not reset, and later
inputs continued to enter through m. Phase, refractory state, and other units'
history were retained. This was a model-internal counterfactual, not a demonstrated
physical operation. Because it also changed effective phase velocity relative to
a reference, it did not isolate information content from operating-point effects.

The direction of the performance difference depended on the preparation policy.
With the frozen, substrate-specific learned readouts, normal T7 performed better
on average, subject to the unmet minimum-effect criterion above. Under the same
fixed preparation candidate in all five circuits and both substrates, normal T7
achieved 34.18%, whereas the intervention achieved 46.91%. The resulting
policy-by-intervention interaction was +16.8164 percentage points, with a
descriptive 95% interval of [+15.5469, +18.1250]. The reversal seen in the pilot was
thus observed again on different inputs to the same circuits and policies. This
is not evidence that it holds across new circuit populations or arbitrary control
policies.

The task scores a binary conjunction, A AND B, where A is the retained binary
condition and B varies between computations. A correct output is defined by
whether the output unit fires within the computation window. When A=0, silence
is correct regardless of B; when A=1, the required response follows B. This
asymmetry is part of the task definition, not an established explanation of the
intervention effect ([task implementation](sources/HISTORY_COUPLING_PILOT_CODE.py)).

The learned-readout comparison also changed sign across input conditions. The
normal-minus-intervention difference was +10.4688 points for A=1 and −2.3047
points for A=0; their difference was +12.7734 points (descriptive 95% interval:
[+10.5469, +15.0000]). Even normal T7 achieved only 21.17% seven-step success for
A=1. These observations motivate examining the task's output asymmetry, training
target, and dynamical operating point; they do not yet identify the cause of the
sign reversal. Differences were +2.6953 and +5.4688 points at holds of 512 and
16,384 steps, respectively. Two hold conditions do not establish a monotonic
relationship, and a contrast between hold-specific effects was not tested.

These secondary analyses were specified in advance but remained descriptive.
They cannot replace the primary decision. Likewise, the pilot's matched memory
transplantation diagnostic did not show a rescue from updating an exact-memory
readout: joint-readiness success was 76.44% with stale information and 76.28%
after updating it, among 624 eligible rows. The small mean absolute memory
change of 0.01470 limits the interpretation of that negative observation. The new
cohort evaluation did not repeat or resolve this rescue experiment.

The case supports a narrower question than whether memory is intrinsically good:
under which input conditions and available policies does retained history improve
a specified computation? Comparing separately recalibrated substrates evaluates
particular substrate–policy combinations, not a pure intervention effect under
one fixed controller or the best attainable performance of either substrate.
The result motivates conditional measurement of usable memory without establishing
a universal requirement for an explicit management layer.

Sources: [pilot report](sources/HISTORY_COUPLING_PILOT_REPORT.ja.md),
[new-cohort report](sources/HISTORY_COUPLING_CONFIRMATION_REPORT.ja.md).

## Figure caption draft

**Figure 2. The effect of retained history depends on preparation policy and input
condition.** (a) Seven-step success for normal T7 and the single-boundary
intervention, each with a frozen pilot-trained readout or the same fixed
preparation candidate. (b) The primary difference and prespecified descriptive
contrasts, with paired group bootstrap intervals; the three-point threshold
applies only to the primary comparison. (c) Input-specific differences under the
learned readouts. (d) Circuit-specific point estimates, without circuit-level
intervals. Positive values in panels b–d favor normal T7; the interaction in panel
b is the learned-readout contrast minus the fixed-preparation contrast. All cells
use the same five circuits and paired history groups. The primary interval's
lower bound is 2.9883 points, so the minimum-effect criterion was not met.

## Reporting and availability note

The new evaluation's 40 saved outcome files passed consistency checks. Ninety-six
trajectories selected before acquisition matched a separate scalar implementation,
with zero maximum absolute state discrepancy in the comparisons made. These were
within-project checks, not an external replication. Individual input files were
saved before their corresponding simulations, but their hashes were recorded
after acquisition rather than immediately at generation as planned; generator
code and seeds had been frozen beforehand. Full methods, software-version
limitations, and this procedural deviation are recorded in the reports. The
current source references are local artifacts; public versioned links must be
provided before submission.
