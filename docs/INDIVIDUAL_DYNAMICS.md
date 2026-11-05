# Individual dynamics: why begin with the unit?

The program begins with a physical-model question: if a unit retains a trace of its past, and that trace changes its motion, what kinds of computation become possible when such units interact?

In the **discrete T7 work-unit implementation bundled here**, each unit carries an internal state `m`, phase `phi`, refractory counter `cd`, and its previous firing event. The step order is:

```text
proposed_phase = phi + omega + kappa*m
fire = (proposed_phase >= 2*pi) and (cd == 0)
m_next = (1-epsilon)*m + drive - beta*fire
phi_next = 0 if fire else proposed_phase modulo (2*pi)
cd_next = R if fire else max(cd-1, 0)
```

See the work-unit loop in [the preserved OTB15 model](../experiments/otb15_local_error_learning/model.py). The input `drive` can include external stimulation, preparation feedback and another unit's previous firing. The exact phase wrapping, refractory rule and update order matter; a generic continuously firing oscillator is not an interchangeable implementation.

The internal state is both affected by history and used in future motion. This is the concrete meaning of **memory-dependent** here. The coefficient `kappa` couples `m` into phase evolution. This definition alone is not a claim of novelty over adaptive or history-dependent oscillator models.

## From a unit to a network

An output event carries consequences of a unit's state into a receiving unit. Connecting units raises questions that cannot be answered from memory retention alone:

- Does the stored distinction produce distinguishable firing?
- Can the receiver use that distinction from its current state?
- Does a query change the state needed for the next query?
- Which histories should receive a later teaching signal?

These questions motivate the network and readiness experiments. Retaining a bit, reading it through firing, and using it in another unit are distinct experimental milestones.

## Distinct forms of memory in the current public study

| Component | Role |
|---|---|
| T7 internal state `m` | History-dependent state that changes phase evolution and responds to input/firing. |
| Companion amplitude `u` and phase `psi` | Added oscillator/companion subsystem; its bistable amplitude bands retain a learned response relation. |
| Eligibility `e` | Decaying trace of the route recently used by an input event. |
| Error accumulator `s` | Integrates eligibility-weighted teaching error and drives the companion amplitude. |
| External control | Calculates the teaching error and readiness condition, supplies routing and preparation timing. |

OTB21 uses the T7-plus-companion system and the auxiliary `e/s` states. It does not demonstrate that bare T7 memory alone provides long-term learning. The companion's retained amplitude changes the effective drive delivered to work T7 units; their output is read from firing. [OTB21's retention condition](METHOD.md).

The historical program contains other configurations and parameter regimes. The equations above describe this release's concrete work-unit implementation rather than a universal equation for every experiment called T7.
