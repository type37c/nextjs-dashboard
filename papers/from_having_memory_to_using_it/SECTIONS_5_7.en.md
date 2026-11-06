# 5. Wall II — Learning something new may corrupt what is retained

The first wall concerns using a retained history in a computation. The second
concerns changing what is retained. An update can acquire the intended relation
while damaging another, and a protective intervention can avoid damage by making
learning ineffective. Acquisition and retention must therefore be measured on the
same trials, with the time and observation costs of protection included.

## 5.1 Protection is not successful learning

OTB20 illustrates the distinction in a fixed oscillator-and-companion learning
system. It varied the amplitude of an externally supplied teaching error while
leaving the underlying T7, companion and trace rules unchanged. In the reported
exploratory reversal conditions, bounded error protected the non-target memory
band in 32/32 cases at each of three waiting settings, but the intended target
update succeeded in 0/32. With ordinary error and a sufficiently long fixed wait
in that exploration, both target updating and non-target protection succeeded
in 32/32. These results concern the tested settings, not error clipping in
general. [OTB20]

A retention-only score would favor an intervention that prevented the required
change. The relevant boundary involves both an upper constraint on interference
and a lower requirement for completing the new update within the available time.
Here, *gating an update* means permitting a useful change while controlling its
effects elsewhere. Merely stopping writes is not success on that joint objective.

## 5.2 A state-based wait preserved old relations at additional cost

OTB21 tested the previously specified guard and a fixed waiting policy under
additional phase and query-duration conditions. After an unlabeled query to an
old operation, the system inherited its complete state. A subsequent query
concerned a different operation and was followed once by the reversed outcome.
Residual eligibility and error-related traces from the earlier activity could
affect which memory cells were changed. The guard read the trace state directly
and inserted waiting before the next query; it did not change the learning rule
or directly clear the traces. [OTB21]

The study used eight saved memory seeds, four phase draws shared across seeds,
two old contexts and two new contexts: 128 conditions per query-duration–policy
cell. These are structured combinations, not 128 independent rules or worlds.
Three query durations and three policies yielded 1,152 learning trials. At the
shortest query duration, the stored-record results were:

| Policy; query duration 1,536 native steps | Taught context correct | Both untouched-operation contexts correct | Both requirements | Mean total live steps |
|---|---:|---:|---:|---:|
| No additional wait | 128/128 | 64/128 | 64/128 | 14,632 |
| Fixed 4,096-step wait | 128/128 | 64/128 | 64/128 | 18,728 |
| State-based guard | 128/128 | 128/128 | 128/128 | 30,040.25 |

Correctness was diagnosed using copies of the post-learning memory initialized
to a standard working state. Diagnostic states and answers were not fed back into
live learning. The table therefore establishes acquisition and retention under
that diagnostic, not successful uninterrupted downstream operation from every
post-learning state. Total live time includes the old and new queries, waiting,
outcome delay and writing, but excludes computation on diagnostic copies. [OTB21]
[OTB21DATA]

The guard achieved the joint criterion in all tested cells, but its benefit came
with substantial additional waiting. At the longest query duration, 4,096 steps,
the fixed-wait policy also achieved acquisition and retention in 128/128 conditions.
The guard's retention condition was sufficient in the tested setting, not a
characterization of the shortest necessary wait. Moreover, changing query duration
also changed when the subsequent outcome and writing occurred. The study did not
isolate a query-deadline effect from the additional time for old traces to decay.

These qualifications determine the claim. OTB21 demonstrates a feasible
acquisition–retention combination over the stated synthetic conditions. It does
not show superiority to a well-tuned fixed wait at the same total time, greater
throughput, or lower energy use. The guard is an external comparator with direct
access to e/s traces; it is not the E7-D oscillator readout embedded into the
learning experiment. The two studies are separate implementations of different
management operations, not consecutive capabilities of one integrated agent.

## 5.3 The second wall is an acquisition–retention–cost question

