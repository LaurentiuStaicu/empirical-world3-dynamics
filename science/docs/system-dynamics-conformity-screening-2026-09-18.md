# System Dynamics / Systems Thinking Conformity Screening

Date: 2026-09-18  
Scope: Empirical World3 Dynamics (EWD), retained World3-03 core and empirical overlay  
Status taxonomy: PASS / WARNING / BLOCKER

## Purpose

This gate does not require EWD to be changed merely to resemble a System Dynamics model. Its purpose is to verify that the retained structural core remains a coherent System Dynamics model and that empirical additions do not silently replace causal stock-flow reasoning with statistical fit.

The governing separation is:

**World3 structural core = System Dynamics**

**Empirical calibration, observation bridges, candidate selection, production refit, medoid selection, backtesting and diagnostics = empirical/statistical layer applied over the SD model**

A lower error metric, better historical fit or favorable backtest is not by itself evidence that a feedback structure is causally valid.

## Methodological basis

The gate follows the model-testing logic associated with Forrester/Senge and Sterman: purpose and boundary adequacy, structure assessment, dimensional consistency, parameter assessment, extreme-condition testing, integration-error testing, behavior reproduction and sensitivity analysis.

Reference modes are treated as behavior-over-time patterns used in problem articulation and model testing, rather than as ordinary pointwise fit targets.

The World3-03 reference model is treated as an SD model with interrelated population, capital, agriculture, non-renewable-resource and persistent-pollution sectors, connected by stocks, flows, delays, nonlinear relationships and feedback loops.

Useful public references:

- John Sterman, *Business Dynamics*, chapter 21 contents: https://mitmgmtfaculty.mit.edu/jsterman/business-dynamics/
- Ford et al., *A system dynamics glossary*: https://doi.org/10.1002/sdr.1641
- Vensim units checking: https://www.vensim.com/documentation/ref_units_check.html
- Vensim integration: https://www.vensim.com/documentation/integration.html
- Vensim TIME STEP guidance: https://www.vensim.com/documentation/ref_time_step.html
- PySD model integration implementation/documentation: https://pysd.readthedocs.io/en/master/_modules/pysd/py_backend/model.html
- Donella Meadows Project World3 synopsis: https://donellameadows.org/archives/a-synopsis-limits-to-growth-the-30-year-update/
- Nebel et al., World3 recalibration and model description: https://doi.org/10.1111/jiec.13442

## Recovery invariants

The reproducibility repair merged in PR #12 did not modify the World3 causal structure.

The authoritative file:

`science/vendor/world3_03/World3_03_Scenarios.mdl`

has the same Git blob on `v0.1.0` and post-recovery `main`:

`46d3a5a8a2bebc42fd0f18ef3079c19c974be942`

and the frozen SHA-256 recorded in the scientific input manifest remains:

`252e0c7eebff23d3c44344b6801cf3c40aec82d25b356ea8cce16a052249ac4d`.

The World3 adapter `science/src/world3_empirical/world3_03.py` is also unchanged between `v0.1.0` and post-recovery `main`.

The only joint-builder change required for recovery was replacement of the broken import from the deleted legacy `build_bau2_e2026.py` with the frozen observation-loader module. No World3 equation, stock, flow, lookup, delay, scenario equation or causal link was modified.

**Recovery causal/stock-flow preservation: PASS.**

## Structural inventory

Static inspection of the authoritative Vensim model detects 15 explicit `INTEG` state equations, including:

- arable land;
- potentially arable land;
- land-yield technology;
- urban and industrial land;
- land fertility;
- industrial capital;
- service capital;
- persistent pollution;
- persistent-pollution technology;
- four age-specific population stocks;
- non-renewable resources;
- resource-conservation technology.

The model also contains explicit smoothing and delay structures including `SMOOTH`, `SMOOTH3`, `SMOOTHI` and `DELAY3`, together with nonlinear lookup functions.

The retained model controls are:

- INITIAL TIME = 1900;
- FINAL TIME = 2100;
- TIME STEP = 0.5 year;
- SAVEPER = TIME STEP.

The current PySD engine uses Euler integration for its standard model stepping. A dedicated EWD diagnostic now reruns BAU2 at 0.5, 0.25 and 0.125 year time steps and tests whether retained outputs converge as the step is halved.

## SYSTEM DYNAMICS CONFORMITY

