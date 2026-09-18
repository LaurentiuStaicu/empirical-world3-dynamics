#!/usr/bin/env python3
"""Numerical integration convergence diagnostic for the retained World3-03 core."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile

import numpy as np

from world3_empirical.world3_03 import (
    WORLD3_03_OUTPUTS,
    _import_pysd,
    _sanitized_model_text,
    _source_model_path,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "configs" / "system_dynamics_conformity.json"


def run_at_step(step: float) -> dict[str, np.ndarray]:
    pysd = _import_pysd()
    source = _source_model_path()
    years = np.arange(1900, 2101, dtype=float)
    with tempfile.TemporaryDirectory(prefix="world3_sd_numerics_") as directory:
        temporary_model = Path(directory) / source.name
        temporary_model.write_text(_sanitized_model_text(source), encoding="utf-8")
        model = pysd.read_vensim(temporary_model)
        raw = model.run(
            params={"scenario": 2},
            return_columns=list(WORLD3_03_OUTPUTS.values()),
            return_timestamps=years,
            time_step=step,
        )
    if not np.isfinite(raw.to_numpy(dtype=float)).all():
        raise SystemExit(f"BLOCKER: non-finite World3 output at time_step={step}")
    return {
        name: raw[engine].to_numpy(dtype=float)
        for name, engine in WORLD3_03_OUTPUTS.items()
    }


def normalized_rmse(a: np.ndarray, b: np.ndarray) -> float:
    scale = max(float(np.max(np.abs(b))), 1e-12)
    return float(np.sqrt(np.mean((a - b) ** 2)) / scale)


def main() -> None:
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    diagnostic = config["numerical_convergence_diagnostic"]
    steps = [float(value) for value in diagnostic["time_steps_year"]]
    if steps != [0.5, 0.25, 0.125]:
        raise SystemExit("BLOCKER: numerical diagnostic requires 0.5/0.25/0.125 year steps")

    results = {step: run_at_step(step) for step in steps}
    metrics: dict[str, dict[str, float | bool]] = {}
    improved = 0

    for name in WORLD3_03_OUTPUTS:
        coarse = normalized_rmse(results[0.5][name], results[0.25][name])
        fine = normalized_rmse(results[0.25][name], results[0.125][name])
        converges = fine <= coarse * 1.05 + 1e-15
        improved += int(converges)
        metrics[name] = {
            "nrmse_dt_0_5_vs_0_25": coarse,
            "nrmse_dt_0_25_vs_0_125": fine,
            "error_reduces_with_halving": converges,
        }

    share_converging = improved / len(metrics)
    max_fine = max(float(row["nrmse_dt_0_25_vs_0_125"]) for row in metrics.values())
    warning_threshold = float(diagnostic["provisional_warning_threshold"])

    if share_converging < 0.8:
        status = "BLOCKER"
    elif max_fine > warning_threshold:
        status = "WARNING"
    else:
        status = "PASS"

    payload = {
        "status": status,
        "scenario": "World3-03 scenario 2 / BAU2",
        "integration_engine": "PySD Euler",
        "time_steps_year": steps,
        "share_outputs_with_reduced_error_after_halving": share_converging,
        "max_fine_step_normalized_rmse": max_fine,
        "warning_threshold": warning_threshold,
        "outputs": metrics,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))

    if status == "BLOCKER":
        raise SystemExit(
            "BLOCKER: World3-03 numerical integration does not show adequate "
            "time-step convergence across retained outputs"
        )


if __name__ == "__main__":
    main()
