# Repository Recovery Plan Derived from File–Data–Content Audit

Date: 2026-09-21  
Status: diagnostic proposal only  
No repairs are implemented by this document.

## Governing rule

Every repair must preserve the retained central World3-03 / Joint 2026 scientific results unless the repair is explicitly approved as a scientific change in a later stage.

Repairs are separated by concern so that a provenance/metadata cleanup cannot silently change model behavior.

## Repair Gate R-FDC-1 — diagnostic execution recovery

Purpose:

Close the five BLOCKER components created by the scientific-core reset, without changing their scientific logic.

### R-FDC-1A — observation-contract imports

Affected files:

- `science/scripts/evaluate_unido_industry_proxy.py`
- `science/scripts/evaluate_unido_iip_volume.py`
- `science/scripts/evaluate_climate_food_link.py`
- `science/scripts/evaluate_regional_agricultural_stress.py`

Current stale dependency:

`build_bau2_e2026`

Current equivalent contract:

`world3_empirical.observations`

Minimal justified substitution:

- `Indicator`, where required, must come from `world3_empirical.observations`;
- `build_indicators` must come from `world3_empirical.observations`;
- no objective function, parameter range, temporal split, bridge, threshold or candidate-selection rule is changed.

Verification required before merge:

1. central clean reproduction remains PASS;
2. each repaired script imports and executes from a clean environment;
3. its manifest continues to state `central_projection_changed: false` or equivalent;
4. no repaired diagnostic writes into retained `data/scenarios` central references;
5. any changed diagnostic result must be explained by an independently identified dependency/version difference rather than silently accepted.

### R-FDC-1B — technology-minerals trajectory source

Affected file:

`science/scripts/evaluate_technology_minerals.py`

Stale inputs:

- `data/scenarios/industry_total.csv`
- `data/scenarios/resources_remaining_pct.csv`

These files were presentation copies removed by the core reset.

The current Joint builder generates the same named diagnostic trajectories under:

`science/outputs/joint_hybrid_2026/`

Minimal justified repair:

Use the generated current Joint output directory as the source of:

- `industry_total.csv`;
- `resources_remaining_pct.csv`.

Do not reconstruct these quantities independently and do not substitute a different resource definition.

Prerequisite:

The Joint 2026 build must run before the mineral diagnostic.

Verification:

- central candidate and Joint manifest must be the same as the retained baseline;
- the mineral script must remain a measurement/risk diagnostic;
- mine-production flows must not be mapped directly onto the latent aggregate World3 resource stock.

## Repair Gate R-FDC-2 — empirical registry completeness

Purpose:

Make `science/data/registry.csv` describe the inputs that the current central observation layer actually consumes.

Minimum additions/changes:

- add the frozen primary FAOSTAT World/Food gross-per-capita production index used by `observations.py`;
- add the UNDP HDI adapter as a central empirical proxy, clearly labelled as secondary transport and as a proxy for World3 HWI;
- add the UN WPP adapter as benchmark/plausibility-guardrail evidence rather than a fitted central target;
- revise the World Bank CO2 entry so its role as an annual pollution-pressure observation target/bridge is explicit.

Also extend registry validation so completeness can be checked against the declared central observation contract.

Non-change requirement:

No observed value, bridge weight or model target changes in this gate.

### Exact central observation/benchmark reconciliation

The current `world3_empirical.observations` contract can be reconciled to the registry as follows:

| EWD indicator | Current observation source | Actual role | Registry state |
|---|---|---|---|
| population | World Bank WDI `SP.POP.TOTL` | fitted empirical target | present |
| industry_per_capita | World Bank WDI `NV.IND.TOTL.KD / SP.POP.TOTL` | fitted empirical proxy | present through the industry-value-added row |
| food_per_capita | FAOSTAT World / Food / Gross per capita Production Index | fitted empirical target | **missing** |
| pollution_pressure | World Bank/EDGAR `EN.GHG.CO2.MT.CE.AR5`, normalized 1990=100 | fitted annual flow observation bridge | present, but current status understates use |
| human_welfare | UNDP HDR 2025 World HDI | fitted empirical proxy for World3 HWI | **missing** |
| population benchmark | UN WPP 2024 World total population, estimate then medium projection | benchmark/plausibility guardrail only | **missing** |

The following retained sources remain diagnostics/supporting evidence and should **not** be promoted in the registry simply because they exist:

- Energy Institute primary energy;
- Aramendia fossil EROI;
- GISTEMP;
- regional cereal/climate panel;
- technology minerals;
- UNIDO MVA/IIP alternatives.

Registry completeness validation should therefore compare the registry against a small explicit declaration of the active observation/benchmark contract, not against every file in `science/data`.

