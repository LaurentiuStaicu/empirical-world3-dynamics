#!/usr/bin/env python3
"""Evaluate a narrow retained error-comparison gate.

This historical helper is not the Real Model S1-S10 promotion contract and does
not by itself authorize any scientific or central-model promotion.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "data" / "scenarios"


def load(filename: str) -> list[dict[str, str]]:
    with (SCENARIOS / filename).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--enforce", action="store_true", help="return non-zero when the gate fails")
    args = parser.parse_args()
    recent = load("backtest_2019_latest.csv")
    multi = load("backtest_multi_origin.csv")
    recent_wins = sum(float(row["bau2_e2026_mape_pct"]) <= float(row["bau2_level_anchored_mape_pct"]) for row in recent)
    multi_wins = sum(float(row["bau2_e2026_mape_pct"]) <= float(row["bau2_level_anchored_mape_pct"]) for row in multi)
    passed = recent_wins == len(recent) and multi_wins >= 2
    print(
        f"Poarta comparativă istorică: {'PASS' if passed else 'FAIL'} · "
        f"holdouturi recente {recent_wins}/{len(recent)} · multi-origin {multi_wins}/{len(multi)}"
    )
    print("Regulă comparativă: toate holdouturile recente și cel puțin două serii multi-origin mai bune decât BAU2 ancorat.")
    print("Limită: acest test nu este echivalent cu validarea științifică sau cu porțile S1-S10 și nu autorizează singur promovarea unui mecanism.")
    return 1 if args.enforce and not passed else 0


if __name__ == "__main__":
    raise SystemExit(main())
