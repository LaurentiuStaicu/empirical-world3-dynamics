#!/usr/bin/env python3
"""Validate the machine-readable R-FDC-6 primary-source provenance audit."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "science/data/provenance/primary_source_audit_2026-09-22.json"

ALLOWED_STATUS = {"PASS", "WARNING", "BLOCKER"}
ALLOWED_LEVELS = {"L1", "L2", "L3", "L4"}
REQUIRED_IDS = {
    "faostat_food_production_indices",
    "undp_hdi_adapter",
    "un_wpp2024_population_adapter",
    "energy_institute_2026",
    "global_carbon_project_2025v15",
}


def fail(message: str) -> None:
    print(f"PRIMARY_SOURCE_AUDIT_FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    payload = json.loads(AUDIT.read_text(encoding="utf-8"))
    sources = payload.get("sources")
    if not isinstance(sources, list) or not sources:
        fail("sources must be a non-empty list")

    ids = [source.get("id") for source in sources]
    if len(ids) != len(set(ids)):
        fail("source IDs must be unique")

    missing = REQUIRED_IDS.difference(ids)
    if missing:
        fail(f"missing required source entries: {sorted(missing)}")

    open_count = 0
    for source in sources:
        source_id = source.get("id", "<missing-id>")
        status = source.get("overall_status")
        level = source.get("evidence_level")

        if status not in ALLOWED_STATUS:
            fail(f"{source_id}: invalid overall_status {status!r}")
        if level not in ALLOWED_LEVELS:
            fail(f"{source_id}: invalid evidence_level {level!r}")

        if status == "PASS" and level != "L4":
            fail(f"{source_id}: PASS requires complete L4 lineage")

        if status != "PASS":
            open_count += 1
            if not source.get("unresolved"):
                fail(f"{source_id}: non-PASS source must state unresolved evidence")
            if not source.get("required_action"):
                fail(f"{source_id}: non-PASS source must state required_action")

    gate_status = payload.get("gate_status")
    expected_gate = "CLOSED" if open_count == 0 else "OPEN"
    if gate_status != expected_gate:
        fail(
            f"gate_status is {gate_status!r}; expected {expected_gate!r} "
            f"for {open_count} non-PASS source(s)"
        )

    resolved = payload.get("resolved_documentation_issue", {})
    if resolved.get("id") != "world3_03_line_endings" or resolved.get("status") != "PASS":
        fail("World3-03 line-ending provenance resolution is missing or not PASS")

    print(
        "PRIMARY_SOURCE_AUDIT_PASS: "
        f"{len(sources)} sources checked; {open_count} remain non-PASS; "
        f"gate={gate_status}"
    )


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as error:
        fail(str(error))