## Repair Gate R-FDC-3 — input-manifest scope

Current problem:

`input_manifest.json` is reproducible but semantically mixes:

- central reproduction inputs;
- later diagnostic raw/processed datasets;
- one hard-coded snapshot date.

Preferred architecture:

1. preserve a narrowly defined **central reproducibility manifest** for direct/transitive Joint 2026 inputs;
2. maintain separate diagnostic/evidence manifests, or a repository-wide evidence inventory with per-dataset vintage dates;
3. avoid one global snapshot date for files acquired on different dates.

At minimum, the manifest must state its actual scope accurately.

Do not change input bytes as part of this gate.

## Repair Gate R-FDC-4 — unambiguous execution routing

Current condition:

EWD exposes both:

- official World3-03 / PySD — current retained structural baseline;
- Pyworld3 1.1 / 1974 implementation — alternate legacy/reference engine.

The public CLI currently routes to the alternate engine.

Required design decision before implementation:

Either:

A. make official World3-03 the default/public EWD execution route and expose Pyworld3 only under an explicit legacy/reference name;

or

B. retire the generic CLI from the scientific-core package and require explicit engine-specific scripts.

The following must not remain ambiguous:

- `run_scenario`;
- `calibration.py`;
- `scenarios.json`;
- `world3-empirical` CLI;
- `run_baselines.py`;
- `compare_empirical.py`.

Backward compatibility is a software concern, but it must not override scientific identity.

## Repair Gate R-FDC-5 — metadata/version consistency

Reconcile:

- public release `0.1.0`;
- package `__version__ = 0.1.0`;
- `CITATION.cff = 0.1.0`;
- `science/pyproject.toml = 0.1`;
- `uv.lock = 0.1`;
- Joint retained manifest `version = 0.1`.

Before changing the Joint manifest, decide whether its field denotes:

- repository/software semantic version; or
- scientific model/schema version.

Do not silently conflate those two concepts.

Closure decision (2026-09-22): the retained Joint manifest `version` denotes the
scientific-artifact version and remains `0.1`. The EWD software/repository
release is recorded separately as `ewd_release_version = 0.1.0`. Automated
version-identity validation checks both roles without requiring the two version
numbers to be identical.

## Repair Gate R-FDC-6 — provenance documentation precision

### World3-03 line endings

The apparent hash conflict is resolved:

- authoritative/original CRLF representation SHA-256:
  `42b22c734a71ee03abc31d80872234fbcd93d3d4fb9a277f606c6d677846731d`;
- repository LF-normalized representation SHA-256:
  `252e0c7eebff23d3c44344b6801cf3c40aec82d25b356ea8cce16a052249ac4d`.

Documentation should record both and state that only line endings differ.

### Primary-source closure

Continue the separate provenance audit for:

- UN WPP;
- UNDP HDI;
- Energy Institute;
- Global Carbon Budget.

Do not mix those provenance closures with execution-routing repairs.

## Repair Gate R-FDC-7 — diagnostic raw-data reproducibility policy

The project should choose and document one policy for non-central diagnostics:

- retain exact raw source snapshots when licensing/size permits; or
- retain authoritative URL, immutable identifier/version, byte hash and deterministic fetch instructions.

Processed-only evidence with an unavailable raw source should not be described as checkout-only reproducible.

Priority examples:

- NASA GISTEMP diagnostic;
- regional cereal/climate panel;
- eGRID raw workbooks.

## Repair Gate R-FDC-8 — rejected experimental mechanisms

`energy_coupling.py` contains an executable resource-fraction -> EROI hypothesis that is currently forbidden for central promotion.

Recommended handling:

- retain only as explicitly rejected/diagnostic experiment if scientifically useful;
- never expose it through the central run;
- require the System Dynamics E1-E10 plus S1-S10 gates before any future reconsideration;
- avoid language suggesting that mere executability makes it an eligible extension.

## Proposed order

1. R-FDC-1 diagnostic execution recovery.
2. R-FDC-2 registry completeness.
3. R-FDC-3 input-manifest scope.
4. R-FDC-4 execution routing.
5. R-FDC-5 metadata/version semantics.
6. R-FDC-6 primary provenance closure.
7. R-FDC-7 diagnostic raw-data policy.
8. R-FDC-8 rejected-mechanism governance.
9. rerun repository-wide audit and require zero unexplained BLOCKER findings.
10. only then reconsider new scientific mechanisms or milestone/version changes.

## Versioning implication

This audit does not decide the next version number.

A version change should follow the actual set of approved repairs and their compatibility/semantic effect. The repository should not choose a milestone number first and then fit the work to it.
