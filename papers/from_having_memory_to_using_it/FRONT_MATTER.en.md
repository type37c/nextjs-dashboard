# From Having Memory to Using It: A Research Agenda for Memory-Dependent Computation

Working manuscript — 6 November 2026. Position-paper draft, not a submission-ready
manuscript. The literature discussion is based on focused primary-source checks;
the experimental references remain local versioned records.

## Abstract

A system can retain information about its past yet fail to use that information
for its next computation. We propose evaluating memory-dependent computation
through the operations that make retained history usable under specified
observation, action, time and resource constraints. Three barriers organize the
agenda: reading history and selecting a feasible preparation; acquiring a new
relation while retaining old ones; and accessing experience held by another
system. Small oscillator studies illustrate these barriers without establishing
oscillator superiority. In a locally fixed evaluation of twenty newly calibrated
circuits, normal dynamics outperformed removal of a pre-boundary history
contribution and replacement with a matched donor contribution. Content and
compatibility with other state remained incompletely separated. Other studies
achieved acquisition with retention at substantial waiting cost and connected use
of separately held relations without recipient learning or conflict-sensitive
abstention. Adverse relay comparisons and an earlier unmet minimum-effect
criterion constrain the interpretation. We use “management” as a functional
description, compatible with operations embedded in learned dynamics, not a
requirement for a separate controller. The practical contribution is a protocol
for measuring retention, readout disturbance, action availability and update
interference, with explicit costs and conditions that would weaken the agenda.

# 1. The gap between retaining history and using it

What makes an internal record of the past useful? A decoder may distinguish two
histories while the system's available actions cannot turn that distinction into
a successful response. An update may acquire a new relation while destroying an
old one. A useful relation may remain inaccessible because it belongs to another
system. These are different obstacles, even when each is summarized as a failure
of memory.

Memory and its use already have substantial theoretical and architectural
treatment. Dynamical capacity measures assess reconstruction of functions of
input history through a specified readout. Adaptive spiking models use internal
state to carry effects of past firing. Gated recurrent units and selective state
space models regulate what is retained or incorporated, and external-memory
architectures make access operations explicit. [DAMB2012] [ALIF2018] [GRU2014]
[MAMBA2023] [NTM2014] These precedents rule out a simple opposition between
“static weights” and systems that possess memory. Fixed learned parameters do
not imply a stateless runtime, and an adaptive state does not need to be called
a memory register to carry history.

Our position is that evaluations of memory-dependent computation should state
not only what history can be recovered, but also what operations can use it,
under which constraints and with what effects on later use. This is especially
concrete when a substrate's update rule is fixed or difficult to redesign.
Choosing a preparatory input, waiting for a trace to decay, or reading another
module's response can then be an actionable intervention even when learning an
arbitrary new recurrence is not available. This setting motivates the question;
it does not establish an advantage over trainable alternatives.

We call these functions *management operations*: reading, selecting preparation,
controlling when updates proceed, and accessing another system's retained
experience. “Layer” denotes an analytical organization of functions. Those
functions can be distributed, implicit in learned dynamics, or implemented by
an external controller. Their number is not a scale of intelligence, and merely
adding more operations need not improve performance.

Three walls structure the paper. First, retained history may be unreadable or
unusable with the available preparation candidates. Second, learning something
new may corrupt what is retained. Third, a relation held elsewhere may remain
inaccessible, or be usable only while connected. We examine these walls through
small numerical oscillator studies, including unfavorable and unresolved results.
The studies do not combine into one demonstrated agent. Their role is to make
the proposed questions concrete and expose the limits of convenient summaries.

The intended contribution is a research agenda with a portable diagnostic
protocol. Readers should be able to identify a preservation target, specify
allowed observations and actions, separate selection failures from candidate
absence, and report acquisition together with retention and cost. Whether that
organization predicts useful interventions beyond the examples is itself a
claim to test, not a conclusion secured by naming the operations.

# 2. Scope, limits, and conditions that would defeat this position

## 2.1 What the evidence covers

The empirical examples are simulations of particular architectures and tasks.
Some use externally trained readouts, some direct state access by an external
guard, and some supplied object identities and connections. None establishes
general reasoning, autonomous semantic acquisition or hardware efficiency.
Readout accuracy, seven-step computation, joint acquisition and retention, and
support propagation are different endpoints and are not added into a single
capability score.

Generalization must be named. New inputs to five known circuits differ from new
circuits drawn from a specified generator; neither guarantees transfer to a new
task, topology or optimization procedure. Primary decisions, descriptive
secondary comparisons and exploratory observations retain their original status.
Within-project numerical checks are distinguished from external replication.

