<p align="center">
  <img src="data/icons/io.github.laurentiustaicu.World3Empirical.svg" width="96" height="96" alt="World3 Empirical icon">
</p>

<h1 align="center">World3 Empirical</h1>

<p align="center">Compare observed global indicators with World3 BAU, BAU2 and BAU Hybrid 2026 in an evidence-aware InfoClar interface.</p>

<p align="center">
  <img alt="Version 1.0.0" src="https://img.shields.io/badge/Version-1.0.0-4e9a06">
  <img alt="elementary OS 8" src="https://img.shields.io/badge/elementary_OS-8-64baff">
  <a href="LICENSE"><img alt="License MIT" src="https://img.shields.io/badge/License-MIT-blue"></a>
</p>

<p align="center">
  <img width="220" alt="Open Web App — Planned" src="https://img.shields.io/badge/Open_Web_App-Planned-9ca3af?style=for-the-badge">
  <a href="https://github.com/LaurentiuStaicu/world3-empirical-flatpak/releases/download/v0.10.2/World3-Empirical-0.10.2-x86_64.flatpak"><img width="220" alt="Download Flatpak v0.10.2" src="https://img.shields.io/badge/Download_Flatpak-v0.10.2-087F73?style=for-the-badge"></a>
</p>

## Current product direction — web first

The active product surface is now the **World3 Empirical web application** in [`web/`](web). Development is web-first through product v1. The existing GTK/Flatpak application is preserved as a prior delivery surface but is intentionally not kept in UI lock-step during this phase; it will be reconciled or rebuilt from the mature web product at or very near v1.

This sequencing change does **not** change the scientific model. The web application reads the same validated scenario and diagnostic files already distributed by the project. Product `v1.0.0` and scientific model `0.10.0` are separate version domains.

The web application implements **InfoClar Model Suite Design Standard v1.1** with an asymmetric adaptive 2×2 workspace: a dominant trajectory chart, Theory/Learn, the five calibrated core indicators, and Evidence & Limits. English is the default language and Romanian is a complete state-preserving alternative. See [`docs/WEB_V1_PRODUCT_CONTRACT.md`](docs/WEB_V1_PRODUCT_CONTRACT.md) and [`docs/INFOCLAR_MODEL_SUITE_DESIGN_STANDARD_V1_1.md`](docs/INFOCLAR_MODEL_SUITE_DESIGN_STANDARD_V1_1.md).

## Run the web product

```bash
cd web
npm install
npm run check
npm run dev
```

For a production static bundle:

```bash
npm run build
```

The build copies validated data from `data/scenarios/` and the R2 structural contract from `science/configs/real_model_structure.json` **byte-for-byte** into generated web assets. A hash check blocks divergence. The browser does not reimplement or rerun World3 equations.

## What the chart shows

Only three model trajectories are presented as central comparison curves: **Original BAU**, **Original BAU2**, and **BAU Hybrid 2026**. Observations remain points. The optional P10–P90 band is the pointwise range of the admitted structural sensitivity ensemble; it is **not** a probabilistic confidence interval and does not express the probability of collapse.

Eight views are available: population, industrial output per capita, food per capita, annual CO₂/activity proxy, human development, total industrial output, persistent-pollution stock, and non-renewable resources remaining. The final two remain explicitly latent.

## Scientific model and validation

BAU Hybrid 2026 is a BAU2-derived World3-03 run calibrated jointly against the five empirical targets and accompanied by diagnostics. Food and annual CO₂ use observation bridges that improve empirical comparability but do not introduce new feedback loops.

The web Evidence & Limits panel reads the existing frozen-2018 backtest, multi-origin validation and descriptive historical-fit files. It does not rename reused historical tests as untouched holdouts, does not turn institutional forecasts into calibration observations, and does not promote R1 diagnostics into the central model.

The complete scientific method, parameter definitions and limitations remain in [`SCIENTIFIC_METHOD.md`](SCIENTIFIC_METHOD.md). Processed release data and contracts are in [`data/scenarios`](data/scenarios); reproducible scientific inputs, tests and audits are under [`science`](science). The conservative R2 structural contract preserves the validated World3 reference core and keeps candidate mechanisms inactive unless they pass S1–S10.

> **Essential limitation:** BAU Hybrid 2026 is an experimental conditional scenario. It does not estimate a probability of collapse, does not uniquely identify the true parameters of the world system and should not be read as a guaranteed point forecast.

## Data sources

The release uses or references World Bank WDI for population and industry, UNIDO for independent manufacturing diagnostics, FAOSTAT Production Indices for food production per capita, World Bank / EDGAR for the annual emissions activity proxy, UNDP for HDI, UN World Population Prospects 2024 as an external demographic benchmark, and World3-03 for original BAU and BAU2 trajectories.

Additional diagnostic registries cover primary energy, EROI, technology minerals and eGRID/EIA accounting. Inclusion in the evidence base does not make these central feedbacks. In particular, the rejected World3 resource-fraction → fossil-EROI coupling remains forbidden.

## Legacy Flatpak surface

The existing elementary OS Flatpak remains available from GitHub Releases and its source is preserved in the repository. During the web-first phase, routine web work does not require a parallel Flatpak UI implementation. The Flatpak release workflow is therefore tag/manual only, while web-only pull requests use dedicated web CI.

## Licensing

Code is released under the [MIT license](LICENSE). Dataset terms remain those of their source institutions. Numeric provenance, snapshots and hashes are recorded in the repository; reproducible issues can be reported through GitHub Issues.
