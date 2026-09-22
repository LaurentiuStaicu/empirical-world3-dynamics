"""Legacy/reference wrapper around Pyworld3 1.1.\n\nThis module is not the retained EWD World3-03 structural baseline. Use\n``world3_empirical.world3_03.run_world3_03`` for the official World3-03 route.\n"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import numpy as np
import pandas as pd
from pyworld3 import World3

from .scenarios import Scenario, load_scenarios


OUTPUT_VARIABLES = {
    "population": "pop",
    "industrial_output": "io",
    "industrial_output_per_capita": "iopc",
    "food": "f",
    "food_per_capita": "fpc",
    "services_per_capita": "sopc",
    "nonrenewable_resources": "nr",
    "nonrenewable_resource_fraction": "nrfr",
    "persistent_pollution": "ppol",
    "persistent_pollution_index": "ppolx",
    "life_expectancy": "le",
}


@dataclass(frozen=True)
class SimulationResult:
    scenario: Scenario
    frame: pd.DataFrame

    def annual(self) -> pd.DataFrame:
        years = np.isclose(self.frame["year"] % 1, 0)
        return self.frame.loc[years].reset_index(drop=True)

    def peak_year(self, variable: str, start_year: float = 1900) -> float:
        subset = self.frame.loc[self.frame["year"] >= start_year]
        if variable not in subset:
            raise KeyError(f"Unknown output variable: {variable}")
        return float(subset.loc[subset[variable].idxmax(), "year"])


def run_scenario(
    scenario: str | Scenario = "world3_standard",
    *,
    year_min: int = 1900,
    year_max: int = 2100,
    dt: float = 0.5,
    extra_constants: Mapping[str, float] | None = None,
    fast: bool = True,
) -> SimulationResult:
    if isinstance(scenario, str):
        scenarios = load_scenarios()
        if scenario not in scenarios:
            raise KeyError(f"Unknown scenario {scenario!r}. Available: {sorted(scenarios)}")
        scenario_obj = scenarios[scenario]
    else:
        scenario_obj = scenario

    constants = dict(scenario_obj.constant_overrides)
    if extra_constants:
        constants.update(extra_constants)

    world = World3(year_min=year_min, year_max=year_max, dt=dt)
    try:
        world.init_world3_constants(**constants)
    except TypeError as exc:
        raise ValueError(f"Invalid World3 constant override: {exc}") from exc
    world.init_world3_variables()
    world.set_world3_table_functions()
    world.set_world3_delay_functions()
    world.run_world3(fast=fast)

    data: dict[str, np.ndarray] = {"year": world.time.copy()}
    for output_name, engine_name in OUTPUT_VARIABLES.items():
        data[output_name] = np.asarray(getattr(world, engine_name), dtype=float)
    frame = pd.DataFrame(data)
    if not np.isfinite(frame.to_numpy()).all():
        raise RuntimeError("World3 simulation produced non-finite output")
    return SimulationResult(scenario=scenario_obj, frame=frame)

\n\ndef run_scenario(\n    scenario: str | Scenario = "world3_standard",\n    *,\n    year_min: int = 1900,\n    year_max: int = 2100,\n    dt: float = 0.5,\n    extra_constants: Mapping[str, float] | None = None,\n    fast: bool = True,\n) -> SimulationResult:\n    """Backward-compatible alias for the legacy Pyworld3 route.\n\n    The retained EWD structural baseline is World3-03 via ``run_world3_03``.\n    New code should call ``run_legacy_scenario`` explicitly when it intends to\n    use the older Pyworld3/reference implementation.\n    """\n    warnings.warn(\n        "run_scenario() uses the legacy Pyworld3 1.1 reference/proxy route; "\n        "use run_world3_03() for the retained EWD World3-03 baseline or "\n        "run_legacy_scenario() when legacy behavior is intended.",\n        DeprecationWarning,\n        stacklevel=2,\n    )\n    return run_legacy_scenario(\n        scenario,\n        year_min=year_min,\n        year_max=year_max,\n        dt=dt,\n        extra_constants=extra_constants,\n        fast=fast,\n    )\n