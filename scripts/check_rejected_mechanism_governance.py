#!/usr/bin/env python3
"""Validate governance of rejected experimental mechanisms.

The check is intentionally offline and does not execute the rejected coupling.
It verifies that the resource-fraction -> fossil-EROI experiment remains
explicitly rejected, forbidden by the Real Model contract, and absent from
central execution routes.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "science/data/audits/rejected_experimental_mechanisms_2026-09-22.json"
STRUCTURE = ROOT / "science/configs/real_model_structure.json"
CONTRACT = ROOT / "science/src/world3_empirical/real_model_contract.py"
ENERGY = ROOT / "science/src/world3_empirical/energy_coupling.py"
EVALUATOR = ROOT / "science/scripts/evaluate_eroi_resource_link.py"
SENSITIVITY = ROOT / "science/scripts/analyze_energy_coupling.py"

COUPLING_ID = "world3_resource_fraction_to_fossil_eroi"
FORBIDDEN_TOKENS = (
    "world3_empirical.energy_coupling",
    "from .energy_coupling",
    "import energy_coupling",
    "coupled_model_text",
    "EROI_SCENARIOS",
)
CENTRAL_EXECUTION_PATHS = (
    "science/src/world3_empirical/__init__.py",
    "science/src/world3_empirical/__main__.py",
    "science/src/world3_empirical/cli.py",
    "science/src/world3_empirical/model.py",
    "science/src/world3_empirical/calibration.py",
    "science/src/world3_empirical/scenarios.py",
    "science/src/world3_empirical/world3_03.py",
    "science/scripts/build_joint_hybrid_2026.py",
    "science/scripts/run_world3_03.py",
    "science/scripts/run_baselines.py",
    "science/scripts/compare_empirical.py",
    "scripts/reproduce_scientific_results.py",
    "scripts/validate_science.py",
    "scripts/promotion_gate.py",
)


def fail(message: str) -> None:
    print(f"REJECTED_MECHANISM_GOVERNANCE_FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_contract_module():
    spec = importlib.util.spec_from_file_location("ewd_real_model_contract", CONTRACT)
    if spec is None or spec.loader is None:
        fail("could not load Real Model contract module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    if audit.get("gate") != "R-FDC-8":
        fail("audit gate must be R-FDC-8")
    if audit.get("gate_status") != "CLOSED_GOVERNANCE":
        fail("R-FDC-8 may close only as CLOSED_GOVERNANCE")

    mechanisms = audit.get("mechanisms")
    if not isinstance(mechanisms, list) or len(mechanisms) != 1:
        fail("the current rejected-mechanism registry must contain exactly one mechanism")
    mechanism = mechanisms[0]
    if mechanism.get("id") != COUPLING_ID:
        fail("rejected coupling ID changed or is missing")
    if mechanism.get("disposition") != "REJECTED_FOR_CENTRAL_PROMOTION":
        fail("coupling is not explicitly rejected for central promotion")
    if mechanism.get("central_route_status") != "FORBIDDEN_AND_NOT_IMPORTED":
        fail("central-route status is not forbidden/not-imported")

    e1 = mechanism.get("reconsideration_requirements", {}).get("E1_E10", {})
    if e1.get("state") != "UNDEFINED_IN_CURRENT_REPOSITORY":
        fail("E1-E10 must remain explicitly undefined until a framework is committed")
    if "does not invent" not in str(e1.get("rule", "")).lower():
        fail("E1-E10 rule must forbid inventing/assuming an undefined framework")

    s1 = mechanism.get("reconsideration_requirements", {}).get("S1_S10", {})
    if s1.get("state") != "REQUIRED_ALL_PASS":
        fail("S1-S10 must be required for any reconsideration")

    structure = json.loads(STRUCTURE.read_text(encoding="utf-8"))
    top_forbidden = set(structure.get("forbidden_couplings", ()))
    if COUPLING_ID not in top_forbidden:
        fail("real_model_structure.json no longer forbids rejected coupling")
    gate_ids = [gate.get("id") for gate in structure.get("promotion_gates", ())]
    if gate_ids != [f"S{i}" for i in range(1, 11)]:
        fail("real_model_structure.json S1-S10 gate contract changed")

    for candidate in structure.get("candidate_interfaces", ()):
        if candidate.get("id") in {"energy_accounting_emissions", "net_energy"}:
            if COUPLING_ID not in set(candidate.get("forbidden_couplings", ())):
                fail(f"{candidate.get('id')}: rejected coupling is no longer forbidden")
            if candidate.get("active_by_default") is not False:
                fail(f"{candidate.get('id')}: candidate must remain inactive by default")
            if candidate.get("central") is not False:
                fail(f"{candidate.get('id')}: candidate cannot be central")

    module = load_contract_module()
    if COUPLING_ID not in set(module.FORBIDDEN_COUPLINGS):
        fail("runtime Real Model contract no longer forbids rejected coupling")
    module.RealModelContract.load(STRUCTURE)

    for relative in CENTRAL_EXECUTION_PATHS:
        path = ROOT / relative
        if not path.is_file():
            fail(f"central execution path missing: {relative}")
        text = path.read_text(encoding="utf-8")
        matches = [token for token in FORBIDDEN_TOKENS if token in text]
        if matches:
            fail(f"{relative}: central route references rejected coupling tokens {matches}")

    energy_text = ENERGY.read_text(encoding="utf-8")
    for phrase in (
        "Rejected EROI sensitivity experiment",
        "forbidden for central promotion",
        "Executability is not evidence",
    ):
        if phrase not in energy_text:
            fail(f"energy_coupling.py missing governance phrase: {phrase!r}")

    evaluator_text = EVALUATOR.read_text(encoding="utf-8")
    if '"governance_disposition": "rejected_for_central_promotion"' not in evaluator_text:
        fail("EROI evaluator does not emit rejected governance disposition")
    if '"backtest_is_sufficient_for_promotion": False' not in evaluator_text:
        fail("EROI evaluator does not state that backtest is insufficient for promotion")
    if "Eligible for the next joint calibration stage." in evaluator_text:
        fail("EROI evaluator still implies backtest-only promotion eligibility")

    sensitivity_text = SENSITIVITY.read_text(encoding="utf-8")
    for phrase in (
        '"production_decision": "not_accepted_into_central_projection"',
        '"governance_disposition": "rejected_for_central_promotion"',
        '"executability_is_not_promotion_evidence": True',
    ):
        if phrase not in sensitivity_text:
            fail(f"energy sensitivity audit missing governance marker: {phrase}")

    if "data/scenarios" in energy_text or "data/scenarios" in evaluator_text or "data/scenarios" in sensitivity_text:
        fail("rejected experiment must not write or route through retained data/scenarios")

    print(
        "REJECTED_MECHANISM_GOVERNANCE_PASS: "
        "resource-fraction -> fossil-EROI remains rejected, forbidden, "
        "and absent from central execution routes"
    )


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as error:
        fail(str(error))
