#!/usr/bin/env python3
"""Validate empirical registry completeness against the active observation contract."""

from __future__ import annotations

from world3_empirical.registry import (
    load_registry,
    validate_active_observation_contract,
)


def main() -> None:
    registry = load_registry()
    summary = validate_active_observation_contract(registry=registry)
    print(
        "Empirical registry contract PASS: "
        f"{summary['central_observation_series']} central observation series + "
        f"{summary['benchmark_series']} benchmark series = "
        f"{summary['active_series_total']} required registry entries."
    )


if __name__ == "__main__":
    main()
