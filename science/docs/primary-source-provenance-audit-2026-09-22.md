# Primary-source provenance closure matrix — 2026-09-22

Status: **R-FDC-6 CLOSED**. This is provenance-only work. No observation value, model equation, mapping, fitted parameter, candidate-selection rule, retained trajectory or scientific claim is changed here.

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
| UN WPP 2024 | population benchmark/guardrail | L4 | PASS | exact 151-year equality reproduced through the official UN single-age files and the documented OWID aggregation route |
| Energy Institute 2026 | energy diagnostic/candidate evidence | L4 | PASS | archived official-download snapshot and pinned mirror are fully identified; all 427 EWD-used Total World observations match exactly |
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

The first direct cross-check used the official `WPP2024_Demographic_Indicators_Medium.csv.gz` and its `TPopulation1July` aggregate. It covered all **151 years, 1950-2100**, with no missing years, but differed from the retained adapter by at most **12 persons**.

That difference is now explained rather than treated as a data defect. The retained adapter follows the OWID WPP pipeline, whose source metadata points to two different official UN files:

- estimates 1950-2023: `WPP2024_PopulationBySingleAgeSex_Medium_1950-2023.csv.gz`
  - size: **62,082,217 bytes**
  - MD5: `f5e699a447a166783588c8919f18cc8b`
  - SHA-256: `f84c75789ccbd385122ad19bac70026d6306878442afbaa24e8e50a23b4bee2f`
- medium projections 2024-2100: `WPP2024_PopulationBySingleAgeSex_Medium_2024-2100.csv.gz`
  - size: **66,954,143 bytes**
  - MD5: `bd6c57bd4abfaa90d4a67c3505b48e4c`
  - SHA-256: `31804a296b663716236cd26c46415271cc9386fb3b2be56aff6467ad32283dc8`

The OWID ETL route was audited at commit `157bea70af7cb58518d7464520dac57fddf091ed`. Its garden processing multiplies each single-age `PopTotal` row from thousands to persons, casts each row to integer, then sums all ages. Reproducing that route from the two official UN files gives **exact equality for all 151 World values, 1950-2100**, with maximum absolute difference **0 persons**.

The earlier <=12-person difference is therefore a representation difference between two official UN-derived routes: direct `TPopulation1July` aggregate versus sum of integerized single-age rows. It is not a provenance defect in the EWD adapter.

WPP therefore reaches **L4 / PASS** for its current benchmark/guardrail role.

## Energy Institute Statistical Review 2026

Official download page:

`https://www.energyinst.org/statistical-review/resources-and-data-downloads`

The 2026 page exposes the data workbook and a consolidated narrow-format CSV, plus methodology and definitions. It also states that historical values can be revised between annual editions.

The Energy Institute page currently exposes the 2026 consolidated narrow-format CSV. Direct automation against the EI page is blocked by Cloudflare, so the closure uses OWID's public content-addressed snapshot of the CSV that OWID documents as manually downloaded from the official EI page.

Archived official-download identity:

- OWID ETL snapshot metadata: `snapshots/energy_institute/2026-06-30/statistical_review_of_world_energy.csv.dvc`
- OWID ETL audited commit: `157bea70af7cb58518d7464520dac57fddf091ed`
- publication date: **2026-06-30**
- OWID access date: **2026-07-02**
- size: **21,056,126 bytes**
- MD5: `f25ee66736be97cfab483d26446a71c2`
- SHA-256: `d197762cfb89012bc4d16ea0ef06766b24cffb37aa47491d391ab8a6d894d1a8`

Pinned EWD mirror identity:

- repository: `shanewhi/world-energy-data`
- commit: `9fc01fc0ae5aea3955968f920e5cd1394fe5ad34`
- file: `Statistical Review of World Energy Narrow format.csv`
- size: **21,056,006 bytes**
- MD5: `d52c342b5020235490e6c519bbf48979`
- SHA-256: `c19b4922cb08316b45d7024233e8cd9d35e14429ee8cf65ab767e647cefc1f95`

The two full files are **not byte-identical** and are not globally CSV-semantic-identical. The first detected difference is an unused row for `Other CIS`, 1965, `co2_combust_per_tes_ej`: the archived official file contains `#DIV/0!`, while the mirror contains `0`.

For the declared EWD role, however, the comparison is exact. EWD uses seven `Total World` variables (`tes_ej`, oil, gas, coal, nuclear, hydro and renewables TES) over 1965-2025: **427 year-variable observations**. All 427 are present in both files and match exactly; maximum absolute difference is **0**.

Therefore the mirror is not claimed to be a byte-for-byte copy of the full EI CSV. It is certified as scientifically faithful for the exact EWD extraction boundary. Energy Institute reaches **L4 / PASS** for that declared role.

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

R-FDC-6 is **CLOSED**.

All required provenance targets are now L4/PASS at their declared EWD roles:

- FAOSTAT — official archive size/hash verified in clean reproduction;
- UNDP HDI — exact 34-year World equality with the official UNDP CSV;
- UN WPP 2024 — exact 151-year equality through the official UN single-age files and documented OWID aggregation route;
- Energy Institute 2026 — exact equality for all 427 `Total World` observations used by EWD against an archived official-download snapshot;
- GCP fossil CO2 2025v15 — complete six-category, 35-year primary-file verification under the declared one-decimal rounding boundary.

No observation value, benchmark definition, model equation, candidate rule, bridge weight, fitted parameter or retained trajectory was changed to obtain this closure.

The next repository audit gate is **R-FDC-7 — diagnostic raw-data reproducibility policy**.
