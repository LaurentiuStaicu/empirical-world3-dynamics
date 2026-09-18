"""Empirical World3 Dynamics (EWD) scientific core."""

from .model import OUTPUT_VARIABLES, SimulationResult, run_scenario
from .scenarios import Scenario, load_scenarios
from .world3_03 import WORLD3_03_OUTPUTS, World303Result, run_world3_03

__all__ = [
    "OUTPUT_VARIABLES",
    "Scenario",
    "SimulationResult",
    "WORLD3_03_OUTPUTS",
    "World303Result",
    "load_scenarios",
    "run_scenario",
    "run_world3_03",
]

__version__ = "0.1"
