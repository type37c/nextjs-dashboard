# Oscillator Mind research map

The organizing question is how memory-dependent individual dynamics become computation, learning and joint use of experience through connections. This map separates the broader program from what a reader can reproduce from this checkout.

## 1. Individual dynamics

Investigate how the history-dependent state changes phase velocity, firing, refractory behavior and response to input. Understand the single unit before attributing network behavior to it. The public [model explanation](INDIVIDUAL_DYNAMICS.md) points to the actual bundled equations. A standalone reproduction of the earlier single-unit studies is a future release task.

## 2. Network computation

Connect memory, processing and output components and test whether a retained distinction becomes useful downstream. In the E/OM line this includes preparation selection for repeated computation.

The included E7-D report records 57.8% seven-query all-correct performance versus 48.5% for the frozen E7 comparator and 51.6% for its refitted mixed comparator. It evaluates new input groups on five known circuits; weights were learned externally. Most remaining failures in that experiment occurred where neither of the two available preparation candidates could succeed. The numerical result is specific to that architecture, not a network-wide completion percentage.

**Public evidence:** [original E7-D report](evidence/E7D_REPORT.md), report only. Its complete acquisition code and data are not included in this checkout.

## 3. Continual computation and learning

Repeated computation changes the state from which the next calculation starts. Learning also acts on a state containing previous activity. This makes preparation a question about both readout and writing.

OTB15 explores prediction-error-driven updates of shared amplitude memory through eligibility and error accumulation. Under supplied feature routing, it reports 64/64 predictions after learning, retention and a rule reversal. A simple numerical table and a non-oscillatory memory comparator also solve that task. The local update is engineered and receives external teaching error.

OTB21 tests whether residual query activity corrupts a relation that has not changed. Its state-based waiting condition retains the old relation across the tested phases and durations, while all policies learn the changed relation. Additional time is a substantial cost. General continual learning and an equal-time advantage remain open.

**Public evidence:** [OTB15 report](evidence/OTB15_REPORT.ja.md), report plus selected frozen dependencies; [OTB21](studies/OTB21.md), fully bundled acquisition, saved data and audit. Reproducing OTB21 starts from included OTB15 learned states, not retraining them.

## 4. Experience sharing

The larger question is whether connected systems can use experience retained by different owners. OTB22 tests a minimal version: three modules separately retain A→B, B→C and C→D and connect through work-unit firing. Its 16/16 supported responses are eight phase configurations × two coordinate representations of the same chain, not sixteen independent semantic tasks. Cutting necessary memory transmission or owner connections removes the response.

This is evidence for a limited **joint-use mechanism while connected**. Recipient learning, contradictory-testimony handling, automatic matching of situations and real communication networks remain research goals. OTB22 uses teacher-driven memory writing rather than OTB15's error-learning mechanism; the two have not been demonstrated as one integrated sharing-and-learning system.

**Public evidence:** [original OTB22 report](evidence/OTB22_REPORT.ja.md), report only. No standalone OTB22 reproduction is bundled yet.

## Evidence levels and release order

| Material | Status in this repository |
|---|---|
| OTB21 saved data, frozen code, dependencies, audit | Public and runnable; local release reproduction recorded. |
| T7/companion model explanation | Grounded in included code; not a separate scientific confirmation. |
| E7-D, OTB15 and OTB22 reports | Public source reports; their wider artifacts are not all bundled. |
| Fully integrated adaptive oscillator network | Research objective, not an established result. |

Useful future releases are a single-unit demonstration, a minimal connected computation, and a self-contained sharing experiment, each with its own assumptions, baselines and reproduction command. They should preserve the earlier failures rather than present a sequence of successes alone.
