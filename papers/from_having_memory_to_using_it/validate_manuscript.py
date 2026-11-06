"""Document checks only: no dynamics, fitting, bootstrap or hypothesis test."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
from decimal import Decimal, ROUND_HALF_UP

from assemble_manuscript import assemble

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
PRIOR = "2e9bf8c066dffe24e11a7e15326416603552e34a"
EXPERIMENT = "bed5dc0462483997fa517fe0c91e997e81635b9a"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(name):
    return json.loads((ROOT / name).read_text())


def normalized(text):
    return "\n".join(line.rstrip() for line in text.strip().splitlines())


def main():
    checks = {}
    manuscript = (ROOT / "MANUSCRIPT.en.md").read_text()
    assert manuscript == assemble()
    checks["assembled_draft_matches_source_parts"] = True

    rel = ROOT.relative_to(REPO).as_posix()
    old = subprocess.check_output(["git", "show", f"{PRIOR}:{rel}/SECTION_4.en.md"], cwd=REPO)
    assert old == (ROOT / "SECTION_4.en.md").read_bytes()
    checks["section_4_unchanged_from_reviewed_commit"] = True

    # All previously committed source snapshots and figures must remain exact.
    tracked = subprocess.check_output([
        "git", "ls-tree", "-r", "--name-only", PRIOR, f"{rel}/sources", f"{rel}/figures"
    ], cwd=REPO, text=True).splitlines()
    for path in tracked:
        assert (REPO / path).read_bytes() == subprocess.check_output(["git", "show", f"{PRIOR}:{path}"], cwd=REPO), path
    checks["unchanged_prior_source_and_figure_files"] = len(tracked)

    inventory = json.loads((REPO / "results/wrong_history_generalization/DELIVERY_MANIFEST.json").read_text())
    count = 0
    for path, entry in inventory["files"].items():
        if path.startswith("papers/"):
            continue
        assert digest(REPO / path) == entry["sha256"], path
        count += 1
    assert count == 2251, count
    checks["experiment_artifacts_unchanged_against_delivery_manifest"] = count

    # References and figure targets, without treating arbitrary brackets as citations.
    definitions = dict(re.findall(r"^\[([^\]]+)\]: (.+)$", manuscript, re.M))
    uses = set(re.findall(r"\[([A-Z][A-Z0-9]+)\](?![:(])", manuscript))
    assert uses <= definitions.keys(), uses - definitions.keys()
    for target in definitions.values():
        if not target.startswith("https://"):
            assert (ROOT / target).is_file(), target
    for target in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", manuscript):
        assert (ROOT / target).is_file(), target
    checks["all_manuscript_citations_and_local_targets_resolve"] = True

    outline = (ROOT / "DETAILED_OUTLINE_2026-11-06.md").read_text()
    app_a = outline.split("## Appendix A.", 1)[1].split("## Appendix B.", 1)[0]
    reader = (ROOT / "READER_PROTOCOL.ja.md").read_text().split("## Appendix A.", 1)[1]
    assert normalized(app_a) == normalized(reader)
    app_b = outline.split("## Appendix B.", 1)[1].split("## 図表の設計", 1)[0]
    evidence = (ROOT / "EVIDENCE_MAP.ja.md").read_text().split("## Appendix B.", 1)[1]
    assert normalized(app_b) in normalized(evidence)
    checks["Japanese_appendices_remain_synchronized"] = True

    # Read stored aggregates, format the quoted values, and compare with prose.
    # These are citation checks, not recomputation of intervals or p values.
    sec = (ROOT / "SECTIONS_5_7.en.md").read_text()
    otb = read_json("sources/OTB21_checked_aggregates.json")["checks"]
    rows = {r["group"]: r for r in otb}
    names = {"usual": "No additional wait", "fixed4096": "Fixed 4,096-step wait", "guard": "State-based guard"}
    for policy, label in names.items():
        row = rows[f"1536/{policy}"]
        values = [row[k] for k in ("current_context_correct", "untouched_operation1_correct", "joint_adaptation_and_retention")]
        time = f'{row["mean_total_live_steps"]:,.2f}'.rstrip("0").rstrip(".")
        line = "| " + label + " | " + " | ".join(f'{v}/{row["trials"]}' for v in values) + f" | {time} |"
        assert line in sec, line
    assert sum(r["trials"] for r in otb) == 1152
    assert rows["4096/fixed4096"]["joint_adaptation_and_retention"] == 128
    checks["OTB21_table_matches_previously_saved_aggregates"] = True

    mc = read_json("sources/MC5C_verdicts.json")
    for arm in ("LIF", "LIF32", "T7"):
        assert f'{mc["means"][arm]["both"]:.3f}' in sec
    delta = mc["secondary"]["both(T7) - both(LIF32)"]
    for key in ("mean", "lo", "hi"):
        assert f'{delta[key]:.3f}'.replace("-", "−") in sec
    assert delta["n"] == 20 and all(x < 0 for x in delta["per_circuit"])
    checks["MC5C_quoted_means_and_interval_match_saved_unrounded_scores"] = True

    hc = read_json("sources/HISTORY_COUPLING_CONFIRMATION_summary.json")["primary"]
    for value in [hc["mean"], *hc["ci95"]]:
        quoted = (Decimal(str(value)) * 100).quantize(Decimal(".0001"), rounding=ROUND_HALF_UP)
        assert str(quoted) in manuscript
    assert hc["ci95"][0] < .03
    checks["earlier_minimum_effect_decision_preserved"] = True

    # These checks establish correspondence with the report text, not raw-data rescoring.
    report_tokens = {
        "sources/OTB20_REPORT.md": ["32/32", "0/32"],
        "sources/OTB22_REPORT.md": ["16/16", "0/16", "0/48", "0/32"],
        "sources/E3B_REPORT.md": ["5/20"],
    }
    for filename, tokens in report_tokens.items():
        report = (ROOT / filename).read_text()
        assert all(token in report for token in tokens)
    checks["OTB20_OTB22_E3b_counts_located_in_primary_reports"] = True

    lit = read_json("sources/literature/manifest.json")["records"]
    bib = (ROOT / "references.bib").read_text()
    bib_keys = set(re.findall(r"@\w+\{([^,]+),", bib))
    assert len(lit) == 8 and bib_keys == set(lit)
    for key, expected_hash in lit.items():
        file = ROOT / f"sources/literature/{key}.json"
        assert digest(file) == expected_hash
        record = json.loads(file.read_text())
        equivalent_urls = {record["url"]}
        if record["paper_id"].startswith("doi:"):
            equivalent_urls.add("https://doi.org/" + record["paper_id"][4:])
        assert definitions[key] in equivalent_urls
        assert len(record["short_source_excerpt"].split()) < 80
        assert record["locator"] and record["coverage"]
    checks["eight_literature_records_bibkeys_urls_and_hashes_match"] = True

    files = sorted(p for p in ROOT.iterdir() if p.suffix in (".md", ".bib", ".py"))
    output = {
        "status": "document checks only; no new acquisition or statistical inference",
        "reviewed_manuscript_commit": PRIOR,
        "experiment_result_commit": EXPERIMENT,
        "checks": checks,
        "manual_review_scope": "OTB20/21/22, MC5C/5D, E3b report interpretation; eight primary literature method passages. Not an exhaustive literature review or external replication.",
        "limitations": "Automated numeric checks cover the listed citations. They do not independently verify every prose claim or all raw experimental records. The prior Section 4 validation is preserved in archive/revision_1_3/.",
        "manuscript_word_count_whitespace_including_tables_and_references": len(manuscript.split()),
        "manuscript_files": {p.name: digest(p) for p in files},
    }
    (ROOT / "MANUSCRIPT_VALIDATION.json").write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"checks": checks, "words": len(manuscript.split())}, indent=2))


if __name__ == "__main__":
    main()