The useful output of this wall is a joint report: what changed, what remained
usable, whether both occurred on the same trials, and what resources that required.
This connects the case to the established stability–plasticity problem without
claiming to solve continual learning generally. For example, elastic weight
consolidation constrains changes to parameters according to their importance for
previous tasks; OTB21 instead delays subsequent activity under a fixed trace-driven
learning rule. The mechanisms and evaluation domains differ. [EWC2016]

A fair comparison would specify a total deadline, include observation and waiting
costs, and compare state-dependent waiting with calibrated fixed waits and waits
drawn from the same duration distribution without using state. Those are research
questions, not additional completed comparisons. Appendix A turns the distinction
between protecting and learning into a protocol that readers can apply to their
own models.

# 6. Wall III — Experience held elsewhere may remain inaccessible

Even when an individual system retains and can use a relation, a recipient may
lack access to it. We distinguish copying a memory, using a provider's response
while connected, learning the relation in the recipient, and handling conflicting
providers. These operations should not be counted as one capability merely
because a task involves multiple modules.

## 6.1 Connected use without copying the provider's memory

OTB22 studied a minimal numerical mechanism for connected use. Three owners held
separate artificial one-step relations, A→B, B→C and C→D. Each owner had local
T7-and-companion memory and working T7 units for four named objects. Connections
between owners transmitted the previous-step firing of working units representing
the same object. The recipient's local memory did not receive a copy of the other
owners' relations. The observation was a support response at the recipient's D
unit following stimulation of A. [OTB22]

Object identity, owner identity, context and the connection pattern were supplied
by the experimenter. The reference task asked whether a supporting path existed
in the specified relation graph. An external path solution was not passed to the
runtime, but the system was not discovering object meanings or semantic alignment.
The study used teacher-driven local writing distinct from OTB15's e/s error-learning
mechanism. During sharing there was no new teaching input to memory and no feedback
from working units or sharing lines into local memory. It consequently did not
test learning the shared experience in the recipient.

## 6.2 Dependency controls delimit what was shared

After exploratory pilots, the main settings were fixed locally before acquisition.
The report is a numerical mechanism test with descriptive analysis, not the same
form of confirmation as E7-D. Eight previously unused initial phases were tested
under two fixed coordinate labelings of the same logical chain. The 16 conditions
are not 16 independent semantic worlds.

| Condition | Recipient D support responses |
|---|---:|
| Three relations form a chain; sharing enabled | 16/16 |
| Same state; sharing disabled | 0/16 |
| Query stimulus omitted | 0/16 |
| Each necessary local memory-to-working transmission disabled in turn | 0/48 |
| Either necessary owner-to-owner connection disabled | 0/32 |
| Provider alone re-experienced the intervening relation as unsupported in the same context | 0/16 |

The local-memory control disabled transmission while preserving the memory itself.
An owner-to-owner disconnection disabled the bundled links for all four objects in
both directions; it was not an ablation of a single directed edge. In the provider-
change comparison, the recipient's starting memory, working state and filters were
held identical across the corresponding conditions. The response depended on the
providers' local experience and on the specified transmission paths, rather than
merely on other owners being present. [OTB22]

Silence was scored as withholding support. It was not interpreted as learned
negation or proof that no possible path existed. Ordinary graph processing can
solve the reference task, so these controls do not establish an advantage of
oscillators over a conventional graph representation. They support the narrower
mechanistic claim that the specified coupled dynamics could use separately held
relations while connected.

## 6.3 More management operations did not always help

The initial continuously connected pilot produced unwanted support and residual
activity and did not meet its original functional criteria. Those failures remain
part of the evidence. Later main acquisition did not establish that the added
handoff restoration or closing of sharing lines was necessary: the tested main
conditions also stopped without the extra handoff restoration. This does not mean
that all external preparation was removed. Pre-query restoration, context and
stimulus timing were still supplied in all modes. Differences between the earlier
stopping pilot and the main acquisition were not causally isolated. [OTB22]

