# Primary-source provenance audit — 2026-09-18

## Scope

This audit follows the successful v0.1 reproducibility repair. It does not alter model equations, parameter ranges, the 128-candidate design, the 2018 selection cutoff, observation bridges, production refit, medoid selection, plausibility guardrails, observed values or retained scientific outputs.

The purpose is narrower: determine whether the data transports used by EWD can be traced to the relevant primary authority and distinguish exact primary verification from adapter/mirror verification.

The machine-readable findings are retained in `science/data/provenance/primary_source_audit_2026-09-18.json`.

## Status interpretation

- **PASS**: primary authority, definition and retained value/transport chain are verified to the stated scope.
- **WARNING**: no material numerical defect was found, but the primary transport/equivalence proof is incomplete.
- **BLOCKER**: provenance is insufficient for the scientific role.

## Findings

| Source | EWD role | Result | Main finding |
|---|---|---|---|
| FAOSTAT Production Indices | central food-per-capita observation | PASS | Clean-runner reproduction downloads the official FAO archive and verifies its frozen size and SHA-256 before use. |
| UN WPP 2024 | population benchmark / plausibility guardrail | WARNING | Checked World anchors differ from the current UN portal by only 1–4 persons, but the repository retains an OWID adapter rather than a frozen primary UN bulk file. |
| UNDP HDR 2025 HDI | central proxy for World3 HWI | WARNING | All eight World anchor values published in HDR 2025 Table 2 match the retained adapter exactly; the official complete time-series file is not yet frozen/hash-pinned in EWD. |
| Energy Institute 2026 | diagnostic/candidate energy evidence | WARNING | The pinned mirror reproduces every EWD base energy value exactly for 1965–2025, but independent byte equivalence against a fresh official EI download is not yet recorded. |
| Global Carbon Project 2025v15 | diagnostic direct-emissions target | WARNING | The EWD snapshot exactly matches its pinned transport; the exact primary Zenodo dataset/file is now identified and the 2024 primary category values round exactly to EWD, but a full direct primary-file comparison is not yet automated. |

## FAOSTAT

Primary authority: Food and Agriculture Organization of the United Nations.

Primary catalog:
https://data.fao.org/catalog/dataset/c978f18c-7f11-4564-a47d-fd92f6353b11

Frozen primary download used by EWD:
https://bulks-faostat.fao.org/production/Production_Indices_E_All_Data_(Normalized).zip

Frozen SHA-256:
`04c58034493d91f02e2495570d3864212ac870ec7f829a5f22577d143a6a8a72`

Frozen size:
`16167197` bytes.

EWD selects:

- Area = World
- Item = Food
- Element = Gross per capita Production Index Number (2014-2016 = 100)

The official FAO catalog describes the production indices as relative to base period 2014–2016 and gives time coverage through 2024. The same catalog contains stale supplemental prose referring to 2004–2006; this conflicts with its abstract, explicit base-period metadata and the actual element selected by EWD. The conflict is therefore retained as a metadata caveat rather than silently resolved.

The post-merge clean-runner reproduction fetched the file from the official FAO URL and passed the exact size/hash gate. This is sufficient for a PASS at the frozen-input level.

## UN World Population Prospects 2024

Primary authority:
United Nations, Department of Economic and Social Affairs, Population Division.

Primary page:
https://population.un.org/wpp

The UN describes WPP 2024 as its official population estimates and projections, with estimates from 1950 and projections through 2100, and recommends bulk CSV for advanced use.

EWD currently retains an OWID adapter. Checked World values are:

| Year | UN Data Portal | EWD adapter | Difference |
|---:|---:|---:|---:|
| 2022 | 8,021,407,192 | 8,021,407,196 | +4 |
| 2023 | 8,091,734,930 | 8,091,734,933 | +3 |
| 2024 | 8,161,972,573 | 8,161,972,574 | +1 |
| 2025 | 8,231,613,070 | 8,231,613,067 | -3 |

These differences are numerically immaterial for the global benchmark but prove that the adapter is not a byte-identical primary snapshot.

The remaining provenance task is to freeze `WPP2024_Demographic_Indicators_Medium.csv.gz` from the UN bulk distribution, record its checksum and compare the full World series used by the benchmark.

