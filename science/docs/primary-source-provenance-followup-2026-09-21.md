# Primary-source provenance follow-up — 2026-09-21

Status: diagnostic provenance work only. No scientific input or retained result is changed by this document.

## Purpose

Refine the provenance warnings identified by the repository file-data-content audit by separating:

1. semantic/source-definition equivalence;
2. transport equivalence;
3. full byte-level primary-source closure.

## UNDP Human Development Index

Current EWD transport:

`science/data/raw/bau2_e2026/2026-08-28/undp_hdi_owid_adapter.csv`

Current use:

The `World` HDI series is a central empirical proxy for World3 human welfare. EWD explicitly states that HDI is not identical to World3 HWI.

Official UNDP source:

- Documentation/download page: `https://hdr.undp.org/data-center/documentation-and-downloads`
- Official HDR 2025 trends table: `https://hdr.undp.org/sites/default/files/2025_HDR/HDR25_Statistical_Annex_HDI_Trends_Table.pdf`
- Official complete time-series endpoint exposed by the UNDP download page:
  `https://hdr.undp.org/sites/default/files/2025_HDR/HDR25_Composite_indices_complete_time_series.csv`

### Anchor verification

The EWD adapter World series matches the official HDR 2025 Table 2 exactly at every published World anchor in the table:

| Year | EWD adapter | Official UNDP Table 2 |
|---:|---:|---:|
| 1990 | 0.608 | 0.608 |
| 2000 | 0.651 | 0.651 |
| 2010 | 0.707 | 0.707 |
| 2015 | 0.731 | 0.731 |
| 2020 | 0.742 | 0.742 |
| 2021 | 0.742 | 0.742 |
| 2022 | 0.752 | 0.752 |
| 2023 | 0.756 | 0.756 |

Conclusion:

The current World-series semantics are independently confirmed against the primary UNDP publication. The remaining provenance risk is transport/full-file closure, not a detected value disagreement.

Required closure:

- archive or deterministically fetch the official UNDP complete time-series file;
- record byte hash, size, release/vintage and source URL;
- compare every annual World HDI observation used by EWD, not only the published table anchors;
- only after full equality is established should the OWID adapter be considered replaceable by the official primary file without a scientific change.

## UN World Population Prospects 2024

Current EWD transport:

`science/data/raw/bau2_e2026/2026-08-28/un_wpp2024_owid_adapter.csv`

Current use:

Population benchmark/plausibility guardrail; not a fitted central population target.

Official UN source:

- `https://population.un.org/wpp/`
- UN DESA WPP 2024 dataset page:
  `https://www.un.org/development/desa/pd/content/World-Population-Prospects-2024`

The official WPP documentation states that the 2024 Revision provides estimates through 2023 and projections to 2100. The WPP download center recommends CSV for bulk use.

The EWD adapter follows the same semantic boundary:

- observed/estimate column through 2023;
- medium projected column from 2024 onward.

Selected EWD World values currently used/available in the adapter include:

- 2023 estimate: 8,091,734,933;
- 2024 medium projection: 8,161,972,574;
- 2030 medium projection: 8,569,124,917;
- 2035 medium projection: 8,885,210,180;
- 2050 medium projection: 9,664,378,585;
- 2100 medium projection: 10,180,160,744.

Conclusion:

The estimate/projection boundary and medium-projection semantics match the primary UN WPP 2024 framework. Full primary-file row equality remains to be checked.

Required closure:

- freeze/hash the official WPP 2024 compact or CSV bulk file;
- extract World total population, both sexes, all ages;
- verify all EWD 1950-2100 World rows and the estimate/medium split exactly;
- retain the official UN citation and release metadata.

## Energy Institute Statistical Review 2026

Current EWD provenance:

`science/data/processed/energy_institute_global_2026.provenance.json`

Current transport:

Pinned GitHub mirror commit with SHA-256 and size recorded.

Official EI source:

`https://www.energyinst.org/statistical-review/resources-and-data-downloads`

The official Energy Institute download page currently exposes:

- Statistical Review of World Energy 2026 data workbook;
- consolidated narrow-format CSV;
- methodology and definitions;
- archive links for earlier editions.

Conclusion:

The authoritative primary download is available. This reduces the need to rely on the mirror as the long-term transport, but does not itself prove byte equivalence between the mirror file and the official 2026 download.

Required closure:

- acquire the official 2026 narrow CSV/workbook directly;
- record source byte hash and size;
- compare the source-faithful Total World variables used by EWD with the current pinned mirror transform;
- preserve vintage, because EI explicitly notes historical values can be revised between annual editions.

## Global Carbon Budget 2025

Current EWD provenance:

`science/data/experiments/gcb_direct_fossil_1990_2024.provenance.json`

Current transport:

Pinned compact transport copy from `datasets/co2-fossil-global`.

Official GCB source:

`https://globalcarbonbudget.org/datahub/the-latest-gcb-data-2025/`

The official data hub exposes the `Global Carbon Budget v2025` workbook directly.

The peer-reviewed GCB 2025 paper explicitly distinguishes fossil-emission categories including:

- coal;
- oil;
- natural gas;
- cement;
- flaring;
- other.

This matches the categories retained in the EWD compact snapshot.

EWD's direct-emissions target intentionally uses only:

`coal + oil + natural gas`

while keeping cement, flaring and other explicit but excluded.

Conclusion:

The experiment boundary is primary-source consistent. Remaining closure is byte/value lineage from the official workbook to the compact 1990-2024 EWD snapshot.

Required closure:

- reconstruct the compact snapshot directly from the official GCB 2025 workbook;
- verify all six categories for 1990-2024;
- hash the official workbook and deterministic derived snapshot;
- retain the current warning that this is a current revised GCB 2025 vintage and not an as-of-origin real-time vintage backtest.

## Result of this follow-up

No evidence was found that requires changing:

- the current World HDI values;
- the WPP benchmark semantics;
- the EI processed boundary;
- the GCB coal/oil/gas direct-emissions boundary.

The remaining work is provenance closure, not model recalibration.

