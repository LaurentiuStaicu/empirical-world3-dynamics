"""Validation for the empirical-series registry."""

from __future__ import annotations

from pathlib import Path
import json

import pandas as pd

from .scenarios import project_root


REQUIRED_COLUMNS = {
    "series_id",
    "model_variable",
    "concept",
    "source_institution",
    "dataset",
    "source_url",
    "unit",
    "start_year",
    "end_year",
    "frequency",
    "observation_type",
    "status",
    "notes",
}
OBSERVATION_TYPES = {"empirical", "latent", "scenario_only"}


def load_registry(path: str | Path | None = None) -> pd.DataFrame:
    source = Path(path) if path else project_root() / "data" / "registry.csv"
    registry = pd.read_csv(source)
    missing = REQUIRED_COLUMNS - set(registry.columns)
    if missing:
        raise ValueError(f"Registry is missing required columns: {sorted(missing)}")
    if registry["series_id"].duplicated().any():
        duplicates = registry.loc[registry["series_id"].duplicated(), "series_id"].tolist()
        raise ValueError(f"Duplicate series_id values: {duplicates}")
    invalid_types = set(registry["observation_type"]) - OBSERVATION_TYPES
    if invalid_types:
        raise ValueError(f"Invalid observation_type values: {sorted(invalid_types)}")
    invalid_years = registry["end_year"] < registry["start_year"]
    if invalid_years.any():
        ids = registry.loc[invalid_years, "series_id"].tolist()
        raise ValueError(f"end_year precedes start_year for: {ids}")
    return registry



def load_active_observation_contract(path: str | Path | None = None) -> dict:
    source = (
        Path(path)
        if path
        else project_root() / "configs" / "active_observation_contract.json"
    )
    payload = json.loads(source.read_text(encoding="utf-8"))
    if payload.get("schema_version") != "1.0":
        raise ValueError("Unsupported active observation contract schema_version")
    for section in ("central_observation_series", "benchmark_series"):
        if section not in payload or not isinstance(payload[section], list):
            raise ValueError(f"Active observation contract is missing list: {section}")
    return payload


def validate_active_observation_contract(
    registry: pd.DataFrame | None = None,
    contract: dict | None = None,
) -> dict[str, int]:
    registry = load_registry() if registry is None else registry
    contract = load_active_observation_contract() if contract is None else contract

    indexed = registry.set_index("series_id", drop=False)
    required = (
        list(contract["central_observation_series"])
        + list(contract["benchmark_series"])
    )

    missing: list[str] = []
    mismatched_types: list[str] = []
    duplicate_contract_ids: list[str] = []
    seen: set[str] = set()

    for entry in required:
        series_id = entry["series_id"]
        if series_id in seen:
            duplicate_contract_ids.append(series_id)
        seen.add(series_id)

        if series_id not in indexed.index:
            missing.append(series_id)
            continue

        actual_type = str(indexed.loc[series_id, "observation_type"])
        expected_type = str(entry["expected_observation_type"])
        if actual_type != expected_type:
            mismatched_types.append(
                f"{series_id}: expected {expected_type}, found {actual_type}"
            )

    if duplicate_contract_ids:
        raise ValueError(
            "Duplicate series_id values in active observation contract: "
            f"{sorted(set(duplicate_contract_ids))}"
        )
    if missing:
        raise ValueError(
            "Registry is missing active observation/benchmark series: "
            f"{sorted(missing)}"
        )
    if mismatched_types:
        raise ValueError(
            "Registry observation_type mismatches active contract: "
            + "; ".join(mismatched_types)
        )

    exclusions = {
        entry["series_id"] for entry in contract.get("exclusions", [])
    }
    active_ids = {entry["series_id"] for entry in required}
    overlap = active_ids & exclusions
    if overlap:
        raise ValueError(
            "Series cannot be both active and explicitly excluded: "
            f"{sorted(overlap)}"
        )

    return {
        "central_observation_series": len(contract["central_observation_series"]),
        "benchmark_series": len(contract["benchmark_series"]),
        "active_series_total": len(required),
    }
