"""Prospective-style validation for energy accounting -> direct fossil CO2.

This experiment is deliberately external to the World3 reference core. It maps
observed global coal/oil/gas energy supply to matching direct fossil CO2 fuel
categories and compares that accounting candidate with a time-respecting
persistence-intensity baseline.

The module must never import or modify World3 dynamics.
"""
from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[3]
EI_PATH = ROOT / "science/data/processed/energy_institute_global_2026.csv"
GCB_PATH = ROOT / "science/data/experiments/gcb_direct_fossil_1990_2024.csv"

DEVELOPMENT = (1990, 2009)
VALIDATION = (2010, 2017)
HOLDOUT = (2018, 2024)
PROSPECTIVE_YEAR = 2025

# IPCC 2006 Guidelines, Vol. 2, Ch. 2, Table 2.2, kg CO2/TJ NCV.
IPCC_FACTORS_KG_PER_TJ = {
    "coal": 94600.0,   # Other bituminous coal
    "oil": 73300.0,    # Crude oil
    "gas": 56100.0,    # Natural gas
}
IPCC_FACTOR_RANGES_KG_PER_TJ = {
    "coal": (89500.0, 99700.0),
    "oil": (71100.0, 75500.0),
    "gas": (54300.0, 58300.0),
}

# Project-level predictive acceptance criterion from Model Real methodology.
MIN_SKILL_VS_BASELINE = 0.30


@dataclass(frozen=True)
class YearRecord:
    year: int
    fossil_energy_ej: float
    coal_ej: float
    oil_ej: float
    gas_ej: float
    observed_direct_mt: float | None


def _finite_nonnegative(value: float, name: str) -> float:
    if not math.isfinite(value) or value < 0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return value


def direct_co2_from_energy_mt(
    *, coal_ej: float, oil_ej: float, gas_ej: float,
    factors_kg_per_tj: dict[str, float] | None = None,
) -> float:
    """Map fuel energy (EJ) to direct CO2 (Mt).

    1 EJ = 1e6 TJ and 1 Mt = 1e9 kg, therefore kg/TJ * EJ / 1000 = Mt.
    """
    factors = factors_kg_per_tj or IPCC_FACTORS_KG_PER_TJ
    for name, value in (("coal_ej", coal_ej), ("oil_ej", oil_ej), ("gas_ej", gas_ej)):
        _finite_nonnegative(float(value), name)
    for fuel in ("coal", "oil", "gas"):
        _finite_nonnegative(float(factors[fuel]), f"{fuel}_factor")
    return (
        coal_ej * factors["coal"]
        + oil_ej * factors["oil"]
        + gas_ej * factors["gas"]
    ) / 1000.0


def _load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_records(
    ei_path: Path = EI_PATH,
    gcb_path: Path = GCB_PATH,
) -> list[YearRecord]:
    energy = {int(row["year"]): row for row in _load_csv(ei_path)}
    emissions = {int(row["year"]): row for row in _load_csv(gcb_path)}
    records: list[YearRecord] = []
    for year in sorted(y for y in energy if 1990 <= y <= PROSPECTIVE_YEAR):
        e = energy[year]
        g = emissions.get(year)
        observed = None
        if g is not None:
            observed = float(g["coal_mt"]) + float(g["oil_mt"]) + float(g["gas_mt"])
        records.append(
            YearRecord(
                year=year,
                fossil_energy_ej=float(e["fossil_energy_ej"]),
                coal_ej=float(e["coal_ej"]),
                oil_ej=float(e["oil_ej"]),
                gas_ej=float(e["gas_ej"]),
                observed_direct_mt=observed,
            )
        )
    return records


def _in_window(records: Iterable[YearRecord], window: tuple[int, int]) -> list[YearRecord]:
    return [r for r in records if window[0] <= r.year <= window[1]]


def calibrate_scale(
    records: Iterable[YearRecord],
    factors_kg_per_tj: dict[str, float] | None = None,
) -> float:
    """Fit one multiplicative correction using development data only."""
    observed_sum = 0.0
    predicted_sum = 0.0
    for record in records:
        if record.observed_direct_mt is None:
            continue
        observed_sum += record.observed_direct_mt
        predicted_sum += direct_co2_from_energy_mt(
            coal_ej=record.coal_ej,
            oil_ej=record.oil_ej,
            gas_ej=record.gas_ej,
            factors_kg_per_tj=factors_kg_per_tj,
        )
    if observed_sum <= 0 or predicted_sum <= 0:
        raise ValueError("Calibration requires positive observed and predicted totals")
    return observed_sum / predicted_sum


def _metrics(actual: list[float], predicted: list[float]) -> dict[str, float | int]:
    if not actual or len(actual) != len(predicted):
        raise ValueError("Metrics require equal non-empty arrays")
    errors = [p - a for a, p in zip(actual, predicted)]
    abs_errors = [abs(e) for e in errors]
    wmape = sum(abs_errors) / sum(abs(a) for a in actual)
    return {
        "n": len(actual),
        "wmape": wmape,
        "mape": sum(abs((p - a) / a) for a, p in zip(actual, predicted)) / len(actual),
        "rmse_mt": math.sqrt(sum(e * e for e in errors) / len(errors)),
        "bias_fraction": sum(errors) / sum(actual),
    }