Preservation of local memory also needs a structural interpretation. With no
feedback from sharing activity into the local memories, identical memory evolution
at equal elapsed time was expected by construction. The checks establish retention
during this readout arrangement, not resistance to interference during new learning.

The conflict condition provides a further limit. One owner retained B→C while
another retained an opposing B↛C experience. Their distinct local responses could
coexist, but the network still supported D in 16/16 conditions. It did not withhold
the conclusion because the providers disagreed. Detecting the conflict in an
external scoring graph is not conflict detection by the oscillator system itself.

The third wall therefore remains only partly crossed. Connected use was
demonstrated within this artificial relation task; automatic semantic alignment,
recipient learning, conflict-sensitive abstention and real distributed communication
were not. The sharing lines were numerical couplings in one process, not a test of
network latency, packet loss or a deployed multi-user service. These limitations
are part of the operational meaning of *sharing*, rather than implementation
details that can be omitted from the capability claim.

# 7. Division of roles, adverse evidence, and related research

The three walls organize questions about operations. They do not imply that a
single kind of unit should perform every operation, or that adding an explicit
management module is always beneficial. The most useful counterexamples are those
that would be inconvenient for a claim of general T7 superiority.

## 7.1 A memory-bearing unit need not be a good relay

MC-5C evaluated a circuit with a T7 memory population, slow and fast LIF relays,
and an output unit on 20 previously unused circuits. Its *both* measure was the
smaller of the distant- and recent-history discrimination accuracies. The main
LIF-relay condition achieved 0.707. Controls included removing each relay and
refitting the remaining weights, as well as swapping the roles. The confirmation
used circuit-level inference and a fixed sequence of primary tests. [MC5C]

A secondary comparison was unfavorable to T7. With refractory period 32 in both
relay models, the reported means were 0.698 for LIF and 0.508 for T7. The paired
mean difference computed from the unrounded saved scores was −0.189, with a
reported 95% interval of [−0.201, −0.178]; every circuit favored LIF. Refractory
periods were matched, but firing rates were not. Thus this comparison did not
match the spike budget or identify a universal difference between the substrates.
[MC5CDATA]

MC-5D explored the issue on a separate five-circuit set. Candidate operating points
were constrained using validation firing-rate targets with a ±20% tolerance at
three levels. LIF relays outperformed T7 relays at all three levels. Clipping
negative phase to zero in a separate diagnostic unit did not remove the gap.
This was an exploration, not a repeat of the confirmation, exact equality of
firing rates, or optimization over every operating point. It narrowed candidate
explanations within the tested setting without identifying a complete mechanism.
[MC5D]

The negative evidence concerns the relay role. It does not demonstrate that T7 is
necessary or advantageous in the upstream memory population, which was not replaced
by LIF in this comparison. A mixed circuit's success cannot be credited entirely
to its oscillator memory units. The possibility that other substrates could perform
every required role remains a legitimate comparison. Role specialization is a
design hypothesis to evaluate, not a way of exempting a preferred unit from
unfavorable comparisons.

## 7.2 Management can be embedded in learned dynamics

The local E3b study gives another constraint on the interpretation. Under its
strengthened training procedure, some small GRUs solved the reset-free task, but
only five of twenty models passed the stated validation learning criterion.
The evaluation reported both all-model and successful-model outcomes. Its results
show that an alternative learned update rule can implement a solution; the best
successful runs should not be presented as the performance of every training run.
Conversely, the observed success fraction is not a general property of GRUs.
Learning targets and temporal resolution differed from T7, so this was not a
matched ranking of the two model families. [E3B]

This example fits an established mechanism. Cho et al.'s recurrent unit uses reset
and update gates to control the use of previous hidden state and the incorporation
of a candidate activation. Mamba makes selected state-space parameters depend on
the current input, enabling selective propagation or forgetting along a sequence.
These models already contain operations over history in their state updates.
The proposal here does not require those operations to reside in a separately
named or anatomically distinct management layer. [GRU2014] [MAMBA2023]

