# Model and scope

The experiment changes one of two known binary response rules while leaving the other unchanged. The routing from operation/context to a relevant feature is supplied by the designer. Eight previously learned memory states are reused. Four synthetic work-oscillator phase configurations are drawn once and shared across comparisons.

Each memory cell combines T7 state with a bistable amplitude `u`, a decaying eligibility trace `e`, and an error accumulator `s`. A source firing tags the corresponding route. A later externally calculated prediction error enters the accumulator.

```text
e_next = exp(-1/tau_e) * e        (source events retag the selected route)
s_next = s + (e * delta - s) / tau_s
h = 0.1 * tanh((m - MC) / 0.25) + 6 * s
du/dt = 2 * NU * u * ((u - 2) - (u - 2)^3 + h)
```

The bistable fold threshold is `hcrit = 2/(3*sqrt(3)) ≈ 0.384900`. For non-target cells already in the low (`u <= 2-1/sqrt(3)`) or high (`u >= 2+1/sqrt(3)`) retention band, constrain both `e` and `abs(s)` below `theta = 0.95*(hcrit-0.1)/6 ≈ 0.045109`. With bounded error `abs(delta)<=1` and no new eligibility tag on these cells, decay and the convex accumulator update keep the tilt below the barrier.

This is a sufficient retention condition for the continuous amplitude equation under those assumptions. It does not guarantee recovery from the intermediate band, arbitrary numerical step sizes, or successful writing of the target cell. Target adaptation is measured separately.

The three policies are immediate progression, a fixed 4,096-step wait, and a wait until the retention condition holds. Work-oscillator restoration inputs remain present. "No direct reset" does not mean "no external preparation".

A current query follows a previous query without its teaching label. A later correct label reverses operation 0. Residual traces can route that label into the unchanged operation 1. Query durations are 1,536/2,048/4,096 steps. Duration and label-arrival timing change together; this does not isolate a pure inference-deadline effect.

The included acquisition and source snapshots specify the exact native step order. They are the authority for reproduction. The compact equations above explain the mechanism rather than replace that implementation.
