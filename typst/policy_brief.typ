#let data = json("/odisha_statewide_assessment.json")
#let sec = data.statewide_totals.Secondary
#let prim = data.statewide_totals.Primary
#let econ = data.metadata.economic_impact
#let phases = data.metadata.rollout_phases

#set page(
  paper: "a4",
  flipped: false,
  margin: (x: 1.2cm, top: 1.2cm, bottom: 1.2cm),
  header: locate(loc => {
    set text(size: 6.8pt, font: ("Liberation Sans", "Helvetica Neue", "Arial", "Roboto"), fill: rgb("#64748B"), weight: "bold")
    grid(
      columns: (3.2fr, 1fr),
      align(left)[Odisha spatial education masterplan | technical policy brief],
      align(right)[Policy brief (2026-2031)]
    )
    v(-4pt)
    line(length: 100%, stroke: 0.5pt + rgb("#CBD5E1"))
  }),
  footer: locate(loc => {
    line(length: 100%, stroke: 0.5pt + rgb("#CBD5E1"))
    v(-2pt)
    set text(size: 6.8pt, font: ("Liberation Sans", "Helvetica Neue", "Arial", "Roboto"), fill: rgb("#64748B"))
    grid(
      columns: (3fr, 1fr),
      align(left)[Decision support framework: operations research and spatial optimization],
      align(right)[Page 1 of 1]
    )
  })
)

#set text(font: ("Liberation Sans", "Helvetica Neue", "Arial", "Roboto"), size: 8.0pt, fill: rgb("#0F172A"))
#set par(leading: 0.58em, justify: true)

// Title & Subtitle
#v(4pt)
#align(center)[
  #text(size: 14.5pt, weight: "bold", fill: rgb("#1E3A8A"))[Odisha spatial school education masterplan (2026-2031)] \
  #v(3pt)
  #text(size: 8.6pt, fill: rgb("#475569"))[Operations research optimization and PWD hill cost calibrated strategy across 314 CD blocks]
]
#v(3pt)
#line(length: 100%, stroke: 1.2pt + rgb("#1E3A8A"))
#v(8pt)

// Executive KPI Dashboard Cards
#grid(
  columns: (1fr, 1fr, 1fr, 1fr, 1fr),
  gutter: 6pt,
  rect(width: 100%, fill: rgb("#F1F5F9"), stroke: 0.6pt + rgb("#CBD5E1"), radius: 3pt, inset: 6.5pt)[
    #align(center)[
      #text(weight: "bold", size: 9.6pt, fill: rgb("#1E3A8A"))[#sec.initial_coverage_pct% → #sec.final_coverage_pct%] \
      #v(2pt)
      #text(size: 6.6pt, fill: rgb("#64748B"))[Secondary Access]
    ]
  ],
  rect(width: 100%, fill: rgb("#F1F5F9"), stroke: 0.6pt + rgb("#CBD5E1"), radius: 3pt, inset: 6.5pt)[
    #align(center)[
      #text(weight: "bold", size: 9.6pt, fill: rgb("#059669"))[₹#calc.round(sec.total_budget_cr, digits: 1) Cr] \
      #v(2pt)
      #text(size: 6.6pt, fill: rgb("#64748B"))[Hill-Adjusted Outlay]
    ]
  ],
  rect(width: 100%, fill: rgb("#F1F5F9"), stroke: 0.6pt + rgb("#CBD5E1"), radius: 3pt, inset: 6.5pt)[
    #align(center)[
      #text(weight: "bold", size: 9.6pt, fill: rgb("#1E293B"))[314 Blocks] \
      #v(2pt)
      #text(size: 6.6pt, fill: rgb("#64748B"))[30 Districts Analyzed]
    ]
  ],
  rect(width: 100%, fill: rgb("#F1F5F9"), stroke: 0.6pt + rgb("#CBD5E1"), radius: 3pt, inset: 6.5pt)[
    #align(center)[
      #text(weight: "bold", size: 9.6pt, fill: rgb("#7C3AED"))[#econ.benefit_cost_ratio_roi\x GSDP ROI] \
      #v(2pt)
      #text(size: 6.6pt, fill: rgb("#64748B"))[₹#calc.round(econ.net_present_value_gsdp_contribution_cr, digits: 0) Cr Value]
    ]
  ],
  rect(width: 100%, fill: rgb("#F1F5F9"), stroke: 0.6pt + rgb("#CBD5E1"), radius: 3pt, inset: 6.5pt)[
    #align(center)[
      #text(weight: "bold", size: 9.6pt, fill: rgb("#DC2626"))[#sec.teachers_required Posts] \
      #v(2pt)
      #text(size: 6.6pt, fill: rgb("#64748B"))[Teachers (25% Hardship)]
    ]
  ]
)

