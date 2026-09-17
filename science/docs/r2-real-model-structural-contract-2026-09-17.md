# R2 — Real Model structural contract

Date: 2026-09-17

Status: design contract only; no central model or release-result change.

## 1. Purpose

R2 defines the structural rules that must exist **before** a new "Real Model" can be implemented, calibrated or used for policy analysis. It follows the R1 empirical-foundation closure and preserves the current BAU Hybrid 2026 release as the reference baseline rather than silently turning R1 diagnostics into new feedbacks.

The long-term purpose is not to choose the historical Limits to Growth scenario that happens to look closest to observations. The target is a new, empirically testable system-dynamics model that may retain structures that survive validation, replace structures that fail, and add missing mechanisms only when their causal and observational contracts are explicit.

R2 therefore freezes architecture semantics before parameter fitting. A better numerical fit is not sufficient evidence that a proposed causal structure belongs in the central model.

## 2. R1 inheritance and non-regression boundary

R2 inherits the R1 evidence-role decisions as constraints:

- the current application remains World3 Empirical 0.10.2 until a separately versioned release changes it;
- the current central scientific trajectory remains BAU Hybrid 2026 v0.10.0, one World3-03 run structurally derived from scenario 2;
- Energy Institute series are observed energy accounting, not a new World3 state by declaration;
- fossil EROI series preserve their primary/final/useful boundaries and remain diagnostic until a causal bridge passes validation;
- eGRID/EIA plant results are physical-accounting diagnostics and do not define global plant-persistence parameters;
- UNIDO manufacturing evidence is an independent industrial diagnostic and does not automatically replace the World Bank bridge;
- critical-mineral series are observed risk registries and do not calibrate the latent World3 non-renewable-resource stock directly;
- institutional forecast vintages are external benchmarks only, never calibration observations;
- rejected or deferred R1 mechanisms remain rejected or deferred until new evidence passes a predeclared gate.

No file in `model/`, no central parameter vector and no released scenario series is modified by this contract.

## 3. Model purpose and decision boundary

The future Real Model is intended to support four classes of question:

1. reproduce and explain observed multi-sector dynamics over historical windows;
2. test whether proposed causal mechanisms improve prediction outside their estimation window;
3. generate conditional future trajectories with uncertainty that is labelled by source;
4. evaluate policy interventions only after the baseline model has passed predictive and structural validation.

The model is not an oracle and does not by itself choose public policy. Policy outputs must remain conditional on explicitly stated objectives, constraints, distributional assumptions, risk tolerance and intervention definitions.

## 4. Structural vocabulary

Every quantity admitted to the Real Model must have exactly one primary structural role.

### Stock

A state accumulated through time by explicit inflows and outflows. A stock must have a declared unit and initialization rule. It may not be replaced by an annual flow merely because the flow is easier to observe.

### Flow

A rate that changes a stock per unit time. Flow units must be stock-units/time and must close the corresponding stock accounting identity.

### Auxiliary

A contemporaneous transformation used to compute flows or interpretable outputs. An auxiliary must not conceal an undeclared stock, delay or cumulative process.

### Exogenous driver

A time series or intervention supplied from outside the endogenous model boundary. The reason it is exogenous must be documented. Forecast values may be used only in explicit scenarios and may not leak into calibration windows.

### Observation bridge

A declared mapping between an observable series and a model state/flow that is not directly measured. A bridge is not automatically a causal feedback.

### Diagnostic

Evidence used to evaluate plausibility, accounting or predictive performance without affecting the central simulation.

## 5. Evidence-role state machine

Every new dataset or mechanism must carry one of the following states:

- `observed`: a versioned empirical series with provenance and measurement boundary;
- `diagnostic`: evidence used to test the model but not drive the central simulation;
- `stress`: a transparent exogenous perturbation used for robustness analysis, not calibration;
- `candidate_feedback`: a causal mechanism with declared stocks/flows/units and a predeclared validation design;
- `central_feedback`: a candidate feedback that has passed every promotion gate and is included in a separately versioned central model;
- `reference`: an inherited structure retained for comparison while its Real Model status is still being tested.

Promotion is one-way only after evidence. A failed `candidate_feedback` returns to `diagnostic` or `stress`; it is not rescued by retuning against the same holdout.

