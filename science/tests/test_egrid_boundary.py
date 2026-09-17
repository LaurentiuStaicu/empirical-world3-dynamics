import unittest
import json
from pathlib import Path

from world3_empirical.egrid_boundary import compare_years, reconcile_boundaries


def plant(year, generation=100, heat=1000, co2=50, capacity=10):
    return dict(YEAR=year, ORISPL=1, PNAME="Plant", PLNGENAN=generation, UNHTI=heat,
                UNCO2=co2, NAMEPCAP=capacity, UNHTISRC="EPA")


def unit(year, heat=1000, co2=50):
    return dict(YEAR=year, ORISPL=1, UNITID="U", PRMVR="GT", UNTOPST="OP",
                FUELU1="NG", NUMGEN=1, HTIAN=heat, CO2AN=co2, HTIANSRC="EPA")


def generator(year, identifier="G", generation=100, capacity=10):
    return dict(YEAR=year, ORISPL=1, GENID=identifier, PRMVR="GT", GENSTAT="OP",
                FUELG1="NG", NAMEPCAP=capacity, GENNTAN=generation,
                GENERSRC="EIA", GENYRONL=2000)


class BoundaryTests(unittest.TestCase):
    def test_exact_components_reconcile(self):
        row = reconcile_boundaries(2021, [plant(2021)], [unit(2021)],
                                   [generator(2021)], [1])[0]
        self.assertTrue(row["plant_generation_matches_generator_sum"])
        self.assertTrue(row["plant_heat_matches_unit_sum"])
        self.assertTrue(row["plant_co2_matches_unit_sum"])
        self.assertEqual(row["reported_heat_rate_btu_per_net_kwh"], 10000)

    def test_boundary_mismatch_is_reported_not_hidden(self):
        row = reconcile_boundaries(2021, [plant(2021)], [unit(2021, 900)],
                                   [generator(2021, generation=90)], [1])[0]
        self.assertFalse(row["plant_generation_matches_generator_sum"])
        self.assertFalse(row["plant_heat_matches_unit_sum"])

    def test_roster_changes_are_explicit(self):
        before = reconcile_boundaries(2021, [plant(2021)], [unit(2021)],
                                      [generator(2021)], [1])[0]
        after = reconcile_boundaries(2022, [plant(2022, 200, 1800, 90, 20)],
                                     [unit(2022, 1800, 90)],
                                     [generator(2022, "G", 100), generator(2022, "N", 100)], [1])[0]
        transition = compare_years([before, after])[0]
        self.assertEqual(transition["added_generator_ids"], ["N"])
        self.assertEqual(transition["nameplate_capacity_ratio"], 2)

    def test_invalid_and_incomplete_inputs_are_rejected(self):
        with self.assertRaises(ValueError):
            reconcile_boundaries(2021, [plant(2021, generation=0)], [unit(2021)],
                                 [generator(2021)], [1])
        with self.assertRaises(ValueError):
            reconcile_boundaries(2021, [], [unit(2021)], [generator(2021)], [1])
        with self.assertRaises(ValueError):
            compare_years([
                reconcile_boundaries(2021, [plant(2021)], [unit(2021)], [generator(2021)], [1])[0],
                reconcile_boundaries(2023, [plant(2023)], [unit(2023)], [generator(2023)], [1])[0],
            ])

    def test_published_artifact_preserves_boundary_evidence(self):
        path = Path(__file__).parents[1] / "data/energy_audit/egrid-boundary-reconciliation.json"
        report = json.loads(path.read_text())
        self.assertEqual(len(report["plant_years"]), 12)
        self.assertFalse(report["central_model_changed"])
        self.assertTrue(all(
            row["plant_generation_matches_generator_sum"]
            and row["plant_heat_matches_unit_sum"]
            and row["plant_co2_matches_unit_sum"]
            for row in report["plant_years"]
        ))
        transitions = {
            (row["plant_id"], row["from_year"]): row for row in report["transitions"]
        }
        self.assertEqual(transitions[(315, 2022)]["added_generator_ids"], ["1A", "1B", "1S"])
        self.assertEqual(transitions[(335, 2022)]["added_generator_ids"], ["1A", "1B", "1S"])
        self.assertEqual(transitions[(56108, 2021)]["added_generator_ids"], [])
        self.assertGreater(transitions[(56108, 2021)]["net_generation_ratio"], 4000)
