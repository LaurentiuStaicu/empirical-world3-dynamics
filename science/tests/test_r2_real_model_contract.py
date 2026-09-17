from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "science" / "src" / "world3_empirical" / "real_model_contract.py"
SPEC = importlib.util.spec_from_file_location("r2_real_model_contract", MODULE_PATH)
assert SPEC and SPEC.loader
R2 = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = R2
SPEC.loader.exec_module(R2)
CONTRACT_PATH = ROOT / "science" / "configs" / "real_model_structure.json"


class R2StructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = R2.RealModelContract.load(CONTRACT_PATH)
        cls.payload = cls.contract.payload

    def test_conservative_reference_core_is_immutable(self):
        architecture = self.payload["architecture"]
        self.assertFalse(architecture["clean_room_topology"])
        self.assertFalse(architecture["reference_core_mutable"])
        self.assertEqual(
            architecture["reference_model"]["source"],
            "science/vendor/world3_03/World3_03_Scenarios.mdl",
        )
        self.assertEqual(
            [baseline["id"] for baseline in architecture["comparison_baselines"]],
            ["bau", "bau2", "bau_hybrid_2026"],
        )

    def test_machine_readable_schema_has_stocks_flows_auxiliaries_units_and_roles(self):
        kinds = set()
        for module in self.payload["modules"]:
            for variable in module["variables"]:
                kinds.add(variable["kind"])
                self.assertTrue(variable["unit"])
                self.assertTrue(variable["dimension"])
                self.assertIn(variable["evidence_role"], self.payload["evidence_roles"])
        self.assertEqual(kinds, {"stock", "flow", "auxiliary"})

    def test_stock_accounting_and_dimensions_are_closed(self):
        self.contract.validate()

    def test_all_candidate_interfaces_are_inactive_and_noncentral(self):
        for candidate in self.payload["candidate_interfaces"]:
            self.assertFalse(candidate["active_by_default"])
            self.assertFalse(candidate["central"])
            interface = self.contract.candidate(candidate["id"])
            self.assertFalse(interface.active)
            self.assertFalse(interface.central)
            self.assertFalse(interface.promotion_allowed)

    def test_inactive_interfaces_are_exact_noops_even_at_extremes(self):
        interface = self.contract.candidate("energy_accounting_emissions")
        reference = {
            "zero": 0.0,
            "tiny": 1e-300,
            "large": 1e300,
            "nested": {"series": [-1e250, 0.0, 1e250]},
        }
        result = interface.apply(
            reference,
            signals=(
                R2.Signal(
                    "observed_primary_energy",
                    1e300,
                    "PJ/year",
                    R2.EvidenceRole.OBSERVED_INPUT,
                ),
            ),
        )
        self.assertEqual(result, reference)
        self.assertIsNot(result, reference)
        self.assertIsNot(result["nested"], reference["nested"])

    def test_nonfinite_signals_are_rejected(self):
        for value in (math.nan, math.inf, -math.inf):
            with self.assertRaises(ValueError):
                R2.Signal(
                    "bad",
                    value,
                    "1",
                    R2.EvidenceRole.DIAGNOSTIC,
                )

    def test_rejected_resource_to_eroi_coupling_cannot_return(self):
        interface = self.contract.candidate("net_energy")
        with self.assertRaisesRegex(ValueError, "Rejected coupling"):
            interface.apply(
                {"population": [1.0]},
                coupling_id="world3_resource_fraction_to_fossil_eroi",
            )

    def test_activation_does_not_silently_create_dynamics(self):
        interface = self.contract.candidate("energy_accounting_emissions")
        interface.active = True
        with self.assertRaisesRegex(RuntimeError, "interfaces only"):
            interface.apply({"population": [1.0]})

    def test_s1_s10_are_all_required_for_promotion(self):
        interface = self.contract.candidate("energy_accounting_emissions")
        for gate in R2.GATE_IDS[:-1]:
            interface.set_gate(gate, R2.GateStatus.PASS)
        self.assertFalse(interface.promotion_allowed)
        interface.set_gate("S10", R2.GateStatus.PASS)
        self.assertTrue(interface.promotion_allowed)

    def test_candidate_selection_is_experiment_only(self):
        selected = self.payload["selected_prospective_candidate"]
        self.assertEqual(selected["id"], "energy_accounting_emissions")
        self.assertEqual(selected["decision"], "selected_for_experiment_only")
        self.assertFalse(selected["central_promotion"])


class World3ReferenceGuardTests(unittest.TestCase):
    def test_adapter_sanitization_policy_is_non_equation_only(self):
        adapter = (
            ROOT / "science" / "src" / "world3_empirical" / "world3_03.py"
        ).read_text(encoding="utf-8")
        self.assertIn("authoritative ``.mdl`` file is preserved byte-for-byte", adapter)
        self.assertIn("non-equation directive removed", adapter)
        self.assertIn('return normalized.replace(directive, "", 1)', adapter)

    def test_reference_model_is_not_modified_by_r2_files(self):
        payload = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        self.assertEqual(
            payload["architecture"]["reference_model"]["equation_policy"],
            "preserve_authoritative_equations",
        )


if __name__ == "__main__":
    unittest.main()
