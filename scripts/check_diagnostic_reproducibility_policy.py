#!/usr/bin/env python3
"""Validate the R-FDC-7 diagnostic raw-data reproducibility policy offline."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "science/data/audits/diagnostic_source_reproducibility_2026-09-22.json"
REMOTE = ROOT / "science/data/diagnostic_remote_inputs.json"
GITIGNORE = ROOT / ".gitignore"

ALLOWED_MODES = {
    "retained_raw",
    "pinned_remote",
    "verified_transport",
    "processed_snapshot_only",
}


def fail(message: str) -> None:
    print(f"DIAGNOSTIC_POLICY_FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def require_file(relative: str, label: str) -> None:
    path = ROOT / relative
    if not path.is_file():
        fail(f"{label} missing: {relative}")


def main() -> None:
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    remote = json.loads(REMOTE.read_text(encoding="utf-8"))
    sources = audit.get("sources")
    remote_sources = remote.get("sources")

    if audit.get("gate") != "R-FDC-7":
        fail("audit gate must be R-FDC-7")
    if audit.get("gate_status") != "CLOSED_POLICY":
        fail("R-FDC-7 policy may close only as CLOSED_POLICY")
    if not isinstance(sources, list) or not sources:
        fail("audit sources must be a non-empty list")
    if not isinstance(remote_sources, dict):
        fail("diagnostic_remote_inputs.json sources must be an object")

    ids = [source.get("id") for source in sources]
    if len(ids) != len(set(ids)):
        fail("audit source IDs must be unique")

    processed_only = 0
    for source in sources:
        source_id = str(source.get("id", "<missing-id>"))
        mode = source.get("mode")
        if mode not in ALLOWED_MODES:
            fail(f"{source_id}: unsupported mode {mode!r}")
        if source.get("policy_status") != "COMPLIANT":
            fail(f"{source_id}: policy_status must be COMPLIANT")

        if mode == "processed_snapshot_only":
            processed_only += 1
            require_file(str(source["processed_artifact"]), f"{source_id} processed artifact")
            require_file(str(source["provenance"]), f"{source_id} provenance")
            if not source.get("historical_raw_sha256"):
                fail(f"{source_id}: historical raw SHA-256 is required")
            if not source.get("limitation") or not source.get("safe_claim"):
                fail(f"{source_id}: processed-only mode needs limitation and safe_claim")
            historical_raw = source.get("historical_raw_path")
            if historical_raw and (ROOT / str(historical_raw)).is_file():
                fail(
                    f"{source_id}: historical raw file now exists; update policy from "
                    "processed_snapshot_only rather than leaving a stale warning"
                )

        elif mode == "retained_raw":
            paths = source.get("retained_paths")
            if not isinstance(paths, list) or not paths:
                fail(f"{source_id}: retained_raw requires retained_paths")
            for relative in paths:
                require_file(str(relative), f"{source_id} retained raw")

        elif mode in {"pinned_remote", "verified_transport"}:
            remote_id = source.get("remote_source_id")
            if not remote_id or remote_id not in remote_sources:
                fail(f"{source_id}: remote_source_id is missing from diagnostic manifest")
            entry = remote_sources[remote_id]
            if not str(entry.get("url", "")).startswith("https://"):
                fail(f"{source_id}: remote URL must use HTTPS")
            if entry.get("hash_algorithm") not in {"sha256", "md5"}:
                fail(f"{source_id}: unsupported remote hash algorithm")
            if not entry.get("hash") or not entry.get("destination"):
                fail(f"{source_id}: remote entry needs hash and destination")
            if not source.get("verification_command") and mode != "pinned_remote":
                fail(f"{source_id}: verified_transport requires verification_command")

            # Cross-check hash/size declarations when the audit repeats them.
            if source.get("sha256") and entry["hash_algorithm"] == "sha256":
                if source["sha256"] != entry["hash"]:
                    fail(f"{source_id}: audit SHA-256 disagrees with remote manifest")
            if source.get("transport_sha256") and entry["hash_algorithm"] == "sha256":
                if source["transport_sha256"] != entry["hash"]:
                    fail(f"{source_id}: transport SHA-256 disagrees with remote manifest")
            if source.get("md5") and entry["hash_algorithm"] == "md5":
                if source["md5"] != entry["hash"]:
                    fail(f"{source_id}: audit MD5 disagrees with remote manifest")
            if source.get("size_bytes") is not None and entry.get("size_bytes") is not None:
                if int(source["size_bytes"]) != int(entry["size_bytes"]):
                    fail(f"{source_id}: audit size disagrees with remote manifest")
            if source.get("transport_size_bytes") is not None and entry.get("size_bytes") is not None:
                if int(source["transport_size_bytes"]) != int(entry["size_bytes"]):
                    fail(f"{source_id}: transport size disagrees with remote manifest")

            if mode == "verified_transport":
                record = source.get("primary_equivalence_record")
                if not record:
                    fail(f"{source_id}: verified_transport requires primary_equivalence_record")
                require_file(str(record), f"{source_id} primary equivalence record")
                if not source.get("equivalence_scope"):
                    fail(f"{source_id}: verified_transport requires equivalence_scope")

    claims = audit.get("claims", {})
    if processed_only:
        if claims.get("source_to_processed_reconstruction") != "PARTIAL":
            fail("processed_snapshot_only sources require source_to_processed_reconstruction=PARTIAL")
        rule = str(claims.get("rule", ""))
        if "processed_snapshot_only" not in rule:
            fail("claims.rule must explicitly constrain processed_snapshot_only wording")

    cache_root = str(remote.get("cache_root", ""))
    if cache_root != ".diagnostic_sources":
        fail("diagnostic cache_root must remain .diagnostic_sources")
    if ".diagnostic_sources/" not in GITIGNORE.read_text(encoding="utf-8"):
        fail(".diagnostic_sources/ must be ignored by Git")

    print(
        "DIAGNOSTIC_POLICY_PASS: "
        f"{len(sources)} sources checked; "
        f"{processed_only} processed-snapshot-only limitation(s); "
        f"{len(remote_sources)} pinned remote materialization(s)"
    )


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as error:
        fail(str(error))