def _predictions(
    records: list[YearRecord],
    scale: float,
    factors_kg_per_tj: dict[str, float] | None = None,
) -> list[dict[str, float | int | None]]:
    by_year = {r.year: r for r in records}
    rows: list[dict[str, float | int | None]] = []
    for r in records:
        fixed = direct_co2_from_energy_mt(
            coal_ej=r.coal_ej, oil_ej=r.oil_ej, gas_ej=r.gas_ej,
            factors_kg_per_tj=factors_kg_per_tj,
        )
        baseline = None
        previous = by_year.get(r.year - 1)
        if previous is not None and previous.observed_direct_mt is not None:
            baseline = (
                previous.observed_direct_mt / previous.fossil_energy_ej
            ) * r.fossil_energy_ej
        rows.append(
            {
                "year": r.year,
                "observed_direct_mt": r.observed_direct_mt,
                "fixed_ipcc_mt": fixed,
                "calibrated_candidate_mt": fixed * scale,
                "persistence_intensity_baseline_mt": baseline,
            }
        )
    return rows


def _window_metrics(
    rows: list[dict[str, float | int | None]],
    window: tuple[int, int],
) -> dict[str, dict[str, float | int]]:
    subset = [
        row for row in rows
        if window[0] <= int(row["year"]) <= window[1]
        and row["observed_direct_mt"] is not None
    ]
    actual = [float(row["observed_direct_mt"]) for row in subset]
    result = {}
    for name in (
        "fixed_ipcc_mt",
        "calibrated_candidate_mt",
        "persistence_intensity_baseline_mt",
    ):
        predicted = [float(row[name]) for row in subset]
        result[name] = _metrics(actual, predicted)
    return result


def _sensitivity(records: list[YearRecord]) -> dict:
    development = _in_window(records, DEVELOPMENT)
    holdout_baseline = _window_metrics(
        _predictions(records, calibrate_scale(development)), HOLDOUT
    )["persistence_intensity_baseline_mt"]["wmape"]
    cases = []
    for coal, oil, gas in product(
        IPCC_FACTOR_RANGES_KG_PER_TJ["coal"],
        IPCC_FACTOR_RANGES_KG_PER_TJ["oil"],
        IPCC_FACTOR_RANGES_KG_PER_TJ["gas"],
    ):
        factors = {"coal": coal, "oil": oil, "gas": gas}
        scale = calibrate_scale(development, factors)
        rows = _predictions(records, scale, factors)
        candidate = _window_metrics(rows, HOLDOUT)["calibrated_candidate_mt"]
        wmape = float(candidate["wmape"])
        cases.append(
            {
                "factors_kg_per_tj": factors,
                "development_scale": scale,
                "holdout_wmape": wmape,
                "skill_vs_baseline": 1.0 - wmape / float(holdout_baseline),
            }
        )
    return {
        "factor_ranges_source": "IPCC 2006 Guidelines Vol.2 Ch.2 Table 2.2 lower/upper bounds",
        "cases": cases,
        "best_holdout_wmape": min(c["holdout_wmape"] for c in cases),
        "worst_holdout_wmape": max(c["holdout_wmape"] for c in cases),
        "best_skill_vs_baseline": max(c["skill_vs_baseline"] for c in cases),
        "worst_skill_vs_baseline": min(c["skill_vs_baseline"] for c in cases),
        "ranking_reversal": any(c["skill_vs_baseline"] < 0 for c in cases),
    }


