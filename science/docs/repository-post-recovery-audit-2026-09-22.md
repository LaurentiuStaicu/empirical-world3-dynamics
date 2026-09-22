# Repository-wide post-recovery audit — 2026-09-22

Status: **R-FDC-9 CLOSED_AUDIT**, contingent on the automated R-FDC-9 validator and retained Scientific reproducibility workflow passing on the final PR head.

Historical baseline:

- branch: `main`
- commit: `795a6b8e42e2a19497f686a89e7c3a6056e6930c`
- files audited: **160**
- original status counts: **97 PASS, 42 WARNING, 5 BLOCKER, 16 NOT_SCIENTIFICALLY_MATERIAL**

Machine-readable post-recovery matrix:

`science/data/audits/repository_post_recovery_audit_2026-09-22.json`

Automated guard:

`scripts/check_repository_post_recovery_audit.py`

## Completion criterion

R-FDC-9 does **not** require every scientific limitation to disappear.

The recovery sequence is complete when:

1. all five original BLOCKER findings are resolved;
2. every original WARNING/BLOCKER entry has an explicit post-recovery disposition;
3. every current tracked file is covered by either the historical inventory or an explicit new-file classification;
4. no unexplained BLOCKER remains;
5. remaining warnings are explicit, non-central and scientifically honest;
6. retained central scientific reproduction remains unchanged and green.

## Historical non-PASS reconciliation

The original audit contained **47 non-PASS entries**.

Post-recovery disposition:

| Disposition | Count | Meaning |
|---|---:|---|
| RESOLVED_PASS | 35 | The original defect/ambiguity has been repaired or machine-governed for the file's declared role. |
| GOVERNED_LIMITATION | 6 | The underlying limitation remains real, but scope and permitted claims are explicit and enforced. |
| REMAINING_WARNING | 6 | A real limitation remains open and is retained as a warning rather than cosmetically converted to PASS. |
| unresolved/unexplained BLOCKER | **0** | No historical blocker remains open. |

## Five original BLOCKER findings

All five R-FDC-1 execution blockers remain resolved:

- UNIDO MVA diagnostic;
- UNIDO IIP diagnostic;
- global climate-food diagnostic;
- regional agricultural-stress diagnostic;
- technology-minerals diagnostic.

The path-scoped **Diagnostic execution recovery** workflow continues to rebuild their prerequisites, execute all five diagnostics, and require:

`git diff --exit-code -- data/scenarios`

Therefore diagnostic recovery cannot silently mutate the retained central reference files.

## Closed warning families

The post-recovery audit confirms closure of the major warning families:

- **R-FDC-2:** active empirical registry completeness and registry-contract validation;
- **R-FDC-3:** scientific input-manifest scope/vintage semantics;
- **R-FDC-4:** public World3-03 routing with explicit legacy/reference Pyworld3 surfaces;
- **R-FDC-5:** EWD v0.1.0 versus Joint artifact v0.1 semantics and World3-03 CRLF/LF provenance;
- **R-FDC-6:** L4 primary-source provenance for FAOSTAT, UNDP HDI, UN WPP, Energy Institute and GCP at their declared EWD roles;
- **R-FDC-7:** diagnostic raw-data policy, pinned remote materialization, and explicit processed-snapshot-only boundaries;
- **R-FDC-8:** rejected resource-fraction → fossil-EROI coupling governance.

## Remaining warnings

Six historical warnings remain intentionally open.

### EIA STEO forecast transcription

`science/data/forecasts/eia-steo-2026-09-11.json`

The values were manually transcribed and the original release bytes were not archived. The artifact remains limited diagnostic/prospective evidence.

### Empirical-model-input World Bank food proxy

`science/data/processed/empirical_model_inputs_2026-08-28.csv`

The file still contains the derived proxy based on anomalous `AG.PRD.FOOD.XD`. The active central food observation is the frozen FAOSTAT series, not this proxy.

### Technology-mineral long history

`science/data/processed/technology_mineral_production_2026-09-08.csv`

The 1900-2023 history remains secondary OWID harmonization of USGS/BGS. The 2024-2025 endpoints are primary USGS MCS 2026. This is diagnostic material and is not a direct observation of the latent aggregate World3 resource stock.

### UNIDO National Accounts metadata conflict

`science/data/processed/unido_national_accounts_world_2026-09-07.csv`

The source-faithful portal conflict between the constant-2020-USD label and `base_year=2015` metadata remains unresolved and explicit.

### World Bank source snapshot anomaly

`science/data/processed/world_bank_global_snapshot_2026-08-28.csv`

The anomalous food-index values remain in the source-faithful snapshot. They remain excluded from central food calibration.

### Historical mineral transport

`science/data/raw/minerals/2026-09-08/owid_global_mine_production.csv`

This remains a secondary OWID harmonization. It is retained as diagnostic evidence rather than promoted to primary-source equivalence.

None of these six warnings changes the active central observation contract, World3-03 equations, Joint candidate selection, bridge weights, production refit, medoid or retained scenario trajectory.

## Governed limitations

Six additional historical warnings are now better described as **governed limitations** rather than unresolved defects:

- GISTEMP historical raw snapshot — processed-snapshot-only policy;
- regional cereal/climate historical raw snapshots — processed-snapshot-only policy;
- GISTEMP ingestion route — deterministic but historical raw bytes unavailable;
- regional agricultural/climate ingestion route — deterministic but historical raw bytes unavailable;
- World Bank ingestion still derives the excluded food proxy, while the active observation contract prevents central use;
- the World3-03 comparison audit may display the excluded food proxy only with `excluded_data_quality` labeling.

These limits remain visible and must not be described as stronger reproducibility or evidence than they support.

## Two final robustness repairs

R-FDC-9 also removes two avoidable ambiguities without changing current scientific results:

1. `evaluate_eroi_resource_link.py` now reads `central_candidate_id` from the Joint manifest instead of hard-coding candidate 114. The current manifest still selects the same candidate.
2. `scripts/promotion_gate.py` is explicitly labelled as a narrow historical error-comparison helper, not the Real Model S1-S10 promotion contract and not standalone scientific promotion authority.

## Repository-wide coverage

After the three R-FDC-9 audit artifacts are added, the tracked repository contains **188 files**.

The validator requires exact set equality between:

- all 160 paths in the historical audit; and
- every explicitly classified file added since that baseline.

An unclassified new file therefore causes R-FDC-9 to fail rather than silently escaping the audit boundary.

## Scientific conclusion

The repository recovery sequence R-FDC-1 through R-FDC-9 is complete at the **repository-integrity, provenance, routing, reproducibility and governance** level when the final CI run passes.

This does **not** imply:

- that every scientific warning has disappeared;
- that every candidate mechanism is validated;
- that the retained scenario is a probabilistic forecast;
- that EROI, climate-water, minerals or AI have become central feedbacks;
- that a release-version increase is automatically required.

Any future scientific mechanism should begin from this recovered baseline and pass its own declared structural and prospective evidence gates rather than being folded into the recovery work.
