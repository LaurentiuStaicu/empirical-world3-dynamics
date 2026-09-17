<p align="center">
  <img src="data/icons/io.github.laurentiustaicu.World3Empirical.svg" width="96" height="96" alt="World3 Empirical icon">
</p>

<h1 align="center">World3 Empirical</h1>

<p align="center">
  Explore observed global indicators alongside the original World3 BAU and BAU2 trajectories and the conditional BAU Hybrid 2026 scenario.
</p>

<p align="center">
  <img alt="Version 0.10.2" src="https://img.shields.io/badge/version-0.10.2-4e9a06">
  <img alt="InfoClar Model Suite v1.1" src="https://img.shields.io/badge/InfoClar%20Model%20Suite-v1.1-3689e6">
  <img alt="elementary OS 8" src="https://img.shields.io/badge/elementary_OS-8-64baff">
  <img alt="Flatpak" src="https://img.shields.io/badge/package-Flatpak-4a90d9">
  <img alt="MIT license" src="https://img.shields.io/badge/license-MIT-blue">
</p>

<p align="center">
  <a href="https://github.com/LaurentiuStaicu/world3-empirical-flatpak/releases/latest/download/World3-Empirical-0.10.2-x86_64.flatpak">
    <img alt="Download Flatpak for elementary OS 8" src="https://img.shields.io/badge/Download%20Flatpak-elementary%20OS%208-4A90D9?logo=flatpak&logoColor=white">
  </a>
</p>

![World3 Empirical displaying population trajectories, observations and the BAU Hybrid 2026 sensitivity range](data/screenshots/world3-empirical-population-cropped.jpg)

World3 Empirical is an offline Vala / GTK 4 application for elementary OS 8. It compares recent global observations with the original World3-03 BAU and BAU2 scenarios and with BAU Hybrid 2026, an empirically calibrated but still conditional BAU2-derived scenario.

The interface follows **InfoClar Model Suite Design Standard v1.1**. English is the default language and Romanian is available from the EN/RO switch without changing the selected indicator or model state. The full implementation mapping is documented in [`docs/INFOCLAR_MODEL_SUITE_DESIGN_STANDARD_V1_1.md`](docs/INFOCLAR_MODEL_SUITE_DESIGN_STANDARD_V1_1.md).

## Interface

The desktop workspace uses a responsive asymmetric 2×2 structure:

| Area | Purpose |
|---|---|
| **Model & trajectories** | Dominant interactive chart with the selected indicator, horizon and P10–P90 structural-sensitivity control. |
| **Theory / Learn** | Explains what the selected variable means in World3, how it connects to the model and where the empirical comparison stops. |
| **Core indicators** | Dashboard for the five empirically calibrated indicators, ordered as population, food per capita, industrial output per capita, annual CO₂ activity proxy and human development. |
| **Evidence & limits** | Source provenance, descriptive fit, frozen-2018 backtest, multi-origin validation, internal support diagnostic and explicit limitations. |

On narrower windows the panels stack while retaining the same semantic order. The model representation remains World3-specific: the suite standard aligns navigation, typography, panels, language behaviour and explanatory structure without forcing every InfoClar application to use the same kind of diagram.

## What the chart shows

The application intentionally keeps only three model trajectories so their differences remain legible:

| Trajectory | Meaning |
|---|---|
| **Original BAU** | The original World3-03 reference scenario, unchanged. |
| **Original BAU2** | World3-03 scenario 2 with a larger initial resource stock, unchanged. |
| **BAU Hybrid 2026** | One World3 run structurally derived from BAU2, calibrated jointly against observations and continued conditionally beyond the latest observed year. |

Black points are observations, not part of a fitted curve. The dashed blue segment is the retrospective hybrid trajectory and the solid blue segment is the post-observation projection. P10–P90 represents sensitivity across 12 admissible structural configurations; it is **not** a confidence interval and does not express the probability of collapse.

The app provides eight views: population, industrial output per capita, food per capita, annual CO₂/activity proxy, human development, total industrial output, persistent-pollution stock and non-renewable resources remaining. The pointer readout reports the exact year and all displayed model values, and the chart keeps five-year grid spacing.

## What BAU Hybrid 2026 is

BAU Hybrid 2026 starts from World3-03 scenario 2. The five calibrated targets and three diagnostics come from the same run and the same seven-parameter vector; individual output curves are not independently adjusted.

