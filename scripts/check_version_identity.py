#!/usr/bin/env python3
"""Verify that the public EWD release identity is consistent across metadata."""

from __future__ import annotations

import json
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    print(f"VERSION_IDENTITY_FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def extract(pattern: str, text: str, label: str) -> str:
    match = re.search(pattern, text, flags=re.MULTILINE)
    if not match:
        fail(f"could not read {label}")
    return match.group(1)


citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
canonical = extract(r"^version:\s*[\"']?([0-9]+\.[0-9]+\.[0-9]+)[\"']?\s*$", citation, "CITATION.cff version")

pyproject = tomllib.loads((ROOT / "science/pyproject.toml").read_text(encoding="utf-8"))
package_version = pyproject["project"]["version"]

lock = tomllib.loads((ROOT / "science/uv.lock").read_text(encoding="utf-8"))
lock_versions = [
    package.get("version")
    for package in lock.get("package", [])
    if package.get("name") == "empirical-world3-dynamics"
]
if len(lock_versions) != 1:
    fail(f"expected one empirical-world3-dynamics package in uv.lock, found {len(lock_versions)}")
lock_version = lock_versions[0]

init_text = (ROOT / "science/src/world3_empirical/__init__.py").read_text(encoding="utf-8")
runtime_version = extract(r'^__version__\s*=\s*[\"\']([^\"\']+)[\"\']\s*$', init_text, "__version__")

manifest_path = ROOT / "data/scenarios/bau_hybrid_2026_manifest.json"
manifest_version = json.loads(manifest_path.read_text(encoding="utf-8"))["version"]

builder_text = (ROOT / "science/scripts/build_joint_hybrid_2026.py").read_text(encoding="utf-8")
builder_version = extract(r'^\s{8}\"version\":\s*\"([^\"]+)\",\s*$', builder_text, "Joint builder manifest version")

observed = {
    "science/pyproject.toml": package_version,
    "science/uv.lock": lock_version,
    "science/src/world3_empirical/__init__.py": runtime_version,
    "data/scenarios/bau_hybrid_2026_manifest.json": manifest_version,
    "science/scripts/build_joint_hybrid_2026.py": builder_version,
}

mismatches = {path: value for path, value in observed.items() if value != canonical}
if mismatches:
    details = ", ".join(f"{path}={value!r}" for path, value in mismatches.items())
    fail(f"canonical CITATION.cff version is {canonical!r}; mismatches: {details}")

release_note = ROOT / f"releases/v{canonical}.md"
if not release_note.is_file():
    fail(f"missing release note {release_note.relative_to(ROOT)}")

status_text = (ROOT / "STATUS.md").read_text(encoding="utf-8")
status_version = extract(
    r"Empirical World3 Dynamics \(EWD\) v([0-9]+\.[0-9]+\.[0-9]+)",
    status_text,
    "STATUS.md release version",
)
if status_version != canonical:
    fail(f"STATUS.md identifies {status_version!r}, expected {canonical!r}")

print(f"VERSION_IDENTITY_PASS: {canonical}")
print("Checked CITATION.cff, package metadata, lockfile, runtime version, Joint builder, retained manifest, release note and STATUS.md")
