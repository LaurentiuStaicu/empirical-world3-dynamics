#!/usr/bin/env python3
"""Static System Dynamics conformity checks for the retained EWD core."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "science" / "configs" / "system_dynamics_conformity.json"
STRUCTURE = ROOT / "science" / "configs" / "real_model_structure.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"BLOCKER: {message}")


def extract_control(text: str, name: str) -> float:
    match = re.search(rf"(?mi)^\s*{re.escape(name)}\s*=\s*([0-9.]+)", text)
    if not match:
        raise SystemExit(f"BLOCKER: missing Vensim control parameter {name}")
    return float(match.group(1))


def main() -> None:
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    structure = json.loads(STRUCTURE.read_text(encoding="utf-8"))
    core = config["structural_core"]

    model_path = ROOT / core["authoritative_model_path"]
    require(model_path.is_file(), "authoritative World3-03 model file is missing")
    require(
        sha256(model_path) == core["authoritative_model_sha256"],
        "authoritative World3-03 bytes differ from the screened structural baseline",
    )

    architecture = structure["architecture"]
    require(
        architecture["reference_core_mutable"] is False,
        "reference_core_mutable must remain false",
    )
    require(
        architecture["reference_model"]["equation_policy"]
        == core["equation_policy"],
        "reference equation policy changed",
    )

    model = model_path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    require(
        extract_control(model, "INITIAL TIME") == core["expected_initial_time"],
        "INITIAL TIME changed",
    )
    require(
        extract_control(model, "FINAL TIME") == core["expected_final_time"],
        "FINAL TIME changed",
    )
    require(
        extract_control(model, "TIME STEP") == core["expected_time_step"],
        "TIME STEP changed",
    )

    integ_count = len(re.findall(r"\bINTEG\s*\(", model, flags=re.IGNORECASE))
    require(
        integ_count >= core["minimum_integ_stock_count"],
        f"expected at least {core['minimum_integ_stock_count']} INTEG stocks; found {integ_count}",
    )

    required_stocks = (
        "Arable Land",
        "Potentially Arable Land",
        "Land Fertility",
        "Industrial Capital",
        "Service Capital",
        "Persistent Pollution",
        "Population 0 To 14",
        "Population 15 To 44",
        "Population 45 To 64",
        "Population 65 Plus",
        "Nonrenewable Resources",
    )
    for stock in required_stocks:
        require(
            re.search(rf"(?mi)^\s*{re.escape(stock)}\s*=\s*INTEG\s*\(", model)
            is not None,
            f"required stock equation missing: {stock}",
        )

    structural_tokens = {
        "delay": ("SMOOTH", "DELAY3"),
        "lookup": ("LOOKUP",),
        "population_flow": ("births", "deaths 0 to 14", "maturation 14 to 15"),
        "capital_flow": ("industrial capital investment", "industrial capital depreciation"),
        "land_flow": ("land development rate", "land erosion rate"),
        "pollution_flow": (
            "persistent pollution appearance rate",
            "persistent pollution assimilation rate",
        ),
        "resource_flow": ("resource usage rate",),
    }
    lowered = model.lower()
    for group, tokens in structural_tokens.items():
        for token in tokens:
            require(token.lower() in lowered, f"missing {group} structural token: {token}")

    promotion = {row["id"] for row in structure["promotion_gates"]}
    require(
        promotion == {f"S{i}" for i in range(1, 11)},
        "existing S1-S10 promotion gate set changed",
    )

    extension_contract = config["future_extension_activation_contract"]
    extension_ids = {
        row["id"]
        for row in extension_contract["required_before_activation"]
    }
    evidence_registry = extension_contract.get("extension_activation_evidence", {})

    for candidate in structure["candidate_interfaces"]:
        if candidate["active_by_default"] or candidate["central"]:
            evidence = evidence_registry.get(candidate["id"])
            require(
                isinstance(evidence, dict),
                f"candidate {candidate['id']} is active/central without SD activation evidence",
            )
            require(
                evidence.get("s1_s10_pass") is True,
                f"candidate {candidate['id']} lacks PASS evidence for S1-S10",
            )
            for gate_id in extension_ids:
                require(
                    evidence.get(gate_id) == "PASS",
                    f"candidate {candidate['id']} lacks PASS evidence for {gate_id}",
                )

        row["id"]
        for row in config["future_extension_activation_contract"]["required_before_activation"]
    }
    require(
        extension_ids == {f"E{i}" for i in range(1, 11)},
        "future extension activation contract must contain E1-E10",
    )

    print(
        "System Dynamics static conformity gate PASS: "
        f"authoritative World3-03 hash preserved; {integ_count} INTEG stocks detected; "
        "delays/lookups/stock-flow tokens present; candidate extensions remain inactive."
    )


if __name__ == "__main__":
    main()
