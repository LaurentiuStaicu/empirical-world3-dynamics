# Scientific status

## Release status

Empirical World3 Dynamics (EWD) v0.1.0 is the initial public scientific-core baseline. The version identifies a frozen software/model snapshot. It does not mean that the model is a probabilistic forecast or that all parameters and mechanisms are empirically identified.

The repository is maintained as a research model core without an end-user interface.

## Canonical modeling paradigm

**Empirical World3 Dynamics (EWD) is an empirical System Dynamics model based on the World3-03 structural core, with a separate empirical calibration, observation, and validation layer.**

The World3-03 reference core is the System Dynamics structure: stocks, flows, auxiliaries, feedback loops, delays, nonlinear lookup functions, and numerical integration. Empirical observation bridges, parameter/candidate selection, production refits, medoid selection, fit diagnostics, sensitivity envelopes, and retrospective/prospective validation procedures are methodological layers applied to that structural model; they are not themselves evidence that the underlying feedback structure has been empirically validated.

This paradigm statement is canonical for the project. Recovery, calibration, provenance work, validation, or future extensions must not silently change the World3-03 stock-flow/feedback paradigm or conflate the empirical layer with the structural SD core. Any proposed paradigm-level change must be explicit, scientifically justified, documented in this file before integration, and accompanied by the relevant boundary, dimensional, structural, extreme-condition, sensitivity, and validation evidence.

## Current empirical/scenario boundary

The retained BAU Hybrid 2026 Joint manifest labels the central model an **experimental scenario model; not a probabilistic forecast**.

The structural base is official World3-03 scenario 2 (BAU2). Model selection is frozen through 2018, while the displayed production trajectory is a separate refit using observations available through 2025. The reported 2019-latest holdout belongs to the model-selection procedure; the displayed production trajectory is therefore not itself a holdout forecast.

The central trajectory is selected as the trajectory medoid of 12 admissible production candidates. The displayed P10-P90 range is a pointwise sensitivity envelope across those candidates, not a calibrated probability or confidence interval.

Historical fit varies substantially by indicator. Several structural parameters remain weakly identified, including resources, industrial output ratio, industrial capital lifetime, land yield, pollution generation, and pollution assimilation.

## Extension boundary

The Real Model extension contract keeps candidate mechanisms inactive by default and outside the central model. Candidate extensions require explicit S1-S10 promotion gates. The World3 reference core remains immutable under this contract, and candidate dynamics cannot be activated merely because an external signal is available.

EROI, climate-water, minerals, and AI are not coupled into the central retained run in this release.

## What v0.1.0 does not claim

- a probabilistic forecast of global outcomes;
- calibrated probabilities for scenario trajectories or turning points;
- complete parameter identifiability;
- empirical validation of every latent World3 state;
- central activation of candidate extension mechanisms;
- an end-user application or production decision system.

Future releases should update this file whenever the scientific or validation boundary changes.
