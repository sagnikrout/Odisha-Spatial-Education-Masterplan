"""
Unit and Integration Test Suite for Odisha Spatial Education Masterplan
Uses standard Python unittest framework for zero-dependency test execution.
"""

import os
import sys
import json
import math
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

def get_pdf_page_count(path):
    """Pure Python PDF page counter (zero third-party dependencies)."""
    with open(path, "rb") as f:
        content = f.read()
    import re
    pages = re.findall(rb"/Type\s*/Page\b", content)
    return len(pages)

JSON_PATH = os.path.join(BASE_DIR, "odisha_statewide_assessment.json")
GEOJSON_PATH = os.path.join(BASE_DIR, "odisha_districts.geojson")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
MAPS_DIR = os.path.join(ASSETS_DIR, "district_maps")

from engine.statewide_analyzer import (
    tobler_hiking_friction,
    DISTRICT_DATABASE,
    TIER_STANDARDS
)


class TestSpatialEngineMath(unittest.TestCase):
    """Unit tests for mathematical and econometric formulas."""

    def test_tobler_friction_flat_terrain(self):
        """Flat terrain (0 to 2.5 deg slope) should have a friction multiplier of 1.0x to 1.20x."""
        friction_0 = tobler_hiking_friction(0.0)
        friction_2 = tobler_hiking_friction(2.5)
        self.assertTrue(0.99 <= friction_0 <= 1.05, f"Friction at 0 deg: {friction_0}")
        self.assertTrue(1.05 <= friction_2 <= 1.25, f"Friction at 2.5 deg: {friction_2}")

    def test_tobler_friction_steep_ghats(self):
        """Steep hill terrain (10 to 20 deg slope) should yield friction multipliers between 1.8x and 3.6x."""
        friction_10 = tobler_hiking_friction(10.0)
        friction_14 = tobler_hiking_friction(14.5)
        friction_20 = tobler_hiking_friction(20.0)
        self.assertTrue(1.70 <= friction_10 <= 2.10, f"Friction at 10 deg: {friction_10}")
        self.assertTrue(2.20 <= friction_14 <= 2.70, f"Friction at 14.5 deg: {friction_14}")
        self.assertTrue(3.00 <= friction_20 <= 4.00, f"Friction at 20 deg: {friction_20}")

    def test_pwd_hill_cost_multiplier_bounds(self):
        """PWD Hill Cost multiplier should scale between 1.0x in plains and <= 1.35x in rugged hills."""
        for dist, data in DISTRICT_DATABASE.items():
            is_hilly = any(k.lower() in data["terrain"].lower() for k in ["hilly", "mountainous", "forest", "hill", "ghat", "steep"])
            slope = 14.5 if is_hilly else 2.5
            friction = tobler_hiking_friction(slope)
            mult = round(1.0 + 0.18 * max(0.0, friction - 1.0), 3)
            if not is_hilly:
                self.assertTrue(1.0 <= mult <= 1.05, f"{dist} plain multiplier {mult}x should be ~1.0x")
            else:
                self.assertTrue(1.15 <= mult <= 1.35, f"{dist} hill multiplier {mult}x out of expected bounds")

    def test_district_and_block_completeness(self):
        """Verify that all 30 districts and exactly 314 CD blocks of Odisha are present."""
        self.assertEqual(len(DISTRICT_DATABASE), 30, f"Expected 30 districts, found {len(DISTRICT_DATABASE)}")
        total_blocks = sum(len(d["blocks"]) for d in DISTRICT_DATABASE.values())
        self.assertEqual(total_blocks, 314, f"Expected 314 blocks, found {total_blocks}")

    def test_district_names_unique(self):
        """Verify no duplicate district names exist."""
        dist_names = list(DISTRICT_DATABASE.keys())
        self.assertEqual(len(dist_names), len(set(dist_names)))

    def test_block_names_within_districts_unique(self):
        """Verify no duplicate block names exist within any single district."""
        for dist, d_info in DISTRICT_DATABASE.items():
            blocks = d_info["blocks"]
            self.assertEqual(len(blocks), len(set(blocks)), f"Duplicate block found in district {dist}")

    def test_vulnerability_and_gpi_ranges(self):
        """Verify vulnerability scores are between 30 and 100, and GPI between 0.75 and 1.00."""
        for dist, d_info in DISTRICT_DATABASE.items():
            self.assertTrue(30 <= d_info["vulnerability"] <= 100, f"Invalid vulnerability score in {dist}")
            self.assertTrue(0.75 <= d_info["gpi"] <= 1.00, f"Invalid GPI in {dist}")


