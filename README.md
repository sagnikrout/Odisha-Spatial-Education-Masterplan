# 🗺️ Odisha Spatial School Education Masterplan (Proof-of-Concept)

> **An exploratory, data-driven GIS optimization and decision-support simulation framework for school infrastructure planning and secondary access equity across all 30 districts of Odisha.**

---

## 📌 Project Overview

Ensuring that every child—regardless of whether they reside in the coastal plains or the rugged Eastern Ghats—has access to high school education within a safe, reachable distance is a cornerstone of the **National Education Policy (NEP 2020)** and **Right to Education (RTE)** norms.

This project is an **independent exploratory simulation prototype** developed to study how **Geographic Information Systems (GIS)** and **spatial buffer optimization** can help:
1. **Identify Spatial Accessibility Gaps**: Map habitations falling outside standard walking and transit thresholds (1km Primary, 3km Upper Primary, 5km Secondary, 7km Higher Secondary).
2. **Mitigate the Class 8 $\rightarrow$ Class 9 Dropout Cliff**: Address the steep drop in secondary transition rates observed in rugged and tribal terrain due to physical distance barriers.
3. **Model Targeted Interventions**: Compare the cost-efficiency of school upgrades, new greenfield campuses, and student transport/residential hostel linkages.
4. **Generate Automated Masterplan Reports**: Build publication-grade district visual profiles and financial estimates.

---

## 📊 Key Visual Highlights

| Malkangiri District GIS Catchment | Student Retention & Accessibility Cliff |
| :---: | :---: |
| ![Malkangiri GIS Map](assets/district_maps/dist_malkangiri.png) | ![Accessibility Cliff Chart](assets/chart_dropout_cliff.png) |

---

## 📑 Complete Document

The full 37-page publication-ready masterplan is available in this repository:
👉 **[Odisha_Spatial_School_Education_Masterplan.pdf](Odisha_Spatial_School_Education_Masterplan.pdf)**

---

## 🏗️ Pipeline Architecture & Repository Structure

```
Map2needs/
├── backend/
│   └── spatial_engine/
│       └── statewide_analyzer.py      # Spatial buffer model & multi-tier budget engine
├── assets/
│   ├── district_maps/                 # 30 high-resolution square 1:1 GIS district maps
│   └── chart_*.png                    # 4 statewide analytical charts
├── share_pack/                        # Curated highlights for sharing & social posts
├── odisha_districts.geojson           # Official 30-district polygon boundary dataset
├── odisha_statewide_assessment.json   # Calculated multi-tier demographic & financial metrics
├── generate_district_maps.py          # Matplotlib-based geospatial visualization generator
├── generate_pdf_report.py             # ReportLab automated PDF compilation engine
├── requirements.txt                   # Python environment dependencies
└── README.md                          # Project documentation
```

---

## 🚀 How to Run & Replicate Locally

### 1. Clone the repository & install dependencies
```bash
git clone https://github.com/<your-username>/Map2needs.git
cd Map2needs
pip install -r requirements.txt
```

### 2. Execute the spatial assessment engine
```bash
python backend/spatial_engine/statewide_analyzer.py
```

### 3. Generate all 30 district GIS maps and analytical charts
```bash
python generate_district_maps.py
```

### 4. Compile the final PDF masterplan report
```bash
python generate_pdf_report.py
```

---

## ⚖️ Disclaimer & Academic Scope

> **Note:** This project is an independent academic simulation and proof-of-concept developed by an enthusiast. All figures, habitation coordinates, and unit costs are modeled approximations designed to demonstrate geospatial decision-support methodologies. They do not represent official government statistics or audited departmental expenditures. Official policy planning requires field verification by local administrative authorities.

---

## 📄 License
Open source under the [MIT License](LICENSE).
