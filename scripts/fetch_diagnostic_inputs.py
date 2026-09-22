#!/usr/bin/env python3
"""Materialize non-central diagnostic source files under a verified local cache.

This fetch path is intentionally separate from scripts/fetch_science_inputs.py.
Central Joint 2026 reproduction must not depend on availability of diagnostic
source servers.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "science" / "data" / "diagnostic_remote_inputs.json"


def digest(path: Path, algorithm: str) -> str:
    try:
        h = hashlib.new(algorithm)
    except ValueError as error:
        raise RuntimeError(f"Unsupported hash algorithm: {algorithm}") from error
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def valid(path: Path, metadata: dict[str, object]) -> bool:
    if not path.is_file():
        return False
    size = metadata.get("size_bytes")
    if size is not None and path.stat().st_size != int(size):
        return False
    algorithm = str(metadata["hash_algorithm"])
    expected = str(metadata["hash"])
    return digest(path, algorithm) == expected


def validate_destination(relative: str, cache_root: str) -> Path:
    root = (ROOT / cache_root).resolve()
    destination = (ROOT / relative).resolve()
    try:
        destination.relative_to(root)
    except ValueError as error:
        raise RuntimeError(
            f"Diagnostic destination escapes cache_root {cache_root!r}: {relative}"
        ) from error
    return destination


def fetch(
    source_id: str,
    metadata: dict[str, object],
    *,
    cache_root: str,
    check_only: bool,
) -> None:
    relative = str(metadata["destination"])
    destination = validate_destination(relative, cache_root)
    if valid(destination, metadata):
        print(f"DIAGNOSTIC_INPUT_PASS: {source_id} -> {relative}")
        return
    if check_only:
        raise RuntimeError(
            f"Diagnostic input absent or corrupt: {source_id} -> {relative}"
        )

    url = str(metadata["url"])
    if not url.startswith("https://"):
        raise RuntimeError(f"Diagnostic source does not use HTTPS: {source_id}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".part")
    temporary.unlink(missing_ok=True)
    try:
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "empirical-world3-dynamics/0.1.0 diagnostic-source-audit",
                "Accept": "*/*",
            },
        )
        with urllib.request.urlopen(request, timeout=180) as response, temporary.open("wb") as output:
            shutil.copyfileobj(response, output, length=1024 * 1024)
        if not valid(temporary, metadata):
            actual_algorithm = str(metadata["hash_algorithm"])
            actual_hash = digest(temporary, actual_algorithm)
            raise RuntimeError(
                f"Downloaded diagnostic input does not match frozen identity: {source_id}; "
                f"size={temporary.stat().st_size}, {actual_algorithm}={actual_hash}"
            )
        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)

    print(f"DIAGNOSTIC_INPUT_FETCHED: {source_id} -> {relative}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        action="append",
        default=[],
        help="Fetch/check only this manifest source ID; repeat for multiple sources.",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Verify already materialized files without network access.",
    )
    args = parser.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    cache_root = str(manifest["cache_root"])
    sources = manifest["sources"]
    selected = args.source or list(sources)

    unknown = sorted(set(selected) - set(sources))
    if unknown:
        raise RuntimeError(f"Unknown diagnostic source IDs: {unknown}")

    for source_id in selected:
        fetch(
            source_id,
            sources[source_id],
            cache_root=cache_root,
            check_only=args.check_only,
        )

    print(f"DIAGNOSTIC_INPUTS_PASS: {len(selected)} source(s) verified")


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(f"DIAGNOSTIC_INPUTS_FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
