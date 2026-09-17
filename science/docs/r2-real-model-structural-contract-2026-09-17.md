# R2 — Real Model structural contract

Date: 17 September 2026

## Decision implemented

R2 uses the conservative G-R2-1 architecture. The already reproduced World3-03
model remains the immutable reference core. The authoritative Vensim file stays
in `science/vendor/world3_03/World3_03_Scenarios.mdl`; R2 does not replace its
topology and does not modify its equations. BAU, BAU2 and BAU Hybrid 2026 remain
the comparison baselines.

New mechanisms are represented by typed interfaces that are inactive and
non-central by default. An inactive interface must be an exact no-op over the
reference outputs. R2 deliberately contains no implicit path by which an R1
diagnostic can alter the central curves.

## Machine-readable structure

`science/configs/real_model_structure.json` is the R2 structural contract. It
declares:

- the immutable reference architecture and frozen comparison baselines;
- reference modules and representative stocks, flows and auxiliaries;
- units, dimensions and evidence roles;
- stock inflow/outflow accounting links;
- candidate extension interfaces and their maturity;
- the rejected coupling blacklist;
- promotion gates S1-S10;
- the single candidate selected for the next prospective experiment.

`science/src/world3_empirical/real_model_contract.py` validates the contract and
provides typed evidence signals and candidate interfaces. The runtime guard
rejects non-finite evidence, rejects the R1 coupling
`world3_resource_fraction_to_fossil_eroi`, prevents an active interface from
silently inventing dynamics, and requires explicit PASS status on every S1-S10
gate before `promotion_allowed` can ever become true.

## S1-S10 promotion gates

The gates are intentionally split between structural verification and
prospective predictive validation:

| Gate | Requirement | Class |
|---|---|---|
| S1 | Boundary adequacy | structural |
| S2 | Structure assessment | structural |
| S3 | Dimensional consistency | structural |
| S4 | Accounting / conservation | structural |
| S5 | Extreme-condition behavior | structural |
| S6 | Numerical robustness | structural |
| S7 | Temporal provenance; no future information | predictive |
| S8 | Prospective out-of-sample skill | predictive |
| S9 | Uncertainty and sensitivity robustness | predictive |
| S10 | Incremental value with no baseline regression | predictive |

Passing interface-level R2 tests is not equivalent to passing the predictive
gates of a candidate mechanism. No R2 candidate is promoted to the central
model by this stage.

## Candidate maturity audit

### Energy accounting → direct emissions

Selected for the prospective experiment only. R1 already has the strongest
boundary, units and conservation foundation here: fuel energy, gross/net
electricity and direct emissions are explicitly separated and tested. This is
not the rejected resource-fraction → EROI feedback. The prospective experiment
must use vintage-safe observed or externally forecast physical quantities and
must be compared against a predeclared baseline before any causal feedback can
be considered.

### Net energy / EROI

Retained as `sensitivity_only`. The R1 test of World3 resource fraction → fossil
EROI lost to persistence and remains explicitly forbidden. R2 does not reopen
that coupling.

### Technology minerals

Retained as a diagnostic interface. R1 has material-specific production and
risk evidence, but not yet a defensible stock-flow model that separately
represents material stocks, mining capacity, refining, recycling, geographic
concentration and development delays.

### Climate → food

Retained as a diagnostic candidate. Both the global-temperature and the first
regional annual-stress formulations failed their predeclared promotion rules.
A future attempt requires a materially better measurement design rather than
retuning the rejected formulations.

### Industry proxy

Retained as a benchmark. UNIDO evidence improves triangulation but did not
produce incremental predictive selector gain sufficient for central
replacement.

## Verification introduced in R2

`science/tests/test_r2_real_model_contract.py` checks:

- conservative boundary and immutable World3 source declaration;
- machine-readable stocks, flows, auxiliaries, units and evidence roles;
- closed stock-flow references and dimensional rate compatibility;
- all candidate interfaces inactive and non-central by default;
- exact no-op behavior under finite extreme values;
- rejection of NaN and infinities;
- hard rejection of the R1 resource→EROI coupling;
- prevention of silent dynamics when an interface is manually activated;
- the requirement that all S1-S10 gates pass before promotion is allowed;
- experiment-only status of the selected candidate;
- the non-equation-only sanitation policy of the existing World3 adapter.

These tests supplement, rather than replace, the existing World3 reproduction,
scientific regression suite, release-contract checks and Flatpak build.

## R2 exit rule

R2 is closed only after the implementation PR passes the complete repository CI,
is merged into `main`, and the post-merge `main` workflow passes scientific
reproduction, release validation and the Flatpak build. Until that happens,
this document describes the implemented contract rather than claiming closure.

## Resulting scientific status

R2 changes architecture and verification, not the central projection. BAU,
BAU2 and BAU Hybrid 2026 remain the comparison baselines. No energy, EROI,
mineral, AI-infrastructure, climate-food or industry diagnostic becomes a
central feedback in R2.
