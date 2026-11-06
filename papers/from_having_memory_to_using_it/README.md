# From Having Memory to Using It

Research agenda manuscript workspace, revision 1.4, 6 November 2026.

Start with **[the English working manuscript](MANUSCRIPT.en.md)**. It contains the
abstract, Sections 1–8, the reader protocol, evidence map, two existing figures,
primary-literature bibliography and experimental source links. It is a readable
draft publicly shared for discussion, not a peer-reviewed or submission-ready paper.

[Publication scope and verification](PUBLICATION.md) · [Download the reviewed bundle](downloads/OSCILLATOR_MIND_PAPER_FULL_DRAFT_2026-11-06.zip)

## Source documents

- [FRONT_MATTER.en.md](FRONT_MATTER.en.md): abstract, introduction, limits and falsifiable commitments, and the model/observation distinction.
- [SECTION_4.en.md](SECTION_4.en.md): Wall I; unchanged from the previously reviewed revision. Its original editorial note records the writing stage then.
- [SECTIONS_5_7.en.md](SECTIONS_5_7.en.md): acquisition versus retention, connected experience use, unfavorable relay comparisons and related work.
- [CONCLUSION_AND_PROTOCOL.en.md](CONCLUSION_AND_PROTOCOL.en.md): conclusion, English reader procedure and compact evidence map.
- [DETAILED_OUTLINE_2026-11-06.md](DETAILED_OUTLINE_2026-11-06.md): Japanese detailed outline v1.3. [READER_PROTOCOL.ja.md](READER_PROTOCOL.ja.md) and [EVIDENCE_MAP.ja.md](EVIDENCE_MAP.ja.md) preserve its full Japanese appendices; the English appendix is an edited presentation, not a line-by-line translation.
- [LITERATURE_CHECK.md](LITERATURE_CHECK.md): claim-focused checks of eight primary papers, with passage locations, short excerpts and coverage limits.
- [REFERENCES.md](REFERENCES.md) and [references.bib](references.bib): bibliography. Six entries cite arXiv versions; e-prop and Dambre cite checked journal records.
- [MANUSCRIPT_VALIDATION.json](MANUSCRIPT_VALIDATION.json): document consistency, stored-number comparisons and unchanged experimental artifact checks. This is not peer review or new experimental confirmation.
- `sources/`: pinned experimental snapshots and literature metadata. Full retrieved paper texts are not redistributed.
- `archive/`: previous outline/protocol revisions and revision 1.3 editorial documents.
- `figures/`: unchanged figures 2 and 3 from the earlier evidence packages. Planned figures 1, 4 and 5 have not been created.

`CASE_STUDY.en.md` and `WRONG_HISTORY_GENERALIZATION.en.md` remain historical
insertion drafts. They are not additional chapters of the assembled manuscript.

## Scientific boundaries

The earlier five-circuit minimum-effect criterion remains **unmet**. The separate
twenty-circuit evaluation supports a positive average normal-minus-removal
difference and an own-component advantage over a matched donor under its specified
generator, calibration procedure and multiplicity plan. Content and state
compatibility remain incompletely separated. Neither the adverse hold ordering nor
unresolved donor/removal comparison is hidden.

OTB21 does not establish matched-time superiority. OTB22 does not establish
recipient learning or conflict-sensitive abstention. The unfavorable MC relay
results constrain a general claim of T7 superiority. Management is a functional
description that can include learned dynamics, not a demonstrated separate seat
of intelligence. The eight-paper check is focused, not an exhaustive novelty review.

## Rebuild and review

```bash
python papers/from_having_memory_to_using_it/assemble_manuscript.py
python papers/from_having_memory_to_using_it/audit_publication.py
```

The assembly preserves source prose and moves existing figure captions into a
figure section. The public audit checks published files against a SHA256 manifest.
It does not rerun dynamics or hypothesis tests. The original `validate_manuscript.py`
requires the full research checkout and Git history; its recorded result is included
for provenance, not presented as a public reproduction of all 2,251 artifacts.
The source experimental result commit is `bed5dc0`; the previously reviewed
manuscript commit is `2e9bf8c`. These identifiers refer to the research repository.

The manuscript and cited source snapshots are now available in this public
repository. Relative links in the manuscript resolve to the included snapshots;
use a commit permalink to cite a fixed version. The full research checkout is not
published by this documentation update. Venue-specific editing, broader literature
coverage where needed, and a standalone reproduction package for the new experiments
remain separate tasks. No new acquisition, statistical test or journal submission
was performed. Historical editorial notes retain their original writing-stage status.
