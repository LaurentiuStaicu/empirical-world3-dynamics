# R2 candidate maturity audit — energy reinvestment bridge

Date: 2026-09-17

Status: candidate selected for a later prospective implementation/validation experiment; interface remains dormant and non-central.

## Decision

R2 selects exactly one mechanism for the next prospective experiment:

`energy reinvestment accounting -> industrial investment burden bridge`

Selection does **not** activate the mechanism, alter World3 equations, recalibrate BAU/BAU2, or replace BAU Hybrid 2026. The machine-readable interface is `active=false` and `central=false`.

The previously tested relationship

`World3 fraction of resources remaining -> fossil EROI`

remains rejected. It must not be used as the causal bridge in this experiment.

## Why energy is the most mature candidate data domain

The Energy Institute Statistical Review of World Energy 2026 provides a global, versioned energy dataset with data through 2025 and downloadable consolidated tables. Its methodology states that published statistics are assembled from government and published sources, that historical observations can be revised when better information becomes available, and that the Review moved to the Physical Energy Content method for Total Energy Supply in 2025. These properties make it suitable as observed accounting evidence provided that each forecast experiment preserves the source vintage.

Sources:

- Energy Institute, *About the Statistical Review*: https://www.energyinst.org/statistical-review/about
- Energy Institute, *Data downloads and archive*: https://www.energyinst.org/statistical-review/resources-and-data-downloads
- Energy Institute, *Statistical Review of World Energy 2026*: https://www.energyinst.org/statistical-review

The repository already registers the 2026 Energy Institute global series and the Aramendia fossil-EROI observations. The R1 audit also preserves the primary/final/useful EROI boundaries separately.

## Why energy is not yet mature enough for a central feedback

EROI values depend materially on system boundary. Published work distinguishes standard/primary, point-of-use/final and extended boundaries and warns that comparisons across different boundaries can change the interpretation of the energy return substantially. The R2 experiment therefore treats each EROI boundary as a separate measurement definition rather than combining them into one fitted series.

Boundary reference:

- Capellán-Pérez et al. (2020), *Standard, Point of Use, and Extended Energy Return on Energy Invested (EROI) ...*, Energies 13(12):3036, https://doi.org/10.3390/en13123036

More importantly, the project's own R1 prospective test rejected the direct resource-to-EROI link. Across the primary, final and useful boundaries, the proposed World3-resource link had larger five-year RMSE than persistence. The failure was not merely a parameter issue: the translation from energy reinvestment to a World3-compatible industrial-capital burden remains empirically unidentified, and BAU2 already contains a generic resource-acquisition capital burden that creates a double-counting risk.

Authoritative project evidence: `science/docs/energy-coupling-audit-2026-08-30.md`.

## Structural validation rationale

The R2 order follows standard system-dynamics validation practice: structural correspondence, boundary adequacy, dimensional consistency and extreme-condition tests precede behavioral reproduction. Later fit is not allowed to compensate for an invalid stock-flow structure.

Reference:

- Barlas, Y. (1996), “Formal aspects of model validity and validation in system dynamics”, *System Dynamics Review* 12(3), 183–210. DOI: 10.1002/(SICI)1099-1727(199623)12:3<183::AID-SDR103>3.0.CO;2-4.

## R2 maturity matrix

| Candidate domain | Observed evidence maturity | Causal bridge maturity | R2 role | Decision |
|---|---|---|---|---|
| Energy / net-energy | comparatively high: global series, explicit vintage and accounting methodology | incomplete: industrial-investment translation unidentified | observed + diagnostic + dormant candidate | **selected for prospective experiment** |
| Climate / water / soil / food | important regional/crop evidence exists | annual-global shortcut previously rejected; valid crop-season bridge still incomplete | diagnostic + dormant candidate | not selected |
| Technology minerals | mineral-specific extraction/risk evidence exists | no defensible aggregation into latent World3 resource stock | observed diagnostic | not selected |
| AI infrastructure | project/announcement evidence remains heterogeneous and realization attrition matters | reproducible connected/utilized capacity panel incomplete | diagnostic/stress | not selected |
| Institutions / debt / geopolitics | broad evidence, heterogeneous definitions | global joint causal identification insufficient | stress only | not selected |

## S1–S10 status at R2 closure

R2 does not claim that the selected candidate has passed S1–S10. The purpose of R2 is to make the scaffold testable and to predeclare the next experiment without promoting a diagnostic into the central model.

- S1 boundary adequacy: specified for the experiment.
- S2 accounting/structural correspondence: specified, including mandatory double-counting reconciliation.
- S3 dimensional consistency: specified and machine-checked for the scaffold.
- S4 parameter assessment: **blocked until a directly defensible bridge observation is registered**.
- S5 extreme conditions: predeclared and scaffold guardrails implemented.
- S6 numerical robustness: predeclared and scaffold accounting tests implemented; future candidate dynamics require their own timestep test.
- S7 historical reproduction: not run for this new mechanism.
- S8 time-respecting predictive validation: not run.
- S9 incremental skill versus the simpler model: not run.
- S10 identification and uncertainty: not run.

Therefore the candidate remains non-central. Any future failure returns it to diagnostic/stress status rather than triggering retuning against the same holdout.

## What R2 has established

The conservative G-R2-1 choice is now executable: the verified World3-03 model remains the reference engine, its vendored source is protected by the existing SHA-256 input manifest, the structural inventory is machine readable, all new interfaces fail closed when activation is attempted, and the single selected candidate has an explicit forbidden-link and double-counting contract.
