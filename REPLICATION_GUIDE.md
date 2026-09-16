# Replication and verification guide

This document details the configuration and commands used to produce the masterplan outputs and verify results.

## 1. Unit cost configuration
1. Open `backend/spatial_engine/statewide_analyzer.py`.
2. Locate `TIER_STANDARDS` for the Secondary tier.
3. Review base unit costs:
   - `base_upgrade_cost_lakhs`: 85.0
   - `base_new_school_cost_lakhs`: 244.0
   - `base_migration_cost_lakhs`: 30.0
4. Execute analyzer:
   ```bash
   python backend/spatial_engine/statewide_analyzer.py
   ```
5. The analyzer computes metrics for all 30 districts and 314 CD blocks, applying the PWD hill cost index and transit operational expenses, setting the statewide secondary capital budget at 6,008.4 crore rupees.

## 2. Visual asset generation
1. Execute map generator:
   ```bash
   python generate_district_maps.py
   ```
2. Generates 30 square 1:1 district catchment maps and 6 analytical charts in `assets/`.

## 3. Document assembly (Typst Publication Suite)
1. Complete automated build:
   ```bash
   python build.py --all
   ```
2. Or compile documents individually via Typst:
   ```bash
   python build.py --typst
   ```
   Compiles:
   - `Odisha_Spatial_School_Education_Masterplan.pdf` (47 pages)
   - `Odisha_Education_Policy_Brief_2026.pdf` (1 page)

## 4. Test verification
Run the verification test suite:
```bash
python build.py --test
# Or directly via unittest:
python -m unittest tests/test_masterplan_suite.py
```
