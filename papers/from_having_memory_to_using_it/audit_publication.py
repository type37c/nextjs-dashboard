"""Check the published document inventory; no experiment or inference is run."""
import hashlib
import json
from pathlib import Path
import re

from assemble_manuscript import assemble

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]


def main():
    manifest = json.loads((ROOT / "PUBLICATION_MANIFEST.json").read_text())
    for relative, entry in manifest["files"].items():
        path = REPO / relative
        assert path.is_file(), relative
        assert hashlib.sha256(path.read_bytes()).hexdigest() == entry["sha256"], relative
    manuscript = (ROOT / "MANUSCRIPT.en.md").read_text()
    assert manuscript == assemble(), "Assembly differs from the published manuscript"
    definitions = dict(re.findall(r"^\[([^\]]+)\]: (.+)$", manuscript, re.M))
    uses = set(re.findall(r"\[([A-Z][A-Z0-9]+)\](?![:(])", manuscript))
    assert uses <= definitions.keys()
    local_targets = [v for v in definitions.values() if not v.startswith("https://")]
    local_targets += re.findall(r"!\[[^\]]*\]\(([^)]+)\)", manuscript)
    for target in local_targets:
        assert (ROOT / target).is_file(), target
    print(json.dumps({
        "published_files_verified": len(manifest["files"]),
        "manuscript_assembly_matches": True,
        "manuscript_local_targets_resolve": True,
        "scope": "file integrity and document consistency only; no experimental reproduction",
    }, indent=2))


if __name__ == "__main__":
    main()