## 6. Reference core and candidate modules

R2 separates the inherited World3 reference core from new candidate interfaces. This is an architectural map, not a declaration that every inherited relationship is true.

### 6.1 Population — reference core

Structural scope: population stocks/cohorts, births, deaths and ageing/maturation flows where represented by the implementation.

Required observables: total population plus demographic rates or cohort evidence when a rate/age structure is being estimated.

Candidate interfaces: food adequacy, services/health, material living conditions, pollution and policy variables. Each effect requires its own lag, sign and measurement justification rather than a generic multiplier.

### 6.2 Industrial and service capital — reference core

Structural scope: productive capital stocks, investment, depreciation, allocation between consumption and reinvestment, and service capacity where separately represented.

Required observables: industrial/manufacturing output diagnostics, capital/investment proxies and population denominators with consistent price/unit conventions.

Critical rule: total output derived from population × per-capita output is a coherence diagnostic and may not be double-weighted as an independent calibration target.

### 6.3 Food, land and agricultural capacity — reference core

Structural scope: agricultural capital, productive land, land development/degradation, food production and input requirements.

Required observables: FAOSTAT production indicators and future crop/land/water evidence at the geographic and seasonal resolution needed by the proposed mechanism.

Critical rule: the current fixed food observation bridge remains a bridge; it is not evidence for a newly identified agricultural feedback.

### 6.4 Non-renewable resources — reference core / latent stock

Structural scope: depletion accounting and the investment burden associated with increasingly difficult resource acquisition.

Required observables for any replacement: resource-specific reserve/resource accounting, extraction flows, grades or effort/cost proxies and substitution/recycling evidence.

Critical rule: mining production flows cannot be equated directly with the latent remaining-resource stock.

### 6.5 Persistent pollution — reference core / latent stock

Structural scope: pollution generation, accumulation, delayed assimilation and effects on other sectors.

Required observables for any replacement: a pollutant-specific or rigorously aggregated stock/flow representation with matching physical boundaries.

Critical rule: annual CO₂ activity observations remain a flow proxy and cannot be treated as the persistent-pollution stock.

### 6.6 Energy and net-energy accounting — candidate module, not central feedback

Current role: `observed` + `diagnostic` + separately testable `candidate_feedback`.

Candidate stocks: resource classes, extraction capital, renewable capacity, grid/storage capacity where justified.

Candidate flows: gross energy production, energy reinvestment, capacity additions/depreciation, storage/grid additions and losses.

Required interfaces: industrial investment burden and physically consistent net-energy accounting. Primary, final and useful EROI boundaries must not be mixed.

Critical rule: do not add an EROI burden on top of an existing World3 resource burden when both represent the same economic cost; double counting must be tested explicitly.

### 6.7 Climate, water, soil and food stress — candidate module, not central feedback

Current role: `observed` regional evidence + `diagnostic`/`candidate_feedback`.

Candidate stocks: atmospheric/thermal state only where needed, soil moisture or water availability, productive land and irrigation/adaptation capacity.

Candidate flows: emissions/uptake where endogenous, recharge/withdrawal, land degradation/restoration and adaptation investment.

Required interface: crop- and season-specific yield/input effects rather than a global annual-temperature multiplier.

Critical rule: the previously rejected temperature-only and annual-national stress formulations are not reopened without a new predeclared structure and independent test.

### 6.8 Technology minerals — observed risk module, not central resource stock

Current role: `observed` + `diagnostic`.

Candidate stocks if promoted later: mineral-specific resources/reserves, in-use stock, recyclable stock and refining capacity.

Candidate flows: extraction, refining, deployment, retirement and recycling.

Critical rule: copper, lithium, nickel, cobalt, rare earths and graphite remain separate until evidence supports an aggregation rule; a single mineral index may hide bottlenecks.

### 6.9 AI infrastructure — design-only candidate module

Current role: `diagnostic`/`stress` until a reproducible observational panel exists.

Candidate stocks: installed compute capacity, grid-connected data-centre capacity, dedicated generation, cooling and relevant semiconductor capacity.

Candidate transition chain: announced → interconnection request → contracted → permitted → construction → connected → utilized, with explicit attrition and delay distributions.

