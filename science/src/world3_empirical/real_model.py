"""R2 Real Model scaffold.

The scaffold deliberately does not reimplement World3.  The verified World3-03
Vensim model remains the executable reference core; this module adds typed,
machine-readable structural contracts and hard guardrails around dormant
candidate interfaces.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from .scenarios import project_root
from .world3_03 import World303Result, run_world3_03


EVIDENCE_ROLES = {
    "observed",
    "diagnostic",
    "stress",
    "candidate_feedback",
    "central_feedback",
    "reference",
}
STRUCTURAL_ROLES = {
    "stock",
    "flow",
    "auxiliary",
    "exogenous_driver",
    "observation_bridge",
    "diagnostic",
}
REQUIRED_GATES = tuple(f"S{i}" for i in range(1, 11))
REQUIRED_BASELINES = ("BAU", "BAU2", "BAU Hybrid 2026")
SELECTED_R2_CANDIDATE = "energy_reinvestment_to_industrial_investment_burden"
REJECTED_R1_ENERGY_LINK = "World3 fraction of resources remaining -> fossil EROI"


class R2StructuralError(ValueError):
    """Raised when the machine-readable R2 contract violates a structural gate."""


@dataclass(frozen=True)
class CandidateInterface:
    id: str
    evidence_role: str
    active: bool
    central: bool
    status: str
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    forbidden_links: tuple[str, ...] = ()
    double_counting_risks: tuple[str, ...] = ()

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "CandidateInterface":
        return cls(
            id=str(value["id"]),
            evidence_role=str(value["evidence_role"]),
            active=bool(value["active"]),
            central=bool(value["central"]),
            status=str(value["status"]),
            inputs=tuple(map(str, value.get("inputs", ()))),
            outputs=tuple(map(str, value.get("outputs", ()))),
            forbidden_links=tuple(map(str, value.get("forbidden_links", ()))),
            double_counting_risks=tuple(map(str, value.get("double_counting_risks", ()))),
        )

    def apply(self, value: Any) -> Any:
        """Return the reference value while the interface is dormant.

        R2 explicitly prohibits silently activating candidate feedbacks.  An
        activated interface therefore fails closed until a later stage supplies
        an implementation that has passed the required gates.
        """
        if self.active or self.central:
            raise R2StructuralError(
                f"R2 candidate {self.id!r} cannot alter the reference core"
            )
        return value


def structure_path() -> Path:
    return project_root() / "configs" / "world3_reference_core.r2.json"


def schema_path() -> Path:
    return project_root() / "configs" / "real_model_structure.schema.json"


def load_structure(path: str | Path | None = None) -> dict[str, Any]:
    source = Path(path) if path else structure_path()
    with source.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    validate_structure(payload)
    return payload


def load_candidate_interfaces(
    payload: Mapping[str, Any] | None = None,
) -> tuple[CandidateInterface, ...]:
    source = payload if payload is not None else load_structure()
    return tuple(
        CandidateInterface.from_mapping(item)
        for item in source["candidate_interfaces"]
    )


def _normalized_dimension(value: Mapping[str, int]) -> dict[str, int]:
    return {str(key): int(power) for key, power in value.items() if int(power) != 0}


def _flow_dimension_for_stock(stock_dimension: Mapping[str, int]) -> dict[str, int]:
    expected = _normalized_dimension(stock_dimension)
    expected["year"] = expected.get("year", 0) - 1
    return _normalized_dimension(expected)


def validate_structure(payload: Mapping[str, Any]) -> None:
    """Validate the R2 pre-simulation structural invariants.

    These checks implement machine-enforceable parts of S1-S3 plus the R2
    non-promotion boundary.  They do not claim that a candidate has passed
    behavioral/predictive gates S7-S10.
    """
    if payload.get("schema_version") != "r2.1":
        raise R2StructuralError("Unsupported R2 structural schema version")

    core = payload.get("reference_core", {})
    if core.get("equation_policy") != "preserve_authoritative_equations":
        raise R2StructuralError("Reference equations must remain authoritative")
    baselines = tuple(core.get("baseline_scenarios", ()))
    if baselines != REQUIRED_BASELINES:
        raise R2StructuralError(
            f"Baseline comparison set changed: expected {REQUIRED_BASELINES!r}"
        )

    modules = payload.get("modules", ())
    if len(modules) < 5:
        raise R2StructuralError("R2 requires the five inherited reference sectors")

    quantity_ids: set[str] = set()
    for module in modules:
        if module.get("evidence_role") != "reference":
            raise R2StructuralError(
                f"Reference module {module.get('id')!r} lost reference evidence role"
            )
        boundary = module.get("boundary", {})
        if set(boundary) != {"endogenous", "exogenous", "excluded"}:
            raise R2StructuralError(
                f"Module {module.get('id')!r} has incomplete system boundary"
            )
        quantities = module.get("quantities", ())
        local = {str(item.get("id")): item for item in quantities}
        for qid, quantity in local.items():
            if not qid or qid in quantity_ids:
                raise R2StructuralError(f"Duplicate or empty quantity id: {qid!r}")
            quantity_ids.add(qid)
            role = quantity.get("role")
            if role not in STRUCTURAL_ROLES:
                raise R2StructuralError(f"Unknown structural role {role!r} for {qid}")
            evidence_role = quantity.get("evidence_role")
            if evidence_role not in EVIDENCE_ROLES:
                raise R2StructuralError(f"Unknown evidence role {evidence_role!r} for {qid}")
            if not quantity.get("unit"):
                raise R2StructuralError(f"Quantity {qid} has no unit")
            if not isinstance(quantity.get("dimension"), dict):
                raise R2StructuralError(f"Quantity {qid} has no machine-readable dimension")

        for qid, quantity in local.items():
            if quantity.get("role") != "flow":
                continue
            stock_id = quantity.get("changes_stock")
            stock = local.get(str(stock_id))
            if stock is None or stock.get("role") != "stock":
                raise R2StructuralError(
                    f"Flow {qid} does not point to a stock in the same module"
                )
            if quantity.get("direction") not in {"in", "out"}:
                raise R2StructuralError(f"Flow {qid} has no accounting direction")
            expected = _flow_dimension_for_stock(stock["dimension"])
            actual = _normalized_dimension(quantity["dimension"])
            if actual != expected:
                raise R2StructuralError(
                    f"Dimensional mismatch for {qid}: {actual!r} != {expected!r}"
                )

    gates = tuple(item.get("id") for item in payload.get("validation_gates", ()))
    if gates != REQUIRED_GATES:
        raise R2StructuralError(f"Validation ladder changed: {gates!r}")

    candidates = load_candidate_interfaces_unvalidated(payload)
    selected = [item for item in candidates if item.status == "selected_for_prospective_experiment"]
    if len(selected) != 1 or selected[0].id != SELECTED_R2_CANDIDATE:
        raise R2StructuralError("R2 must select exactly one prospective candidate")
    for candidate in candidates:
        if candidate.evidence_role not in {"candidate_feedback", "diagnostic", "stress"}:
            raise R2StructuralError(
                f"Candidate {candidate.id} has invalid evidence role {candidate.evidence_role}"
            )
        if candidate.active or candidate.central:
            raise R2StructuralError(
                f"Candidate {candidate.id} was silently promoted or activated"
            )
    if REJECTED_R1_ENERGY_LINK not in selected[0].forbidden_links:
        raise R2StructuralError("Rejected R1 resource-to-EROI link is not guarded")


def load_candidate_interfaces_unvalidated(
    payload: Mapping[str, Any],
) -> tuple[CandidateInterface, ...]:
    return tuple(
        CandidateInterface.from_mapping(item)
        for item in payload.get("candidate_interfaces", ())
    )


def advance_stock(
    stock: float,
    *,
    inflow: float,
    outflow: float,
    dt: float,
) -> float:
    """One accounting-conserving stock step used by R2 structural tests.

    The helper is intentionally generic and is not a replacement for any
    World3 equation.  It exists to test boundary, accounting, extreme-condition
    and timestep invariants before a candidate simulation is allowed.
    """
    values = (stock, inflow, outflow, dt)
    if any(not isinstance(value, (int, float)) for value in values):
        raise TypeError("Stock integration inputs must be numeric")
    if stock < 0 or inflow < 0 or outflow < 0 or dt <= 0:
        raise R2StructuralError("Stocks/flows must be non-negative and dt positive")
    result = stock + (inflow - outflow) * dt
    if result < -1e-12:
        raise R2StructuralError("Outflow would drive stock negative")
    return max(0.0, float(result))


def run_reference_core(
    scenario: int = 2,
    *,
    years: Sequence[int] = tuple(range(1900, 2101)),
    payload: Mapping[str, Any] | None = None,
) -> World303Result:
    """Run the unchanged World3 reference core through the R2 scaffold."""
    structure = dict(payload) if payload is not None else load_structure()
    validate_structure(structure)
    for interface in load_candidate_interfaces_unvalidated(structure):
        if interface.active or interface.central:
            raise R2StructuralError("R2 cannot execute active candidate feedbacks")
    return run_world3_03(scenario=scenario, years=years)
