# Diagnostic raw-data reproducibility policy — 2026-09-22

Status: **R-FDC-7 CLOSED_POLICY**

This gate defines and validates how non-central diagnostic inputs may be described and rematerialized. It does **not** claim that every historical raw source can still be reconstructed, and it changes no central observation, model equation, candidate rule, fitted parameter or retained Joint 2026 result.

Machine-readable records:

- `science/data/audits/diagnostic_source_reproducibility_2026-09-22.json`
- `science/data/diagnostic_remote_inputs.json`

Validation and materialization:

- `scripts/check_diagnostic_reproducibility_policy.py`
- `scripts/fetch_diagnostic_inputs.py`
- manual workflow: **Diagnostic source materialization**

## Policy modes

| Mode | Meaning | Permitted reproducibility claim |
|---|---|---|
| `retained_raw` | exact raw source bytes are retained in the repository scientific-input inventory | source-to-processed reconstruction can be checkout-reproducible |
| `pinned_remote` | exact raw source is external but has a versioned/immutable identity, checksum and deterministic fetch path | source-to-processed reconstruction is reproducible while the pinned object remains retrievable |
| `verified_transport` | a pinned transport copy is used and equivalence to the primary source is independently established for the exact EWD extraction boundary | reconstruction is reproducible for the declared EWD role; whole-file primary identity must not be implied unless proven |
| `processed_snapshot_only` | historical raw bytes are unavailable but the processed diagnostic artifact is retained | downstream diagnostic replay is reproducible; historical source-to-processed reconstruction is not |

## Current audit result

The policy audit covers the non-central diagnostic inputs identified by the repository file-data-content audit.

### Retained raw

Technology-mineral and UNIDO diagnostic inputs are retained in the repository and remain source-to-processed reconstructable from checkout.

### Pinned remote

The following sources have deterministic external materialization contracts:

- EPA eGRID 2021;
- EPA eGRID 2022;
- EPA eGRID 2023 rev2;
- Aramendia et al. fossil EROI dataset (Figshare file 46240243);
- Global Carbon Project 2025v15.

Each entry records an HTTPS URL, cryptographic hash, local diagnostic-cache destination, and where applicable file size or immutable identifier.

### Verified transport

Energy Institute 2026 uses the pinned `shanewhi/world-energy-data` transport. R-FDC-6 independently established exact equality for all 427 `Total World` observations used by EWD against an archived official EI 2026 download. Whole-file byte identity is explicitly not claimed.

### Processed snapshot only

Three historical source snapshots cannot currently be reconstructed byte-for-byte:

1. NASA GISTEMP snapshot dated 2026-08-31;
2. FAOSTAT Production Crops/Livestock archive used by the regional cereal/climate panel;
3. OWID/ERA5 regional temperature and precipitation downloads dated 2026-08-31.

Their upstream endpoints are living datasets. The historical raw hashes are preserved in provenance, but the exact historical raw files are not retained and current endpoints must not be treated as proof of those old bytes.

For these cases the safe claim is deliberately narrower: **downstream diagnostic execution from the retained processed snapshot is reproducible; historical raw-to-processed reconstruction is not currently reproducible.**

## Separation from central Joint reproduction

Diagnostic downloads are materialized under:

`.diagnostic_sources/`

That directory is Git-ignored and is not part of `science/data/remote_inputs.json`.

This separation is intentional. A temporary outage, redirect or retirement of an external diagnostic source must not make the retained central Joint 2026 trajectory unreproducible.

The ordinary Scientific reproducibility workflow therefore validates the policy **offline**, while the manual **Diagnostic source materialization** workflow tests external retrieval and hashes.

## Closure rule

R-FDC-7 is closed as **CLOSED_POLICY**, not as a universal raw-data closure claim.

The gate is satisfied because every audited diagnostic source has one explicit policy mode and the repository prevents stronger claims than the available evidence supports.

If an exact historical raw snapshot is later recovered, its entry should be promoted from `processed_snapshot_only` to `retained_raw` or `pinned_remote`, with hashes and provenance updated accordingly.

## Next gate

**R-FDC-8 — rejected experimental mechanisms.**

The next audit step should ensure executable but rejected hypotheses such as the resource-fraction → EROI coupling cannot be mistaken for accepted central mechanisms.