## 2.2 Claims that can fail

The following are prospective commitments for a research agenda. The examples
do not establish all of them.

| Claim to test in a specified model and task family | Comparison | Consequence of an adequately precise adverse result |
|---|---|---|
| State-dependent management offers a practical benefit | Match total deadlines, training and observation costs against calibrated fixed policies | Withdraw the practical advantage for that family if it disappears under matched budgets |
| The failure decomposition predicts effective interventions | Use a diagnosis to choose between readout and candidate-set changes, then compare prediction against simple accuracy or elapsed-time baselines | Narrow the framework's diagnostic claim if it adds no predictive value |
| A recipient uses another owner's experience | Change provider experience with the recipient held fixed; ablate memory transmission and communication | Withdraw the experience-use interpretation if responses are independent of provider content or explained by supplied answers |
| The protocol contributes beyond one oscillator implementation | Apply it to prespecified alternative substrates and assess reproducible diagnostic distinctions | Limit it to an oscillator-specific organization if it adds nothing beyond existing measures elsewhere |

A nonsignificant comparison alone is not decisive evidence against a claim.
The design must specify a meaningful effect, uncertainty and the range over which
the adverse evidence is informative. Conversely, a failed prediction should not
be rescued by adding a new operation after observing the result. If fair-budget
benefits consistently disappear and the decomposition does not predict effective
interventions, the case for a distinct research agenda weakens.

## 2.3 A positive estimate that did not meet the chosen criterion

The earlier history-contribution evaluation provides a reporting example.
Before acquiring a new input cohort for five known circuits, the analysis required
the lower bound of a paired-group bootstrap interval to exceed three percentage
points. The normal-minus-removal estimate was +4.0820 points, with a 95% interval
of [+2.9883, +5.1563]. The chosen minimum-effect criterion was not met. Rounding
the lower bound upward, adding observations to that sample, or substituting a
favorable secondary result would not preserve the original decision. [HCREPORT]

There is no scientific discontinuity between 2.9883 and three points. The estimate,
uncertainty and decision under a chosen rule answer different questions. The later
twenty-circuit study examined a separate generalization claim and did not change
the earlier decision. Following the rule is reporting discipline, not additional
evidence for a mechanism or for the proposed framework.

# 3. What is stored, what is observable, and who controls it?

A useful description separates the state that carries history from the operation
that accesses it. In one discrete T7 working-unit implementation, the memory
variable m contributes to phase advance:

```text
proposed_phase = phi + omega + kappa*m
fire = (proposed_phase >= 2*pi) and (cd == 0)
m_next = (1-epsilon)*m + drive - beta*fire
phi_next = 0 if fire else proposed_phase modulo (2*pi)
cd_next = R if fire else max(cd-1, 0)
```

This specifies an update order for the working unit, not every model in the
research series. Coupled implementations also track other state, such as prior
spikes. The persistent effect of history on phase is an implementation property,
not a novelty claim over adaptive or history-dependent neuron models. [HCCODE]

Several distinct quantities must not collapse into the word “memory.” The T7
variable m affects ongoing motion. OTB relation memories also use companion
amplitude states. Eligibility and error-related traces participate in subsequent
writing. A readout may maintain another copy, and a controller may store learned
weights. The location, lifetime and role of each should be stated separately.

For this agenda, *retention* means that a specified past distinction remains in
state or subsequent response; *expression* and *transmission* mean that a
corresponding difference appears in an observable output and reaches a receiver.
*Usability* is relative to a task: whether the permitted information and operations
can turn the retained distinction into the required result before the deadline.
It is not a substrate-intrinsic scalar.

Every experiment should therefore distinguish runtime inputs from evaluator-only
information. Labels used to train a selector, counterfactual outcomes used to
diagnose candidate availability, and external guards with privileged state access
have different roles. Their separation lets an external reader assess which
function the substrate performed and which was supplied by its training or control
environment.

[DAMB2012]: https://doi.org/10.1038/srep00514
[ALIF2018]: https://arxiv.org/abs/1803.09574
[GRU2014]: https://arxiv.org/abs/1406.1078
[MAMBA2023]: https://arxiv.org/abs/2312.00752
[NTM2014]: https://arxiv.org/abs/1410.5401
[HCREPORT]: sources/HISTORY_COUPLING_CONFIRMATION_REPORT.ja.md
[HCCODE]: sources/HISTORY_COUPLING_PILOT_CODE.py
