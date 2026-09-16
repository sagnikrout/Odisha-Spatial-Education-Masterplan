"""
Odisha Spatial Education Masterplan: Pipeline Build & Orchestration Engine
Builds statewide assessments, renders 30 district atlas plates, and compiles Typst publications.
"""

import os
import sys
import time
import argparse
import subprocess
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_typst_command(root_dir, typ_file, out_pdf):
    """
    Resolves the typst command for compiling documents across Windows, Linux, and WSL.
    Prefers native typst if available in PATH or local bin, else uses WSL environment on Windows.
    """
    typst_path = shutil.which("typst")
    if typst_path:
        return [typst_path, "compile", "--root", root_dir, typ_file, out_pdf]

    local_bin = os.path.expanduser("~/.local/bin/typst")
    if os.path.exists(local_bin):
        return [local_bin, "compile", "--root", root_dir, typ_file, out_pdf]

    if sys.platform == "win32":
        wsl_bin = shutil.which("wsl")
        if wsl_bin:
            def to_wsl(p):
                p_norm = os.path.abspath(p).replace("\\", "/")
                if len(p_norm) >= 2 and p_norm[1] == ":":
                    return f"/mnt/{p_norm[0].lower()}{p_norm[2:]}"
                return p_norm

            wsl_root = to_wsl(root_dir)
            wsl_typ = to_wsl(typ_file)
            wsl_pdf = to_wsl(out_pdf)
            return ["wsl", "-u", "sagnik", "/home/sagnik/.local/bin/typst", "compile", "--root", wsl_root, wsl_typ, wsl_pdf]

    raise FileNotFoundError(
        "Typst executable not found in PATH, ~/.local/bin/typst, or WSL. "
        "Please install Typst (e.g. winget install Typst.Typst, or cargo install --locked typst-cli)."
    )


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
    subprocess.run(get_typst_command(BASE_DIR, brief_typ, brief_pdf), cwd=BASE_DIR, check=True)
    print(f"Generated {brief_pdf} ({os.path.getsize(brief_pdf) / 1024:.1f} KB)")

    # 2. Comprehensive Masterplan Publication (37 pages)
    master_typ = os.path.join(BASE_DIR, "typst", "masterplan.typ")
    master_pdf = os.path.join(BASE_DIR, "Odisha_Spatial_School_Education_Masterplan.pdf")
    print(f"Compiling {master_pdf}...")
    subprocess.run(get_typst_command(BASE_DIR, master_typ, master_pdf), cwd=BASE_DIR, check=True)
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
