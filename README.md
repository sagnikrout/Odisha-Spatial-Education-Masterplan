# Odisha Spatial School Education Masterplan (2026-2031)

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Optimization: Submodular Pareto MCLP](https://img.shields.io/badge/Optimization-Submodular%20Pareto%20MCLP-purple.svg)](https://en.wikipedia.org/wiki/Maximum_coverage_problem)
[![Geospatial: Pure Python & Matplotlib](https://img.shields.io/badge/GIS-Pure%20Python%20%7C%20Matplotlib-orange.svg)](https://matplotlib.org/)
[![Publishing Engine: Typst](https://img.shields.io/badge/Publishing-Typst%200.11-cyan.svg)](https://typst.app/)

Statewide operations research optimization, 314 Community Development Block GIS analysis, Public Works Department (PWD) hill cost calibration, and briefing suite for the 30 districts of Odisha.

## Problem statement

Under the Right to Education (RTE) Act of 2009, primary schooling saturation reached 69.9% baseline coverage within a 1 km radius. However, secondary education (Grades 9-10, 5 km norm) was not expanded at parity, creating a geographic transition barrier across the Eastern Ghats and forested corridors. In rugged blocks, walking distances exceed 7 to 10 kilometers over steep terrain, producing an acute drop in continuation rates between Grade 8 and Grade 9.

This platform replaces discretionary, demand-driven capital allocations with a mathematically bounded facility location framework that maximizes student coverage per public rupee spent while accounting for physical topography and civil construction costs.

## Document and deliverable suite

| Deliverable | Description | Extent | Path |
| :--- | :--- | :--- | :--- |
| Full masterplan publication | Complete institutional masterplan report with statewide analytics, 30 district atlas plates, operational rollout schedule, and 314-block register | 23 pages | [Odisha_Spatial_School_Education_Masterplan.pdf](Odisha_Spatial_School_Education_Masterplan.pdf) |
| Executive policy brief | Standalone executive dashboard of spatial findings, tier allocations, and econometric returns | 1 page | [Odisha_Education_Policy_Brief_2026.pdf](Odisha_Education_Policy_Brief_2026.pdf) |
| District GIS maps | Cartographic plates showing habitation clusters, buffer zones, and proposed interventions | 30 maps | [assets/district_maps/](assets/district_maps/) |

## Methodological architecture

1. **Facility location optimization (Submodular Pareto MCLP):** Formulates school placement as a Maximum Coverage Location Problem under capital constraints. Due to submodularity, greedy selection guarantees solutions within $(1 - 1/e) \approx 63.2\%$ of the global mathematical optimum (Nemhauser-Wolsey theorem). The algorithm constructs a Pareto frontier across budgets from 500 to 10,000 crore rupees.
2. **Topographic walking friction (Tobler hiking function):** Models physiological travel velocity across slope gradients in the Eastern Ghats:
   $$\text{Velocity}(\theta) = 6 \cdot e^{-3.5 \cdot |\tan(\theta) + 0.05|}$$
   Slopes between 10° and 20° impose walking friction multipliers of 1.8x to 2.5x relative to flat terrain, converting nominal 5 km buffer circles into compressed isochrones.
3. **PWD hill area cost calibration:** Adjusts civil engineering estimates using the Public Works Department schedule of rates (+18% to +30% in high-friction blocks) to reflect material haulage, ghat road transit, and slope grading expenses.
4. **Multimodal transit integration:** Where habitation density is too low to justify fixed campus construction, the model provisions 2,250 mini-buses (24 seats) and 1,308 feeder vans (12 seats) operated by local Mission Shakti Self-Help Groups, requiring 147.7 crore rupees in annual fleet operational expenditure.
5. **Staffing and residential allocation:** Allocates 10,136 secondary teacher posts with a 25% remote area hardship allowance and 3-year service commitment, 743 dedicated girls' hostels (100 beds each), and 331 cyclone-resilient coastal school retrofits.
6. **Econometric return model:** Projects 184,000 students retained over a 5-year rollout. Incorporating a rural wage premium of 42,000 rupees per year, a 70% labor absorption factor, and a 6% discount rate across working careers, the estimated net present value of direct gross state domestic product contribution is 5,322.9 crore rupees against a 6,931.8 crore rupee secondary capital outlay (0.77x direct wage benefit-cost ratio).

## Statewide multi-tier metrics

| Education tier | Distance norm | Existing schools | Baseline access | Target access | Proposed upgrades | Proposed new campuses | Transit hubs | Capital outlay |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Primary (Grades 1-5) | 1.0 km | 37,192 | 69.9% | 98.2% | 1,434 | 877 | 986 | 2,102.4 Cr |
| Upper Primary (Grades 6-8) | 3.0 km | 13,430 | 62.6% | 97.8% | 1,812 | 1,055 | 1,172 | 3,490.1 Cr |
| Secondary (Grades 9-10) | 5.0 km | 6,066 | 52.3% | 97.2% | 2,340 | 1,364 | 1,507 | 6,931.8 Cr |
| Higher Secondary (Grades 11-12) | 7.0 km | 1,644 | 41.9% | 96.5% | 2,935 | 1,630 | 1,722 | 11,925.1 Cr |
| **Total (All tiers)** | - | **58,332** | - | - | **8,521** | **4,926** | **5,387** | **24,449.4 Cr** |

### Secondary operational provisions
- Secondary subject teachers (1:30 pupil-teacher ratio): 10,136 posts
- Girls' residential hostels (100 beds): 743 facilities
- Student transit fleet: 2,250 mini-buses and 1,308 feeder vans
- Annual transit fleet operating expenditure: 147.7 crore rupees per year
- Cyclone-resilient campus retrofits: 331 campuses

## Repository structure

```
Map2needs/
├── engine/
│   └── statewide_analyzer.py        # Submodular Pareto MCLP & demographic engine
├── typst/
│   ├── masterplan.typ                   # 23-page publication masterplan layout
│   └── policy_brief.typ                 # 1-page policy brief layout
├── assets/
│   ├── district_maps/                   # 30 district GIS maps (dist_*.png)
│   └── chart_*.png                      # 6 statewide analytical charts
├── tests/
│   └── test_masterplan_suite.py         # Complete verification test suite
├── odisha_districts.geojson             # Survey of India district boundaries
├── odisha_statewide_assessment.json     # Calibrated assessment dataset
├── build.py                             # Pipeline build orchestrator
├── generate_district_maps.py            # 30-district cartographic plate generator
├── generate_analytical_charts.py        # 6 publication analytical charts generator
├── requirements.txt                     # Lean Python dependencies
├── LICENSE                              # MIT License
└── README.md                            # System documentation
```

## Replication and execution

### Prerequisites

- Python 3.13+ with `pip`
- [Typst](https://typst.app/) 0.11+ (native binary in PATH, `~/.local/bin/typst`, or WSL)

### Quick start

```bash
# 1. Install dependencies (numpy, matplotlib, pypdf)
pip install -r requirements.txt

# 2. Run complete end-to-end build (assessment, charts, maps, typst, tests)
python build.py --all
```

### Stage-by-stage execution

```bash
# Step 1: Run spatial & operations research assessment
python build.py --assess

# Step 2: Render 6 analytical charts (fast: ~3 seconds)
python build.py --charts

# Step 3: Render all 30 district GIS maps and charts
python build.py --maps

# Step 4: Compile Typst publication documents
python build.py --typst

# Step 5: Run test suite
python build.py --test
```

Direct unittest execution:
```bash
python -m unittest tests/test_masterplan_suite.py
```

## Scope notice

This system is an operations research model developed for academic policy analysis and infrastructure planning. Coordinates, boundary polygons, and unit costs are modeled approximations based on public data sources. Administrative deployment requires ground verification by state authorities.

## License

MIT License (see [LICENSE](LICENSE)).
