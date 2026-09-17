from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class InfoClarSuiteContractTests(unittest.TestCase):
    def test_suite_window_is_application_entry_shell(self):
        application = (ROOT / "src" / "Application.vala").read_text(encoding="utf-8")
        meson = (ROOT / "meson.build").read_text(encoding="utf-8")
        self.assertIn("new SuiteWindow (this)", application)
        self.assertIn("'src/SuiteWindow.vala'", meson)

    def test_v11_four_panel_information_architecture(self):
        source = (ROOT / "src" / "SuiteWindow.vala").read_text(encoding="utf-8")
        for builder in (
            "build_chart_panel ()",
            "build_theory_panel ()",
            "build_dashboard_panel ()",
            "build_auxiliary_panel ()",
        ):
            self.assertIn(builder, source)
        self.assertIn("flow.max_children_per_line = 2", source)
        self.assertIn("flow.min_children_per_line = 1", source)
        self.assertIn("flow.homogeneous = false", source)

    def test_english_is_default_and_romanian_is_available(self):
        source = (ROOT / "src" / "SuiteWindow.vala").read_text(encoding="utf-8")
        self.assertIn("private bool romanian = false", source)
        self.assertIn('new Gtk.ToggleButton.with_label ("EN")', source)
        self.assertIn('new Gtk.ToggleButton.with_label ("RO")', source)
        self.assertIn("en_button.active = true", source)
        self.assertIn("LABELS_EN", source)
        self.assertIn("LABELS_RO", source)

    def test_chart_language_switch_covers_interactive_annotations(self):
        chart = (ROOT / "src" / "ChartView.vala").read_text(encoding="utf-8")
        self.assertIn("public void set_romanian", chart)
        self.assertIn('tr ("Year %d · %s", "Anul %d · %s")', chart)
        self.assertIn('tr ("Observed", "Observat")', chart)
        self.assertIn('tr ("Unit: ", "Unitate: ")', chart)

    def test_uniformisation_does_not_modify_scientific_release_files(self):
        conformance = (
            ROOT / "docs" / "INFOCLAR_MODEL_SUITE_DESIGN_STANDARD_V1_1.md"
        ).read_text(encoding="utf-8")
        self.assertIn("presentation-layer change", conformance)
        self.assertIn("modify BAU, BAU2 or BAU Hybrid 2026 central curves", conformance)
        self.assertIn("R1 empirical-foundation contract remains authoritative", conformance)


if __name__ == "__main__":
    unittest.main()
