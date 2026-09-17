import csv
import json
import unittest
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent


class R1EmpiricalFoundationTests(unittest.TestCase):
    def _registry(self):
        with (ROOT / "data" / "registry.csv").open(encoding="utf-8", newline="") as handle:
            return {row["series_id"]: row for row in csv.DictReader(handle)}

    def test_empirical_layers_have_explicit_roles(self):
        registry = self._registry()
        self.assertEqual(
            registry["ei_primary_energy"]["status"],
            "ingested_snapshot_2026_08_30",
        )
        self.assertEqual(
            registry["aramendia_global_fossil_eroi"]["status"],
            "ingested_snapshot_2026_08_30",
        )
        self.assertEqual(
            registry["unido_world_iip_public_balanced"]["status"],
            "ingested_diagnostic_2026_09_08",
        )
        self.assertEqual(
            registry["technology_mineral_production"]["status"],
            "ingested_risk_registry_2026_09_08",
        )
        self.assertEqual(
            registry["world3_persistent_pollution"]["observation_type"],
            "latent",
        )

    def test_eroi_accounting_boundaries_remain_separate(self):
        frame = pd.read_csv(
            ROOT / "data" / "processed" / "aramendia_global_fossil_eroi_2024.csv"
        )
        expected = {
            "fossil_primary_eroi_including_indirect",
            "fossil_primary_eroi_direct_only",
            "fossil_final_eroi_including_indirect",
            "fossil_final_eroi_direct_only",
            "fossil_useful_eroi_including_indirect",
            "fossil_useful_eroi_direct_only",
        }
        self.assertTrue(expected.issubset(frame.columns))
        self.assertEqual((int(frame.year.min()), int(frame.year.max())), (1971, 2020))

    def test_external_forecasts_are_not_observations(self):
        payload = json.loads(
            (ROOT / "data" / "forecasts" / "eia-steo-2026-09-11.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertTrue(payload["records"])
        self.assertTrue(
            all(row["evidence_type"] == "forecast" for row in payload["records"])
        )

    def test_r1_does_not_promote_energy_or_minerals_into_central_model(self):
        manifest = json.loads(
            (REPO / "data" / "scenarios" / "bau_hybrid_2026_manifest.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(manifest["version"], "0.10.0")
        self.assertEqual(
            manifest["structural_model"], "official World3-03 scenario 2 (BAU2)"
        )
        self.assertFalse(
            any(key.startswith("energy") for key in manifest["central_parameters"])
        )
        self.assertEqual(
            set(manifest["central_parameters"]),
            {
                "resources",
                "industrial_output_ratio",
                "industrial_capital_life",
                "land_yield",
                "pollution_generation",
                "pollution_assimilation",
                "family_size",
            },
        )


if __name__ == "__main__":
    unittest.main()
