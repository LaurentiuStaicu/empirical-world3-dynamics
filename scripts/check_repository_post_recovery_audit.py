#!/usr/bin/env python3
"""Validate the R-FDC-9 repository-wide post-recovery audit."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
HISTORICAL = ROOT / "science/data/audits/repository_file_data_content_inventory_2026-09-21.json"
AUDIT = ROOT / "science/data/audits/repository_post_recovery_audit_2026-09-22.json"
SCIENCE_WORKFLOW = ROOT / ".github/workflows/science-reproducibility.yml"
DIAGNOSTIC_WORKFLOW = ROOT / ".github/workflows/diagnostic-execution.yml"

BLOCKER_PATHS = {
    "science/scripts/evaluate_unido_industry_proxy.py",
    "science/scripts/evaluate_unido_iip_volume.py",
    "science/scripts/evaluate_climate_food_link.py",
    "science/scripts/evaluate_regional_agricultural_stress.py",
    "science/scripts/evaluate_technology_minerals.py",
}

ALLOWED_DISPOSITIONS = {
    "RESOLVED_PASS",
    "GOVERNED_LIMITATION",
    "REMAINING_WARNING",
}


def fail(message: str) -> None:
    print(f"POST_RECOVERY_AUDIT_FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def tracked_files() -> set[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return {line for line in result.stdout.splitlines() if line}


def require_text(path: Path, needles: tuple[str, ...], label: str) -> None:
    text = path.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            fail(f"{label} missing required text: {needle!r}")


def forbid_text(path: Path, needles: tuple[str, ...], label: str) -> None:
    text = path.read_text(encoding="utf-8")
    for needle in needles:
        if needle in text:
            fail(f"{label} still contains forbidden/stale text: {needle!r}")


def compile_python_sources(paths: set[str]) -> None:
    failures: list[str] = []
    for relative in sorted(path for path in paths if path.endswith(".py")):
        source = (ROOT / relative).read_text(encoding="utf-8")
        try:
            compile(source, relative, "exec")
        except SyntaxError as error:
            failures.append(f"{relative}: {error}")
    if failures:
        fail("Python syntax failures: " + "; ".join(failures))


def main() -> None:
    historical = json.loads(HISTORICAL.read_text(encoding="utf-8"))
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))

    if audit.get("gate") != "R-FDC-9":
        fail("audit gate must be R-FDC-9")
    if audit.get("gate_status") != "CLOSED_AUDIT":
        fail("R-FDC-9 may close only as CLOSED_AUDIT")

    historical_entries = historical.get("entries", [])
    historical_paths = {entry["path"] for entry in historical_entries}
    historical_nonpass = {
        entry["path"]
        for entry in historical_entries
        if entry.get("audit_status") in {"WARNING", "BLOCKER"}
    }
    historical_blockers = {
        entry["path"]
        for entry in historical_entries
        if entry.get("audit_status") == "BLOCKER"
    }

    if historical_blockers != BLOCKER_PATHS:
        fail(
            "historical BLOCKER register differs from the five declared recovery targets"
        )

    resolutions = audit.get("historical_nonpass_resolution", [])
    resolution_paths = [entry.get("path") for entry in resolutions]
    if len(resolution_paths) != len(set(resolution_paths)):
        fail("historical non-PASS resolution paths must be unique")
    if set(resolution_paths) != historical_nonpass:
        missing = sorted(historical_nonpass - set(resolution_paths))
        extra = sorted(set(resolution_paths) - historical_nonpass)
        fail(f"historical non-PASS coverage mismatch; missing={missing}; extra={extra}")

    dispositions = {entry.get("current_disposition") for entry in resolutions}
    if not dispositions.issubset(ALLOWED_DISPOSITIONS):
        fail(f"unsupported post-recovery dispositions: {sorted(dispositions - ALLOWED_DISPOSITIONS)}")

    for entry in resolutions:
        if entry["path"] in historical_blockers and entry["current_disposition"] != "RESOLVED_PASS":
            fail(f"historical blocker not resolved: {entry['path']}")

    remaining_warning_paths = {
        entry["path"] for entry in audit.get("remaining_warnings", [])
    }
    expected_remaining = {
        entry["path"]
        for entry in resolutions
        if entry["current_disposition"] == "REMAINING_WARNING"
    }
    if remaining_warning_paths != expected_remaining:
        fail("remaining_warnings does not match REMAINING_WARNING dispositions")

    governed_paths = {
        entry["path"] for entry in audit.get("governed_limitations", [])
    }
    expected_governed = {
        entry["path"]
        for entry in resolutions
        if entry["current_disposition"] == "GOVERNED_LIMITATION"
    }
    if governed_paths != expected_governed:
        fail("governed_limitations does not match GOVERNED_LIMITATION dispositions")

    for entry in audit.get("remaining_warnings", []):
        if entry.get("status") != "WARNING":
            fail(f"remaining warning has non-WARNING status: {entry.get('path')}")
        if entry.get("central_model_impact") is not False:
            fail(f"remaining warning is not explicitly non-central: {entry.get('path')}")
        if not entry.get("rationale"):
            fail(f"remaining warning lacks rationale: {entry.get('path')}")

    blocker_summary = audit.get("blocker_summary", {})
    if blocker_summary.get("historical_blockers") != 5:
        fail("historical blocker count must remain 5")
    if blocker_summary.get("unresolved_blockers") != 0:
        fail("R-FDC-9 cannot close with unresolved blockers")
    if blocker_summary.get("unexplained_blockers") != []:
        fail("R-FDC-9 cannot close with unexplained blockers")

    new_entries = audit.get("new_files_since_historical_baseline", [])
    new_paths = [entry.get("path") for entry in new_entries]
    if len(new_paths) != len(set(new_paths)):
        fail("new-file coverage paths must be unique")
    if any(entry.get("status") != "PASS" for entry in new_entries):
        fail("every new file must have an explicit PASS classification for its declared role")

    current = tracked_files()
    expected = historical_paths | set(new_paths)
    if current != expected:
        missing = sorted(current - expected)
        stale = sorted(expected - current)
        fail(f"tracked-file coverage mismatch; unclassified={missing}; missing={stale}")

    expected_count = int(
        audit["post_recovery_scope"]["expected_tracked_files_after_this_gate"]
    )
    if len(current) != expected_count:
        fail(f"tracked file count is {len(current)}, expected {expected_count}")

    compile_python_sources(current)

    for relative in (
        "science/scripts/evaluate_unido_industry_proxy.py",
        "science/scripts/evaluate_unido_iip_volume.py",
        "science/scripts/evaluate_climate_food_link.py",
        "science/scripts/evaluate_regional_agricultural_stress.py",
    ):
        forbid_text(
            ROOT / relative,
            ("build_bau2_e2026",),
            relative,
        )

    forbid_text(
        ROOT / "science/scripts/evaluate_technology_minerals.py",
        (
            'data/scenarios/industry_total.csv',
            'data/scenarios/resources_remaining_pct.csv',
        ),
        "technology-minerals diagnostic",
    )

    diagnostic_workflow_text = DIAGNOSTIC_WORKFLOW.read_text(encoding="utf-8")
    for relative in sorted(BLOCKER_PATHS):
        if relative not in diagnostic_workflow_text:
            fail(f"diagnostic execution workflow no longer covers {relative}")
    if "git diff --exit-code -- data/scenarios" not in diagnostic_workflow_text:
        fail("diagnostic execution workflow no longer protects retained central references")

    science_workflow_text = SCIENCE_WORKFLOW.read_text(encoding="utf-8")
    for guard in (
        "check_registry_contract.py",
        "check_execution_routing.py",
        "check_version_identity.py",
        "check_primary_source_audit.py",
        "check_diagnostic_reproducibility_policy.py",
        "check_rejected_mechanism_governance.py",
        "check_repository_post_recovery_audit.py",
    ):
        if guard not in science_workflow_text:
            fail(f"scientific reproducibility workflow is missing guard {guard}")

    require_text(
        ROOT / "science/scripts/evaluate_eroi_resource_link.py",
        (
            'manifest["central_candidate_id"]',
            '"backtest_is_sufficient_for_promotion": False',
            '"governance_disposition": "rejected_for_central_promotion"',
        ),
        "EROI resource-link evaluator",
    )
    forbid_text(
        ROOT / "science/scripts/evaluate_eroi_resource_link.py",
        ('["series_resources_remaining_pct"][114]',),
        "EROI resource-link evaluator",
    )

    require_text(
        ROOT / "scripts/promotion_gate.py",
        (
            "narrow retained error-comparison gate",
            "not the Real Model S1-S10 promotion contract",
            "nu autorizează singur promovarea unui mecanism",
        ),
        "historical comparison gate",
    )

    gates = audit.get("recovery_gates", [])
    if [item.get("gate") for item in gates] != [f"R-FDC-{i}" for i in range(1, 10)]:
        fail("recovery gate sequence must be exactly R-FDC-1 through R-FDC-9")

    print(
        "POST_RECOVERY_AUDIT_PASS: "
        f"{len(current)} tracked files covered; "
        f"{len(historical_nonpass)} historical non-PASS entries classified; "
        f"{len(remaining_warning_paths)} explicit warnings remain; "
        "0 unresolved/unexplained blockers"
    )


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError, subprocess.SubprocessError) as error:
        fail(str(error))