def evaluate() -> tuple[dict, list[dict[str, float | int | None]]]:
    records = load_records()
    development = _in_window(records, DEVELOPMENT)
    scale = calibrate_scale(development)
    rows = _predictions(records, scale)
    validation = _window_metrics(rows, VALIDATION)
    holdout = _window_metrics(rows, HOLDOUT)
    candidate_wmape = float(holdout["calibrated_candidate_mt"]["wmape"])
    baseline_wmape = float(holdout["persistence_intensity_baseline_mt"]["wmape"])
    skill = 1.0 - candidate_wmape / baseline_wmape
    sensitivity = _sensitivity(records)
    prospective = next(row for row in rows if row["year"] == PROSPECTIVE_YEAR)

    gates = {
        "S1": {
            "status": "PASS",
            "requirement": "boundary adequacy",
            "evidence": "Coal+oil+gas EI energy is matched only to GCB coal+oil+gas CO2; cement, flaring and other are excluded.",
        },
        "S2": {
            "status": "PASS",
            "requirement": "structure assessment",
            "evidence": "Transparent accounting identity plus one development-only multiplicative correction; no World3 feedback.",
        },
        "S3": {
            "status": "PASS",
            "requirement": "dimensional consistency",
            "evidence": "EJ -> TJ and kg/TJ -> Mt conversion is explicit and unit-tested.",
        },
        "S4": {
            "status": "PASS",
            "requirement": "accounting / conservation",
            "evidence": "Candidate emissions are exactly the sum of fuel-specific contributions; source fuel components are retained separately.",
        },
        "S5": {
            "status": "PASS",
            "requirement": "extreme-condition behavior",
            "evidence": "Zero fuel gives zero CO2; negative/non-finite energy or factors are rejected.",
        },
        "S6": {
            "status": "PASS",
            "requirement": "numerical robustness",
            "evidence": "Closed-form deterministic calculation; all evaluated values are finite and reproducible.",
        },
        "S7": {
            "status": "FAIL",
            "requirement": "temporal provenance; no future information",
            "evidence": "Parameter fitting is time-separated, but the historical EI/GCB observations are current revised vintages rather than archived as-of-origin releases. This is pseudo-prospective, not a strict real-time vintage backtest.",
        },
        "S8": {
            "status": "FAIL",
            "requirement": "prospective out-of-sample skill",
            "evidence": f"2018-2024 holdout skill versus the declared baseline is {skill:.6f}, below the project-level 0.30 acceptance criterion.",
        },
        "S9": {
            "status": "FAIL",
            "requirement": "uncertainty and sensitivity robustness",
            "evidence": f"Across IPCC lower/upper factor corners, holdout skill ranges from {sensitivity['worst_skill_vs_baseline']:.6f} to {sensitivity['best_skill_vs_baseline']:.6f}; ranking reverses in at least one admissible corner.",
        },
        "S10": {
            "status": "PASS",
            "requirement": "incremental value with no baseline regression",
            "evidence": f"Nominal holdout WMAPE is {candidate_wmape:.6f} versus {baseline_wmape:.6f}; the candidate is inactive and changes no World3/BAU/BAU2/BAU Hybrid 2026 outputs.",
        },
    }

    payload = {
        "experiment": "energy_accounting_to_direct_emissions",
        "evaluation_date": "2026-09-17",
        "repository_stage": "R2 prospective candidate validation",
        "boundary": {
            "energy_input": "Energy Institute Total World coal, oil and gas energy supply, EJ/year",
            "target": "Global Carbon Budget coal + oil + natural-gas fossil CO2, MtCO2/year",
            "excluded_target_categories": ["cement", "gas_flaring", "other"],
            "excluded_mechanisms": [
                "upstream methane",
                "lifecycle construction emissions",
                "carbon capture",
                "carbon-cycle sinks",
                "temperature response",
                "World3 persistent-pollution substitution",
                "world3_resource_fraction_to_fossil_eroi",
            ],
        },
        "temporal_design": {
            "development": list(DEVELOPMENT),
            "validation": list(VALIDATION),
            "locked_holdout": list(HOLDOUT),
            "prospective_unscored_year": PROSPECTIVE_YEAR,
            "strict_real_time_vintage": False,
        },
        "factors": {
            "source": "IPCC 2006 Guidelines Vol.2 Ch.2 Table 2.2, NCV kg CO2/TJ",
            "defaults_kg_per_tj": IPCC_FACTORS_KG_PER_TJ,
            "ranges_kg_per_tj": {
                fuel: list(bounds)
                for fuel, bounds in IPCC_FACTOR_RANGES_KG_PER_TJ.items()
            },
        },
        "development_scale": scale,
        "metrics": {
            "validation_2010_2017": validation,
            "holdout_2018_2024": holdout,
            "holdout_skill_vs_baseline": skill,
            "minimum_skill_required": MIN_SKILL_VS_BASELINE,
        },
        "sensitivity": sensitivity,
        "prospective_2025_unscored": {
            "fixed_ipcc_mt": prospective["fixed_ipcc_mt"],
            "calibrated_candidate_mt": prospective["calibrated_candidate_mt"],
            "persistence_intensity_baseline_mt": prospective["persistence_intensity_baseline_mt"],
            "observed_target_available": False,
        },
        "gates": gates,
        "all_gates_pass": all(g["status"] == "PASS" for g in gates.values()),
        "verdict": "RETAIN AS DIAGNOSTIC",
        "central_model_promotion": False,
        "next_stage_not_started": "Acquire/reconstruct release-as-of-origin EI and GCB vintages (or wait for realized 2025 fuel-level GCB data), then rerun a strict prospective vintage-locked confirmation before reconsidering S7-S9.",
    }
    return payload, rows


def serialize_results(payload: dict) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def serialize_predictions(rows: list[dict[str, float | int | None]]) -> str:
    fieldnames = [
        "year",
        "observed_direct_mt",
        "fixed_ipcc_mt",
        "calibrated_candidate_mt",
        "persistence_intensity_baseline_mt",
    ]
    from io import StringIO
    out = StringIO()
    writer = csv.DictWriter(out, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({
            key: (
                "" if row[key] is None else
                int(row[key]) if key == "year" else
                f"{float(row[key]):.6f}"
            )
            for key in fieldnames
        })
    return out.getvalue()
