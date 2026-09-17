# Energy accounting → direct emissions — prospective recovery and gate audit

Date: 17 September 2026  
Branch: `science/energy-direct-emissions-prospective`  
Candidate: `energy_accounting_emissions`  
Final verdict: **RETAIN AS DIAGNOSTIC**

## Recovery audit

Before this work was materialized, `main` and `science/energy-direct-emissions-prospective` both pointed to `fdf23945384f05f2325014a822926ed6689fa736`. No experiment commit or PR existed. Numerical fragments discussed in conversation were therefore treated as non-authoritative and were recomputed from persisted data and code. This report, the frozen data snapshot, provenance, executable evaluator, annual prediction table, result JSON, tests, and CI reproduction check are the authoritative record.

No file under the World3-03 vendor model, BAU, BAU2, or BAU Hybrid 2026 central scenario outputs is changed by this experiment. The forbidden coupling `world3_resource_fraction_to_fossil_eroi` remains excluded.

## Scientific boundary contract

The candidate estimates **direct fossil CO2 associated with coal, oil, and natural gas energy**, not total greenhouse-gas emissions and not atmospheric concentration, temperature, lifecycle emissions, upstream methane, cement process emissions, flaring, or the World3 persistent-pollution stock.

Energy input is the Energy Institute (EI) Statistical Review global series. EI documents that fossil primary energy continues to be reported in net terms, with fuel-specific gross-to-net calorific adjustments. That makes the exajoule series compatible in heating-value basis with the IPCC Tier-1 factors used here, which are expressed on a net-calorific-value basis.

Observed target is the Global Carbon Budget (GCB) 2025 fuel breakdown: `Solid Fuel + Liquid Fuel + Gas Fuel`. The snapshot retains `Cement`, `Gas Flaring`, and `Other` as explicit columns so that exclusion from the target is auditable rather than implicit.

The accounting identity is:

`MtCO2 = Σ_fuel [ EJ_fuel × EF_fuel(kgCO2/TJ) / 1000 ]`

IPCC Table 2.2 defaults are 94,600 kg CO2/TJ NCV for other bituminous coal, 73,300 for crude oil, and 56,100 for natural gas. The candidate adds only one scalar correction estimated on the development period. There is no World3 state, stock, feedback, resource fraction, or EROI term in the equation.

The machine-readable contract is `science/configs/energy_direct_emissions_boundary.json`.

## Literature and data audit

The IPCC 2006 Guidelines, Volume 2, Chapter 2 specify CO2 factors in kg CO2/TJ on a net-calorific basis and state that the factors reflect fuel carbon content with an oxidation factor of 1. Table 2.2 also supplies lower and upper bounds; those bounds are used directly for the sensitivity corners rather than inventing an uncertainty band.

The EI Statistical Review provides the global energy series and states that the 2025 methodology change primarily changes treatment of non-combustible energy; fossil primary-energy consumption remains reported in net terms. EI also states that historical values are revised when better data or methods become available. That revision policy is scientifically material for S7.

The Global Carbon Budget 2025 paper reports final fossil CO2 data through 2024 and supplies emissions by fuel type. It separates coal, oil, natural gas, cement, flaring and other, allowing this experiment to retain a narrow three-fuel combustion target while keeping excluded process categories visible.

Primary references:

- IPCC 2006 Guidelines, Volume 2, Chapter 2: https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_2_Ch2_Stationary_Combustion.pdf
- Energy Institute Statistical Review downloads/methodology: https://www.energyinst.org/statistical-review/resources-and-data-downloads
- Energy Institute methodology: https://www.energyinst.org/__data/assets/pdf_file/0003/1658154/Methodology-2025.pdf
- Global Carbon Budget 2025 data hub: https://globalcarbonbudget.org/datahub/the-latest-gcb-data-2025/
- Friedlingstein et al., Global Carbon Budget 2025, ESSD: https://essd.copernicus.org/articles/18/3211/2026/

## Sources, provenance and vintage

EI input is the already-persisted `science/data/processed/energy_institute_global_2026.csv` with provenance in its adjacent JSON. Coverage is 1965–2025, Total World.

GCB target values are frozen in `science/data/experiments/gcb_direct_fossil_1990_2024.csv`, with provenance and SHA-256 in `gcb_direct_fossil_1990_2024.provenance.json`. The GCB 2025 paper provides final fuel-type data through 2024.

This creates a deliberate limitation: parameter estimation and evaluation windows are strictly separated, but both EI and GCB histories are **current revised vintages**. Archived release-as-of-origin datasets were not reconstructed here. The experiment is therefore pseudo-prospective / rolling-origin in information use, not a strict real-time vintage backtest.

## Predeclared temporal design and baselines

Development/calibration is 1990–2009, validation is 2010–2017, locked holdout is 2018–2024, and 2025 is prospective and deliberately unscored.

