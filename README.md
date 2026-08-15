# 🗺️ Odisha Spatial School Education Masterplan (2026–2031)

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: Operations Research Masterplan](https://img.shields.io/badge/Status-Operations%20Research%20Platform-green.svg)]()
[![Optimization: PuLP MILP](https://img.shields.io/badge/Optimization-PuLP%20MILP%20%7C%20MCLP-purple.svg)]()
[![Geospatial: GeoPandas & Shapely](https://img.shields.io/badge/GIS-GeoPandas%20%7C%20Shapely-orange.svg)]()
[![PDF Engine: ReportLab](https://img.shields.io/badge/PDF-ReportLab%205.0-red.svg)]()

> **A statewide Operations Research optimization platform, 314 Community Development Block GIS analysis, universal secondary access strategy, and multi-tier capital outlay estimation model across all 30 districts of Odisha.**

---

## 📑 Quick Links
- 📄 **[Download Full 47-Page Masterplan PDF (15.1 MB)](Odisha_Spatial_School_Education_Masterplan.pdf)**
- 🗺️ **[Browse 30 District GIS Catchment Maps](assets/district_maps/)**
- 📊 **[View 6 Statewide Analytical Charts](assets/)**
- 📦 **[Curated Presentation & Share Pack](share_pack/)**

---

## 📌 Executive & Methodological Summary

Ensuring that every child—regardless of whether they reside in coastal plains, mineral plateaus, or the rugged Eastern Ghats—has access to secondary education within a safe, reachable distance is a core mandate of the **National Education Policy (NEP 2020)** and **Right to Education (RTE)** norms.

This project delivers an **advanced Operations Research and automated document generation pipeline** that integrates:
1. **Mathematical Facility Location Optimization (PuLP MILP / MCLP)**: Formulates and solves the Maximal Covering Location Problem to maximize student population coverage under strict capital budget constraints ($B$).
2. **Topographic Walking Friction (Tobler's Hiking Function)**: Models slope resistance and terrain walking impedance across Eastern Ghats and dense forest corridors ($1.8\times - 2.4\times$ multiplier).
3. **All 314 Community Development (CD) Blocks**: Micro-demographic habitation modeling across all 314 administrative blocks of Odisha.
4. **Social & Human Resource Framework**: Models Gender Parity Index (GPI), girls' dedicated hostels (588 facilities), subject teacher recruitments (9,144 posts at 1:30 PTR), and coastal cyclone resilience upgrades (396 schools).
5. **High-Precision Visual GIS Assets**: Generates 30 un-distorted 1:1 square district maps and 6 analytical charts.
6. **Publication-Grade 47-Page Masterplan PDF**: Compiled with running headers, footers, dynamic two-pass page numbering, mathematical formulation proofs, and a complete 314-block appendix matrix.

---

## 📊 Key Visual Highlights

| Malkangiri District GIS Catchment (5km Halos & Gaps) | The Spatial Accessibility Cliff (Class 8 → 9) |
| :---: | :---: |
| ![Malkangiri GIS Map](assets/district_maps/dist_malkangiri.png) | ![Accessibility Cliff Chart](assets/chart_dropout_cliff.png) |

| PuLP Operations Research Efficiency Frontier | Gender Parity & Girls' Residential Hostels |
| :---: | :---: |
| ![MCLP Frontier](assets/chart_mclp_frontier.png) | ![Gender Equity](assets/chart_gender_equity.png) |

---

## 📈 Statewide Multi-Tier & Staffing Assessment

| Education Tier | Distance Norm | Existing Schools | Baseline Access | Target Access | Proposed Upgrades | Proposed New Campuses | Transport & Hostel Hubs | Total Estimated Outlay |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Primary (Grades 1–5)** | 1.0 km | 32,836 | 74.9% | **99.2%** | 1,333 | 730 | 719 | **₹879.65 Cr** |
| **Upper Primary (Grades 6–8)** | 3.0 km | 12,238 | 67.9% | **99.2%** | 1,726 | 934 | 899 | **₹2,059.32 Cr** |
| **Secondary (Grades 9–10)** | 5.0 km | 5,744 | 59.1% | **91.6%** | 2,182 | 1,195 | 1,172 | **₹5,122.10 Cr** |
| **Higher Secondary (Grades 11–12)** | 7.0 km | 1,675 | 48.7% | **81.2%** | 2,819 | 1,495 | 1,407 | **₹11,755.75 Cr** |
| **Statewide Total (All Tiers)** | — | **52,493** | — | — | **8,060** | **4,354** | **4,197** | **₹19,816.82 Cr** |

### Additional Operational & Equity Provisions (Secondary Tier)
- **Secondary Subject Teachers (1:30 PTR)**: **9,144 Posts** (Math, Science, English, Social Science)
- **Girls' Dedicated Residential Hostels**: **588 Facilities** in remote tribal corridors
- **Coastal Cyclone Resilient School Upgrades**: **396 Campuses** across coastal deltaic belts

---

## 🏗️ Project Architecture

```
Map2needs/
├── backend/
│   └── spatial_engine/
│       └── statewide_analyzer.py      # PuLP MILP solver, Tobler friction & 314-block engine
├── assets/
│   ├── district_maps/                 # 30 high-resolution square 1:1 GIS district maps
│   ├── chart_*.png                    # 6 statewide analytical charts
│   └── page_*_preview.png             # Rendered preview pages of the 47-page PDF
├── share_pack/                        # Curated highlights & social visual assets
├── odisha_districts.geojson           # Official 30-district polygon boundary dataset
├── odisha_statewide_assessment.json   # Calculated multi-tier demographic & financial metrics
├── generate_district_maps.py          # Matplotlib geospatial visualization generator
├── generate_pdf_report.py             # ReportLab automated PDF compilation engine
├── requirements.txt                   # Python environment dependencies
├── REPLICATION_GUIDE.md               # Step-by-step replication guide
├── LICENSE                            # MIT License
└── README.md                          # Comprehensive project documentation
```

---

## 🚀 How to Run Locally

```bash
# 1. Clone repository & install dependencies
git clone https://github.com/sagnikrout/Odisha-Spatial-Education-Masterplan.git
cd Odisha-Spatial-Education-Masterplan
pip install -r requirements.txt

# 2. Run the Operations Research assessment engine (PuLP + 314 blocks)
python backend/spatial_engine/statewide_analyzer.py

# 3. Generate all 30 district GIS maps and 6 analytical charts
python generate_district_maps.py

# 4. Compile the 47-page publication-grade PDF masterplan
python generate_pdf_report.py
```

---

## ⚖️ Disclaimer & Academic Scope

> **Note:** This project is an **independent exploratory simulation and decision-support modeling platform** developed for research, methodology demonstration, and public policy discourse. All figures, habitation coordinates, and unit costs are modeled approximations designed to showcase geospatial operations research methodologies. They do not represent official government statistics or audited departmental expenditures. Policy execution requires field verification by local administrative authorities.

---

## 📄 License
Open source under the [MIT License](LICENSE).
