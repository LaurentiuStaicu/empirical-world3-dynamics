#!/usr/bin/env python3
"""Regression check for unambiguous EWD execution routing."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch

import pandas as pd

import world3_empirical.cli as cli
from world3_empirical.model import run_legacy_scenario, run_scenario


def main() -> None:
    if cli.OFFICIAL_SCENARIOS != {"bau": 1, "bau2": 2}:
        raise SystemExit("Execution routing changed: official scenario map is not BAU/BAU2")

    parser = cli.build_parser()
    official = parser.parse_args(["simulate", "--output", "out.csv"])
    if official.scenario != "bau2":
        raise SystemExit("Generic simulate command must default to official World3-03 BAU2")

    legacy = parser.parse_args(["simulate-legacy", "--output", "out.csv"])
    if legacy.scenario != "world3_standard":
        raise SystemExit("Legacy command default changed unexpectedly")

    if run_scenario is run_legacy_scenario:
        raise SystemExit("Backward-compatible run_scenario must remain a warning wrapper")

    with TemporaryDirectory(prefix="ewd_route_check_") as directory:
        root = Path(directory)

        official_result = SimpleNamespace(
            frame=pd.DataFrame({"year": [2000.0, 2001.0], "population": [1.0, 1.01]}),
            scenario_name="world3_03_bau2",
        )
        official_output = root / "official.csv"
        with patch.object(cli, "run_world3_03", return_value=official_result) as mocked:
            code = cli.main([
                "simulate",
                "--scenario", "bau2",
                "--year-min", "2000",
                "--year-max", "2001",
                "--output", str(official_output),
            ])
        if code != 0 or not official_output.is_file():
            raise SystemExit("Official simulate route did not complete successfully")
        mocked.assert_called_once_with(2, years=(2000, 2001))

        legacy_result = SimpleNamespace(
            frame=pd.DataFrame({"year": [2000.0], "population": [1.0]}),
            scenario=SimpleNamespace(evidence_status="reference_implementation"),
        )
        legacy_output = root / "legacy.csv"
        with patch.object(cli, "run_legacy_scenario", return_value=legacy_result) as mocked:
            code = cli.main([
                "simulate-legacy",
                "--scenario", "world3_standard",
                "--year-min", "2000",
                "--year-max", "2001",
                "--dt", "0.5",
                "--output", str(legacy_output),
            ])
        if code != 0 or not legacy_output.is_file():
            raise SystemExit("Legacy simulate route did not complete successfully")
        mocked.assert_called_once_with(
            "world3_standard", year_min=2000, year_max=2001, dt=0.5
        )

    print(
        "Execution routing PASS: generic simulate -> official World3-03; "
        "simulate-legacy -> explicit Pyworld3 1.1 reference route."
    )


if __name__ == "__main__":
    main()
