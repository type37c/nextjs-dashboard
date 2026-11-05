# OTB21: fixed readiness policies on new work phases and query deadlines

2026-11-05. Final boundary evaluation for this integration study. No parameter
adjustment or further search follows these results within this experiment.

The saved OTB15 retained memories are unchanged (normal seeds 24001..24008).
Generate four work-phase vectors, shared across all seeds, using NumPy RNG 27501,
uniform [0,2pi) independently for three work oscillators. Initial work m=-1.2,
refractory state=512, and previous event=0. These are declared new synthetic input
conditions, not measured natural histories or new independent worlds.

For each seed, phase vector and old pair 2/3, execute one unlabeled old-context
query for 4096 steps with restore128, then retain its complete memory/work state.
From each resulting boundary, run current pair 0/1 with a total query duration
1536, 2048, or 4096 steps, restore128 preparation, and one delayed observation.
The observed world reverses operation 0 only; operation 1 remains unchanged.

Three preparation policies are frozen before these new inputs are acquired:

- usual: no additional wait.
- fixed4096: wait 4096 steps before the current query. This value was selected
  from the earlier OTB20 delay grid, not from OTB21 results.
- guard: reuse OTB19's unchanged threshold theta=.95*(hcrit-.1)/6 and its waiting
  calculation from the actual noncurrent e/s state.

The original T7, companion, eligibility and error-integration equations remain
unchanged. Waiting uses original advance(query=False, delta=0), which also applies
the existing restoration input to work states. No live phase/state reset occurs
after the old query. World outcomes enter only the write error, computed from the
actual current-query prediction. A pending prediction uses the original (.5,.5)
probability convention; no hidden rule is sent to the query or guard.

The full factorial is 8 seeds x 4 phase draws x 2 old pairs x 2 current pairs x
3 query durations x 3 policies = 1152 learning trials. Every trial has one outcome
delay of 1000 steps and one write of 8000 steps. Four-context canonical probes
operate on copies after writing and do not return to the live state.

Record current-context adaptation separately from unchanged operation-1 bands
and responses. Also record source-event times, whether the current context was
tagged, at-write e/s, the guard bounds, extra waiting, and total live time. The
guard supplies a sufficient condition for protecting noncurrent memory; it does
not guarantee that the current input is processed, tagged, or learned by a short
deadline. All unknown/incorrect cases remain in the denominator.

Check finite/positive states, all saved band endpoints, and guard bounds for all
trials. Save full old/wait/query/delay/write traces for the preselected first
seed, phase index 0, old pair 2, current pair 1, query duration 1536, policies
usual and guard. Continuous-time bounds and selected numerical traces are
distinct evidence. No arbitrary-step numerical invariance theorem is claimed.

Snapshot/hash source, design, generated inputs, all eight memory source files,
and the earlier frozen policy/configuration records before acquisition. The CLI
requires an explicit output name and refuses existing output directories.

This evaluation checks changed phase/history/deadline inputs in an existing
four-context binary task family. It is not confirmation on novel semantic rules,
new physical devices, broad scale, or general autonomous learning.