Critical rule: announced compute or projects cannot be treated as realized electricity demand.

### 6.10 Institutions, debt and geopolitics — stress layer

Current role: `stress` only.

These factors may change investment delays, trade, depreciation and other rates, but the global causal relationships remain too weakly identified for joint central calibration. Stress shocks must therefore be explicit, reversible and reported separately from estimated structural parameters.

## 7. Boundary and interface contract

Each module specification must provide:

- system boundary: endogenous, exogenous and excluded variables;
- stock/flow diagram and signed causal interfaces;
- units and dimensional equations;
- initialization year and initialization source;
- spatial aggregation level;
- temporal resolution and integration step;
- observational counterparts and observation bridges;
- parameter meaning, provenance and admissible range;
- lag/delay meaning and implementation;
- known double-counting risks;
- failure mode under extreme conditions;
- datasets allowed for estimation, selection and independent evaluation.

A causal edge without these fields is descriptive theory, not an implementable Real Model feedback.

## 8. Structural validation ladder

A proposed module or feedback is tested in this order. Later success cannot compensate for an earlier structural failure.

### Gate S1 — Boundary adequacy

The endogenous/exogenous/excluded boundary must fit the stated model purpose. Missing processes that materially determine the target cannot be hidden in a fitted coefficient.

### Gate S2 — Structural correspondence and accounting

Stocks and flows must correspond to the claimed real processes. Conservation/accounting identities must close where physics or accounting requires them.

### Gate S3 — Dimensional consistency

Every equation must be dimensionally consistent without arbitrary conversion factors. Stock-flow units must close exactly.

### Gate S4 — Parameter assessment

Every estimated parameter must have a real-world interpretation, source/provenance rule and plausible domain. A parameter that only exists to improve fit is insufficient.

### Gate S5 — Extreme-condition behavior

Zero, boundary and physically extreme inputs must produce interpretable model behavior and respect non-negativity/conservation constraints where applicable.

### Gate S6 — Numerical robustness

Material behavior must remain stable under a stricter integration step or a justified alternative numerical configuration. Numerical artifacts cannot be promoted as dynamics.

### Gate S7 — Historical behavior reproduction

Only after S1–S6 may the candidate be judged on historical trajectory reproduction. Fit diagnostics are descriptive here and do not establish causality.

### Gate S8 — Time-respecting predictive validation

Parameter estimation and structural selection must use only information available at each origin. Later observations must remain unavailable until evaluation. External forecast vintages remain benchmarks, not hidden future covariates.

### Gate S9 — Incremental skill against the simpler model

The candidate must be compared with the model without the extension using the same origins, observations, metrics and loss definition. Improvements must be consistent enough to survive the predeclared acceptance rule and must not be purchased by catastrophic deterioration in another central sector.

### Gate S10 — Identification and uncertainty

The mechanism must be sufficiently identified for its intended use. If materially different structures/parameters yield indistinguishable historical and predictive behavior, the extension remains structural sensitivity or a stress scenario.

Only after S1–S10 may a `candidate_feedback` be proposed for `central_feedback` status, and that promotion requires a separately reviewed central-model version.

## 9. Temporal and data-vintage contract

For every predictive experiment:

- define estimation, structural-selection and evaluation windows before looking at evaluation outcomes;
- preserve raw-source vintage or retrieval metadata whenever the source can be revised;
- do not use a series released after the forecast origin unless the experiment is explicitly retrospective and labelled as such;
- do not reuse a previously inspected holdout as if it were newly untouched confirmation;
- compare all alternatives on the same information set;
- preserve failed candidates and rejection reasons in the audit trail.

Forecasts from UN, IEA, EIA, institutions or other models are evaluated as external forecast vintages. They do not become observations and do not enter calibration merely because they are authoritative.

## 10. Uncertainty contract

The Real Model must distinguish at least four uncertainty classes:

1. **measurement uncertainty** — error/revision in observed data;
2. **parameter uncertainty** — uncertainty conditional on a fixed accepted structure;
3. **structural uncertainty** — competing plausible equations, boundaries or feedback topologies;
4. **scenario/policy uncertainty** — future exogenous choices, shocks and intervention paths.

