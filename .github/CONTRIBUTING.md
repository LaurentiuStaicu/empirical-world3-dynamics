# Contributing to Empirical World3 Dynamics (EWD)

EWD is an empirical **System Dynamics** model built on the World3-03 structural core. Contributions must preserve the distinction between the structural SD model and the empirical calibration/observation/validation layer.

## Before contributing

Read [README.md](../README.md), [STATUS.md](../STATUS.md), and the retained release notes under [releases/](../releases/).

## Scientific invariants

Unless a deliberate paradigm-level change is explicitly justified and reviewed:

- the World3-03 structural core is not silently redefined;
- stocks, flows, feedbacks, delays, nonlinear functions and numerical integration remain structurally distinct from the empirical layer;
- scenarios are not described as probabilistic forecasts;
- P10-P90 candidate envelopes are not described as calibrated probability/confidence intervals;
- weak parameter identification must remain visible;
- candidate extensions such as EROI, climate-water, minerals or AI remain inactive until their promotion gates pass.

## Data and calibration contributions

Document source, vintage, units, transformation, calibration/selection boundary and validation role. Distinguish model-selection data, production refits, holdouts and prospective checks.

## Verification

The repository's **Scientific reproducibility** GitHub Actions workflow must pass. Its core retained-artifact checks reproduce the frozen input manifest, central scientific artifacts and direct-emissions diagnostic.

## Release changes

Do not bump the public version as part of an unrelated contribution. A version identifies a frozen scientific-core artifact and does not imply forecast certainty or complete empirical identification.

## Security

Do not publish sensitive vulnerability details in a public issue.
