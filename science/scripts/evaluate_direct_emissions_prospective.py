#!/usr/bin/env python3
"""Generate or verify the frozen direct-emissions prospective experiment artifacts."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "science" / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from world3_empirical.direct_emissions_experiment import (  # noqa: E402
    evaluate,
    serialize_predictions,
    serialize_results,
)

RESULTS = ROOT / "science/data/experiments/energy_direct_emissions_prospective_2026-09-17.json"
PREDICTIONS = ROOT / "science/data/experiments/energy_direct_emissions_predictions_2026-09-17.csv"


def _matches(path: Path, content: str) -> bool:
    if path.suffix == ".json":
        return json.loads(path.read_text(encoding="utf-8")) == json.loads(content)
    return path.read_text(encoding="utf-8") == content


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if committed artifacts differ")
    args = parser.parse_args()

    payload, rows = evaluate()
    expected = {
        RESULTS: serialize_results(payload),
        PREDICTIONS: serialize_predictions(rows),
    }

    if args.check:
        failures = []
        for path, content in expected.items():
            if not path.is_file():
                failures.append(f"missing {path.relative_to(ROOT)}")
            elif not _matches(path, content):
                failures.append(f"stale {path.relative_to(ROOT)}")
        if failures:
            raise SystemExit("Direct-emissions reproduction failed: " + "; ".join(failures))
        print("Direct-emissions prospective artifacts reproduce semantically; prediction CSV is byte-identical.")
        return

    for path, content in expected.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