The main application of an explicit preparation question is a substrate whose
update rule is fixed or constrained, where changing a readout or available input
operation is different from learning a new internal recurrence. This is a problem
setting, not evidence that fixed substrates are superior to trainable ones.

## 7.3 Connections to existing memory research

The distinction between holding information and making it useful has substantial
precedent. The following connections constrain the proposed agenda; they are not
a claim to have originated selective reading, gating, adaptation or memory access.

**Adaptive spiking state.** Bellec et al.'s LSNNs include adapting neurons whose
thresholds reflect preceding firing activity and decay toward baseline. Their
weights and, in some settings, connectivity are optimized with BPTT. Adaptation
is therefore a legitimate history-bearing state, not a category to exclude from
memory in order to make T7 distinctive. Even a non-adaptive LIF membrane is a
dynamical state; it is inaccurate to call LIF intrinsically history-free.
[ALIF2018]

**Capacity and readout.** Dambre et al. quantify dynamical information processing
through linear reconstruction of functions of input history, under explicit
assumptions. Their work already connects memory and computation through an
allowed readout. Our proposed report adds questions about interventions during
operation: which allowed action can succeed, what reading changes, and what
learning or sharing costs. This is a complementary evaluation agenda, not a
replacement capacity theorem. We do not infer that the T7 cases satisfy that
theory's assumptions or evade its bounds. [DAMB2012]

**Temporal credit and protection.** E-prop combines locally computed eligibility
traces with learning signals to approximate gradient-based learning in recurrent
networks. That temporal credit-assignment mechanism is not the same operation as
deciding when a later query or update can safely proceed. Likewise, EWC protects
parameters important for old tasks through a weighted penalty during new learning.
These precedents make it untenable to describe runtime history or interference
protection as problems ignored by mainstream learning research. OTB21 supplies a
small fixed-rule example of a different intervention, not a replacement for those
learning methods. [EPROP2020] [EWC2016]

**Explicit external access.** Neural Turing Machines couple a controller to a
memory bank through selective read and write operations, including erase and add
components. Retrieval-augmented generation combines a parametric generator with
retrieval from a non-parametric document index. Access and modification of memory
are already explicit architectural subjects in these systems. Their successes do
not establish the oscillator mechanisms, and an oscillator sharing result is not
a demonstration of document retrieval, semantic grounding or recipient learning.
[NTM2014] [RAG2020]

These are claim-focused checks of eight primary papers, not an exhaustive review
of control, reservoir computing, continual learning, distributed memory or
cognition. The contribution proposed here is a constrained research agenda and a
portable measurement protocol, illustrated by successful, adverse and unresolved
oscillator cases. Its value must ultimately be judged by whether the distinctions
help predict useful interventions beyond these examples, not by giving established
mechanisms a new name.

## Primary experimental and literature references

[OTB20]: sources/OTB20_REPORT.md
[OTB21]: sources/OTB21_REPORT.md
[OTB21DATA]: sources/OTB21_checked_aggregates.json
[OTB22]: sources/OTB22_REPORT.md
[MC5C]: sources/MC5C_REPORT.md
[MC5CDATA]: sources/MC5C_verdicts.json
[MC5D]: sources/MC5D_REPORT.md
[E3B]: sources/E3B_REPORT.md
[ALIF2018]: https://arxiv.org/abs/1803.09574
[EPROP2020]: https://doi.org/10.1038/s41467-020-17236-y
[DAMB2012]: https://doi.org/10.1038/srep00514
[GRU2014]: https://arxiv.org/abs/1406.1078
[MAMBA2023]: https://arxiv.org/abs/2312.00752
[EWC2016]: https://arxiv.org/abs/1612.00796
[NTM2014]: https://arxiv.org/abs/1410.5401
[RAG2020]: https://arxiv.org/abs/2005.11401
