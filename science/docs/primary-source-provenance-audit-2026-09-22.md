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
| UNDP HDR 2025 HDI | central human-welfare proxy | L4 | PASS | none for current transport equivalence; official file hash/size and exact 34-year World equality are recorded |
| UN WPP 2024 | population benchmark/guardrail | L4 | WARNING | complete 151-year comparison exists, but the retained transport differs from the official bulk file by up to 12 persons; transport precision rule still needs explanation |
| Energy Institute 2026 | energy diagnostic/candidate evidence | L1 | WARNING | identify a stable official automated download path and compare it with the pinned mirror transport |
| GCP fossil CO2 2025v15 | direct-emissions diagnostic | L4 | PASS | none for current compact snapshot lineage; all six categories/35 years are primary-source verified within declared one-decimal rounding |

## UNDP HDR 2025

Official documentation:

`https://hdr.undp.org/data-center/documentation-and-downloads`

Official complete time-series endpoint:

`https://hdr.undp.org/sites/default/files/2025_HDR/HDR25_Composite_indices_complete_time_series.csv`

The official CSV was downloaded directly in the 2026-09-22 provenance probe.

Recorded primary-file identity:

- size: **2,001,263 bytes**
- SHA-256: `61ed82e5b66c88dfca8ff9fac775c63981ecab6a254862af97acacc41c143117`
- MD5: `4026e513775f3431488a2d77bc6b6a1d`

The official file contains 34 World HDI observations for 1990-2023. All 34 match the retained EWD adapter **exactly**: no missing years, no mismatches, maximum absolute difference 0.

For the current EWD role, UNDP HDI therefore reaches **L4 / PASS**. The conceptual limitation remains unchanged: HDI is a proxy for World3 HWI, not a direct observation of that model construct.

## UN World Population Prospects 2024

Official portal:

`https://population.un.org/wpp/`

Official dataset page:

`https://www.un.org/development/desa/pd/content/World-Population-Prospects-2024`

Official bulk file identified for the medium variant:

`https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20(Standard)/CSV_FILES/WPP2024_Demographic_Indicators_Medium.csv.gz`

UN DESA describes WPP 2024 as the official estimates/projections source, with estimates from 1950 to the present and projections to 2100, and explicitly recommends CSV bulk download for advanced users.

The official compressed bulk file was downloaded directly in the 2026-09-22 provenance probe.

Recorded primary-file identity:

- compressed size: **16,557,272 bytes**
- decompressed size: **40,819,701 bytes**
- SHA-256: `286ac36bb1415e2e1ade03acfef0a29f0e4c087e2f78e38c48f50c5df89082bc`
- MD5: `a33419c11b407086db7af94252c5a95d`

The comparison used the official `TPopulation1July` field and covered all **151 years, 1950-2100**, with no missing years in either source. The retained adapter is extremely close but not numerically identical to the official bulk file: maximum absolute difference **12 persons**; 28 years differ by more than 5 persons.

Because the comparison is complete but the exact secondary-transport precision rule has not yet been documented, WPP is now **L4 / WARNING**, not PASS. No benchmark value is changed merely to force equality.

## Energy Institute Statistical Review 2026

Official download page:

`https://www.energyinst.org/statistical-review/resources-and-data-downloads`

The 2026 page exposes the data workbook and a consolidated narrow-format CSV, plus methodology and definitions. It also states that historical values can be revised between annual editions.

EWD currently uses a pinned mirror transport. A GitHub Actions probe attempted direct automated retrieval from the official Energy Institute page on 2026-09-22 and received **HTTP 403 Forbidden**. Browser-visible authority and dataset availability are confirmed, but a stable machine-download path has not yet been established.

The next closure step is not to change the model; it is to identify a documented official download endpoint or access method, record the official bytes/hash, and compare the seven Total World base variables already used by the existing ingestion.

## Global Carbon Project 2025v15

Primary Zenodo record:

`https://zenodo.org/records/17417124`

Primary dataset version:

`2025v15`

Exact primary file:

`GCB2025v15_MtCO2_flat.csv`

Primary-record MD5:

`3008e30d913af5926a83d0d0775fb72e`

The exact primary file was downloaded directly from Zenodo in the 2026-09-22 provenance probe.

Recorded primary-file identity:

- size: **3,147,221 bytes**
- SHA-256: `20650c19b394d91b6b31cddff2fbc9508bcdbbed7c3f93660336f2f655f367ff`
- MD5: `3008e30d913af5926a83d0d0775fb72e` — exactly the checksum published by the primary Zenodo record.

All six retained categories (coal, oil, gas, cement, flaring and other) were compared for every year **1990-2024**. There are no missing years. The largest absolute difference is **0.049964 MtCO2/year**, below the 0.051 tolerance implied by the retained one-decimal snapshot.

GCP therefore reaches **L4 / PASS** for the current compact diagnostic lineage. The diagnostic boundary itself remains unchanged: coal + oil + gas form the direct-combustion target, while cement, flaring and other remain explicit but excluded.

## World3-03 line-ending provenance

This documentation issue is already closed:

- upstream/original CRLF SHA-256: `42b22c734a71ee03abc31d80872234fbcd93d3d4fb9a277f606c6d677846731d`;
- repository-normalized LF SHA-256: `252e0c7eebff23d3c44344b6801cf3c40aec82d25b356ea8cce16a052249ac4d`.

The difference is line-ending normalization only; no equation or numerical parameter differs.

## Decision

R-FDC-6 remains **OPEN**, but the open set has narrowed substantially.

Closed in this pass:

- FAOSTAT — L4/PASS;
- UNDP HDI — L4/PASS with exact 34-year World equality;
- GCP fossil CO2 2025v15 — L4/PASS with complete six-category comparison under the declared one-decimal rounding boundary.

Still open:

- UN WPP 2024 — L4/WARNING because all 151 years are compared but the retained transport differs by up to 12 persons and the exact precision/transport rule is not yet documented;
- Energy Institute 2026 — L1/WARNING because official browser-visible datasets are confirmed but automated primary-byte retrieval returned HTTP 403.

No result here justifies changing observation values, benchmark definitions, model equations or central World3 mechanisms. The next work should explain the WPP transport discrepancy and establish a stable official Energy Institute download path.
