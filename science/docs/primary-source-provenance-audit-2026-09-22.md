# Primary-source provenance closure matrix — 2026-09-22

Status: **R-FDC-6 OPEN**. This is provenance-only work. No observation value, model equation, mapping, fitted parameter, candidate-selection rule, retained trajectory or scientific claim is changed here.

Machine-readable companion:

`science/data/provenance/primary_source_audit_2026-09-22.json`

## Why this gate exists

The repository already distinguishes source semantics from model semantics, but the remaining warnings are not all the same kind of problem. R-FDC-6 therefore separates four evidence levels:

1. **L1 — authority identified:** authoritative institution, dataset and scientific role are explicit.
2. **L2 — semantics reconciled:** selected definitions, boundaries or published anchors have been independently matched.
3. **L3 — primary artifact identified:** exact official artifact/version/file and immutable checksum metadata are known when exposed by the authority.
4. **L4 — complete lineage:** the full primary-file-to-retained-input byte/value path has been reproduced and recorded.

Only L4 is sufficient for a `PASS` when the repository claims frozen primary-source closure.

## Current closure matrix

| Source | EWD role | Evidence | Status | Remaining closure |
|---|---|---:|---|---|
| FAOSTAT Production Indices | central food observation | L4 | PASS | none; official archive is size/hash verified during clean reproduction |
| UNDP HDR 2025 HDI | central human-welfare proxy | L2 | WARNING | freeze/hash official CSV and compare every World HDI year used by EWD |
| UN WPP 2024 | population benchmark/guardrail | L2 | WARNING | freeze/hash official bulk CSV/GZ and compare all World rows and estimate/projection split |
| Energy Institute 2026 | energy diagnostic/candidate evidence | L1 | WARNING | compare official 2026 download with the pinned mirror transport |
| GCP fossil CO2 2025v15 | direct-emissions diagnostic | L3 | WARNING | reconstruct the EWD compact snapshot directly from the primary Zenodo file and compare all retained rows/categories |

## UNDP HDR 2025

Official documentation:

`https://hdr.undp.org/data-center/documentation-and-downloads`

Official complete time-series endpoint:

`https://hdr.undp.org/sites/default/files/2025_HDR/HDR25_Composite_indices_complete_time_series.csv`

The UNDP documentation page exposes **All composite indices and components time series (1990-2023)**. The 2026-09-21 EWD provenance follow-up already records exact agreement at all eight published World HDI anchors (1990, 2000, 2010, 2015, 2020, 2021, 2022 and 2023).

That establishes source semantics and anchor consistency, but not complete transport closure. The official CSV bytes are not yet frozen/hash-pinned in EWD and the complete annual World series has not yet been compared in repository automation.

Because HDI is a **central observation proxy**, this remains the highest-priority open provenance item.

## UN World Population Prospects 2024

Official portal:

`https://population.un.org/wpp/`

Official dataset page:

`https://www.un.org/development/desa/pd/content/World-Population-Prospects-2024`

Official bulk file identified for the medium variant:

`https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20(Standard)/CSV_FILES/WPP2024_Demographic_Indicators_Medium.csv.gz`

UN DESA describes WPP 2024 as the official estimates/projections source, with estimates from 1950 to the present and projections to 2100, and explicitly recommends CSV bulk download for advanced users.

This matches the EWD semantic boundary: estimate series through 2023, medium projection from 2024 onward. Full primary-file row equality remains open.

## Energy Institute Statistical Review 2026

Official download page:

`https://www.energyinst.org/statistical-review/resources-and-data-downloads`

The 2026 page exposes the data workbook and a consolidated narrow-format CSV, plus methodology and definitions. It also states that historical values can be revised between annual editions.

EWD currently uses a pinned mirror transport. The next closure step is not to change the model; it is to compare the official 2026 source directly with the seven Total World base variables already used by the existing ingestion.

## Global Carbon Project 2025v15

Primary Zenodo record:

`https://zenodo.org/records/17417124`

Primary dataset version:

`2025v15`

Exact primary file:

`GCB2025v15_MtCO2_flat.csv`

Primary-record MD5:

`3008e30d913af5926a83d0d0775fb72e`

The primary record therefore reaches L3: exact artifact identity and checksum metadata are known. EWD still needs a complete direct reconstruction/comparison for all six retained categories and all years 1990-2024 before this source can be declared L4/PASS.

The Global Carbon Budget 2025 paper and official data hub remain consistent with the diagnostic boundary: coal, oil and gas are distinguished from cement, flaring and other fossil-emission categories.

## World3-03 line-ending provenance

This documentation issue is already closed:

- upstream/original CRLF SHA-256: `42b22c734a71ee03abc31d80872234fbcd93d3d4fb9a277f606c6d677846731d`;
- repository-normalized LF SHA-256: `252e0c7eebff23d3c44344b6801cf3c40aec82d25b356ea8cce16a052249ac4d`.

The difference is line-ending normalization only; no equation or numerical parameter differs.

## Decision

R-FDC-6 remains **OPEN**.

No evidence found in this pass justifies changing the current HDI values, WPP benchmark semantics, Energy Institute processed boundary, GCP target boundary, or any central World3 mechanism.

The next safe action is a dedicated byte/value closure for UNDP first, then WPP, with EI and GCP following. Until those comparisons exist, the current adapters/transports remain in place and their warnings remain explicit.
