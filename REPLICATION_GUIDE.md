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

## 3. Document assembly
1. Compile full 47-page masterplan:
   ```bash
   python generate_pdf_report.py
   ```
2. Compile 10-slide executive presentation deck:
   ```bash
   python generate_executive_deck.py
   ```
3. Compile 1-page executive policy brief:
   ```bash
   python generate_policy_brief.py
   ```
4. Compile 30 district action memos:
   ```bash
   python generate_district_memos.py
   ```

## 4. Test verification
Run the test suite:
```bash
python -m unittest tests/test_masterplan_suite.py
```
