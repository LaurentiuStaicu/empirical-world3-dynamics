from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
PREVIEW = ROOT / ".github" / "EWD_README_PREVIEW.md"
CONTRACT = ROOT / ".github" / "readme_design_contract.json"
STATUS = ROOT / "STATUS.md"
CITATION = ROOT / "CITATION.cff"
RELEASE = ROOT / "releases" / "v0.1.0.md"
LIGHT = ROOT / "assets" / "readme" / "ewd-concept-overview-light.svg"
DARK = ROOT / "assets" / "readme" / "ewd-concept-overview-dark.svg"
PREVIEW_LIGHT = ROOT / ".github" / "readme-assets" / "ewd-concept-overview-light.svg"
PREVIEW_DARK = ROOT / ".github" / "readme-assets" / "ewd-concept-overview-dark.svg"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def slugify_heading(value: str) -> str:
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"\s+", "-", value.strip())


def main() -> None:
    text = read(README)
    lower = text.lower()
    header = text.split("---", 1)[0]
    status = read(STATUS).lower()
    citation = read(CITATION)
    release = read(RELEASE).lower()
    contract = json.loads(read(CONTRACT))

    require('width="112"' in header, "README icon must remain 112px")
    require('<h2 align="center">Empirical World3 Dynamics (EWD)</h2>' in header, "README must use compact h2 title")
    require(len(re.findall(r"<img alt=", header)) == 3, "README must expose exactly three primary header badges")
    require("Scientific reproducibility" in header, "README must expose the real scientific reproducibility badge")
    require("MIT License" in header, "README must expose MIT license badge")
    require("blue?style=" not in header, "README must use suite grayscale badges")

    require("Version: 0.1.0" in text, "README release badge must expose v0.1.0 explicitly")
    require(re.search(r"(?m)^version:\s*0\.1\.0\s*$", citation) is not None, "CITATION.cff version mismatch")
    require("# empirical world3 dynamics v0.1.0" in release, "v0.1.0 release note missing")

    required_readme = (
        "world3-03 structure remains the model core",
        "experimental scenario model, not a probabilistic forecast",
        "model selection is frozen through 2018",
        "uses observations available through 2025",
        "12 admissible",
        "trajectory medoid",
        "structural sensitivity envelope, not probability",
        "candidate extensions | **inactive**",
        "several parameters remain weakly identified",
        "does not currently claim",
        "p10-p90 envelope is a confidence interval",
    )
    for token in required_readme:
        require(token in lower, f"README scientific boundary missing: {token}")

    require("experimental scenario model, not a probabilistic forecast" in status, "STATUS forecast boundary mismatch")
    require("frozen through 2018" in status, "STATUS model-selection boundary mismatch")
    require("observations through 2025" in status, "STATUS production-refit boundary mismatch")
    require("12" in status and "medoid" in status, "STATUS production-candidate/medoid state mismatch")
    require("p10-p90" in status and "not" in status and "probability" in status, "STATUS sensitivity boundary mismatch")

    for phrase in contract["current_public_state"]["weak_identification_examples"]:
        require(phrase.lower() in lower, f"README weak-identification example missing: {phrase}")

    require(LIGHT.is_file() and DARK.is_file(), "Public light/dark concept assets missing")
    require(LIGHT.read_bytes() == PREVIEW_LIGHT.read_bytes(), "Public light asset diverges from reviewed preview")
    require(DARK.read_bytes() == PREVIEW_DARK.read_bytes(), "Public dark asset diverges from reviewed preview")
    require("assets/readme/ewd-concept-overview-light.svg" in text, "README light asset link missing")
    require("assets/readme/ewd-concept-overview-dark.svg" in text, "README dark asset link missing")
    require("prefers-color-scheme: dark" in text and "prefers-color-scheme: light" in text, "Responsive picture sources missing")

    targets = set(re.findall(r"\[[^\]]+\]\(([^)]+)\)", text))
    targets.update(re.findall(r'(?:href|src|srcset)="([^"]+)"', text))
    unresolved: list[str] = []
    for target in targets:
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        clean = target.split("#", 1)[0].split("?", 1)[0]
        if clean and not (ROOT / clean).exists():
            unresolved.append(target)
    require(not unresolved, f"Unresolved README local links: {unresolved}")

    headings: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if match:
            headings.append(slugify_heading(match.group(1)))
    quick_nav = re.findall(r'href="#([^"]+)"', header)
    require(bool(quick_nav), "README quick navigation missing")
    for anchor in quick_nav:
        require(anchor in headings, f"Quick-navigation anchor does not resolve: {anchor}")

    budget = contract["public_readme_quality_budget"]
    plain = re.sub(r"<[^>]+>", " ", text)
    words = re.findall(r"\b[\w][\w./+-]*\b", plain)
    primary_headings = [
        line for line in text.splitlines()
        if re.match(r"^#{1,6}\s", line) or re.search(r"<h[1-6]", line)
    ]
    require(len(words) <= budget["maximum_words"], f"README word budget exceeded: {len(words)}")
    require(len(primary_headings) <= budget["maximum_primary_headings"], "README heading budget exceeded")

    require(".github/CONTRIBUTING.md" in text, "Contributing route missing")
    require(".github/SUPPORT.md" in text, "Support route missing")
    require("CITATION.cff" in text, "Citation route missing")
    require("maintained by **Laurentiu Staicu**" in text, "Maintainer route missing")

    preview = read(PREVIEW)
    require(text != preview, "Public README must be root-adapted rather than copied byte-for-byte from preview")
    require('src="assets/icon.png"' in text, "Public icon path must be root-relative")
    require('src="../assets/icon.png"' in preview, "Preview must retain .github-relative icon path")

    print(
        f"EWD README contract PASS: {len(words)} words, "
        f"{len(primary_headings)} headings, {len(quick_nav)} quick-nav anchors."
    )


if __name__ == "__main__":
    main()
