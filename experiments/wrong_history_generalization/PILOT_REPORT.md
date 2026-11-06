# Training-only pilot report

2026-11-06. Three new circuits810000–810002, excluded from the main evaluation.
No evaluation cohort or held-out success criterion was used for these choices.
Ancestral clocked R,135-candidate P/weight, E7-A preparation, and E7-D threshold
calibration completed on all three. Original native-generator equality was checked
against historical circuits200–204. Self-donor sham and old B0/B2 numerical parity
passed. The final donor rule is a random paired derangement; an initial synthetic
cyclic-matching check is retained in logs, but paired blocks were selected before
readout pilot acquisition to permit dependence-preserving secondary bootstrap.

All96 readout-training rows across the three circuits had donors (both holds reuse
them). All12 arm-specific readouts had both labels and converged; no fallback.
Each arm used448 training rows before selective filtering. No training accuracy
is reported as generalization. Structural calibration cost is separate.

|Circuit|Hold|Donor/own SD|Absolute KS|Mean absolute displacement|Correlation|
|---|---:|---:|---:|---:|---:|
|810000|512|1.0004|0.0625|0.0626|0.9490|
|810000|16384|0.9986|0.0625|0.0990|0.9771|
|810001|512|0.9967|0.0625|0.0497|0.9695|
|810001|16384|1.0007|0.0625|0.1238|0.9712|
|810002|512|0.9783|0.0938|0.0686|0.9303|
|810002|16384|1.0009|0.0625|0.0989|0.9770|

Marginal component scales were close, but the high correlations show that the
same-A/current-input pairing retains considerable shared structure. These donors
are not unrelated histories in an unconditional sense. Neither magnitude matching
nor a future equivalence outcome would alone identify operating-point causality.
No donors were chosen by outcome or phase distance. Exact recipient current input
amplitude was retained in the donor-prefix simulation.

Proceed with20 other circuits and64 evaluation groups each. Retain the proposed
±2-point equivalence margin as a stated substantive tolerance; these three pilot
circuits do not validate its power. Primary inference uses circuits; secondary
within-circuit resampling keeps paired donor blocks together. The two scientific
questions require five Holm-corrected claims, detailed in PLAN.md.

No adjustment of donors, margins or circuit selection is allowed after main
outcomes. Failed distribution diagnostics will be reported rather than repaired
or used to remove circuits.