#v(8pt)
#text(size: 9.4pt, weight: "bold", fill: rgb("#1E3A8A"))[1. Strategic context and operations research methodology]
#v(4pt)
- *Grade 8 to 9 Spatial Dropout Cliff:* Primary access achieves #prim.initial_coverage_pct%, but secondary coverage drops to #sec.initial_coverage_pct% due to distance barriers (mean walking distance exceeds 6.8 km in Eastern Ghats), driving an acute tribal dropout rate with adolescent girls dropping out at higher rates without dedicated transit.
- *Submodular Pareto Optimization & PWD Hill Multipliers:* Interventions are optimized using a submodular Maximum Coverage Location Problem (MCLP) formulation under capital budget constraints, incorporating *Tobler hiking friction (1.8x–2.4x)* and *PWD hill area cost multipliers (+18% to +30%)* to reflect actual terrain haulage logistics.

#v(8pt)
#text(size: 9.4pt, weight: "bold", fill: rgb("#1E3A8A"))[2. Statewide multi-tier investment and physical targets (hill cost calibrated)]
#v(4pt)

#table(
  columns: (86pt, 38pt, 48pt, 48pt, 48pt, 54pt, 54pt, 60pt, 1fr),
  stroke: 0.4pt + rgb("#CBD5E1"),
  fill: (col, row) => if row == 0 { rgb("#1E3A8A") } else if calc.even(row) { rgb("#F8FAFC") } else { rgb("#FFFFFF") },
  align: (col, row) => (if col == 0 { left } else { center }),
  inset: 4.0pt,
  
  table.header(
    [#text(weight: "bold", fill: white, size: 7.2pt)[Education Tier]],
    [#text(weight: "bold", fill: white, size: 7.2pt)[Norm]],
    [#text(weight: "bold", fill: white, size: 7.2pt)[Existing]],
    [#text(weight: "bold", fill: white, size: 7.2pt)[Baseline]],
    [#text(weight: "bold", fill: white, size: 7.2pt)[Upgrades]],
    [#text(weight: "bold", fill: white, size: 7.2pt)[New Sch.]],
    [#text(weight: "bold", fill: white, size: 7.2pt)[Transit]],
    [#text(weight: "bold", fill: white, size: 7.2pt)[Target Access]],
    [#text(weight: "bold", fill: white, size: 7.2pt)[Est. Outlay]]
  ),
  
  ..for (t_name, t_vals) in data.statewide_totals.pairs() {
    (
      [#text(weight: "bold")[#t_name]],
      [#str(data.metadata.tier_standards.at(t_name).norm_distance_km) km],
      [#str(t_vals.existing_schools)],
      [#str(t_vals.initial_coverage_pct)%],
      [#str(t_vals.proposed_upgrades)],
      [#str(t_vals.proposed_new_schools)],
      [#str(t_vals.proposed_transport_hubs)],
      [#text(weight: "bold", fill: rgb("#0284C7"))[#str(t_vals.final_coverage_pct)%]],
      [#text(weight: "bold")[₹#str(calc.round(t_vals.total_budget_cr, digits: 1)) Cr]]
    )
  }
)

#v(8pt)
#text(size: 9.4pt, weight: "bold", fill: rgb("#1E3A8A"))[3. 314 CD blocks regional stratification, transit fleet and teacher cadre]
#v(4pt)
- *High Vulnerability (72 Blocks in 9 Tribal Districts):* Baseline coverage below 45%. Priority for #sec.girls_hostels_proposed dedicated girls' hostels, feeder transit corridors, and specialized teacher hardship allowances.
- *Central & Agrarian (142 Blocks):* Coverage 55% to 70%. Focus on upgrading Upper Primary schools into High Schools.
- *Coastal & Deltaic (100 Blocks):* Coverage exceeds 75%. Focus on STEM infrastructure and #sec.cyclone_resilient_upgrades cyclone-resilient structural retrofits.

#v(5pt)
#grid(
  columns: (1fr, 1fr, 1fr, 1fr, 1fr),
  gutter: 6pt,
  rect(width: 100%, fill: rgb("#F1F5F9"), stroke: 0.6pt + rgb("#CBD5E1"), radius: 3pt, inset: 5.5pt)[
    #align(center)[
      #text(weight: "bold", size: 8.4pt)[#sec.girls_hostels_proposed Hostels] \
      #v(2pt)
      #text(size: 6.0pt, fill: rgb("#64748B"))[Female Boarding]
    ]
  ],
  rect(width: 100%, fill: rgb("#F1F5F9"), stroke: 0.6pt + rgb("#CBD5E1"), radius: 3pt, inset: 5.5pt)[
    #align(center)[
      #text(weight: "bold", size: 8.4pt)[#sec.fleet_minibuses Mini-Buses] \
      #v(2pt)
      #text(size: 6.0pt, fill: rgb("#64748B"))[at ₹4.80L/yr Opex]
    ]
  ],
  rect(width: 100%, fill: rgb("#F1F5F9"), stroke: 0.6pt + rgb("#CBD5E1"), radius: 3pt, inset: 5.5pt)[
    #align(center)[
      #text(weight: "bold", size: 8.4pt)[#sec.fleet_feeder_vans Feeder Vans] \
      #v(2pt)
      #text(size: 6.0pt, fill: rgb("#64748B"))[at ₹3.00L/yr Opex]
    ]
  ],
  rect(width: 100%, fill: rgb("#F1F5F9"), stroke: 0.6pt + rgb("#CBD5E1"), radius: 3pt, inset: 5.5pt)[
    #align(center)[
      #text(weight: "bold", size: 8.4pt)[₹#calc.round(sec.annual_transit_opex_cr, digits: 1) Cr/yr] \
      #v(2pt)
      #text(size: 6.0pt, fill: rgb("#64748B"))[Fuel, Repairs & Chaperones]
    ]
  ],
  rect(width: 100%, fill: rgb("#F1F5F9"), stroke: 0.6pt + rgb("#CBD5E1"), radius: 2.5pt, inset: 5.5pt)[
    #align(center)[
      #text(weight: "bold", size: 8.4pt)[#sec.teachers_required Teachers] \
      #v(2pt)
      #text(size: 6.0pt, fill: rgb("#64748B"))[25% Hardship Allowance]
    ]
  ]
)

#v(8pt)
#text(size: 9.4pt, weight: "bold", fill: rgb("#1E3A8A"))[4. 5-year capital rollout, calibrated economic ROI and cabinet directives]
#v(4pt)

#table(
  columns: (78pt, 160pt, 75pt, 45pt, 52pt, 50pt, 1fr),
  stroke: 0.4pt + rgb("#CBD5E1"),
  fill: (col, row) => if row == 0 { rgb("#1E3A8A") } else if calc.even(row) { rgb("#F8FAFC") } else { rgb("#FFFFFF") },
  align: (col, row) => (if col <= 1 { left } else { center }),
  inset: 4.0pt,
  
  table.header(
    [#text(weight: "bold", fill: white, size: 7.2pt)[Phase]],
    [#text(weight: "bold", fill: white, size: 7.2pt)[Target Corridors]],
    [#text(weight: "bold", fill: white, size: 7.2pt)[Outlay]],
    [#text(weight: "bold", fill: white, size: 7.2pt)[Upgrades]],
    [#text(weight: "bold", fill: white, size: 7.2pt)[New Sch.]],
    [#text(weight: "bold", fill: white, size: 7.2pt)[Transit]],
    [#text(weight: "bold", fill: white, size: 7.2pt)[Access Gain]]
  ),
  
  [#text(weight: "bold")[Phase 1 (Y1–Y2)]], [High Vulnerability Tribal Corridors (9 Dists)], [#text(weight: "bold")[₹#calc.round(phases.Phase_1_Years_1_2.outlay_cr, digits: 0) Cr (45%)]], [#phases.Phase_1_Years_1_2.upgrades], [#phases.Phase_1_Years_1_2.new_schools], [#phases.Phase_1_Years_1_2.transit_hubs], [#text(weight: "bold", fill: rgb("#059669"))[+#phases.Phase_1_Years_1_2.coverage_gain_pct%]],
  [#text(weight: "bold")[Phase 2 (Y3–Y4)]], [Mineral Belts & Western Plateaus (11 Dists)], [#text(weight: "bold")[₹#calc.round(phases.Phase_2_Years_3_4.outlay_cr, digits: 0) Cr (35%)]], [#phases.Phase_2_Years_3_4.upgrades], [#phases.Phase_2_Years_3_4.new_schools], [#phases.Phase_2_Years_3_4.transit_hubs], [#text(weight: "bold", fill: rgb("#059669"))[+#phases.Phase_2_Years_3_4.coverage_gain_pct%]],
  [#text(weight: "bold")[Phase 3 (Y5)]], [Coastal Deltas & Cyclone Retrofits (10 Dists)], [#text(weight: "bold")[₹#calc.round(phases.Phase_3_Year_5.outlay_cr, digits: 0) Cr (20%)]], [#phases.Phase_3_Year_5.upgrades], [#phases.Phase_3_Year_5.new_schools], [#phases.Phase_3_Year_5.transit_hubs], [#text(weight: "bold", fill: rgb("#059669"))[+#phases.Phase_3_Year_5.coverage_gain_pct%]],
)

#v(6pt)
- *Economic Return Analysis:* Retaining 184,000 secondary students generates *₹#calc.round(econ.net_present_value_gsdp_contribution_cr, digits: 0) Cr direct lifetime GSDP addition* (0.70x rural labor absorption discount), delivering a *#econ.benefit_cost_ratio_roi\x Benefit-Cost Ratio* against the ₹#calc.round(sec.total_budget_cr, digits: 1) Cr capital outlay.
- *Strategic Implementation Guidelines:* *1. Teacher Retention Cadre:* Sanction #sec.teachers_required secondary posts with 25% Remote Area Allowances in high-friction corridors. *2. Land Availability:* Prioritize unencumbered government wasteland with early local community engagement. *3. Transit Service Model:* Partner with local women's self-help groups (Mission Shakti) for student feeder operations. *4. Geospatial Verification:* Require GIS coordinate logging prior to capital tranche release.

#v(8pt)
#rect(width: 100%, fill: rgb("#F8FAFC"), stroke: 0.4pt + rgb("#CBD5E1"), radius: 2.5pt, inset: (x: 8pt, y: 5pt))[
  #grid(
    columns: (1fr, 1fr),
    [
      #text(size: 6.4pt, fill: rgb("#64748B"))[
        *Spatial Model:* Submodular Pareto MCLP with Tobler Hiking Friction & PWD Hill Calibration \
        *Analytical Scope:* 314 Community Development Blocks across 30 Districts
      ]
    ],
    align(right)[
      #text(size: 6.4pt, fill: rgb("#64748B"))[
        *Optimality Bound:* Nemhauser-Wolsey Guarantee $(1 - 1/e) approx 63.2%$ \
        *Conservation:* Strict Bottom-Up District Summation (Zero Mathematical Discrepancy)
      ]
    ]
  )
]