| ID | Criterion | Verdict | Current evidence / limitation |
|---|---|---|---|
| SD01 | Problem statement and purpose | **WARNING** | EWD has a research purpose and scientific status, but the dynamic problem statement is not yet expressed as a compact, explicit SD problem articulation tied to named reference modes. |
| SD02 | System boundary | **PASS** | The retained World3-03 core has a defined global boundary spanning population, capital, agriculture, non-renewable resources and pollution; candidate extensions remain outside the core. |
| SD03 | Endogenous vs exogenous variables | **WARNING** | The executable model distinguishes state equations, auxiliaries, constants and scenario controls, but EWD does not yet publish a complete explicit endogenous/exogenous inventory for the retained core. |
| SD04 | Reference modes / behavior over time | **WARNING** | Observed trajectories and historical comparisons exist, but formal purpose-linked SD reference modes are not yet separately pre-specified. Statistical target series are not automatically reference modes. |
| SD05 | Stocks | **PASS** | Explicit Vensim `INTEG` stocks are present; 15 are detected in the authoritative World3-03 file. |
| SD06 | Inflows and outflows | **PASS** | Core accumulations are expressed as rate balances, including births/deaths/maturation, investment/depreciation, land development/erosion/conversion, pollution appearance/assimilation and resource use. |
| SD07 | Auxiliaries | **PASS** | The model contains algebraic auxiliaries connecting stocks, rates, allocation rules and nonlinear response functions. |
| SD08 | Closed feedback loops | **PASS** | World3-03 contains endogenous closed feedback across population, capital, food/land, resources and pollution rather than a feed-forward statistical architecture. |
| SD09 | Reinforcing and balancing loops | **PASS** | Reinforcing population and capital accumulation loops and multiple resource/food/pollution balancing constraints are structurally present. |
| SD10 | Delays | **PASS** | Explicit perception, health, pollution-transmission, labor-utilization, social-adjustment and technology-development delays are retained. |
| SD11 | Nonlinearities and lookup functions | **PASS** | Lookup/table functions and nonlinear response relationships are integral to the retained model. |
| SD12 | Dimensional consistency | **WARNING** | Units are encoded throughout the Vensim model and stock-flow units are structurally plausible, but the current EWD CI does not yet run an independent full Vensim-equivalent units check over every equation. |
| SD13 | Conservation / accumulation identities | **PASS** | State variables are defined as explicit integrations of net rates. The principal population, capital, land, pollution and resource balances retain their accumulation identities. |
| SD14 | Integration method and numerical error | **WARNING** | The engine and step are now explicit and an automated 0.5/0.25/0.125-year convergence diagnostic is active. No numerical blocker has been detected. A cross-engine Vensim-vs-PySD equivalence test is not yet part of the retained baseline. |
| SD15 | Extreme-condition behavior | **WARNING** | Candidate mechanisms have used extreme-condition gates, but the reset baseline does not yet contain a comprehensive full-core World3 extreme-condition regression suite. |
| SD16 | Sensitivity | **WARNING** | EWD has parameter ensembles, sensitivity envelopes and identifiability diagnostics, but SD structural sensitivity/loop-dominance analysis is not yet complete. |
| SD17 | Boundary adequacy | **WARNING** | World3 has a clear structural boundary, but adequacy must be judged against EWD's precise purpose/reference modes; that purpose-specific assessment is not yet complete. |
| SD18 | Behavior reproduction | **WARNING** | EWD has historical fit and retrospective backtests, but these are not equivalent to SD behavior-pattern validation of the causal feedback hypothesis, especially where observation bridges dominate. |
| SD19 | Structural model vs measurement/observation model separation | **PASS** | The code and current screening clearly separate World3 structural dynamics from observations, mappings, bridges, candidate scoring, refit, medoid selection and diagnostics. |

### Current SD verdict

**World3-03 structural core: PASS as a System Dynamics structural model.**

**EWD System Dynamics conformity evidence package: WARNING, with no current BLOCKER.**

The warnings are not findings that World3 is “not System Dynamics.” They identify tests/documentation that EWD must add before claiming that its empirical work validates the World3 causal structure.

## Interpretation rule for empirical results

The following inference is prohibited:

`better statistical fit -> validated feedback structure`

The allowed interpretation is narrower:

`better statistical fit -> evidence that the selected empirical mapping/calibration procedure reproduces the evaluated observations better under the tested design`.

Evidence for causal feedback structure requires structural plausibility, correct boundary, units, stock-flow logic, delays, extreme-condition behavior, sensitivity and behavior-pattern evidence in addition to statistical fit.

In particular:

- the food observation bridge cannot by itself validate the World3 agricultural feedback structure;
- the pollution observation bridge cannot by itself validate the World3 persistent-pollution stock feedback;
- a candidate selected by an error metric is not automatically a structurally better SD model;
- a medoid trajectory is a trajectory-selection device, not an SD mechanism;
- an uncertainty/sensitivity envelope is not a causal validation result.

## Mandatory activation gate for future structural extensions

EROI/net energy, climate-water, minerals, AI-related mechanisms and every other future structural extension must remain inactive until all of the following are explicitly documented and passed:

1. **Explicit causal mechanism.** State the hypothesized causal relationship and why it belongs in the dynamic hypothesis.
2. **Clear stock-flow location.** Identify the stock, flow or auxiliary equations affected and whether a new accumulation is required.
3. **Feedback loop.** Identify the closed feedback loop entered or created, including polarity and expected dominant behavior.
4. **Units.** Specify units and demonstrate dimensional consistency.
5. **Delays.** Identify relevant physical, informational, behavioral or institutional delays and justify their formulation.
6. **Evidence.** Provide empirical and/or theoretical evidence for the mechanism, not merely correlation.
7. **Parameterization.** Define parameter meanings, ranges, source evidence and estimation/calibration rules.
8. **Extreme-condition tests.** Demonstrate sensible behavior when relevant inputs/stocks/parameters approach extreme values.
9. **Sensitivity.** Determine whether plausible parameter or structural variation changes the behavior mode or conclusions.
10. **Incremental validation.** Demonstrate added explanatory/predictive value without degrading established baseline behavior, using temporally valid evidence where prediction is claimed.

A mechanism must also satisfy the existing S1-S10 promotion gates.

**Data availability, correlation, lower MAPE, a visually improved fit or topical importance are not sufficient reasons for activation.**

The CI validator now rejects an extension that becomes `active_by_default` or `central` unless an explicit activation-evidence record shows PASS for E1-E10 and confirms S1-S10 PASS.

## Required follow-up work

The SD gate identifies five remaining methodological tasks before the conformity package itself should receive an unqualified PASS:

1. write a compact EWD dynamic problem statement and explicit reference modes;
2. publish a complete endogenous/exogenous/boundary inventory;
3. run or reproduce a full equation-level units consistency check;
4. restore a systematic core extreme-condition test suite;
5. add structural sensitivity / loop-dominance and behavior-pattern tests separately from ordinary fit/backtesting.

These tasks are verification/validation work. They do not imply that new mechanisms should be added to World3.
