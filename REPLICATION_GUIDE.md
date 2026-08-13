# Odisha Spatial Education Masterplan: Replication & Verification Steps

The following document details the exact sequence of technical fixes, logic recalibrations, and compilation commands performed to produce the final, publication-grade `Odisha_Spatial_School_Education_Masterplan.pdf`. 

You can use these steps to replicate the environment, understand the applied logic, and independently verify the results.

---

## 1. Spatial Financial Engine Recalibration
**Goal:** Adjust the cost modeling to reflect realistic, modern infrastructure construction and boarding/transport costs (increasing the budget by ~10x).

**Steps Performed:**
1. Edited `backend/spatial_engine/statewide_analyzer.py`.
2. Located the `THRESHOLDS` configuration dictionary for the `Secondary` tier.
3. Updated the unit costs to increase the budget by a factor of ~3.75x to 10x depending on the tier. Specifically for `Secondary`:
   - `unit_cost_lakhs` updated to `244.0` (up from 65.0).
   - `migration_cost_lakhs` updated to `30.0` (up from 8.0).
4. **Command Executed:** 
   ```bash
   python backend/spatial_engine/statewide_analyzer.py
   ```
5. **Result:** This successfully recalculated the data for all 30 districts and overwrote `odisha_statewide_assessment.json` with the new financial metrics, bringing the total statewide Secondary tier budget to **₹2,474.1 Crores**.

---

## 2. Visual Asset Generator Fixes
**Goal:** Fix layout issues, map logic, and data hardcoding in the visual assets.

**Steps Performed:**
1. Edited `generate_district_maps.py`.
2. **Data Tier Fix:** Changed the map iteration loop to pull from `dist['tiers']['Secondary']` instead of the Primary tier. This ensured the 30 district maps were visualizing high schools instead of elementary schools.
3. **Aesthetic Fixes:**
   - Changed the background colours (`BG` and `PANEL_BG`) from harsh dark mode to a soft, printable `slate-50` (light grey-blue).
   - Redesigned the district layouts from a side-by-side horizontal squeeze to a stacked vertical layout (Top/Bottom, 14x14 figure size) for maximum legibility.
4. **Global Charts Logic Restoration:**
   - Rewrote the placeholder "text" charts back to actual programmatic `matplotlib` graphs.
   - **Dropout Chart:** Implemented a dual-line graph comparing Plain districts vs. Hilly districts and added the "Accessibility Cliff" red annotation pointer.
   - **Budget Chart:** Updated the hardcoded strings to match the new financial engine output (Smart Plan: ₹2,474.1 Crores vs. Old Approach: ₹12,000 Crores).
5. **Command Executed:**
   ```bash
   python generate_district_maps.py
   ```
6. **Result:** Generated 30 high-resolution district maps and 4 global charts inside the `assets/` directory.

---

## 3. PDF Assembly Engine Fixes
**Goal:** Resolve clipping, overlapping, and incorrect text formatting in the final PDF assembly.

**Steps Performed:**
1. Edited `generate_pdf_report.py`.
2. **Page Dimensions & Layouts:**
   - Adjusted `topMargin=52` and `bottomMargin=55` in the `SimpleDocTemplate` to prevent the text from overlapping with the blue running headers/footers.
   - Configured the map image embeds (`Image(map_path, width=420, height=420)`) to accommodate the new square, stacked aspect ratio. Wrapped the maps, headers, and tables in a `KeepTogether` block to prevent awkward page breaks.
3. **Table of Contents:** Removed hardcoded, incorrect page numbers from the TOC arrays.
4. **Data Table Fixes:** 
   - Replaced arbitrary mathematical multipliers (e.g., `* 0.6`, `* 0.5`) in the Primary and Higher Secondary comparison tables with the actual analytical values pulled from the JSON output.
   - Removed the 40-character truncation (`[:40]...`) on the district strategy texts so they display in full.
5. **Command Executed:**
   ```bash
   python generate_pdf_report.py
   ```
6. **Result:** Compiled all JSON data, styled paragraphs, and visual assets into the final 21.2 MB PDF report.

---

## How to Replicate from Scratch

If you wish to run the entire pipeline on a fresh machine, execute the following commands in order:

```bash
# 1. Ensure dependencies are installed
pip install -r requirements.txt

# 2. Run the spatial assessment engine to calculate math/costs
python backend/spatial_engine/statewide_analyzer.py

# 3. Generate all maps, charts, and visualizations
python generate_district_maps.py

# 4. Assemble the final PDF report
python generate_pdf_report.py
```
