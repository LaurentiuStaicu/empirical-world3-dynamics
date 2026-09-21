# Repository File–Data–Content Audit — 2026-09-21

## Scope

This is a diagnostic audit of the complete file tree of `LaurentiuStaicu/empirical-world3-dynamics` at:

- branch: `main`
- baseline commit: `795a6b8e42e2a19497f686a89e7c3a6056e6930c`
- total files classified: **160**

No model equation, parameter, observation value, retained scientific result or central-model decision is changed by this audit.

The machine-readable inventory is:

`science/data/audits/repository_file_data_content_inventory_2026-09-21.json`

## Status summary

| Status | Files | Meaning |
|---|---:|---|
| PASS | 97 | Audited content is internally coherent for its declared role and no material problem was identified in this pass. |
| WARNING | 42 | File is usable for its declared role, but provenance, terminology, routing, reproducibility, metadata or scientific interpretation requires correction/closure. |
| BLOCKER | 5 | The component cannot currently execute or reproduce its declared diagnostic function. These blockers are outside the retained central Joint 2026 reproduction path. |
| NOT_SCIENTIFICALLY_MATERIAL | 16 | Presentation/governance/repository-support material that does not determine scientific results. |
| PENDING | 0 | First-pass classification is complete. |

A file-level PASS does **not** mean that the scientific hypothesis represented by the file has passed a promotion gate. For example, the retained direct-emissions experiment files can be PASS as faithful records while the experiment itself correctly remains `RETAIN AS DIAGNOSTIC`.

## Central baseline status

The retained central scientific path remains reproducible:

`World3-03 -> observations -> 128-candidate Joint 2026 procedure -> retained diagnostics/manifest`.

The earlier reproducibility repair was independently verified on a clean GitHub runner and did not modify the authoritative World3-03 structural model.

None of the five blockers identified below is imported by `scripts/reproduce_scientific_results.py` or required to reproduce the retained Joint 2026 artifacts.

## BLOCKER register

### FDC-B01 — UNIDO MVA diagnostic stale import

File:

`science/scripts/evaluate_unido_industry_proxy.py`

The script imports the deleted legacy module `build_bau2_e2026`.

Impact:

The retained UNIDO-MVA alternative-target audit cannot currently be rerun from `main`.

Central model impact:

None. UNIDO remains diagnostic/benchmark evidence.

Required later action:

Migrate only the observation contract import to the current `world3_empirical.observations` boundary and verify that regenerated diagnostic results remain scientifically equivalent. Do not change the central model as part of that repair.

### FDC-B02 — UNIDO IIP diagnostic stale import

File:

`science/scripts/evaluate_unido_iip_volume.py`

Same deleted `build_bau2_e2026` dependency.

Impact:

The public balanced-panel IIP alternative-target audit cannot currently be rerun.

Central model impact:

None.

### FDC-B03 — climate-food diagnostic stale import

File:

`science/scripts/evaluate_climate_food_link.py`

The script still imports `build_bau2_e2026`.

Impact:

The global temperature/food diagnostic is not executable in the current scientific-core checkout.

Central model impact:

None. Climate-food remains inactive and diagnostic.

### FDC-B04 — regional agricultural stress diagnostic stale import

File:

`science/scripts/evaluate_regional_agricultural_stress.py`

The script still imports `build_bau2_e2026`.

Impact:

The regional cereal/climate diagnostic cannot currently be rerun.

Central model impact:

None.

### FDC-B05 — technology-minerals diagnostic stale trajectory inputs

File:

`science/scripts/evaluate_technology_minerals.py`

The script expects:

- `data/scenarios/industry_total.csv`
- `data/scenarios/resources_remaining_pct.csv`

Those legacy trajectory files were removed by the scientific-core reset.

Impact:

The technology-mineral comparison cannot execute from current `main`.

Central model impact:

None. Mineral data remain an observed-flow/risk diagnostic and are not used to calibrate the latent World3 resource stock.

## High-priority WARNING register

### FDC-W01 — empirical registry is not complete with respect to the actual central measurement layer

`science/data/registry.csv` does not contain dedicated rows for three inputs used by `world3_empirical.observations`:

