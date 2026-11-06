"""Assemble the English working draft without changing its source sections."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
PARTS = (
    "FRONT_MATTER.en.md", "SECTION_4.en.md", "SECTIONS_5_7.en.md",
    "CONCLUSION_AND_PROTOCOL.en.md",
)


def assemble():
    definitions = {}
    bodies = []
    caption3 = ""
    for filename in PARTS:
        body = (ROOT / filename).read_text()
        for key, target in re.findall(r"^\[([^\]]+)\]: (.+)$", body, re.M):
            if key in definitions:
                assert definitions[key] == target, (key, target)
            definitions[key] = target
        body = re.sub(r"^\[[^\]]+\]: .+\n?", "", body, flags=re.M)
        body = re.sub(r"^## Primary (?:experimental records|experimental and literature references)\n", "", body, flags=re.M)
        if filename == "SECTION_4.en.md":
            body = body.replace(
                "English manuscript draft, 6 November 2026. This section integrates the evidence\n"
                "identified in the revised outline. References below identify primary experimental\n"
                "records; they are not a substitute for the paper's pending literature review.\n\n", "")
            body, caption3 = body.split("## Figure 3 caption draft\n", 1)
        # Keep one document title; sections and subsections nest below it.
        body = re.sub(r"^(#{1,2}) (?=(?:[1-8]\. |[1-8]\.\d|Appendix |A\.))", r"#\1 ", body, flags=re.M)
        bodies.append(body.strip())

    historic = (ROOT / "CASE_STUDY.en.md").read_text()
    caption2 = historic.split("## Figure caption draft\n", 1)[1].split("## Reporting and availability note", 1)[0].strip()
    figures = (
        "## Figures\n\nFigures retain their existing numbering from the evidence packages.\n\n"
        "![Figure 2: usable memory under different preparation policies](figures/figure2_usable_memory.png)\n\n"
        + caption2 + "\n\n"
        "![Figure 3: new circuits and matched donor control](figures/figure3_wrong_history_generalization.png)\n\n"
        + caption3.strip()
    )
    references = (ROOT / "REFERENCES.md").read_text().replace(
        "# References — primary literature checked for this draft", "## References — primary literature", 1)
    records = "## Primary experimental records\n\nLocal versioned snapshots used by this working draft:\n\n" + "\n".join(
        f"- [{key}]({target})" for key, target in definitions.items() if not target.startswith("http"))
    refs = "\n".join(f"[{key}]: {target}" for key, target in definitions.items())
    return "\n\n".join(bodies + [figures, references.strip(), records, refs]) + "\n"


if __name__ == "__main__":
    target = ROOT / "MANUSCRIPT.en.md"
    target.write_text(assemble())
    print(f"Assembled {target.name}: {len(target.read_text().split())} whitespace-delimited words")
