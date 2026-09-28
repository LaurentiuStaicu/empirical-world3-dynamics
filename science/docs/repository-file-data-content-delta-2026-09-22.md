# Post-Recovery Delta Audit — 2026-09-22

Baseline before repair: `795a6b8e42e2a19497f686a89e7c3a6056e6930c`  
Repair merge commit: `dd12af9989b36ad0f77fb0a50f47e0cf8f337cba`

## Scope

This document does not rewrite the 2026-09-21 repository-wide audit. That earlier audit remains the historical record of the state in which five diagnostic components were blocked.

This delta records only what changed after the approved R-FDC-1 recovery.

## Verification

Post-merge `main` passed both independent gates:

- Scientific reproducibility run #98: **SUCCESS**
- Diagnostic execution recovery run #3: **SUCCESS**

The diagnostic workflow also passed:

`git diff --exit-code -- data/scenarios`

Therefore the committed retained central references were not modified by the repair.

## Resolved blockers

| Component | Before | After | Evidence |
|---|---|---|---|
| UNIDO MVA diagnostic | BLOCKER | PASS | Current frozen observation contract imports; executes; remains diagnostic-only |
| UNIDO IIP diagnostic | BLOCKER | PASS | Current frozen observation contract imports; executes; remains diagnostic-only |
| Global climate-food diagnostic | BLOCKER | PASS | Executes; decision remains outside central BAU Hybrid |
| Regional agricultural-stress diagnostic | BLOCKER | PASS | Executes; `accepted=false` remains unchanged |
| Technology-minerals diagnostic | BLOCKER | PASS | Uses current generated Joint trajectories; remains risk registry / not central calibration |

For the four observation-import repairs, the current `world3_empirical.observations` contract was compared with the pre-reset observation contract and preserves the same indicator definitions, normalizations and source semantics.

For technology minerals, the Joint builder block generating `industry_total.csv` and `resources_remaining_pct.csv` is textually identical before and after the scientific-core reset. The repair changed only where the diagnostic reads those generated trajectories.

## Current repository audit state

The current tree contains 165 files.

| Status | Count |
|---|---:|
| PASS | 107 |
| WARNING | 42 |
| BLOCKER | 0 |
| NOT_SCIENTIFICALLY_MATERIAL | 16 |

The five files added after the original 160-file snapshot are audit/recovery documentation plus the path-scoped diagnostic workflow; all five are PASS for their declared roles.

## Scientific interpretation

R-FDC-1 repaired execution, not scientific claims.

The following remain unchanged:

- World3-03 structural equations and stock-flow structure;
- 128-candidate design;
- selection cutoff 2018;
- observation bridges;
- production refit;
- medoid selection;
- retained central outputs;
- diagnostic promotion decisions.

No previously rejected or diagnostic-only mechanism became central.

## Subsequent closure status

The recovery sequence continued after this historical R-FDC-1 delta:

| Gate | Status | Closure |
|---|---|---|
| R-FDC-2 — empirical registry completeness | CLOSED | PR #23; active observation/benchmark contract and registry completeness gate |
| R-FDC-3 — input-manifest scope semantics | CLOSED | PR #24; repository-wide retained-input inventory semantics separated from the central-baseline freeze date |
| R-FDC-4 — public execution routing | CLOSED | PR #25; official World3-03 is the unambiguous public EWD route and Pyworld3 is explicitly legacy/reference |
| R-FDC-5 — version/provenance identity | CLOSED | PR #26; preserve Joint artifact v0.1, link it to EWD v0.1.0, enforce version semantics, and document CRLF/LF World3-03 hash provenance |

These later repairs are traceability/routing changes. They do not change observation values, model equations, candidate design, fitted parameters, bridge weights, medoid selection or the scientific interpretation of the retained central trajectory.

## Closure after R-FDC-5

**R-FDC-6 — primary-source provenance closure — CLOSED**

The machine-readable closure matrix and human-readable audit separate source authority, semantic reconciliation, exact primary-artifact identity and complete primary-file lineage:

- `science/data/provenance/primary_source_audit_2026-09-22.json`
- `science/docs/primary-source-provenance-audit-2026-09-22.md`

FAOSTAT, UNDP HDI, UN WPP, Energy Institute and Global Carbon Project are all L4/PASS at their declared EWD roles. The closure required no change to observation values, benchmark definitions, bridge weights, World3-03 equations/parameters, candidate selection, production refit, medoid or retained trajectories.

**R-FDC-7 — diagnostic raw-data reproducibility policy — CLOSED_POLICY.**

The repository now distinguishes retained raw, pinned remote, verified transport and processed-snapshot-only diagnostics. External diagnostic materialization is isolated from central Joint reproduction, and offline CI rejects stronger reproducibility claims than the evidence supports.

**R-FDC-8 — rejected experimental mechanisms — CLOSED_GOVERNANCE.**

The executable resource-fraction -> fossil-EROI experiment remains rejected and sensitivity-only. CI now enforces the forbidden-coupling registry, absence from central execution routes, and the rule that executability or a single backtest PASS is not promotion evidence. E1-E10 remains explicitly undefined rather than being silently invented.

**R-FDC-9 — repository-wide post-recovery audit — CLOSED_AUDIT**, contingent on final CI.

The final audit reconciles all 47 historical non-PASS entries, requires exact tracked-file coverage, preserves six explicit remaining warnings and six governed limitations, and requires zero unresolved or unexplained BLOCKER findings.

**Recovery sequence status: R-FDC-1 through R-FDC-9 complete at repository-integrity/governance level once the final Scientific reproducibility run is green.**
