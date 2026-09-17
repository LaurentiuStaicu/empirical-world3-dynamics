# World3 Empirical Web — product v1.0.0

This is the web-first product surface for World3 Empirical. It implements the InfoClar Model Suite Design Standard v1.1 while preserving the scientific package unchanged.

The web product version and the scientific model version are intentionally separate. Product `1.0.0` means the web interface is feature-complete for the current InfoClar contract; it does **not** rename the validated model or scenario release. The header reads the model version and data snapshot from `data/scenarios/scenario_schema.json` at runtime.

## Development

```bash
cd web
npm install
npm run check
npm run dev
```

`npm run sync-data` copies the already validated scenario and diagnostic artifacts byte-for-byte into `web/public/data`. These generated copies are ignored by Git. No model equation or scientific output is recalculated in the browser.

## Build

```bash
npm run build
```

The resulting `web/dist/` directory is a portable static application. Vite uses a relative base path, so the build can be hosted below a repository path as well as at a domain root.

## Product contract

The dominant trajectory chart preserves only BAU, BAU2 and BAU Hybrid 2026 plus observed points and the structural P10–P90 band. Theory/Learn explains the selected variable and its interpretation boundary. The dashboard shows the five calibrated indicators. Evidence & Limits reads the frozen-2018 backtest, multi-origin validation and descriptive fit diagnostics. English is the default and Romanian is a full state-preserving alternative.
