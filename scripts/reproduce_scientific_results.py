#!/usr/bin/env python3
"""Rebuild retained scientific results and compare them with committed reference outputs.

CSV and JSON structure is compared exactly. Floating-point values are compared with a
very small tolerance because mathematically equivalent numerical libraries can
legitimately differ in their final machine-precision digits across platforms.
"""

from __future__ import annotations

import csv
from decimal import Decimal, InvalidOperation
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SCIENCE = ROOT / "science"
OUTPUT = SCIENCE / "outputs" / "joint_hybrid_2026"
REFERENCE = ROOT / "data" / "scenarios"
FILES = [
    "backtest_2019_latest.csv",
    "backtest_multi_origin.csv",
    "fit_diagnostics.csv",
    "parameter_identifiability.csv",
    "candidate_ranking.csv",
    "validation_candidate_ranking.csv",
    "bridge_validation.csv",
    "lookup_extrapolation_audit.csv",
]

RELATIVE_TOLERANCE = Decimal("1e-12")
ABSOLUTE_TOLERANCE = Decimal("1e-12")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_inputs() -> None:
    manifest_path = SCIENCE / "data" / "input_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for relative, expected in manifest["files"].items():
        path = ROOT / relative
        if sha256(path) != expected:
            raise RuntimeError(f"Scientific input hash mismatch: {relative}")
    for relative, metadata in manifest.get("remote_files", {}).items():
        path = ROOT / relative
        if (
            not path.is_file()
            or path.stat().st_size != int(metadata["size_bytes"])
            or sha256(path) != metadata["sha256"]
        ):
            raise RuntimeError(f"Remote scientific input hash mismatch: {relative}")


def run(script: str) -> None:
    environment = os.environ.copy()
    paths = [str(SCIENCE / "src"), str(SCIENCE / "scripts"), str(SCIENCE / "vendor")]
    if environment.get("PYTHONPATH"):
        paths.append(environment["PYTHONPATH"])
    environment["PYTHONPATH"] = os.pathsep.join(paths)
    subprocess.run(
        [sys.executable, str(SCIENCE / "scripts" / script)],
        cwd=SCIENCE,
        env=environment,
        check=True,
    )


def decimal_value(value: str) -> Decimal | None:
    try:
        parsed = Decimal(value)
    except InvalidOperation:
        return None
    return parsed if parsed.is_finite() else None


def numeric_difference(
    generated: Decimal,
    reference: Decimal,
    location: str,
) -> Decimal:
    difference = abs(generated - reference)
    allowed = max(
        ABSOLUTE_TOLERANCE,
        RELATIVE_TOLERANCE * max(abs(generated), abs(reference)),
    )
    if difference > allowed:
        raise RuntimeError(
            f"Reproduction mismatch at {location}: generated={generated}, "
            f"reference={reference}, absolute difference={difference}, "
            f"allowed={allowed}"
        )
    return difference


def compare_csv(generated: Path, reference: Path) -> Decimal:
    with generated.open(newline="", encoding="utf-8") as generated_handle:
        generated_rows = list(csv.reader(generated_handle))
    with reference.open(newline="", encoding="utf-8") as reference_handle:
        reference_rows = list(csv.reader(reference_handle))

    if len(generated_rows) != len(reference_rows):
        raise RuntimeError(
            f"Reproduction mismatch in {generated.name}: generated row count "
            f"{len(generated_rows)} != reference row count {len(reference_rows)}"
        )

    maximum_difference = Decimal(0)
    for row_number, (generated_row, reference_row) in enumerate(
        zip(generated_rows, reference_rows), start=1
    ):
        if len(generated_row) != len(reference_row):
            raise RuntimeError(
                f"Reproduction mismatch in {generated.name}, row {row_number}: "
                f"generated column count {len(generated_row)} != reference column "
                f"count {len(reference_row)}"
            )
        for column_number, (generated_cell, reference_cell) in enumerate(
            zip(generated_row, reference_row), start=1
        ):
            if generated_cell == reference_cell:
                continue
            generated_number = decimal_value(generated_cell)
            reference_number = decimal_value(reference_cell)
            if generated_number is None or reference_number is None:
                raise RuntimeError(
                    f"Reproduction mismatch in {generated.name}, row {row_number}, "
                    f"column {column_number}: {generated_cell!r} != {reference_cell!r}"
                )
            difference = numeric_difference(
                generated_number,
                reference_number,
                f"{generated.name}, row {row_number}, column {column_number}",
            )
            maximum_difference = max(maximum_difference, difference)
    return maximum_difference


def compare_json_values(generated, reference, location: str) -> Decimal:
    if isinstance(generated, dict) and isinstance(reference, dict):
        if generated.keys() != reference.keys():
            raise RuntimeError(f"Reproduction mismatch at {location}: JSON keys differ")
        maximum = Decimal(0)
        for key in generated:
            maximum = max(
                maximum,
                compare_json_values(generated[key], reference[key], f"{location}.{key}"),
            )
        return maximum
    if isinstance(generated, list) and isinstance(reference, list):
        if len(generated) != len(reference):
            raise RuntimeError(f"Reproduction mismatch at {location}: list lengths differ")
        maximum = Decimal(0)
        for index, (generated_item, reference_item) in enumerate(zip(generated, reference)):
            maximum = max(
                maximum,
                compare_json_values(
                    generated_item, reference_item, f"{location}[{index}]"
                ),
            )
        return maximum
    if type(generated) is not type(reference):
        raise RuntimeError(
            f"Reproduction mismatch at {location}: JSON types "
            f"{type(generated).__name__} and {type(reference).__name__} differ"
        )
    if isinstance(generated, Decimal):
        return numeric_difference(generated, reference, location)
    if generated != reference:
        raise RuntimeError(
            f"Reproduction mismatch at {location}: {generated!r} != {reference!r}"
        )
    return Decimal(0)


def compare_json(generated: Path, reference: Path) -> Decimal:
    generated_payload = json.loads(
        generated.read_text(encoding="utf-8"), parse_float=Decimal
    )
    reference_payload = json.loads(
        reference.read_text(encoding="utf-8"), parse_float=Decimal
    )
    return compare_json_values(generated_payload, reference_payload, generated.name)


def compare(generated: Path, reference: Path) -> Decimal:
    if generated.read_bytes() == reference.read_bytes():
        return Decimal(0)
    if generated.suffix == ".csv":
        return compare_csv(generated, reference)
    if generated.suffix == ".json":
        return compare_json(generated, reference)
    raise RuntimeError(f"No semantic comparator for {generated.name}")


def main() -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "fetch_science_inputs.py")],
        cwd=ROOT,
        check=True,
    )
    verify_inputs()
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    run("run_world3_03.py")
    run("build_joint_hybrid_2026.py")
    maximum_difference = Decimal(0)
    for filename in FILES:
        maximum_difference = max(
            maximum_difference,
            compare(OUTPUT / filename, REFERENCE / filename),
        )
    maximum_difference = max(
        maximum_difference,
        compare(OUTPUT / "manifest.json", REFERENCE / "bau_hybrid_2026_manifest.json"),
    )
    print(
        f"Reproducere științifică reușită: {len(FILES)} CSV-uri și manifest "
        f"semantic identice; abatere numerică absolută maximă "
        f"{maximum_difference}."
    )


if __name__ == "__main__":
    main()