Three estimates are compared: raw IPCC accounting from EI fuel energy; calibrated accounting using one development-only scale; and a persistence-intensity baseline defined as prior-year observed direct-CO2 intensity multiplied by current-year fossil energy.

The project-level minimum skill criterion is 0.30 against the baseline. The central World3 baselines are not used as predictors here because this candidate is a fuel-accounting observation mechanism; World3-03, BAU, BAU2 and BAU Hybrid 2026 remain frozen system-level comparators and receive no new coupling.

## Results

Development-only scale: `0.937350649483`.

Validation 2010–2017 gives calibrated-candidate WMAPE `0.3699%`, persistence-intensity baseline `0.4820%`, and raw IPCC accounting `6.5886%`.

Locked holdout 2018–2024 gives calibrated-candidate WMAPE `0.3013%`, persistence-intensity baseline `0.3367%`, raw IPCC `6.7386%`, and candidate skill versus baseline `0.105041`.

The nominal calibrated candidate is slightly better than persistence on this holdout, but the gain is much smaller than the project-level 0.30 skill requirement. The raw default-factor calculation has a persistent positive bias of roughly 6–7%, showing why the one-parameter reconciliation is necessary.

### Sensitivity

All eight corners formed by the IPCC lower/upper CO2-factor ranges were evaluated. The scalar is refit using **development data only** for every corner. Holdout WMAPE ranges from `0.2888%` to `0.4061%`; skill versus baseline ranges from `-0.206268` to `0.142091`. The ranking reverses for some admissible factor combinations, so the incremental advantage is not robust.

### 2025 prospective output — deliberately unscored

No matching final GCB 2025 fuel-level target is available in the frozen target dataset. These are predictions, not validation results: raw IPCC accounting `38.892 GtCO2`, calibrated candidate `36.455 GtCO2`, and persistence-intensity baseline `36.610 GtCO2`. They must not be scored until a matching realized fuel-level observation is frozen.

## S1–S10 gate audit

| Gate | Status | Evidence |
|---|---|---|
| S1 boundary adequacy | PASS | Coal/oil/gas energy and CO2 categories are explicitly matched; excluded process categories remain visible. |
| S2 structure assessment | PASS | Accounting identity + one development-only scalar; no hidden dynamics or World3 feedback. |
| S3 dimensional consistency | PASS | EJ→TJ and kg/TJ→Mt conversion explicit and tested. |
| S4 accounting/conservation | PASS | Fuel contributions sum exactly to the candidate total. |
| S5 extreme conditions | PASS | Zero input gives zero; negative/non-finite inputs fail closed. |
| S6 numerical robustness | PASS | Closed-form deterministic calculations reproduce. |
| S7 temporal provenance / no future information | **FAIL** | Split is time-safe, but historical input values are current revised vintages, not archived release-as-of-origin vintages. |
| S8 prospective OOS skill | **FAIL** | Holdout skill `0.105041` is below the `0.30` project criterion. |
| S9 uncertainty/sensitivity robustness | **FAIL** | IPCC factor-range corners include negative skill; comparator ranking reverses. |
| S10 incremental value / no baseline regression | PASS | Nominal holdout WMAPE is lower than persistence and candidate remains inactive, so central baselines are untouched. |

Because S7, S8 and S9 fail, **central promotion is prohibited**.

## Software and reproducibility contract

`science/scripts/evaluate_direct_emissions_prospective.py` regenerates the JSON result and annual prediction CSV. `--check` semantically compares JSON and byte-compares the prediction CSV with committed artifacts. `science/tests/test_direct_emissions_prospective.py` covers units, boundaries, development-only calibration, baseline timing, unscored 2025 behavior, sensitivity, the forbidden EROI coupling, gate status, machine-readable boundary invariants, and artifact reproduction. CI invokes the `--check` path in addition to the full scientific reproduction, unit tests, release validation, and Flatpak build.

## Limitations remaining

The principal limitation is vintage authenticity: annual revisions in EI and GCB mean this is not a historical real-time forecast recreation. Fuel aggregation is also broad: the IPCC defaults represent reference fuel types, while EI coal and oil aggregates mix multiple grades/products; the scalar correction is descriptive reconciliation, not a new causal mechanism. The 2018–2024 holdout contains only seven annual observations, and the nominal advantage over persistence is small and sensitive to factor composition.

## Closure decision

**RETAIN AS DIAGNOSTIC.**

The accounting module is useful for boundary checks and for translating a physical fuel mix into an emissions diagnostic, but it does not satisfy all prospective promotion gates. It must remain outside the central World3 dynamics.

The next justified stage, **not started here**, is a strict release-as-of-origin confirmation: reconstruct archived EI/GCB vintages (or freeze the realized 2025 fuel-level GCB outcome when available), rerun the predeclared comparison without retuning the holdout contract, and only then reconsider S7–S9 and promotion.
