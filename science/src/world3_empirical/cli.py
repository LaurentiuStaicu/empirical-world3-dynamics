"""Command-line interface with explicit structural-engine routing."""

from __future__ import annotations

import argparse
from pathlib import Path

from .model import run_legacy_scenario
from .scenarios import load_scenarios
from .world3_03 import run_world3_03


OFFICIAL_SCENARIOS = {"bau": 1, "bau2": 2}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="world3-empirical",
        description=(
            "Empirical World3 Dynamics. The default simulate command runs the "
            "retained official World3-03 structural baseline via PySD. The older "
            "Pyworld3 1.1 implementation is available only through simulate-legacy."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    simulate = subparsers.add_parser(
        "simulate",
        help="Run the official World3-03 BAU or BAU2 structural baseline",
    )
    simulate.add_argument(
        "--scenario",
        choices=sorted(OFFICIAL_SCENARIOS),
        default="bau2",
        help="Official World3-03 scenario (default: bau2)",
    )
    simulate.add_argument("--year-min", type=int, default=1900)
    simulate.add_argument("--year-max", type=int, default=2100)
    simulate.add_argument("--output", type=Path, required=True)

    legacy = subparsers.add_parser(
        "simulate-legacy",
        help="Run the legacy/reference Pyworld3 1.1 scenario layer",
    )
    legacy.add_argument(
        "--scenario",
        choices=sorted(load_scenarios()),
        default="world3_standard",
    )
    legacy.add_argument("--year-min", type=int, default=1900)
    legacy.add_argument("--year-max", type=int, default=2100)
    legacy.add_argument("--dt", type=float, default=0.5)
    legacy.add_argument("--output", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.year_min > args.year_max:
        parser.error("--year-min must be less than or equal to --year-max")

    if args.command == "simulate":
        years = tuple(range(args.year_min, args.year_max + 1))
        result = run_world3_03(OFFICIAL_SCENARIOS[args.scenario], years=years)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        result.frame.to_csv(args.output, index=False)
        print(f"Saved {len(result.frame)} rows to {args.output}")
        print("Engine: official World3-03 via PySD")
        print(f"Scenario: {result.scenario_name}")
        return 0

    if args.command == "simulate-legacy":
        result = run_legacy_scenario(
            args.scenario,
            year_min=args.year_min,
            year_max=args.year_max,
            dt=args.dt,
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        result.frame.to_csv(args.output, index=False)
        print(f"Saved {len(result.frame)} rows to {args.output}")
        print("Engine: legacy/reference Pyworld3 1.1")
        print(f"Scenario status: {result.scenario.evidence_status}")
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
