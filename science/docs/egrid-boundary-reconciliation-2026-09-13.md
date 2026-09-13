# eGRID plant/unit/generator boundary reconciliation

This post-hoc audit follows the four plants that dominate the raw persistence
errors through the official eGRID plant, unit and generator sheets for data
years 2021–2023. It does not alter the central model, remove observations or
estimate a new efficiency parameter.

The three official EPA workbooks are verified against the previously recorded
SHA-256 hashes before extraction. Reproduce the compact evidence file with:

```sh
python3 scripts/audit_egrid_boundaries.py \
  eGRID2021_data.xlsx egrid2022_data.xlsx egrid2023_data_rev2.xlsx
```

## Internal reconciliation

For all 12 reviewed plant-years:

- plant net generation equals the sum of generator net generation;
- plant unadjusted heat input equals the sum of unit heat input;
- plant unadjusted CO2 equals the sum of unit CO2.

This rules out a simple summation bug in the extraction. It does not establish
that generator generation from EIA-923 and unit heat input from EPA CAMD/CAPD
cover the same generating equipment in every year.

## California: generator coverage changes

AES Alamitos (ORIS 315) contains generators 3, 4 and 5 in the 2021 and 2022
generator sheets. The unit sheets already include the large CT1 and CT2 heat
inputs, but those units show no associated-generator count. In 2023 the
generator sheet additionally contains 1A, 1B and 1S, all reported as online
since 2020. Nameplate capacity rises from 1,115 to 1,793 MW and net generation
rises 5.24-fold, while heat input falls to 0.86 of its prior value. The implied
heat rate therefore falls from 51,666 to 8,493 Btu/net kWh.

AES Huntington Beach (ORIS 335) has only generator 2 in the 2021 and 2022
generator sheets, while the unit sheets include CT1 and CT2 heat input. In 2023
the generator sheet adds 1A, 1B and 1S, also marked online since 2020. Nameplate
capacity rises from 218 to 917.2 MW and net generation rises 30.23-fold while
heat input falls to 0.83 of its prior value. The implied heat rate falls from
268,014 to 7,327 Btu/net kWh.

The discontinuity is therefore an accounting-boundary change, not evidence of
a sudden physical efficiency gain. ORIS continuity is insufficient for a
temporal model when the generator roster changes or is incompletely represented.

## Louisiana: incompatible 2021 denominator

T J Labbe (ORIS 56108) and Hargis-Hebert (56283) keep the same two generators,
same 100.8 MW nameplate capacity and same two combustion units throughout the
three editions. In 2021 their generator-derived net generation is only 22 and
30 MWh, while CAMD unit heat input is 276,526 and 370,831 MMBtu. This creates
physically unusable ratios of approximately 12.57 and 12.36 million Btu/net
kWh. In 2022, generation rises 4,362-fold and 2,808-fold, but heat input only
3.77-fold and 2.50-fold; the ratios return to approximately 10,856 and 11,013
Btu/net kWh and remain similar in 2023.

The workbook evidence establishes a cross-source boundary incompatibility for
2021, but not its upstream cause. The audit must not relabel these values as an
outage or reporting error without checking the underlying EIA-923 and CAMD
records.

## Consequence for modelling

Raw plant-ratio persistence is invalid when either the generator inventory
changes or the prior ratio is outside a physically interpretable range. A
future estimator should use explicit eligibility rules defined from training
data only, track generator composition, and partially pool eligible plants by
prime mover and fuel. Because these rules were motivated by inspecting
2021–2023 outcomes, their performance must be assessed on different years.

The generated JSON preserves the 12 plant-year summaries, component records,
source labels, internal reconciliation flags and every year-to-year roster and
ratio change used above.
