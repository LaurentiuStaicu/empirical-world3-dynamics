from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from world3_empirical.real_model import (
    REJECTED_R1_ENERGY_LINK,
    REQUIRED_BASELINES,
    R2StructuralError,
    SELECTED_R2_CANDIDATE,
    advance_stock,
    load_candidate_interfaces,
    load_structure,
    run_reference_core,
    schema_path,
    structure_path,
    validate_structure,
)
from world3_empirical.scenarios import project_root


class R2RealModelContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = load_structure()

    def test_machine_readable_schema_and_contract_exist(self) -> None:
        schema = json.loads(schema_path().read_text(encoding="utf-8"))
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertIn("module", schema["$defs"])
        self.assertIn("candidate", schema["$defs"])
        self.assertTrue(structure_path().is_file())

    def test_reference_core_is_conservative_and_baselines_are_frozen(self) -> None:
        core = self.payload["reference_core"]
        self.assertEqual(core["equation_policy"], "preserve_authoritative_equations")
        self.assertEqual(tuple(core["baseline_scenarios"]), REQUIRED_BASELINES)
        self.assertEqual(
            core["source_path"],
            "science/vendor/world3_03/World3_03_Scenarios.mdl",
        )

    def test_authoritative_world3_source_hash_is_unchanged(self) -> None:
        root = project_root()
        manifest = json.loads((root / "data" / "input_manifest.json").read_text(encoding="utf-8"))
        key = "science/vendor/world3_03/World3_03_Scenarios.mdl"
        expected = manifest["files"][key]
        actual = hashlib.sha256((root / "vendor" / "world3_03" / "World3_03_Scenarios.mdl").read_bytes()).hexdigest()
        self.assertEqual(actual, expected)

    def test_all_candidate_interfaces_are_dormant_and_noncentral(self) -> None:
        interfaces = load_candidate_interfaces(self.payload)
        self.assertGreaterEqual(len(interfaces), 1)
        self.assertTrue(all(not item.active for item in interfaces))
        self.assertTrue(all(not item.central for item in interfaces))
        selected = [item for item in interfaces if item.status == "selected_for_prospective_experiment"]
        self.assertEqual([item.id for item in selected], [SELECTED_R2_CANDIDATE])
        self.assertIn(REJECTED_R1_ENERGY_LINK, selected[0].forbidden_links)

    def test_dormant_interfaces_are_identity_maps_even_at_extremes(self) -> None:
        interface = next(
            item for item in load_candidate_interfaces(self.payload)
            if item.id == SELECTED_R2_CANDIDATE
        )
        for value in (0.0, 1.0, 1e-12, 1e30, -1e30, {"reference": "unchanged"}):
            self.assertEqual(interface.apply(value), value)

    def test_silent_activation_fails_closed(self) -> None:
        tampered = copy.deepcopy(self.payload)
        tampered["candidate_interfaces"][0]["active"] = True
        with self.assertRaises(R2StructuralError):
            validate_structure(tampered)

    def test_dimensional_mismatch_fails_before_simulation(self) -> None:
        tampered = copy.deepcopy(self.payload)
        population = tampered["modules"][0]
        births = next(item for item in population["quantities"] if item["id"] == "births")
        births["dimension"] = {"person": 1}
        with self.assertRaises(R2StructuralError):
            validate_structure(tampered)

    def test_incomplete_boundary_fails_before_simulation(self) -> None:
        tampered = copy.deepcopy(self.payload)
        del tampered["modules"][0]["boundary"]["excluded"]
        with self.assertRaises(R2StructuralError):
            validate_structure(tampered)

    def test_rejected_resource_to_eroi_link_cannot_disappear(self) -> None:
        tampered = copy.deepcopy(self.payload)
        selected = next(
            item for item in tampered["candidate_interfaces"]
            if item["id"] == SELECTED_R2_CANDIDATE
        )
        selected["forbidden_links"] = []
        with self.assertRaises(R2StructuralError):
            validate_structure(tampered)

    def test_stock_accounting_zero_and_boundary_conditions(self) -> None:
        self.assertEqual(advance_stock(0.0, inflow=0.0, outflow=0.0, dt=0.5), 0.0)
        self.assertEqual(advance_stock(10.0, inflow=0.0, outflow=2.0, dt=5.0), 0.0)
        with self.assertRaises(R2StructuralError):
            advance_stock(1.0, inflow=0.0, outflow=2.0, dt=1.0)
        with self.assertRaises(R2StructuralError):
            advance_stock(-1.0, inflow=0.0, outflow=0.0, dt=1.0)

    def test_constant_flow_accounting_is_timestep_robust(self) -> None:
        coarse = advance_stock(100.0, inflow=10.0, outflow=4.0, dt=1.0)
        fine = 100.0
        for _ in range(100):
            fine = advance_stock(fine, inflow=10.0, outflow=4.0, dt=0.01)
        self.assertAlmostEqual(coarse, fine, places=12)

    def test_scaffold_delegates_to_world3_without_candidate_transformation(self) -> None:
        sentinel = object()
        years = (1900, 2000, 2100)
        with patch("world3_empirical.real_model.run_world3_03", return_value=sentinel) as runner:
            result = run_reference_core(scenario=2, years=years, payload=self.payload)
        self.assertIs(result, sentinel)
        runner.assert_called_once_with(scenario=2, years=years)


if __name__ == "__main__":
    unittest.main()
