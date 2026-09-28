# Changelog

All notable public scientific-core releases of Empirical World3 Dynamics (EWD) are recorded here.

## Unreleased

### Scientific traceability

- closed R-FDC-9 repository-wide post-recovery audit: all 47 historical non-PASS entries are reconciled, every tracked file is covered, six non-central warnings remain explicit, and zero unresolved/unexplained BLOCKER findings remain;
- closed R-FDC-8 rejected experimental mechanism governance: the resource-fraction -> fossil-EROI experiment remains executable only for sensitivity/audit purposes, is CI-forbidden from central routes, and cannot become promotion-eligible from executability or a single backtest result;
- closed the R-FDC-7 diagnostic raw-data reproducibility policy with isolated diagnostic source materialization, offline policy validation, and explicit processed-snapshot-only warnings for historical raw sources that cannot currently be rematerialized exactly;
- closed R-FDC-6 primary-source provenance with a machine-readable L1-L4 evidence matrix and CI validation; FAOSTAT, UNDP HDI, UN WPP, Energy Institute and GCP now have L4/PASS lineage at their declared EWD roles, without changing retained scientific values;
- reconciled the v0.1.0 software/repository identity across package metadata, lockfile and runtime metadata; preserved the Joint scientific-artifact version as 0.1, linked it explicitly to EWD release 0.1.0 via a separate field, and added a CI regression gate to prevent future semantic/version drift;
- clarified World3-03 source provenance by recording both the original CRLF ingestion SHA-256 and the repository-normalized LF SHA-256, without changing equations or numerical parameters.

### Repository governance

- prepared a suite-consistent professional EWD landing-page preview with grayscale header, canonical scientific-status boundaries, responsive conceptual figure, reproducibility path, provenance routing and reader navigation; the public README remains unchanged pending visual review;
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
