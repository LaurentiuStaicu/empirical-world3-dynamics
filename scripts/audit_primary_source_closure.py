#!/usr/bin/env python3
"""One-off online probe for R-FDC-6 primary-source byte/value closure.

This script is diagnostic only. It downloads authoritative primary files,
computes byte hashes/sizes, and compares the relevant World series with the
currently retained EWD adapters/snapshots. It does not modify repository files.
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import io
import json
import re
import urllib.request
import urllib.parse
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

SOURCES = {
    "undp": "https://hdr.undp.org/sites/default/files/2025_HDR/HDR25_Composite_indices_complete_time_series.csv",
    "wpp": "https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20(Standard)/CSV_FILES/WPP2024_Demographic_Indicators_Medium.csv.gz",
    "gcb": "https://zenodo.org/records/17417124/files/GCB2025v15_MtCO2_flat.csv?download=1",
    "ei_page": "https://www.energyinst.org/statistical-review/resources-and-data-downloads",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def md5_bytes(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()


def fetch(url: str) -> tuple[bytes, dict[str, Any]]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "empirical-world3-dynamics-provenance-audit/0.1.0",
            "Accept": "*/*",
        },
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        data = response.read()
        meta = {
            "requested_url": url,
            "final_url": response.geturl(),
            "http_status": getattr(response, "status", None),
            "content_type": response.headers.get("Content-Type"),
            "content_length_header": response.headers.get("Content-Length"),
            "size_bytes": len(data),
            "sha256": sha256_bytes(data),
            "md5": md5_bytes(data),
        }
        return data, meta


def decode_text(data: bytes) -> tuple[str, str]:
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return data.decode(encoding), encoding
        except UnicodeDecodeError:
            pass
    raise UnicodeDecodeError("unknown", data, 0, 1, "no supported encoding")


def reader_from_text(text: str) -> csv.DictReader:
    sample = text[:65536]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
    except csv.Error:
        dialect = csv.excel
    return csv.DictReader(io.StringIO(text), dialect=dialect)


def parse_float(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip().replace("\u00a0", "").replace(",", "")
    if text in {"", "..", "...", "NA", "N/A", "nan", "NaN"}:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def load_local_long_series(path: Path, entity_key: str, entity_value: str, year_key: str, value_key: str) -> dict[int, float]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = csv.DictReader(handle)
        result: dict[int, float] = {}
        for row in rows:
            if row.get(entity_key) != entity_value:
                continue
            year = int(float(row[year_key]))
            value = parse_float(row.get(value_key))
            if value is not None:
                result[year] = value
        return result


def compare_series(primary: dict[int, float], retained: dict[int, float], *, tolerance: float = 0.0) -> dict[str, Any]:
    years = sorted(set(primary) & set(retained))
    missing_primary = sorted(set(retained) - set(primary))
    missing_retained = sorted(set(primary) - set(retained))
    diffs = {year: primary[year] - retained[year] for year in years}
    abs_diffs = {year: abs(value) for year, value in diffs.items()}
    mismatches = [year for year in years if abs_diffs[year] > tolerance]
    worst = sorted(abs_diffs.items(), key=lambda item: item[1], reverse=True)[:10]
    return {
        "compared_years": len(years),
        "first_year": years[0] if years else None,
        "last_year": years[-1] if years else None,
        "missing_in_primary": missing_primary,
        "missing_in_retained": missing_retained,
        "tolerance": tolerance,
        "mismatch_count": len(mismatches),
        "maximum_absolute_difference": worst[0][1] if worst else None,
        "worst_years": [{"year": y, "absolute_difference": d} for y, d in worst],
    }


def probe_undp() -> dict[str, Any]:
    data, meta = fetch(SOURCES["undp"])
    text, encoding = decode_text(data)
    rows = list(reader_from_text(text))
    fields = list(rows[0].keys()) if rows else []

    hdi_columns: dict[int, str] = {}
    for field in fields:
        match = re.fullmatch(r"hdi[_\- ]?(\d{4})", field.strip(), flags=re.IGNORECASE)
        if match:
            hdi_columns[int(match.group(1))] = field

    world_row = None
    for row in rows:
        values = {str(value).strip() for value in row.values() if value is not None}
        if "World" in values or "WLD" in values:
            world_row = row
            break

    result: dict[str, Any] = {
        "download": meta,
        "decoded_encoding": encoding,
        "row_count": len(rows),
        "field_count": len(fields),
        "field_sample": fields[:30],
        "hdi_year_columns_found": [min(hdi_columns) if hdi_columns else None, max(hdi_columns) if hdi_columns else None],
        "world_row_found": world_row is not None,
    }
    if world_row is None or not hdi_columns:
        result["comparison_status"] = "PARSE_OPEN"
        return result

    primary = {
        year: value
        for year, column in hdi_columns.items()
        if (value := parse_float(world_row.get(column))) is not None
    }
    retained = load_local_long_series(
        ROOT / "science/data/raw/bau2_e2026/2026-08-28/undp_hdi_owid_adapter.csv",
        "Entity",
        "World",
        "Year",
        "Human Development Index",
    )
    result["primary_world_years"] = len(primary)
    result["retained_world_years"] = len(retained)
    result["comparison"] = compare_series(primary, retained, tolerance=0.0)
    result["comparison_status"] = (
        "EXACT_PASS"
        if result["comparison"]["mismatch_count"] == 0
        and not result["comparison"]["missing_in_primary"]
        else "DIFFERENCE_OR_COVERAGE"
    )
    return result


def probe_wpp() -> dict[str, Any]:
    data, meta = fetch(SOURCES["wpp"])
    decompressed = gzip.decompress(data)
    text, encoding = decode_text(decompressed)
    rows = list(reader_from_text(text))
    fields = list(rows[0].keys()) if rows else []
    normalized = {field.strip().lower(): field for field in fields}

    def choose(*names: str) -> str | None:
        for name in names:
            if name.lower() in normalized:
                return normalized[name.lower()]
        return None

    location_field = choose("Location", "LocName", "Entity")
    locid_field = choose("LocID", "LocationID")
    year_field = choose("Time", "Year", "TimePeriod")
    population_field = choose("PopTotal", "TPopulation1July", "TPopulation", "Population")

    primary: dict[int, float] = {}
    world_rows = 0
    if year_field and population_field:
        for row in rows:
            is_world = False
            if location_field and str(row.get(location_field, "")).strip() == "World":
                is_world = True
            if locid_field and str(row.get(locid_field, "")).strip() == "900":
                is_world = True
            if not is_world:
                continue
            value = parse_float(row.get(population_field))
            year_value = parse_float(row.get(year_field))
            if value is None or year_value is None:
                continue
            world_rows += 1
            year = int(year_value)
            if value < 100_000_000:
                value *= 1000.0
            primary[year] = value

    adapter_path = ROOT / "science/data/raw/bau2_e2026/2026-08-28/un_wpp2024_owid_adapter.csv"
    retained: dict[int, float] = {}
    with adapter_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if row.get("entity") != "World":
                continue
            year = int(float(row["year"]))
            estimate = parse_float(row.get("population__sex_all__age_all__variant_estimates"))
            medium = parse_float(row.get("population__sex_all__age_all__variant_medium__projected"))
            value = estimate if estimate is not None else medium
            if value is not None:
                retained[year] = value

    result: dict[str, Any] = {
        "download": meta,
        "decompressed_size_bytes": len(decompressed),
        "decoded_encoding": encoding,
        "row_count": len(rows),
        "field_count": len(fields),
        "field_sample": fields[:40],
        "selected_fields": {
            "location": location_field,
            "locid": locid_field,
            "year": year_field,
            "population": population_field,
        },
        "world_rows_parsed": world_rows,
        "primary_world_years": len(primary),
        "retained_world_years": len(retained),
    }
    if not primary:
        result["comparison_status"] = "PARSE_OPEN"
        return result

    # WPP bulk population values may be published in thousands with finite
    # decimal precision, so record exact differences rather than assuming
    # byte-level equality with a secondary transport.
    result["comparison"] = compare_series(primary, retained, tolerance=5.0)
    result["comparison_status"] = (
        "WITHIN_5_PERSONS_PASS"
        if result["comparison"]["mismatch_count"] == 0
        and not result["comparison"]["missing_in_primary"]
        else "DIFFERENCE_OR_COVERAGE"
    )
    return result


def probe_gcb() -> dict[str, Any]:
    data, meta = fetch(SOURCES["gcb"])
    text, encoding = decode_text(data)
    rows = list(reader_from_text(text))
    fields = list(rows[0].keys()) if rows else []
    normalized = {field.strip().lower(): field for field in fields}

    def choose(*names: str) -> str | None:
        for name in names:
            if name.lower() in normalized:
                return normalized[name.lower()]
        return None

    country_field = choose("Country", "Entity", "Area")
    year_field = choose("Year")
    mappings = {
        "coal_mt": choose("Coal"),
        "oil_mt": choose("Oil"),
        "gas_mt": choose("Gas"),
        "cement_mt": choose("Cement"),
        "flaring_mt": choose("Flaring"),
        "other_mt": choose("Other"),
    }

    primary: dict[int, dict[str, float]] = {}
    if country_field and year_field and all(mappings.values()):
        for row in rows:
            country = str(row.get(country_field, "")).strip()
            if country not in {"Global", "World"}:
                continue
            year_value = parse_float(row.get(year_field))
            if year_value is None:
                continue
            values: dict[str, float] = {}
            ok = True
            for target, source in mappings.items():
                value = parse_float(row.get(source))
                if value is None:
                    ok = False
                    break
                values[target] = value
            if ok:
                primary[int(year_value)] = values

    local_path = ROOT / "science/data/experiments/gcb_direct_fossil_1990_2024.csv"
    retained: dict[int, dict[str, float]] = {}
    with local_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            year = int(float(row["year"]))
            retained[year] = {
                key: float(row[key])
                for key in mappings
            }

    comparisons: dict[str, Any] = {}
    if primary:
        for key in mappings:
            p = {year: values[key] for year, values in primary.items() if 1990 <= year <= 2024}
            r = {year: values[key] for year, values in retained.items()}
            comparisons[key] = compare_series(p, r, tolerance=0.051)

    result: dict[str, Any] = {
        "download": meta,
        "decoded_encoding": encoding,
        "row_count": len(rows),
        "field_count": len(fields),
        "field_sample": fields[:30],
        "selected_fields": {
            "country": country_field,
            "year": year_field,
            **mappings,
        },
        "primary_world_years": len(primary),
        "retained_world_years": len(retained),
        "comparisons": comparisons,
    }
    if not primary:
        result["comparison_status"] = "PARSE_OPEN"
        return result

    good = all(
        comp["mismatch_count"] == 0 and not comp["missing_in_primary"]
        for comp in comparisons.values()
    )
    result["comparison_status"] = "ROUNDING_EQUIVALENT_PASS" if good else "DIFFERENCE_OR_COVERAGE"
    return result


def probe_ei_page() -> dict[str, Any]:
    data, meta = fetch(SOURCES["ei_page"])
    text, encoding = decode_text(data)
    hrefs = re.findall(r'''href=["']([^"']+)["']''', text, flags=re.IGNORECASE)
    candidates: list[str] = []
    for href in hrefs:
        absolute = urllib.parse.urljoin(SOURCES["ei_page"], href)
        low = absolute.lower()
        if (
            low.endswith(".csv")
            or ".csv?" in low
            or low.endswith(".xlsx")
            or ".xlsx?" in low
            or "narrow" in low
            or "statistical-review" in low and ("download" in low or "__data/assets" in low)
        ):
            if absolute not in candidates:
                candidates.append(absolute)

    downloads: list[dict[str, Any]] = []
    for url in candidates:
        low = url.lower()
        if not (".csv" in low or "narrow" in low):
            continue
        try:
            candidate_data, candidate_meta = fetch(url)
            candidate_meta["url"] = url
            candidate_meta["looks_like_csv"] = b"," in candidate_data[:4096] and b"\n" in candidate_data[:4096]
            downloads.append(candidate_meta)
        except Exception as error:
            downloads.append({
                "url": url,
                "probe_status": "ERROR",
                "error_type": type(error).__name__,
                "error": str(error),
            })

    return {
        "page_download": meta,
        "decoded_encoding": encoding,
        "candidate_links": candidates,
        "candidate_downloads": downloads,
    }


def main() -> None:
    results: dict[str, Any] = {
        "probe_date": "2026-09-22",
        "purpose": "R-FDC-6 primary-source byte/value verification; no repository mutation",
        "sources": {},
    }
    for name, function in [
        ("undp", probe_undp),
        ("wpp", probe_wpp),
        ("gcb", probe_gcb),
        ("energy_institute", probe_ei_page),
    ]:
        try:
            results["sources"][name] = function()
        except Exception as error:  # diagnostic: retain all source outcomes
            results["sources"][name] = {
                "probe_status": "ERROR",
                "error_type": type(error).__name__,
                "error": str(error),
            }

    output = ROOT / "primary-source-provenance-verification.json"
    output.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