class TestAssessmentJSONIntegrity(unittest.TestCase):
    """Tests verifying the consistency and validity of the compiled statewide assessment dataset."""

    @classmethod
    def setUpClass(cls):
        if not os.path.exists(JSON_PATH):
            raise unittest.SkipTest(f"Assessment file {JSON_PATH} does not exist")
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            cls.assessment_data = json.load(f)

    def test_all_30_districts_in_json(self):
        self.assertEqual(len(self.assessment_data["districts"]), 30)
        self.assertEqual(self.assessment_data["metadata"]["total_districts"], 30)
        self.assertEqual(self.assessment_data["metadata"]["total_blocks"], 314)

    def test_four_tier_standards_present(self):
        tiers = self.assessment_data["statewide_totals"]
        for tier in ["Primary", "Upper Primary", "Secondary", "Higher Secondary"]:
            self.assertIn(tier, tiers)
            self.assertGreater(tiers[tier]["existing_schools"], 0)
            self.assertGreater(tiers[tier]["proposed_upgrades"], 0)
            self.assertGreater(tiers[tier]["proposed_new_schools"], 0)
            self.assertGreater(tiers[tier]["total_budget_cr"], 0.0)
            self.assertGreater(tiers[tier]["final_coverage_pct"], tiers[tier]["initial_coverage_pct"])

    def test_secondary_tier_targets_and_roi(self):
        sec = self.assessment_data["statewide_totals"]["Secondary"]
        self.assertGreaterEqual(sec["final_coverage_pct"], 90.0)
        self.assertGreater(sec["teachers_required"], 8000)
        self.assertGreaterEqual(sec["annual_transit_opex_cr"], 60.0)

        econ = self.assessment_data["metadata"]["economic_impact"]
        self.assertGreaterEqual(econ["total_students_saved_from_dropout_5yr"], 150000)
        self.assertGreaterEqual(econ["benefit_cost_ratio_roi"], 0.7)

    def test_pareto_frontier_monotonicity(self):
        """Coverage should monotonically increase with capital budget on the Pareto frontier."""
        frontier = self.assessment_data["metadata"]["pareto_frontier"]
        self.assertGreaterEqual(len(frontier), 5)
        for i in range(len(frontier) - 1):
            self.assertLessEqual(frontier[i]["budget_cr"], frontier[i+1]["budget_cr"])
            self.assertLessEqual(frontier[i]["coverage_pct"], frontier[i+1]["coverage_pct"])


class TestDocumentOutputIntegrity(unittest.TestCase):
    """Integration tests verifying generated PDFs, page counts, and cartographic assets."""

    def test_masterplan_pdf_page_count(self):
        pdf_path = os.path.join(BASE_DIR, "Odisha_Spatial_School_Education_Masterplan.pdf")
        self.assertTrue(os.path.exists(pdf_path), "Masterplan PDF missing")
        count = get_pdf_page_count(pdf_path)
        self.assertTrue(20 <= count <= 25, f"Masterplan should be 20-25 pages, found {count}")

    def test_policy_brief_page_count(self):
        pdf_path = os.path.join(BASE_DIR, "Odisha_Education_Policy_Brief_2026.pdf")
        self.assertTrue(os.path.exists(pdf_path), "Policy Brief PDF missing")
        count = get_pdf_page_count(pdf_path)
        self.assertEqual(count, 1, f"Policy Brief should be exactly 1 page, found {count}")

    def test_all_30_district_maps_exist(self):
        self.assertTrue(os.path.exists(MAPS_DIR))
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        for d in data["districts"]:
            clean_name = d["district_name"].lower().replace(" ", "_")
            map_path = os.path.join(MAPS_DIR, f"dist_{clean_name}.png")
            self.assertTrue(os.path.exists(map_path), f"Missing map for district {d['district_name']} at {map_path}")


