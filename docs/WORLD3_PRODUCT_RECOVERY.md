# World3 Product Recovery — execution record

## Frozen prerequisite

Product Recovery starts only after PR #9 (`Energy accounting → direct emissions`) is merged and its post-merge CI is green. The scientific verdict is immutable for this pass: **RETAIN AS DIAGNOSTIC**. No BAU, BAU2 or BAU Hybrid 2026 values are changed.

## Recovery objective

Rebuild the web product around temporal trajectories and model-derived turning points rather than the previous four-panel layout. The dominant chart is the product; Theory and Evidence become on-demand secondary surfaces.

## Scientific semantics

`web/public/product-recovery-contract.json` is the authoritative machine-readable definition of product metrics. It prevents retrospective threshold selection, separates scenario alignment from forecast/probability, and forbids event-time uncertainty claims from pointwise P10–P90 bands.

## Classic scenarios

Comprehensive Technology and Stabilized World are documented in Theory but are not plotted in this pass because the repository does not currently package authoritative versioned trajectories with provenance. They must not be reconstructed approximately merely to make the chart look richer.

## Intervention gate

The current scientific package has no validated intervention operator/trajectory set that can support reproducible baseline-vs-intervention timing experiments. Numeric controls remain disabled by design; the application says why. Preparedness/resilience is explicitly external to World3 and uses UNDRR/OECD domains.

## Visual usefulness audit

The web CI captures and uploads:

- `desktop-1440x900.png`;
- `laptop-1366x768.png`;
- `mobile-390x844.png`;
- `visual-audit.json`.

For desktop/laptop the trajectory chart must occupy 70–82% of the trajectory-stage width. The gate also checks manual completeness, Evidence & Limits semantics, scenario-toggle behaviour and mobile horizontal overflow.

Software-green without screenshot/product review is not sufficient for integration.
