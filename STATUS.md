# Scientific status

## Release status

Empirical World3 Dynamics (EWD) v0.1.0 is the initial public scientific-core baseline. The version identifies a frozen software/model snapshot. It does not mean that the model is a probabilistic forecast or that all parameters and mechanisms are empirically identified.

The repository is maintained as a research model core without an end-user interface.

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
