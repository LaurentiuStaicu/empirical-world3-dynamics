#!/usr/bin/env python3
"""Generate a deterministic hash inventory for retained scientific inputs."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCIENCE = ROOT / "science"
OUTPUT = SCIENCE / "data" / "input_manifest.json"
REMOTE = SCIENCE / "data" / "remote_inputs.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    remote_manifest = json.loads(REMOTE.read_text(encoding="utf-8"))
    remote_files = remote_manifest["files"]
    remote_paths = {ROOT / relative for relative in remote_files}
    candidates = [
        path
        for directory in (SCIENCE / "data" / "raw", SCIENCE / "data" / "processed")
        for path in directory.rglob("*")
        if path.is_file() and path not in remote_paths
    ]
    candidates.extend(
        [
            SCIENCE / "data" / "registry.csv",
            REMOTE,
            SCIENCE / "vendor" / "world3_03" / "World3_03_Scenarios.mdl",
        ]
    )
    files = sorted(set(candidates))
    payload = {
        "manifest_version": "1.2",
        "hash_algorithm": "SHA-256",
        "manifest_scope": "retained_scientific_input_inventory",
        "scope_description": (
            "Hashes retained scientific raw/processed inputs plus the empirical "
            "registry, remote-input manifest, and authoritative World3-03 model. "
            "The inventory includes both central and diagnostic/supporting inputs "
            "and is not a single-vintage dataset snapshot. Per-dataset retrieval "
            "and vintage dates belong in filenames, the registry, and provenance "
            "sidecars."
        ),
        "central_baseline_freeze_date": "2026-08-30",
        # Backward-compatible alias retained temporarily for external consumers.
        # It refers only to the central baseline freeze date, not to the date of
        # every file hashed by this repository-wide scientific input inventory.
        "snapshot_date": "2026-08-30",
        "snapshot_date_semantics": (
            "deprecated compatibility alias for central_baseline_freeze_date; "
            "not a per-file retrieval or vintage date"
        ),
        "local_file_count": len(files),
        "remote_file_count": len(remote_files),
        "file_count": len(files) + len(remote_files),
        "files": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in files
        },
        "remote_files": remote_files,
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        f"Wrote {OUTPUT.relative_to(ROOT)} with {len(files)} local and "
        f"{len(remote_files)} remote input hashes."
    )


if __name__ == "__main__":
    main()
