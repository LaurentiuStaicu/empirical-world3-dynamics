# World3 Empirical — web-first product contract v1.0

Date: 17 September 2026

## Direction

Until product v1, World3 Empirical is developed **web-first**. The GTK/Flatpak application is a frozen prior delivery surface and is not the active product target. It may be reconciled or rebuilt from the mature web product at or very near v1. Web work must not require equivalent Flatpak UI work during this phase.

The web product version is separate from the scientific model version. `web/package.json` may reach `1.0.0` while `data/scenarios/scenario_schema.json` continues to report the validated scientific release and model version. Product versioning must never imply an unperformed scientific recalibration.

## InfoClar v1.1 mapping

The web product implements the shared asymmetric adaptive 2×2 workspace:

1. **Model & trajectories** — dominant interactive World3 trajectory chart with indicator, horizon and P10–P90 structural-sensitivity controls. Only original BAU, original BAU2 and BAU Hybrid 2026 are model curves; observed data remain points.
2. **Theory / Learn** — selected-variable theory, stock/flow role, measurement boundary and the machine-readable R2 structural contract.
3. **Core indicators** — population, food per capita, industrial output per capita, annual CO₂ activity proxy and human development, in stable priority order.
4. **Evidence & limits** — provenance, frozen-2018 backtest, multi-origin validation, descriptive fit and explicit interpretation limits.

English is the default language. Romanian changes all user-facing interface text while preserving selected indicator, horizon and uncertainty state. The layout stacks semantically on narrower screens.

## Scientific non-regression

The browser does not execute or reimplement World3 equations. Before development and production builds, `web/scripts/sync-data.mjs` copies the existing validated scenario and diagnostic artifacts byte-for-byte into generated static assets. `web/scripts/verify-contract.mjs` verifies source/copy SHA-256 identity and the R2 architecture constraints.

The web layer must not:

- modify BAU, BAU2 or BAU Hybrid 2026 values;
- read `forecast_median` as the displayed central trajectory;
- reinterpret P10–P90 as a confidence or probability interval;
- fabricate observations for latent World3 states;
- promote R1 energy, EROI, mineral or other diagnostics into central feedbacks;
- reactivate the rejected `world3_resource_fraction_to_fossil_eroi` coupling;
- activate any R2 candidate interface by default;
- bypass the S1–S10 promotion gates.

## Definition of product v1.0.0

Product v1.0.0 is reached when the static web application:

- loads the eight existing indicator views from the validated package;
- displays the three baseline trajectories, observed points and optional structural P10–P90 band;
- provides pointer and keyboard inspection of annual chart values;
- exposes the five-indicator dashboard and current validation diagnostics;
- explains theory and evidence roles without merging observation proxies with latent mechanisms;
- provides full EN/RO UI, responsive desktop/mobile behaviour and basic keyboard/accessibility support;
- preserves UI state in shareable URL parameters;
- passes TypeScript checking, scientific-copy hash verification and a production Vite build in dedicated web CI.

A public hosting target is operational deployment, not a scientific gate. The CI build artifact is the authoritative deployable static bundle until a hosting surface is enabled.