This source is not the central observed population calibration target, so the present issue is a provenance WARNING, not a central-model BLOCKER.

## UNDP HDI

Primary authority:
United Nations Development Programme, Human Development Report Office.

Primary downloads page:
https://hdr.undp.org/data-center/documentation-and-downloads

Official complete time-series link:
https://hdr.undp.org/sites/default/files/2025_HDR/HDR25_Composite_indices_complete_time_series.csv

The 2025 HDR Table 2 World HDI anchors are:

| Year | UNDP | EWD adapter |
|---:|---:|---:|
| 1990 | 0.608 | 0.608 |
| 2000 | 0.651 | 0.651 |
| 2010 | 0.707 | 0.707 |
| 2015 | 0.731 | 0.731 |
| 2020 | 0.742 | 0.742 |
| 2021 | 0.742 | 0.742 |
| 2022 | 0.752 | 0.752 |
| 2023 | 0.756 | 0.756 |

All published anchors match exactly.

However, HDI is a central observational proxy in EWD, and the retained file is still an OWID transport. Therefore full primary-file comparison and hash-pinning remain a higher-priority provenance task.

This transport issue is separate from the conceptual observation-model issue: HDI remains a proxy for, not a direct observation of, the World3 Human Welfare Index.

## Energy Institute 2026

Primary authority:
Energy Institute.

Official data page:
https://www.energyinst.org/statistical-review/resources-and-data-downloads

The official page exposes the 2026 Statistical Review and a consolidated narrow-format CSV. It also warns that historical data can be revised between editions.

EWD records a pinned transport through:

https://github.com/shanewhi/world-energy-data

commit:
`9fc01fc0ae5aea3955968f920e5cd1394fe5ad34`

source SHA-256:
`c19b4922cb08316b45d7024233e8cd9d35e14429ee8cf65ab767e647cefc1f95`

The seven base Total World series used by EWD match the pinned mirror exactly for every year 1965–2025:

- total primary energy;
- oil;
- gas;
- coal;
- nuclear;
- hydro;
- renewables.

Derived fossil/non-fossil totals and shares differ only through output rounding, with maximum observed absolute difference below `5e-8`.

Thus mirror-to-EWD provenance is verified. Independent official-download-to-mirror byte equivalence remains open.

Energy Institute data are currently diagnostic/candidate evidence rather than a central calibration target.

## Global Carbon Project

Primary authority:
Global Carbon Project.

Primary dataset record:
https://zenodo.org/records/17417124

DOI:
`10.5281/zenodo.17417124`

Version:
`2025v15`

Primary file:
`GCB2025v15_MtCO2_flat.csv`

Published MD5:
`3008e30d913af5926a83d0d0775fb72e`

The EWD 1990–2024 category snapshot is exactly equal to the pinned transport blob for every retained year/category.

The primary 2024 World values are approximately:

- coal: 15,805.254 MtCO2;
- oil: 12,470.596 MtCO2;
- gas: 8,009.828 MtCO2;
- cement: 1,472.817 MtCO2;
- flaring: 415.708 MtCO2;
- other: 424.376 MtCO2.

They round exactly to the one-decimal values retained by EWD.

The experiment intentionally uses only coal + oil + natural gas as its direct-combustion target. Cement, flaring and other are retained explicitly but excluded. This boundary must not be confused with total fossil CO2 including cement.

The remaining provenance task is a complete direct Zenodo-file-to-EWD row comparison. Until captured, the overall source remains WARNING even though no numerical discrepancy has been found.

## Scientific consequence

No evidence found in this audit justifies changing any current model value or retained scientific result.

The source status after this phase is:

- FAOSTAT: primary provenance closed;
- UN WPP: primary authority/numeric anchors verified, primary file closure open;
- UNDP HDI: primary authority/numeric anchors verified, primary file closure open;
- Energy Institute: transport transformation verified, official byte-equivalence open;
- GCB: exact primary dataset identified and key values reconciled, complete direct primary-file comparison open.

The next justified action is to close the remaining three transport gaps in this order:

1. UNDP HDI, because it is a central observational proxy.
2. UN WPP, because it participates in population guardrails/benchmarking.
3. Energy Institute and GCB direct-file equivalence, because they currently support diagnostic/candidate modules rather than central calibration.

No model-development milestone should be started from this audit alone.