The selection procedure evaluates 128 predeclared configurations. Validation selection uses data ending in 2018, leaving later observations as a recent untouched test for that procedure. The displayed central line is subsequently refit using all currently available observations and is an actual World3 run selected from 12 final admissible configurations.

Food and annual CO₂ use two observation bridges selected only with pre-2019 data. They improve comparability between World3 states and observed indicators but do not add new sectors or feedback loops.

The complete scientific method, parameter definitions, validation results and limitations are in [`SCIENTIFIC_METHOD.md`](SCIENTIFIC_METHOD.md). Processed release data and contracts are in [`data/scenarios`](data/scenarios); reproducible scientific inputs, tests and audits are under [`science`](science).

> **Essential limitation:** BAU Hybrid 2026 is an experimental conditional scenario. It does not estimate a probability of collapse, does not uniquely identify the true parameters of the world system and should not be read as a guaranteed point forecast.

## Empirical foundation and R1 boundary

The R1 empirical-foundation closure preserves evidence roles instead of forcing every useful dataset into the central model. Energy Institute primary-energy data, fossil EROI observations, UNIDO industrial diagnostics, technology-mineral registries, external forecast vintages and eGRID/EIA physical-accounting audits are retained as observed evidence or diagnostics according to their provenance and identification strength.

Failed or insufficiently identified mechanisms remain visible as rejected/diagnostic evidence. In particular, EROI accounting stages stay separate, institutional forecasts are not calibration observations, and eGRID plant-level persistence results are not promoted into central World3 parameters. The central BAU Hybrid 2026 scientific release therefore remains unchanged by R1.

## Data sources

The distributed release uses or references World Bank WDI for population and industry, UNIDO for independent manufacturing diagnostics, FAOSTAT Production Indices for food production per capita, World Bank / EDGAR for the annual emissions activity proxy, UNDP for HDI, UN World Population Prospects 2024 as an external demographic benchmark, and World3-03 for the original BAU and BAU2 trajectories.

Additional diagnostic registries cover primary energy, EROI, technology minerals and eGRID/EIA gas-plant accounting. These do not become coupled feedbacks merely because they are included in the evidence base.

## Install on elementary OS 8

For the latest published x86_64 Flatpak, use the download button at the top of this page. Open the `.flatpak` file with elementary Sideload and confirm installation. The application runs offline after installation.

For development or audit, install the elementary OS 8 platform/SDK and Flatpak Builder once, then build from source:

```bash
flatpak install --user appcenter io.elementary.Platform//8 io.elementary.Sdk//8
flatpak install --user flathub org.flatpak.Builder
git clone https://github.com/LaurentiuStaicu/world3-empirical-flatpak.git
cd world3-empirical-flatpak
./build-flatpak.sh
```

Launch with:

```bash
flatpak run io.github.laurentiustaicu.World3Empirical
```

Repository validation can be run independently:

```bash
make validate
make test
make science-test
uv run --project science --extra world3-03 python scripts/reproduce_scientific_results.py
```

The CI contract reproduces the frozen scientific release, validates integrity manifests, runs scientific and application tests and builds the elementary OS Flatpak before integration.

## Romanian summary

World3 Empirical este o aplicație offline pentru elementary OS 8 care compară observații globale cu scenariile originale World3-03 BAU și BAU2 și cu BAU Hibrid 2026. Interfața respectă **InfoClar Model Suite Design Standard v1.1**: graficul modelului rămâne dominant, teoria este explicată în panoul din dreapta, indicatorii empirici principali sunt grupați într-un dashboard, iar dovezile și limitele sunt separate într-un panou propriu. Limba implicită este engleza, iar comutatorul EN/RO schimbă interfața fără să schimbe starea modelului.

BAU Hibrid 2026 rămâne un scenariu experimental condițional, nu o prognoză probabilistică. Banda P10–P90 reprezintă sensibilitate structurală, iar datele energetice, EROI, mineralele și auditurile eGRID/EIA nu sunt promovate automat în feedbackurile modelului central.

## Development, limits and licensing

The application is built with Vala, GTK 4 and Granite 7 for elementary OS 8. Aggregate global indicators hide regional and distributional differences; World Bank industry and HDI are proxies, while persistent pollution and remaining resources are latent World3 states rather than direct observations.

Code is released under the [MIT license](LICENSE). FAOSTAT series are CC BY 4.0; other datasets retain the terms of their source institutions. Numeric provenance, snapshots and hashes are recorded in the repository. Reproducible issues can be reported through [GitHub Issues](https://github.com/LaurentiuStaicu/world3-empirical-flatpak/issues).
