"""R2 structural contract for conservative Real Model extensions.

This module deliberately does not import or mutate the central World3 runtime.
Candidate mechanisms are typed, inactive by default, and cannot be promoted to
the central model unless all S1-S10 gates have explicitly passed.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum
import json
import math
from pathlib import Path
from typing import Any, Mapping


GATE_IDS = tuple(f"S{i}" for i in range(1, 11))
FORBIDDEN_COUPLINGS = frozenset({"world3_resource_fraction_to_fossil_eroi"})


class EvidenceRole(str, Enum):
    REFERENCE_EQUATION = "reference_equation"
    OBSERVED_INPUT = "observed_input"
    CALIBRATION_CANDIDATE = "calibration_candidate"
    DIAGNOSTIC = "diagnostic"
    BENCHMARK = "benchmark"
    SENSITIVITY_ONLY = "sensitivity_only"
    PROSPECTIVE_VALIDATION = "prospective_validation"
    EXCLUDED_FROM_COUPLING = "excluded_from_coupling"


class GateStatus(str, Enum):
    NOT_TESTED = "not_tested"
    PASS = "pass"
    FAIL = "fail"


@dataclass(frozen=True)
class Signal:
    name: str
    value: float
    unit: str
    evidence_role: EvidenceRole

    def __post_init__(self) -> None:
        if not self.name or not self.unit:
            raise ValueError("Signal name and unit must be non-empty")
        if not math.isfinite(float(self.value)):
            raise ValueError(f"Signal {self.name!r} must be finite")


@dataclass
class CandidateInterface:
    candidate_id: str
    active: bool = False
    central: bool = False
    gate_status: dict[str, GateStatus] = field(
        default_factory=lambda: {gate: GateStatus.NOT_TESTED for gate in GATE_IDS}
    )

    def __post_init__(self) -> None:
        if not self.candidate_id:
            raise ValueError("candidate_id must be non-empty")
        if self.central:
            raise ValueError("R2 candidate interfaces cannot start as central")
        if set(self.gate_status) != set(GATE_IDS):
            raise ValueError("gate_status must contain exactly S1-S10")

    def apply(
        self,
        reference_outputs: Mapping[str, Any],
        *,
        signals: tuple[Signal, ...] = (),
        coupling_id: str | None = None,
    ) -> dict[str, Any]:
        """Return unchanged reference outputs while the extension is inactive.

        R2 only establishes the interface and guardrails. Even for an activated
        experiment, coupling logic belongs to a separately reviewed prospective
        experiment and is not implemented here.
        """
        if coupling_id in FORBIDDEN_COUPLINGS:
            raise ValueError(f"Rejected coupling cannot be reintroduced: {coupling_id}")
        for signal in signals:
            if not isinstance(signal, Signal):
                raise TypeError("signals must contain Signal instances")
        if self.active:
            raise RuntimeError(
                "R2 defines interfaces only; activated candidate dynamics require "
                "a separately implemented prospective experiment"
            )
        return deepcopy(dict(reference_outputs))

    def set_gate(self, gate_id: str, status: GateStatus) -> None:
        if gate_id not in GATE_IDS:
            raise KeyError(f"Unknown promotion gate: {gate_id}")
        if not isinstance(status, GateStatus):
            raise TypeError("status must be a GateStatus")
        self.gate_status[gate_id] = status

    @property
    def promotion_allowed(self) -> bool:
        return all(self.gate_status[gate] is GateStatus.PASS for gate in GATE_IDS)


@dataclass(frozen=True)
class RealModelContract:
    payload: Mapping[str, Any]

    @classmethod
    def load(cls, path: str | Path) -> "RealModelContract":
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        contract = cls(payload)
        contract.validate()
        return contract

    def validate(self) -> None:
        architecture = self.payload.get("architecture", {})
        if architecture.get("clean_room_topology") is not False:
            raise ValueError("R2 must not use a clean-room topology")
        if architecture.get("reference_core_mutable") is not False:
            raise ValueError("World3 reference core must remain immutable")

        roles = set(self.payload.get("evidence_roles", ()))
        required_roles = {role.value for role in EvidenceRole}
        if roles != required_roles:
            raise ValueError("Evidence-role vocabulary does not match the R2 contract")

        gates = self.payload.get("promotion_gates", ())
        if [gate.get("id") for gate in gates] != list(GATE_IDS):
            raise ValueError("Promotion gates must be ordered S1-S10")

        modules = self.payload.get("modules", ())
        if not modules:
            raise ValueError("At least one reference module is required")
        declared_variables: set[str] = set()
        flows: dict[str, Mapping[str, Any]] = {}
        stocks: list[Mapping[str, Any]] = []
        for module in modules:
            if module.get("role") != "reference_core":
                raise ValueError("R2 reference modules must be marked reference_core")
            for variable in module.get("variables", ()):
                variable_id = variable.get("id")
                if not variable_id or variable_id in declared_variables:
                    raise ValueError(f"Duplicate or missing variable id: {variable_id!r}")
                declared_variables.add(variable_id)
                if variable.get("kind") not in {"stock", "flow", "auxiliary"}:
                    raise ValueError(f"Invalid variable kind for {variable_id}")
                if not variable.get("unit") or not variable.get("dimension"):
                    raise ValueError(f"Missing unit/dimension for {variable_id}")
                if variable.get("evidence_role") not in roles:
                    raise ValueError(f"Unknown evidence role for {variable_id}")
                if variable["kind"] == "flow":
                    flows[variable_id] = variable
                elif variable["kind"] == "stock":
                    stocks.append(variable)

        for stock in stocks:
            for flow_id in (*stock.get("inflows", ()), *stock.get("outflows", ())):
                if flow_id not in flows:
                    raise ValueError(
                        f"Stock {stock['id']} references undeclared flow {flow_id}"
                    )
            expected_rate_dimension = f"{stock['dimension']}_rate"
            for flow_id in (*stock.get("inflows", ()), *stock.get("outflows", ())):
                if flows[flow_id]["dimension"] != expected_rate_dimension:
                    raise ValueError(
                        f"Flow {flow_id} is dimensionally inconsistent with "
                        f"stock {stock['id']}"
                    )

        declared_forbidden = set(self.payload.get("forbidden_couplings", ()))
        if declared_forbidden != set(FORBIDDEN_COUPLINGS):
            raise ValueError(
                "Top-level forbidden coupling registry must exactly match the "
                "enforced Real Model contract"
            )

        for candidate in self.payload.get("candidate_interfaces", ()):
            if candidate.get("active_by_default") is not False:
                raise ValueError(f"Candidate {candidate.get('id')} must start inactive")
            if candidate.get("central") is not False:
                raise ValueError(f"Candidate {candidate.get('id')} cannot start central")
            forbidden = set(candidate.get("forbidden_couplings", ()))
            if not forbidden.issubset(FORBIDDEN_COUPLINGS):
                raise ValueError(f"Unknown forbidden coupling on {candidate.get('id')}")

        selected = self.payload.get("selected_prospective_candidate", {})
        if selected.get("central_promotion") is not False:
            raise ValueError("R2 selection is experiment-only, never central promotion")
        candidate_ids = {
            candidate["id"] for candidate in self.payload.get("candidate_interfaces", ())
        }
        if selected.get("id") not in candidate_ids:
            raise ValueError("Selected prospective candidate must be declared")

    def candidate(self, candidate_id: str) -> CandidateInterface:
        for candidate in self.payload["candidate_interfaces"]:
            if candidate["id"] == candidate_id:
                if candidate["active_by_default"] is not False:
                    raise ValueError("Candidate is not inactive by default")
                return CandidateInterface(candidate_id=candidate_id)
        raise KeyError(candidate_id)
