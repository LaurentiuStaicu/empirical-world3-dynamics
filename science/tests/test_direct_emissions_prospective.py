import dataclasses
import json
import unittest

from world3_empirical.direct_emissions_experiment import (
    DEVELOPMENT,
    HOLDOUT,
    PROSPECTIVE_YEAR,
    ROOT,
    calibrate_scale,
    direct_co2_from_energy_mt,
    evaluate,
    load_records,
    serialize_predictions,
    serialize_results,
)


class DirectEmissionsProspectiveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = load_records()
        cls.payload, cls.rows = evaluate()

    def test_unit_conversion(self):
        self.assertAlmostEqual(
            direct_co2_from_energy_mt(coal_ej=1, oil_ej=1, gas_ej=1),
            224.0,
        )
        self.assertEqual(
            direct_co2_from_energy_mt(coal_ej=0, oil_ej=0, gas_ej=0),
            0.0,
        )
        for value in (-1, float("nan"), float("inf")):
            with self.subTest(value=value), self.assertRaises(ValueError):
                direct_co2_from_energy_mt(coal_ej=value, oil_ej=0, gas_ej=0)

    def test_target_boundary_excludes_process_categories(self):
        first = next(r for r in self.records if r.year == 1990)
        self.assertAlmostEqual(first.observed_direct_mt, 21646.4)

    def test_calibration_uses_development_only(self):
        development = [r for r in self.records if DEVELOPMENT[0] <= r.year <= DEVELOPMENT[1]]
        original = calibrate_scale(development)
        changed = [
            dataclasses.replace(r, observed_direct_mt=1e9)
            if r.year >= HOLDOUT[0] else r
            for r in self.records
        ]
        changed_development = [r for r in changed if DEVELOPMENT[0] <= r.year <= DEVELOPMENT[1]]
        self.assertEqual(original, calibrate_scale(changed_development))
        self.assertAlmostEqual(original, 0.9373506494829146)

    def test_declared_baseline_is_time_respecting(self):
        by_year = {r.year: r for r in self.records}
        row_2024 = next(row for row in self.rows if row["year"] == 2024)
        expected = (
            by_year[2023].observed_direct_mt / by_year[2023].fossil_energy_ej
        ) * by_year[2024].fossil_energy_ej
        self.assertAlmostEqual(row_2024["persistence_intensity_baseline_mt"], expected)

    def test_2025_prediction_is_unscored(self):
        record = next(r for r in self.records if r.year == PROSPECTIVE_YEAR)
        self.assertIsNone(record.observed_direct_mt)
        prospective = self.payload["prospective_2025_unscored"]
        self.assertFalse(prospective["observed_target_available"])

    def test_gate_result_is_diagnostic_only(self):
        statuses = {gate: body["status"] for gate, body in self.payload["gates"].items()}
        self.assertEqual(statuses["S7"], "FAIL")
        self.assertEqual(statuses["S8"], "FAIL")
        self.assertEqual(statuses["S9"], "FAIL")
        self.assertEqual(statuses["S10"], "PASS")
        self.assertFalse(self.payload["all_gates_pass"])
        self.assertEqual(self.payload["verdict"], "RETAIN AS DIAGNOSTIC")
        self.assertFalse(self.payload["central_model_promotion"])

    def test_sensitivity_detects_ranking_reversal(self):
        sensitivity = self.payload["sensitivity"]
        self.assertTrue(sensitivity["ranking_reversal"])
        self.assertLess(sensitivity["worst_skill_vs_baseline"], 0)
        self.assertGreater(sensitivity["best_skill_vs_baseline"], 0)

    def test_machine_readable_boundary_contract(self):
        contract = json.loads(
            (ROOT / "science/configs/energy_direct_emissions_boundary.json").read_text(encoding="utf-8")
        )
        self.assertFalse(contract["central"])
        self.assertEqual(contract["minimum_skill_vs_baseline"], 0.30)
        self.assertIn("World3-03", contract["frozen_comparators"])
        self.assertIn("BAU", contract["frozen_comparators"])
        self.assertIn("BAU2", contract["frozen_comparators"])
        self.assertIn("BAU Hybrid 2026", contract["frozen_comparators"])
        self.assertIn("world3_resource_fraction_to_fossil_eroi", contract["forbidden"])

    def test_forbidden_coupling_remains_excluded(self):
        excluded = self.payload["boundary"]["excluded_mechanisms"]
        self.assertIn("world3_resource_fraction_to_fossil_eroi", excluded)

    def test_frozen_artifacts_reproduce(self):
        results = ROOT / "science/data/experiments/energy_direct_emissions_prospective_2026-09-17.json"
        predictions = ROOT / "science/data/experiments/energy_direct_emissions_predictions_2026-09-17.csv"
        self.assertEqual(json.loads(results.read_text(encoding="utf-8")), json.loads(serialize_results(self.payload)))
        self.assertEqual(predictions.read_text(encoding="utf-8"), serialize_predictions(self.rows))


if __name__ == "__main__":
    unittest.main()
