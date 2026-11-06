# From Having Memory to Using It

Research agenda manuscript workspace, revision 1.3, 6 November 2026.

- `DETAILED_OUTLINE_2026-11-06.md`: Japanese outline v1.2, integrating the new-circuit evaluation in Section 4 and Appendix B while preserving the three-wall structure and adverse MC/OTB evidence.
- `SECTION_4.en.md`: integrated English first draft of Wall I, with primary-source references and a Figure 3 caption. It does not replace the historical case-study drafts.
- `EVIDENCE_MAP.ja.md`: extracted Appendix B, including claim strength, unresolved comparisons and wording rules.
- `CASE_STUDY.en.md`: English insertion draft for Sections 2.3 and 4.4, figure caption, and reporting note. No introduction is included.
- `WRONG_HISTORY_GENERALIZATION.en.md`: subsequent 20-circuit evaluation and matched-donor control, including adverse hold-ordering evidence and the limits of content identification.
- `READER_PROTOCOL.ja.md`: synchronized Appendix A, including a policy-by-intervention comparison and conditional-effect reporting.
- `figures/figure2_usable_memory.pdf` / `.png`: central figure drawn directly from the saved fresh-cohort summary.
- `sources/`: evidence snapshots; original provenance, history-coupling evidence and `wrong_history_manifest.json` are separate. The latter pins the new evidence to result commit `bed5dc0`.
- `archive/`: earlier outline and reader-protocol revisions, retained before integration.
- `figures/figure3_wrong_history_generalization.*`: unchanged PNG/PDF/SVG copies of the new experiment figure, supporting Section 4.

The earlier five-circuit example reports a positive mean difference whose prespecified minimum-effect criterion was **not met**. Secondary sign reversals do not replace that primary decision. The subsequent addendum supports a positive average difference across 20 newly calibrated circuits and an own-component advantage over a matched donor, under a distinct zero-based generalization test. It does not change the earlier decision. Content versus state compatibility, and the cause of input-specific differences, remain unresolved. The hold ordering reversed in the new panel; two hold conditions are not a monotonic gradient.

The earlier evidence is tied to local experiment commit `bd22f95`; the subsequent addendum uses the separate acquisition freeze `0862365`. These are not currently published GitHub evidence URLs. Public versioned links and completion of the primary-literature review remain necessary before submission. The manuscript edits do not change either frozen experiment or acquire more data.

Regenerate the presentation figure using the pilot requirements from the repository:

```bash
python papers/from_having_memory_to_using_it/figures/plot_case_study.py
```

## Current writing stage

Section 4 is drafted. Sections 5–7, the limits section and Appendix A remain to be
assembled into continuous prose. The introduction and abstract follow primary-
literature checking. No further experiment is required to complete this writing
step. `WRITING_CHANGELOG.ja.md` records what changed and which interpretations
remain hypotheses. No new acquisition, statistical test, submission or publication
was performed for this manuscript revision.