class TestCrossDocumentConsistency(unittest.TestCase):
    """Tests ensuring zero numerical drift and complete mathematical conservation across documents."""

    @classmethod
    def setUpClass(cls):
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            cls.data = json.load(f)

    def test_rollout_phase_strict_conservation(self):
        """Rollout phases must strictly sum to the secondary education totals."""
        phases = self.data["metadata"]["rollout_phases"]
        sec = self.data["statewide_totals"]["Secondary"]

        tot_up = sum(p["upgrades"] for p in phases.values())
        tot_new = sum(p["new_schools"] for p in phases.values())
        tot_tr = sum(p["transit_hubs"] for p in phases.values())
        tot_teach = sum(p["teachers"] for p in phases.values())
        tot_outlay = sum(p["outlay_cr"] for p in phases.values())

        self.assertEqual(tot_up, sec["proposed_upgrades"], "Phase upgrades do not conserve")
        self.assertEqual(tot_new, sec["proposed_new_schools"], "Phase new schools do not conserve")
        self.assertEqual(tot_tr, sec["proposed_transport_hubs"], "Phase transit hubs do not conserve")
        self.assertEqual(tot_teach, sec["teachers_required"], "Phase teachers do not conserve")
        self.assertAlmostEqual(tot_outlay, sec["total_budget_cr"], places=2, msg="Phase outlays do not conserve")

    def test_district_to_state_summation_conservation(self):
        """District secondary allocations must sum exactly to statewide totals."""
        sec = self.data["statewide_totals"]["Secondary"]
        dists = self.data["districts"]

        sum_up = sum(d["tiers"]["Secondary"]["proposed_upgrades"] for d in dists)
        sum_new = sum(d["tiers"]["Secondary"]["proposed_new_schools"] for d in dists)
        sum_tr = sum(d["tiers"]["Secondary"]["proposed_transport_hubs"] for d in dists)
        sum_teach = sum(d["tiers"]["Secondary"]["teachers_required"] for d in dists)
        sum_hostels = sum(d["tiers"]["Secondary"]["girls_hostels_proposed"] for d in dists)
        sum_cyclone = sum(d["tiers"]["Secondary"]["cyclone_resilient_upgrades"] for d in dists)
        sum_budget = sum(d["tiers"]["Secondary"]["total_budget_cr"] for d in dists)

        self.assertEqual(sum_up, sec["proposed_upgrades"])
        self.assertEqual(sum_new, sec["proposed_new_schools"])
        self.assertEqual(sum_tr, sec["proposed_transport_hubs"])
        self.assertEqual(sum_teach, sec["teachers_required"])
        self.assertEqual(sum_hostels, sec["girls_hostels_proposed"])
        self.assertEqual(sum_cyclone, sec["cyclone_resilient_upgrades"])
        self.assertAlmostEqual(sum_budget, sec["total_budget_cr"], places=1)

    def test_policy_brief_typst_bindings(self):
        """Policy brief Typst file must use dynamic bindings for key operational indicators."""
        brief_typ = os.path.join(BASE_DIR, "typst", "policy_brief.typ")
        with open(brief_typ, "r", encoding="utf-8") as f:
            content = f.read()

        # Must not contain old stale hardcoded values
        self.assertNotIn("9,144", content, "Stale teacher count found in policy_brief.typ")
        self.assertNotIn("588 Girls", content, "Stale girls hostel count found in policy_brief.typ")
        self.assertNotIn("396 cyclone", content, "Stale cyclone retrofit count found in policy_brief.typ")
        self.assertNotIn("59.1%", content, "Stale secondary baseline coverage found in policy_brief.typ")

        # Must use dynamic references
        self.assertIn("#sec.teachers_required", content)
        self.assertIn("#sec.girls_hostels_proposed", content)
        self.assertIn("#sec.cyclone_resilient_upgrades", content)

    def test_repository_agents_md_integrity(self):
        """Repository must have a consolidated AGENTS.md rulebook at root and no redundant .agents directory."""
        agents_md = os.path.join(BASE_DIR, "AGENTS.md")
        self.assertTrue(os.path.exists(agents_md), "Root AGENTS.md missing")
        with open(agents_md, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Professional Document Generation", content)
        self.assertIn("Tight Loop Performance Exception", content)

        legacy_agents = os.path.join(BASE_DIR, ".agents")
        self.assertFalse(os.path.exists(legacy_agents), "Legacy .agents directory should be removed")

    def test_engine_scripts_exist(self):
        """All engine scripts must exist under engine/ directory."""
        for script_name in ["statewide_analyzer.py", "generate_district_maps.py", "generate_analytical_charts.py"]:
            script_path = os.path.join(BASE_DIR, "engine", script_name)
            self.assertTrue(os.path.exists(script_path), f"Engine script {script_name} missing from engine/")


if __name__ == "__main__":
    unittest.main(verbosity=2)
