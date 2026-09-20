# Changelog

All notable public scientific-core releases of Empirical World3 Dynamics (EWD) are recorded here.

## Unreleased

### Repository governance

- added workflow-level concurrency so superseded scientific-reproducibility runs on the same branch/PR head are canceled instead of consuming duplicate compute;
- added EWD-specific contribution and support guidance;
- added structured reproducibility and scientific/model issue forms;
- added a pull-request checklist preserving the World3-03 structural core, scenario/non-probabilistic boundary and candidate-extension gates;
- deferred security-policy and code-of-conduct adoption until private reporting and enforcement routes are explicitly configured.

## 0.1.0 - 2026-09-18

Initial public scientific-core baseline.

### Included

- World3 system-dynamics reference engine and retained scenario definitions;
- observed source and processed data used by the scientific core;
- calibration, backtest and validation artifacts;
- BAU Hybrid 2026 retained manifests and diagnostics;
- provenance and scientific-input manifests;
- conservative extension contracts and promotion gates;
- reproducibility and validation scripts;
- standardized EWD project identity and release metadata.

### Scientific status

The retained hybrid model is an experimental scenario model, not a probabilistic forecast. The production trajectory is a post-validation refit rather than an independent holdout forecast. Pointwise P10-P90 ranges are structural sensitivity envelopes, not probability intervals. Several parameters remain weakly identified.

### Scope boundary

This release intentionally excludes the previous end-user product layer. Candidate external mechanisms remain outside the central model unless their declared scientific promotion gates are passed.
