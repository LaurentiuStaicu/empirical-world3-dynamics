from __future__ import annotations

import json
import unittest

from world3_empirical.real_model import (
    REJECTED_R1_ENERGY_LINK,
    SELECTED_R2_CANDIDATE,
)
from world3_empirical.scenarios import project_root


class R2CandidateProtocolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = project_root()
        cls.path = cls.root / "configs" / "r2_energy_reinvestment_experiment.json"
        cls.protocol = json.loads(cls.path.read_text(encoding="utf-8"))

    def test_protocol_selects_only_the_declared_candidate_without_activation(self) -> None:
        self.assertEqual(self.protocol["candidate_interface"], SELECTED_R2_CANDIDATE)
        self.assertFalse(self.protocol["central_model_change_authorized"])
        self.assertEqual(self.protocol["status"], "predeclared_selected_not_activated")

    def test_rejected_r1_direct_coupling_stays_rejected(self) -> None:
        self.assertEqual(self.protocol["explicitly_rejected_reuse"], REJECTED_R1_ENERGY_LINK)

    def test_all_existing_inputs_are_registered_files(self) -> None:
        repository_root = self.root.parent
        for relative in self.protocol["existing_inputs"]:
            self.assertTrue((repository_root / relative).is_file(), relative)

    def test_structural_and_predictive_gate_states_are_explicit(self) -> None:
        gates = self.protocol["structural_gates"]
        self.assertEqual(tuple(gates), tuple(f"S{i}" for i in range(1, 11)))
        self.assertEqual(gates["S4"], "blocked_pending_bridge_observation")
        for gate in ("S7", "S8", "S9", "S10"):
            self.assertEqual(gates[gate], "not_run")

    def test_protocol_requires_same_information_set_and_dormant_baseline(self) -> None:
        temporal = self.protocol["temporal_validation"]
        self.assertIn("same World3 reference core", temporal["baseline_comparison"])
        self.assertIn("candidate interface dormant", temporal["baseline_comparison"])
        self.assertGreaterEqual(temporal["minimum_horizon_years"], 5)
        self.assertIn("Previously inspected holdouts", temporal["holdout_rule"])

    def test_double_counting_guard_is_mandatory(self) -> None:
        guard = self.protocol["double_counting_guard"].lower()
        self.assertIn("do not add", guard)
        self.assertIn("world3 resource-acquisition burden", guard)
        self.assertIn("non-overlapping", guard)


if __name__ == "__main__":
    unittest.main()
