"""
Odisha Spatial Education Masterplan: Pipeline Build & Orchestration Engine
Builds statewide assessments, renders 30 district atlas plates, and compiles Typst publications.
"""

import os
import sys
import time
import argparse
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TYPST_BIN = os.path.expanduser("~/.local/bin/typst")
if not os.path.exists(TYPST_BIN):
    TYPST_BIN = "typst"


def run_assessment():
    print("\n[1/4] Running Operations Research Assessment Engine...")
    t0 = time.time()
    script = os.path.join(BASE_DIR, "backend", "spatial_engine", "statewide_analyzer.py")
    res = subprocess.run([sys.executable, script], cwd=BASE_DIR, check=True)
    print(f"Assessment complete in {time.time() - t0:.2f}s.")


def generate_maps():
    print("\n[2/4] Rendering 30 District Cartographic Plates & Analytical Charts...")
    t0 = time.time()
    script = os.path.join(BASE_DIR, "generate_district_maps.py")
    res = subprocess.run([sys.executable, script], cwd=BASE_DIR, check=True)
    print(f"Map and chart generation complete in {time.time() - t0:.2f}s.")


def compile_typst_documents():
    print("\n[3/4] Compiling Typst Publication Document Suite...")
    t0 = time.time()

    # 1. Executive Policy Brief (1 page)
    brief_typ = os.path.join(BASE_DIR, "typst", "policy_brief.typ")
    brief_pdf = os.path.join(BASE_DIR, "Odisha_Education_Policy_Brief_2026.pdf")
    print(f"Compiling {brief_pdf}...")
    subprocess.run([TYPST_BIN, "compile", "--root", BASE_DIR, brief_typ, brief_pdf], cwd=BASE_DIR, check=True)
    print(f"Generated {brief_pdf} ({os.path.getsize(brief_pdf) / 1024:.1f} KB)")

    # 2. Masterplan Report (47 pages)
    master_typ = os.path.join(BASE_DIR, "typst", "masterplan.typ")
    master_pdf = os.path.join(BASE_DIR, "Odisha_Spatial_School_Education_Masterplan.pdf")
    print(f"Compiling {master_pdf}...")
    subprocess.run([TYPST_BIN, "compile", "--root", BASE_DIR, master_typ, master_pdf], cwd=BASE_DIR, check=True)
    print(f"Generated {master_pdf} ({os.path.getsize(master_pdf) / (1024 * 1024):.2f} MB)")

    print(f"Typst compilation complete in {time.time() - t0:.2f}s.")


def run_tests():
    print("\n[4/4] Running Masterplan Verification Test Suite...")
    t0 = time.time()
    res = subprocess.run([sys.executable, "-m", "unittest", "tests/test_masterplan_suite.py"], cwd=BASE_DIR, check=True)
    print(f"Test suite passed in {time.time() - t0:.2f}s.")


def main():
    parser = argparse.ArgumentParser(description="Odisha Spatial Education Masterplan Orchestrator")
    parser.add_argument("--all", action="store_true", help="Execute complete pipeline (assess, maps, typst, test)")
    parser.add_argument("--assess", action="store_true", help="Run spatial and OR assessment")
    parser.add_argument("--maps", action="store_true", help="Render all district maps and charts")
    parser.add_argument("--typst", action="store_true", help="Compile Typst PDFs")
    parser.add_argument("--test", action="store_true", help="Run unit test suite")

    args = parser.parse_args()

    if not any([args.all, args.assess, args.maps, args.typst, args.test]):
        parser.print_help()
        sys.exit(1)

    t_start = time.time()
    if args.all or args.assess:
        run_assessment()
    if args.all or args.maps:
        generate_maps()
    if args.all or args.typst:
        compile_typst_documents()
    if args.all or args.test:
        run_tests()

    print(f"\nPipeline finished successfully in {time.time() - t_start:.2f}s total.")


if __name__ == "__main__":
    main()