- primary FAOSTAT food-per-capita production index;
- UNDP HDI OWID adapter used as a central observed proxy;
- UN WPP 2024 OWID adapter used as a population benchmark/plausibility guardrail.

The World Bank CO2 row is also labelled `auxiliary_not_direct_calibration`, while its series participates in the retained pollution-pressure observation target.

The current registry validator checks schema, duplicate IDs and year ordering but does not test registry completeness against actual model inputs.

### FDC-W02 — scientific input manifest conflates central snapshot and repository-wide audit inputs

`scripts/generate_science_input_manifest.py` recursively hashes all retained `science/data/raw` and `science/data/processed` files while hard-coding:

`snapshot_date = 2026-08-30`.

Consequently, the manifest includes later UNIDO, minerals and climate diagnostic snapshots even though they were created after the declared snapshot date.

The hashes remain valuable and reproducible. The problem is semantic: this is no longer only a frozen **central-model** input snapshot.

### FDC-W03 — two executable World3 routes coexist without sufficiently strong routing labels

The retained scientific baseline uses:

- official World3-03 Vensim model;
- PySD adapter;
- official scenario 2 / BAU2.

However, the package also exposes a second route:

- vendored Pyworld3 1.1 / 1974 implementation;
- `model.py`;
- `scenarios.json`;
- `run_scenario()`;
- command-line entry point `world3-empirical`.

That route contains a `bau2_structural_proxy` explicitly documented as **not the exact World3-03 BAU2 parameterization**.

This does not contaminate Joint 2026, but a user invoking the package CLI can reasonably assume that the command executes the current EWD baseline when it actually executes the alternate legacy engine.

Related files include `calibration.py`, `run_baselines.py` and `compare_empirical.py`.

### FDC-W04 — version identity is inconsistent

Public/release identity:

`0.1.0`

but:

- `science/pyproject.toml`: `0.1`
- `science/uv.lock`: project version `0.1`
- retained Joint manifest: `0.1`

This is a metadata/traceability issue, not a scientific result discrepancy.

### FDC-W05 — World3-03 third-party hash statement requires reconciliation

`science/THIRD_PARTY_NOTICES.md` records the ingestion SHA-256:

`42b22c734a71ee03abc31d80872234fbcd93d3d4fb9a277f606c6d677846731d`

while the current scientific input manifest verifies:

`252e0c7eebff23d3c44344b6801cf3c40aec82d25b356ea8cce16a052249ac4d`.

The repository enforces LF line endings. Line-ending normalization is a plausible explanation, but this audit has not yet obtained the authoritative original bytes needed to prove the relationship. Until then the notice should not be treated as fully reconciled provenance.

### FDC-W06 — primary-source closure remains incomplete for central adapters

The central UNDP HDI input and the UN WPP benchmark are retained as OWID adapters.

The primary-source provenance audit has independently matched published anchors, but complete official source files have not yet been frozen/hash-pinned in the repository.

This issue is particularly material for HDI because it is a central observation proxy.

### FDC-W07 — several diagnostic raw snapshots are not retained

Examples:

- NASA GISTEMP processed provenance identifies a raw file/hash not present in current checkout;
- regional cereal/climate provenance identifies three raw source files/hashes not present in current checkout;
- eGRID source metadata intentionally records `raw_file_in_repository=false`.

Processed/derived evidence remains retained, and eGRID temporal/influence diagnostics are reproducible from retained cohorts. However, full raw-to-processed offline reproduction is not uniform across all diagnostic modules.

### FDC-W08 — rejected/unvalidated EROI coupling implementation remains in the source tree

`world3_empirical.energy_coupling` implements an explicit World3 resource-fraction -> fossil-EROI scenario link for structural sensitivity experiments.

The current structural contract lists `world3_resource_fraction_to_fossil_eroi` as a forbidden coupling for central promotion, and the earlier empirical link test did not justify promotion.

The code can remain as a historical/rejected diagnostic hypothesis, but its status must stay visibly distinct from an eligible EWD structural extension.

## Data-content findings

### World Bank

The snapshot construction is deterministic and source URLs are explicit.

The retained `AG.PRD.FOOD.XD` series contains the previously identified anomalous flat values and remains excluded from central food calibration.

The derived `food_per_capita_proxy_index` remains inside `empirical_model_inputs_2026-08-28.csv`, but the current central observation module uses the frozen FAOSTAT input instead.

