"""Usage: python3 scripts/audit_egrid_boundaries.py EGRID2021.xlsx EGRID2022.xlsx EGRID2023.xlsx"""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "science/src"), str(ROOT / "science/vendor")]
import openpyxl

from world3_empirical.egrid_boundary import compare_years, reconcile_boundaries

PLANTS = (315, 335, 56108, 56283)


def read_sheet(workbook, name):
    rows = workbook[name].iter_rows(values_only=True)
    next(rows)
    header = next(rows)
    if len(header) != len(set(header)):
        raise ValueError(f"Duplicate fields in {name}")
    return [dict(zip(header, row)) for row in rows if row[4] in PLANTS]


def main():
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    all_records = []
    source_hashes = {}
    for year, filename in zip((2021, 2022, 2023), sys.argv[1:]):
        source = Path(filename)
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        metadata_name = "egrid-source.json" if year == 2023 else f"egrid{year}-source.json"
        metadata = json.loads((ROOT / "science/data/energy_audit" / metadata_name).read_text())
        if digest != metadata["sha256"]:
            raise ValueError(f"Unreviewed eGRID {year} revision")
        workbook = openpyxl.load_workbook(source, read_only=True, data_only=True)
        suffix = str(year)[-2:]
        all_records.extend(reconcile_boundaries(
            year,
            read_sheet(workbook, f"PLNT{suffix}"),
            read_sheet(workbook, f"UNT{suffix}"),
            read_sheet(workbook, f"GEN{suffix}"),
            PLANTS,
        ))
        workbook.close()
        source_hashes[str(year)] = digest
    report = {
        "status": "post_hoc_boundary_reconciliation",
        "central_model_changed": False,
        "source_sha256": source_hashes,
        "plant_years": all_records,
        "transitions": compare_years(all_records),
    }
    target = ROOT / "science/data/energy_audit/egrid-boundary-reconciliation.json"
    temporary = target.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    temporary.replace(target)
    print(f"Wrote {target} with {len(all_records)} reconciled plant-years")


if __name__ == "__main__":
    main()
