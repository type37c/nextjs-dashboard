# OTB19: preparing a live learning stream against stale eligibility

2026-11-05. Exploratory integration stress test. The oscillator and OTB15 learning
equations remain unchanged. No result-dependent lane selection or parameter tuning.

## Question

An unlabeled query can leave an eligibility trace in a context that will not
receive the next label. Can a later context's outcome update that old context,
and can state-dependent waiting before the new query protect it without clearing
the trace or changing the memory update equation?

## Fixed inputs and live sequence

Use the retained OTB15 normal memories and work states for seeds 24001..24008.
For every seed, cross old context pairs {2,3} (operation 1) with current pairs
{0,1} (operation 0), and stable/reversed operation-0 worlds. Operation 1 never
changes. The unobserved other operation-0 context is scored separately; it is not
expected to acquire a changed correspondence without a relevant observation.

One unlabeled old-context query runs for 4096 steps with restore128 preparation.
Its final memory, work states, eligibility and residual error state become the
live starting state for four repetitions of the current-context query followed
by delayed feedback. Work phases and refractory states are never reset in the
live sequence. The current query also uses 4096 total steps and restore128.
The original OTB15 observe function supplies the 1000-step delay and 8000-step
write, using the actual prediction and observed outcome. Labels enter only that
feedback calculation. State-readiness decisions do not receive world outcomes.

Policies (all 256 lanes):

- usual: no extra wait before current queries; normal feedback.
- guard: before each current query, wait until all six noncurrent cells satisfy
  the analytic bound below, then normal feedback.
- fixed_once: one conservative fixed wait before the first current query, then
  no extra waits. The known schedule introduces no other context between the four
  current observations, so repeating the fixed wait is unnecessary.
- zero_error: no extra wait, feedback delta forced to zero by the existing OTB15
  zero-error control. Labels are still recorded for scoring.

The fixed wait is computed from e<=1 and |s|<=1, not fitted to outcomes. It is a
conservative baseline, not the best possible fixed wait. A delay yoked to guard's
decision would produce the same dynamics here; waiting, rather than a distinct
new physical mechanism, is the intervention.

## Analytic guard

The double-well fold tilt is hcrit=2/(3 sqrt(3)). The memory tilt is
h=hold_eta*tanh((m-MC)/SCALE)+alpha*s. Set

    theta = 0.95*(hcrit-hold_eta)/alpha.

For noncurrent cells, no source event retags e during the forthcoming current
query; e decays. During a label write, |delta|<=1 and

    s_next=(1-1/tau_s)*s+(1/tau_s)*e*delta.

For tau_s>=1 this is bounded by max(|s_initial|, e_initial). Thus e,|s|<=theta
ensures |h| <= hold_eta+alpha*theta < hcrit throughout the following query,
delay and write. In the continuous radial equation this makes the certified
low/high bands forward invariant. This does not assert the same theorem for
arbitrary numerical integration step sizes.

During waiting, query=False and delta=0: e(t)=e0 exp(-t/tau_e) and
s(t)=s0(1-1/tau_s)^t. Compute the required steps from these formulas and verify
the bound on the actual resulting state. Waiting uses the unchanged original
advance function, which also applies its existing work-state restoring input.
There is no direct assignment to m, phase, u, e or s in the live loop.

## Records and checks

Save all initial/post-old/pre-wait/post-wait/post-query/post-write states, actual
predictions/errors, current-context adaptation, both untouched operation-1 bands
and canonical responses, and costs. Canonical four-context probes start from a
fixed diagnostic work state and copied memory; they never update the live lane.
Record probes initially, after the old query and after every learning episode.

Cost records include waiting steps, query/feedback steps and summed absolute
work-restoration current. This numerical input measure is not physical energy.
An independent work-only recurrence checks the effort and endpoint for waiting
and feedback segments. Before every protected write, evaluate the noncurrent
tilt bound from actual state. Check certified bands at all recorded boundaries.

Record full first-episode traces for the mechanically chosen first seed, old
pair 2, current pair 1, reversed world, policies usual and guard. Inspect every
native-step noncurrent tilt and amplitude band in those traces. Other lanes use
the analytic bound and boundary checks, not an asserted full independent replay.

Before acquisition, snapshot/hash this design, runner, imported OTB15 and OTB17
models, OTB15 specification, and all eight source result files. Refuse an existing
output directory and retain failures. Kernel validation concerns implementation;
this study tests a finite workload, not general credit assignment or autonomous
meaning acquisition. Negative results remain valid outcomes.