### FAOSTAT

The central food input is the only large remote file fetched during clean reproduction. URL, expected size and SHA-256 are fixed and verified before use.

Primary-source provenance design is strong.

### UNDP / UN WPP

Adapters are hash-pinned and central execution is reproducible, but they remain secondary transports pending complete primary-source freeze.

### Energy Institute

The processed 1965-2025 series has explicit global fuel components, fossil/non-fossil shares and a retained component-reconciliation residual.

Ingestion rejects missing variables, duplicate year-variable cells, gaps, invalid shares and component disagreement above 0.1%.

Official EI authority and transport mirror are distinguished. Independent official-download byte equivalence remains a provenance-closure issue rather than a transformation error.

### GISTEMP

The processed global annual series has explicit 1880-2025 coverage and a clear 1951-1980 anomaly base.

The processed result is retained and hashed; the local raw snapshot itself is not retained.

### UNIDO

The official National Accounts and IIP raw inputs needed for the current diagnostic reconstructions are retained.

The public IIP reconstruction is transparently a 101-country balanced panel with 94.49% of available 2020 MVA weight and is not presented as UNIDO's official world aggregate.

The National Accounts provenance correctly preserves rather than silently resolves the portal conflict between the 'constant 2020 USD' label and the `base_year=2015` metadata field.

### Technology minerals

2024-2025 endpoints are tied to primary USGS MCS 2026 material with deterministic line-ending normalization/hashes.

The longer history uses an OWID harmonization of USGS/BGS and therefore remains secondary-source evidence.

Different commodities are not summed as tonnes and mine production is not treated as direct observation of the World3 aggregate resource stock.

### eGRID / EIA

EPA eGRID 2021, 2022 and 2023 are correctly treated as release-lagged datasets. The retained temporal comparisons are explicitly hindcasts, not real-time prospective tests.

The 2023 source metadata identifies EPA Rev.2 dated 2025-06-12.

The retained EIA 2014-2024 coal and natural-gas average heat-rate series agrees with EIA Electric Power Annual Table 8.1.

eGRID cohort selection, accounting-boundary reconciliation, temporal stability and influence analysis all preserve provenance and do not promote a central mechanism.

### Vendored Pyworld3

The vendored engine identifies itself as Pyworld3 1.1.

Comparison with upstream tag `v1.1` shows:

- `__init__.py` is byte-identical;
- all other vendored code/table files are content-identical after CRLF -> LF normalization;
- the CeCILL license is byte-identical.

Thus the vendored content is source-faithful. Its issue in EWD is **routing/status**, not code provenance.

## Retained-result integrity

The central retained result set remains governed by clean reproduction and semantic comparison of:

- `backtest_2019_latest.csv`
- `backtest_multi_origin.csv`
- `fit_diagnostics.csv`
- `parameter_identifiability.csv`
- `candidate_ranking.csv`
- `validation_candidate_ranking.csv`
- `bridge_validation.csv`
- `lookup_extrapolation_audit.csv`
- `bau_hybrid_2026_manifest.json`

The direct-emissions diagnostic artifacts are also regenerated/checked separately by CI.

## Interpretation

The repository is not in a state where "everything outside the central model is broken." Most scientific/support files pass their declared role.

The dominant pattern is instead:

1. the **central baseline is reproducible**;
2. several **diagnostic branches lost dependencies during the scientific-core reset**;
3. some **provenance/inventory metadata did not evolve with the new central architecture**;
4. the repository still contains a **legacy Pyworld3 execution route** that is scientifically distinct from the retained World3-03 baseline;
5. primary-source provenance closure is incomplete for several adapters/transport paths.

## Development implication

No new mechanism should be added as a response to this audit.

The next repair stage, if explicitly approved, should be a **non-scientific-integrity repair** with narrowly separated changes:

1. repair the five broken diagnostic execution chains without changing their scientific logic;
2. make registry/input-manifest scopes reflect actual usage;
3. make official World3-03 the unambiguous central/public execution route and label or quarantine the alternate Pyworld3 route;
4. reconcile version/provenance metadata;
5. continue primary-source closure.

Each repair should demonstrate that central retained scientific artifacts remain unchanged.
