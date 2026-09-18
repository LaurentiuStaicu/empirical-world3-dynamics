"""Frozen observation inputs used by the retained joint BAU Hybrid 2026 model.

This module contains only the observation contracts and deterministic loaders
needed by the joint scientific model. It deliberately excludes the legacy
per-indicator forecast layer that previously lived in build_bau2_e2026.py.

All local adapter files are part of the scientific input manifest. The FAOSTAT
archive is fetched and hash-verified by scripts/fetch_science_inputs.py before
the joint builder runs.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import zipfile

import pandas as pd

from .scenarios import project_root


ROOT = project_root()
RAW = ROOT / "data" / "raw" / "bau2_e2026" / "2026-08-28"
PROCESSED = ROOT / "data" / "processed"
BAU2 = ROOT / "outputs" / "world3_03_bau2.csv"
BAU = ROOT / "outputs" / "world3_03_bau.csv"


@dataclass(frozen=True)
class Indicator:
    key: str
    label: str
    unit: str
    observed: pd.Series
    model: pd.Series
    model_alt: pd.Series
    source: str
    source_url: str
    status: str
    benchmark: pd.Series | None = None
    lower: float | None = None
    upper: float | None = None


def _require_file(path: Path) -> Path:
    if not path.is_file():
        raise FileNotFoundError(
            f"Frozen scientific input is missing: {path.relative_to(ROOT)}"
        )
    return path


def load_faostat_food() -> pd.Series:
    archive = _require_file(RAW / "faostat_production_indices.zip")
    parts: list[pd.DataFrame] = []
    with zipfile.ZipFile(archive) as bundle:
        csv_name = next(
            name for name in bundle.namelist() if name.endswith("(Normalized).csv")
        )
        with bundle.open(csv_name) as handle:
            for chunk in pd.read_csv(handle, encoding="latin-1", chunksize=300_000):
                selected = chunk[
                    chunk["Area"].eq("World")
                    & chunk["Item"].eq("Food")
                    & chunk["Element"].eq(
                        "Gross per capita Production Index Number (2014-2016 = 100)"
                    )
                ][["Year", "Value"]]
                if not selected.empty:
                    parts.append(selected)
    if not parts:
        raise RuntimeError("FAOSTAT archive contains no World/Food per-capita series")
    frame = pd.concat(parts, ignore_index=True).drop_duplicates("Year")
    return frame.set_index("Year")["Value"].sort_index()


def load_hdi() -> pd.Series:
    path = _require_file(RAW / "undp_hdi_owid_adapter.csv")
    frame = pd.read_csv(path)
    world = frame.loc[frame["Entity"].eq("World")]
    if world.empty:
        raise RuntimeError("Frozen UNDP/OWID HDI adapter contains no World series")
    return world.set_index("Year")["Human Development Index"].sort_index()


def load_un_population() -> pd.Series:
    path = _require_file(RAW / "un_wpp2024_owid_adapter.csv")
    frame = pd.read_csv(path)
    world = frame.loc[frame["entity"].eq("World")].set_index("year")
    if world.empty:
        raise RuntimeError("Frozen UN WPP/OWID population adapter contains no World series")
    observed = world["population__sex_all__age_all__variant_estimates"]
    projected = world["population__sex_all__age_all__variant_medium__projected"]
    return (observed.combine_first(projected) / 1e9).sort_index()


def normalize(series: pd.Series, base_year: int) -> pd.Series:
    return 100.0 * series / float(series.loc[base_year])


def build_indicators() -> tuple[list[Indicator], list[Path]]:
    empirical = pd.read_csv(
        PROCESSED / "empirical_model_inputs_2026-08-28.csv"
    ).set_index("year")
    bau2 = pd.read_csv(_require_file(BAU2)).set_index("year")
    bau2.index = bau2.index.astype(int)
    bau = pd.read_csv(_require_file(BAU)).set_index("year")
    bau.index = bau.index.astype(int)

    fao_food = load_faostat_food()
    hdi = load_hdi()
    un_population = load_un_population()

    population = empirical["population"].dropna() / 1e9
    industry_pc = (
        empirical["industrial_output"] / empirical["population"]
    ).dropna()
    industry_pc = normalize(industry_pc, 2015)
    ghg_flow = normalize(empirical["fossil_co2_proxy"].dropna(), 1990)

    indicators = [
        Indicator(
            "population",
            "Populație mondială",
            "miliarde persoane",
            population,
            bau2["population"] / 1e9,
            bau["population"] / 1e9,
            "World Bank WDI SP.POP.TOTL",
            "https://api.worldbank.org/v2/country/WLD/indicator/SP.POP.TOTL",
            "observat până în 2025; valoarea 2025 poate fi estimată",
            benchmark=un_population,
            lower=0,
        ),
        Indicator(
            "industry_per_capita",
            "Producție industrială pe locuitor",
            "indice, 2015=100",
            industry_pc,
            normalize(bau2["industrial_output_per_capita"], 2015),
            normalize(bau["industrial_output_per_capita"], 2015),
            "World Bank WDI NV.IND.TOTL.KD / populație",
            "https://api.worldbank.org/v2/country/WLD/indicator/NV.IND.TOTL.KD",
            "proxy observat până în 2025; include construcții",
            lower=0,
        ),
        Indicator(
            "food_per_capita",
            "Producție alimentară pe locuitor",
            "indice FAO, 2014–2016=100",
            fao_food,
            normalize(bau2["food_per_capita"], 2015),
            normalize(bau["food_per_capita"], 2015),
            "FAOSTAT Production Indices, World, Food, gross per capita",
            "https://www.fao.org/faostat/en/#data/QI",
            "observat până în 2024; agregat fizic ponderat cu prețuri",
            lower=0,
        ),
        Indicator(
            "pollution_pressure",
            "Emisii antropice anuale (proxy)",
            "indice de flux, 1990=100",
            ghg_flow,
            normalize(bau2["persistent_pollution_generation_rate"], 1990),
            normalize(bau["persistent_pollution_generation_rate"], 1990),
            "World Bank / EDGAR proxy EN.GHG.CO2.MT.CE.AR5",
            "https://edgar.jrc.ec.europa.eu/dataset_ghg2025",
            (
                "observat până în 2024; comparație flux-la-flux cu generarea "
                "generică de poluare World3, nu cu stocul latent"
            ),
            lower=0,
        ),
        Indicator(
            "human_welfare",
            "Dezvoltare umană",
            "indice 0–1",
            hdi,
            bau2["human_welfare_index"],
            bau["human_welfare_index"],
            "UNDP Human Development Report 2025, HDI",
            "https://hdr.undp.org/data-center/documentation-and-downloads",
            "observat până în 2023; HDI nu este identic cu HWI World3",
            lower=0,
            upper=1,
        ),
    ]
    return indicators, [
        RAW / "faostat_production_indices.zip",
        RAW / "undp_hdi_owid_adapter.csv",
        RAW / "un_wpp2024_owid_adapter.csv",
    ]