An ensemble of admissible structures is not a posterior probability distribution unless a probabilistic model, likelihood and calibration procedure justify that interpretation and predictive coverage is evaluated. The current P10–P90 structural range therefore remains structural sensitivity.

Long-horizon event probabilities such as "collapse probability" are deferred until the relevant structural and probabilistic model has passed the validation ladder. Until then, report conditional scenario frequencies or sensitivity ranges with explicit conditioning assumptions.

## 11. Calibration contract

R2 does not authorize Bayesian or other full-model calibration. Calibration begins only after a topology and observation model have passed S1–S6.

When calibration is introduced:

- priors must be attached to interpretable parameters and documented evidence, not chosen only to reproduce a preferred scenario;
- observation error models must match the scale and measurement process of each data series;
- derived observations must not be independently weighted if this double-counts their source series;
- calibration and structural selection must remain separate from evaluation data;
- convergence diagnostics are necessary but not sufficient evidence of model validity;
- a more complex model must demonstrate incremental predictive value over a simpler baseline.

Numerical thresholds from earlier planning material are treated as provisional design hypotheses until a metric-specific R2 validation protocol ratifies them; they are not silently adopted as scientific acceptance thresholds.

## 12. Policy-analysis contract

Policy analysis is downstream of a validated baseline Real Model.

A policy experiment must declare:

- the intervention variable(s) and whether they act on a flow, allocation rule, delay, capacity or exogenous driver;
- implementation start, ramp, duration and reversibility;
- resource/cost constraint and any opportunity cost represented inside the model;
- outcomes and distributional dimensions used to evaluate impact;
- uncertainty classes propagated through the result;
- side effects and trade-offs across sectors;
- baseline and counterfactual definitions.

The model may compare conditional outcomes. It must not label a policy "optimal" without an explicit objective/utility function, constraints and stakeholder value weights. Public-policy decisions remain a human decision informed by model evidence.

## 13. R2 implementation sequence

R2 implementation, after this contract is accepted, should proceed in separable layers:

1. encode a machine-readable structural schema for modules, states, flows, units and evidence roles;
2. encode the inherited World3 reference core in that schema without changing its equations;
3. add invariant/unit/boundary tests that can run before simulation;
4. expose candidate-module interfaces as dormant contracts, not active feedbacks;
5. choose one candidate mechanism for a predeclared implementation/validation experiment;
6. only after that experiment passes S1–S10 consider a new central-model version.

The existing evidence suggests energy/net-energy is the most data-mature candidate interface, but R1 specifically rejected the tested direct coupling. R2 therefore does **not** authorize an energy coupling by default.

## 14. Decision gate G-R2-1

The next scientific implementation requires a genuine design decision that this contract intentionally does not make:

**Should the first executable Real Model scaffold preserve the validated World3-compatible reference core and expose new mechanisms as dormant, typed interfaces, or should R2 start from a clean-room stock-flow topology?**

The conservative option is the World3-compatible scaffold because it provides an already reproduced comparison baseline and permits one mechanism at a time to be tested against it. A clean-room topology offers greater architectural freedom but would simultaneously change many structural assumptions and make attribution of predictive gains/losses harder.

No implementation branch may promote a candidate feedback or alter the central curves until G-R2-1 is resolved.

## 15. R2 exit criteria

R2 structural-contract stage is complete when:

- this contract is versioned and reviewed;
- automated tests assert its non-regression and mandatory structural gates;
- the current central scientific release reproduces unchanged;
- no R1 diagnostic has been silently promoted;
- G-R2-1 is presented as the next explicit scientific architecture decision.

## References informing the validation order

- Sterman, J. D. (2000). *Business Dynamics: Systems Thinking and Modeling for a Complex World*, chapter 21, model testing in practice.
- Barlas, Y. (1996). "Formal aspects of model validity and validation in system dynamics." *System Dynamics Review* 12(3), 183–210. DOI: 10.1002/(SICI)1099-1727(199623)12:3<183::AID-SDR103>3.0.CO;2-4.
- Existing repository audits in `science/docs/`, especially the R1 empirical-foundation closure and `dynamic-extensions.md`, remain the authoritative evidence-role history for this project.
