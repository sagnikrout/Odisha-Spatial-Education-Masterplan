# Odisha Spatial School Education Masterplan (2026-2031)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Optimization: Submodular Pareto MCLP](https://img.shields.io/badge/Optimization-Submodular%20Pareto%20MCLP-purple.svg)](https://en.wikipedia.org/wiki/Maximum_coverage_problem)
[![Geospatial: Pure Python & Matplotlib](https://img.shields.io/badge/GIS-Pure%20Python%20%7C%20Matplotlib-orange.svg)](https://matplotlib.org/)
[![Publishing Engine: Typst](https://img.shields.io/badge/Publishing-Typst%200.11-cyan.svg)](https://typst.app/)

Statewide operations research optimization, 314 Community Development Block GIS analysis, Public Works Department (PWD) hill cost calibration, and briefing suite for the 30 districts of Odisha.

## Document and briefing suite

| Deliverable | Description | Path |
| :--- | :--- | :--- |
| Full masterplan report | 47-page masterplan with 314-block appendix | [Odisha_Spatial_School_Education_Masterplan.pdf](Odisha_Spatial_School_Education_Masterplan.pdf) |
| Executive presentation deck | 10-slide presentation | [Odisha_Spatial_Education_Executive_Deck.pdf](Odisha_Spatial_Education_Executive_Deck.pdf) |
| Executive policy brief | Single-page standalone summary | [Odisha_Education_Policy_Brief_2026.pdf](Odisha_Education_Policy_Brief_2026.pdf) |
| 30 district action memos | Localized 2-page action memos for administrative officers | [district_action_memos/](district_action_memos/) |
| 30 district GIS maps | Square 1:1 catchment maps | [assets/district_maps/](assets/district_maps/) |
| Visual presentation pack | Visual charts for reporting | [share_pack/](share_pack/) |

## Methodology

The platform models secondary school accessibility under National Education Policy (NEP 2020) and Right to Education (RTE) distance standards.

1. **Facility location optimization (Submodular Pareto MCLP):** Solves the Maximal Covering Location Problem with Nemhauser-Wolsey optimality bounds under capital budget constraints and computes marginal returns across the Pareto frontier.
2. **Topographic walking friction (Tobler hiking function):** Estimates walking speed and impedance on terrain slopes across the Eastern Ghats and forested areas (1.8x to 2.4x distance multiplier).
3. **PWD hill area cost index:** Applies a location cost factor (+18% to +30%) to civil construction in hill blocks for material transport and logistics.
4. **Demographic modeling across 314 CD blocks:** Tabulates habitations and school access for each administrative block in the state.
5. **Transit fleet allocation:** Assigns 1,027 mini-buses (24 seats) and 603 feeder vans (12 seats) with estimated operational expenditure of 68.0 crore rupees per year for drivers, fuel, vehicle upkeep, and chaperones.
6. **Staffing and residential allocation:** Models 9,144 subject teacher posts with a 25% remote area allowance and 3-year service commitment, 588 girls' hostels, and 396 cyclone-resistant coastal upgrades.
7. **Economic return estimation:** Projects 184,000 retained secondary school students over 5 years. Using a 0.75 labor absorption factor, estimated net present value of gross state domestic product contribution is 10,796.3 crore rupees against a 6,008.4 crore rupee secondary capital outlay (1.8x benefit-cost ratio).

## Statewide multi-tier and staffing metrics

| Education tier | Distance norm | Existing schools | Baseline access | Target access | Proposed upgrades | Proposed new campuses | Transport and hostel hubs | Capital outlay |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Primary (Grades 1-5) | 1.0 km | 32,836 | 74.9% | 99.2% | 1,333 | 730 | 719 | 968.18 Cr |
| Upper Primary (Grades 6-8) | 3.0 km | 12,238 | 67.9% | 99.2% | 1,726 | 934 | 899 | 2,279.79 Cr |
| Secondary (Grades 9-10) | 5.0 km | 5,744 | 59.1% | 91.6% | 2,182 | 1,195 | 1,172 | 6,008.42 Cr |
| Higher Secondary (Grades 11-12) | 7.0 km | 1,675 | 48.7% | 81.2% | 2,819 | 1,495 | 1,407 | 13,991.66 Cr |
| Total (All tiers) | - | 52,493 | - | - | 8,060 | 4,354 | 4,197 | 23,248.05 Cr |

### Secondary operational provisions
- Secondary subject teachers (1:30 pupil-teacher ratio): 9,144 posts
- Girls' residential hostels: 588 facilities
- Student transit fleet: 1,027 mini-buses and 603 feeder vans
- Cyclone resilient school retrofits: 396 campuses

## Project structure

```
Map2needs/
├── backend/
│   └── spatial_engine/
│       └── statewide_analyzer.py        # Submodular Pareto MCLP engine & demographic analysis
├── typst/
│   ├── masterplan.typ                   # High-speed 47-page masterplan publication
│   └── policy_brief.typ                 # 1-page executive briefing template
├── assets/
│   ├── district_maps/                   # 30 district GIS maps (4-zone modular layout)
│   └── chart_*.png                      # Statewide analytical charts
├── district_action_memos/               # 30 district action memos
├── share_pack/                          # Visual charts
├── tests/
│   └── test_masterplan_suite.py         # Unit and integration test suite
├── odisha_districts.geojson             # 30-district official survey boundaries
├── odisha_statewide_assessment.json     # Demographic and cost outputs
├── build.py                             # Master CLI pipeline orchestrator
├── generate_district_maps.py            # Map generation script
├── requirements.txt                     # Lean dependencies (numpy, matplotlib)
├── LICENSE                              # MIT License
└── README.md                            # Documentation
```

## Local execution

```bash
# 1. Install lean dependencies
pip install -r requirements.txt

# 2. Complete End-to-End Build (Assess, Map, Compile, Test)
python build.py --all

# Or run individual stages:
python build.py --assess   # Run spatial & OR assessment
python build.py --maps     # Render 30 district maps & 6 charts
python build.py --typst    # Compile publication PDFs with Typst
python build.py --test     # Run verification test suite
```

## Scope notice

This project is a simulation and planning model developed for research and policy analysis. Habitation coordinates and unit costs are modeled approximations. Implementation requires field verification by state and local administrative bodies.

## License
MIT License (see LICENSE).
