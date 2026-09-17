# InfoClar Model Suite Design Standard v1.1 — World3 Empirical conformance

This document records how the World3 Empirical application implements the shared InfoClar Model Suite Design Standard v1.1. It is a conformance note for the application, not the visual reference sketch.

## Shared suite rules

- The application uses a common suite header with the application name, the current version and an EN/RO language switch.
- English is the default interface language; Romanian is available without changing the model state.
- The desktop workspace follows an asymmetric 2×2 information architecture:
  1. upper-left: the dominant model representation and its controls;
  2. upper-right: theory, tutorial and context;
  3. lower-left: the most decision-relevant observed/calibrated indicators;
  4. lower-right: evidence, provenance, validation and limitations.
- The layout is adaptive. Panels wrap and stack on narrower windows rather than shrinking the model representation below a readable width.
- Typography, spacing, cards, controls, labels, tooltips and icon use rely on the elementary OS / GTK 4 / Granite visual language rather than a separate custom widget theme.
- The visual representation remains model-specific. World3 Empirical therefore keeps a trajectory chart rather than imitating the causal diagram used by the Cognitive Epistemic Model or the stock-flow representation of the macro-financial model.

## World3-specific mapping

### Upper-left — Model & trajectories

The dominant panel preserves the three intended model curves only: original BAU, original BAU2 and BAU Hybrid 2026, together with observed points and the structural P10–P90 sensitivity band. Indicator, horizon and uncertainty controls remain attached to the graph they affect.

### Upper-right — Theory / Learn

The theory panel explains the selected variable, its role in the World3 stock-flow structure and the interpretation boundary between observed data and latent mechanisms. It also keeps the critical distinction between empirical observation bridges and actual feedback mechanisms.

### Lower-left — Core indicators

The dashboard presents the five empirically calibrated indicators in a stable priority order: population, food per capita, industrial output per capita, annual CO₂ activity proxy and human development. Each card shows the BAU Hybrid 2026 value for 2035, the latest observed value and the structural P10–P90 range.

### Lower-right — Evidence & limits

The auxiliary panel keeps source provenance, descriptive fit, the frozen-2018 backtest, multi-origin validation, the internal projection-support diagnostic and the explicit limitations. Latent variables remain labelled as latent and do not acquire fabricated empirical validation.

## Scientific non-regression boundary

The v1.1 uniformisation is a presentation-layer change. It must not:

- modify BAU, BAU2 or BAU Hybrid 2026 central curves;
- change the seven-parameter central vector;
- promote R1 diagnostic evidence into model parameters;
- reinterpret institutional forecasts as calibration observations;
- merge observation proxies with latent World3 stocks;
- relabel P10–P90 sensitivity as a probabilistic confidence interval.

The R1 empirical-foundation contract remains authoritative for these boundaries.

## Responsive behaviour

The desktop target is two panels per row, with a larger minimum width for the model/chart and dashboard panels than for theory/evidence panels. GTK `FlowBox` provides the breakpoint behaviour: when the available width no longer supports the wide+narrow pair, the panels stack vertically while preserving their semantic order.

## Language behaviour

English is loaded first. Switching to Romanian updates panel titles, controls, explanatory text, dashboard details, evidence diagnostics, source labels, the chart tooltip, chart unit prefix, cutoff annotation, legend and hover readout. Numeric data, selected indicator, horizon and uncertainty state are preserved across the switch.
