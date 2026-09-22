# Rejected experimental mechanism governance — 2026-09-22

Status: **R-FDC-8 CLOSED_GOVERNANCE**

This gate governs executable scientific hypotheses that have been tested or retained for sensitivity/audit purposes but are **not accepted central EWD mechanisms**.

Machine-readable companion:

`science/data/audits/rejected_experimental_mechanisms_2026-09-22.json`

Automated guard:

`scripts/check_rejected_mechanism_governance.py`

## Governed mechanism

`world3_resource_fraction_to_fossil_eroi`

Implementation retained for auditability:

- `science/src/world3_empirical/energy_coupling.py`

Evaluation and structural-sensitivity routes:

- `science/scripts/evaluate_eroi_resource_link.py`
- `science/scripts/analyze_energy_coupling.py`

Disposition:

**REJECTED_FOR_CENTRAL_PROMOTION**

The experiment remains executable so its assumptions and structural effects can be inspected. Executability is not evidence that the hypothesized causal relationship is valid, identified, calibrated, or eligible for central promotion.

## Why it remains rejected

The retained evaluation asks whether World3 resource depletion predicts observed fossil EROI better than persistence over five-year multi-origin tests at three accounting boundaries: primary, final, and useful EROI.

The current retained result does not support the resource-fraction link over persistence across all three declared boundaries. The structural-sensitivity runner therefore already records:

- `production_decision = not_accepted_into_central_projection`;
- the link is not empirically calibrated;
- the central BAU Hybrid 2026 run must remain unchanged.

R-FDC-8 does not re-evaluate or relax that scientific decision. It makes the governance consequence machine-enforceable.

## Central-routing guard

The rejected coupling must remain absent from:

- public package exports and CLI routing;
- the official World3-03 runner;
- central calibration and scenario routing;
- the Joint 2026 builder;
- retained scientific reproduction;
- the central promotion-gate script.

The CI guard scans these explicit central execution paths and fails if they import or reference the rejected coupling implementation.

The existing Real Model contract also forbids this coupling in both code and `science/configs/real_model_structure.json`.

## Backtest rule

A future retrospective backtest result is **not sufficient for promotion**.

The EROI evaluator now records:

- `governance_disposition = rejected_for_central_promotion`;
- `backtest_is_sufficient_for_promotion = false`.

Even if that individual predictive screen were to pass after new data or methodology, the result would mean only that one screen passed. It would not automatically make the mechanism eligible for the Joint calibration stage.

## E1-E10 boundary

The historical audit note says that reconsideration would require a new **E1-E10/S1-S10** review.

The repository already defines S1-S10 in `science/configs/real_model_structure.json`.

It does **not** currently define a versioned E1-E10 framework.

R-FDC-8 therefore deliberately does not invent E1-E10 names, thresholds, or pass states. The machine-readable registry records E1-E10 as:

`UNDEFINED_IN_CURRENT_REPOSITORY`

Before any future reconsideration, an E1-E10 framework would first have to be explicitly specified, versioned, scientifically justified, reviewed, and committed. Only then could its results be evaluated.

This treatment is also consistent with established System Dynamics practice, where model evaluation is performed through explicit tests such as boundary adequacy, structure/parameter assessment, dimensional consistency, extreme-condition testing, integration-error testing, behavior reproduction, and sensitivity analysis rather than by treating executability as validation.

## Existing S1-S10 gates

S1-S10 remain necessary for any candidate extension:

- S1 boundary adequacy
- S2 structure assessment
- S3 dimensional consistency
- S4 accounting conservation
- S5 extreme conditions
- S6 numerical robustness
- S7 temporal provenance / no future information
- S8 prospective out-of-sample skill
- S9 uncertainty and sensitivity robustness
- S10 incremental value and no baseline regression

For this rejected coupling, all S1-S10 passing would be **necessary but not sufficient**. Reconsideration also requires newly defined E1-E10 criteria, new prospective evidence, and an explicit paradigm-level review before any central-model change.

## Non-change contract

R-FDC-8 changes governance wording and automated guardrails only.

It does not alter:

- the EROI coupling equations;
- the central World3-03 equations;
- any observation series;
- calibration candidates;
- bridge mappings or weights;
- the retained BAU Hybrid 2026 trajectory;
- the current scientific rejection result.

## Next gate

**R-FDC-9 — repository-wide post-recovery audit.**

That audit should rerun the file/data/content inventory after R-FDC-1 through R-FDC-8 and require zero unexplained BLOCKER findings before considering the recovery sequence complete.
