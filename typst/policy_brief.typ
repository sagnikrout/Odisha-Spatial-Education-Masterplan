#let data = json("/odisha_statewide_assessment.json")
#let sec = data.statewide_totals.Secondary
#let econ = data.metadata.economic_impact

#set page(
  paper: "a4",
  flipped: false,
  margin: (x: 1.0cm, top: 1.0cm, bottom: 1.0cm),
  header: locate(loc => {
    set text(size: 7.5pt, font: "Liberation Sans", fill: rgb("#64748B"), weight: "bold")
    grid(
      columns: (1fr, 1fr),
      align(left)[GOVERNMENT OF ODISHA | DEPARTMENT OF SCHOOL & MASS EDUCATION],
      align(right)[EXECUTIVE POLICY BRIEF (2026-2031)]
    )
    v(-4pt)
    line(length: 100%, stroke: 0.5pt + rgb("#CBD5E1"))
  }),
  footer: locate(loc => {
    line(length: 100%, stroke: 0.5pt + rgb("#CBD5E1"))
    v(-2pt)
    set text(size: 7.0pt, font: "Liberation Sans", fill: rgb("#64748B"))
    grid(
      columns: (1fr, 1fr),
      align(left)[Confidential — Operations Research & Spatial Decision-Support Brief],
      align(right)[Page 1 of 1]
    )
  })
)

#set text(font: "Liberation Sans", size: 6.8pt, fill: rgb("#0F172A"))
#set par(leading: 0.45em, justify: true)

// Title & Subtitle
#v(2pt)
#align(center)[
  #text(size: 13pt, weight: "bold", fill: rgb("#1E3A8A"))[ODISHA SPATIAL SCHOOL EDUCATION MASTERPLAN (2026-2031)] \
  #v(-2pt)
  #text(size: 7.5pt, fill: rgb("#64748B"))[Audited Operations Research & PWD Hill Cost Calibrated Strategy Across 314 CD Blocks]
]
#v(-2pt)
#line(length: 100%, stroke: 1.2pt + rgb("#1E3A8A"))
#v(2pt)

// Executive KPI Dashboard Cards
#grid(
  columns: (1fr, 1fr, 1fr, 1fr, 1fr),
  gutter: 4pt,
  rect(width: 100%, fill: rgb("#F1F5F9"), stroke: 0.5pt + rgb("#CBD5E1"), radius: 2pt, inset: 3.5pt)[
    #align(center)[
      #text(weight: "bold", size: 8.0pt, fill: rgb("#1E3A8A"))[#sec.initial_coverage_pct% → #sec.final_coverage_pct%] \
      #text(size: 5.5pt, fill: rgb("#64748B"))[Secondary Access]
    ]
  ],
  rect(width: 100%, fill: rgb("#F1F5F9"), stroke: 0.5pt + rgb("#CBD5E1"), radius: 2pt, inset: 3.5pt)[
    #align(center)[
      #text(weight: "bold", size: 8.0pt, fill: rgb("#059669"))[₹#calc.round(sec.total_budget_cr, digits: 1) Cr] \
      #text(size: 5.5pt, fill: rgb("#64748B"))[Hill-Adjusted Outlay]
    ]
  ],
  rect(width: 100%, fill: rgb("#F1F5F9"), stroke: 0.5pt + rgb("#CBD5E1"), radius: 2pt, inset: 3.5pt)[
    #align(center)[
      #text(weight: "bold", size: 8.0pt, fill: rgb("#1E293B"))[314 Blocks] \
      #text(size: 5.5pt, fill: rgb("#64748B"))[30 Districts Analyzed]
    ]
  ],
  rect(width: 100%, fill: rgb("#F1F5F9"), stroke: 0.5pt + rgb("#CBD5E1"), radius: 2pt, inset: 3.5pt)[
    #align(center)[
      #text(weight: "bold", size: 8.0pt, fill: rgb("#7C3AED"))[#econ.benefit_cost_ratio_roi\x GSDP ROI] \
      #text(size: 5.5pt, fill: rgb("#64748B"))[₹#calc.round(econ.net_present_value_gsdp_contribution_cr, digits: 0) Cr Value]
    ]
  ],
  rect(width: 100%, fill: rgb("#F1F5F9"), stroke: 0.5pt + rgb("#CBD5E1"), radius: 2pt, inset: 3.5pt)[
    #align(center)[
      #text(weight: "bold", size: 8.0pt, fill: rgb("#DC2626"))[9,144 Posts] \
      #text(size: 5.5pt, fill: rgb("#64748B"))[Teachers (25% Hardship)]
    ]
  ]
)

#v(1pt)
#text(size: 8.2pt, weight: "bold", fill: rgb("#1E3A8A"))[1. Strategic Context & Operations Research Methodology]
#v(1pt)
- *Grade 8 → 9 Spatial Dropout Cliff:* While primary access achieves >74%, secondary coverage drops to 59.1% due to distance barriers (mean distance >6.8 km in Eastern Ghats), driving >42% tribal dropout with adolescent girls dropping out at 2.3x higher rates without safe transit.
- *Submodular Pareto MCLP & PWD Hill Multipliers:* Interventions are optimized using a submodular Maximum Coverage Location Problem (MCLP) engine under capital constraints, incorporating *Tobler's Hiking Slope Resistance (1.8x–2.4x)* and *PWD Hill Cost Multipliers (+18% to +30%)* to model realistic ghat logistics.

#v(1pt)
#text(size: 8.2pt, weight: "bold", fill: rgb("#1E3A8A"))[2. Statewide Multi-Tier Investment & Physical Targets (Hill Cost Calibrated)]
#v(1pt)

#table(
  columns: (78pt, 36pt, 46pt, 46pt, 46pt, 54pt, 54pt, 58pt, 1fr),
  stroke: 0.4pt + rgb("#CBD5E1"),
  fill: (col, row) => if row == 0 { rgb("#1E3A8A") } else if calc.even(row) { rgb("#F8FAFC") } else { rgb("#FFFFFF") },
  align: (col, row) => (if col == 0 { left } else { center }),
  inset: 2.2pt,
  
  // Headers
  table.header(
    [#text(weight: "bold", fill: white, size: 6.2pt)[Education Tier]],
    [#text(weight: "bold", fill: white, size: 6.2pt)[Norm]],
    [#text(weight: "bold", fill: white, size: 6.2pt)[Existing]],
    [#text(weight: "bold", fill: white, size: 6.2pt)[Baseline]],
    [#text(weight: "bold", fill: white, size: 6.2pt)[Upgrades]],
    [#text(weight: "bold", fill: white, size: 6.2pt)[New Sch.]],
    [#text(weight: "bold", fill: white, size: 6.2pt)[Transit]],
    [#text(weight: "bold", fill: white, size: 6.2pt)[Target Access]],
    [#text(weight: "bold", fill: white, size: 6.2pt)[Est. Outlay]]
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

#v(1pt)
#text(size: 8.2pt, weight: "bold", fill: rgb("#1E3A8A"))[3. 314 CD Blocks Regional Stratification, Transit Fleet & Teacher Cadre]
#v(1pt)
- *High Vulnerability (72 Blocks in 9 Tribal Dists):* Coverage \< 45%. Priority for dedicated girls' hostels, feeder transit, and teacher hardship pay.
- *Central & Agrarian (142 Blocks):* Coverage 55–70%. Focus on expanding existing Upper Primary schools into High Schools.
- *Coastal & Deltaic (100 Blocks):* Coverage > 75%. Focus on STEM infrastructure and 396 cyclone-resilient structural retrofits.

#v(1pt)
#grid(
  columns: (1fr, 1fr, 1fr, 1fr, 1fr),
  gutter: 4pt,
  rect(width: 100%, fill: rgb("#F1F5F9"), stroke: 0.5pt + rgb("#CBD5E1"), radius: 2pt, inset: 2.8pt)[
    #align(center)[
      #text(weight: "bold", size: 7.2pt)[588 Girls' Hostels] \
      #text(size: 5.0pt, fill: rgb("#64748B"))[Guarantees female retention]
    ]
  ],
  rect(width: 100%, fill: rgb("#F1F5F9"), stroke: 0.5pt + rgb("#CBD5E1"), radius: 2pt, inset: 2.8pt)[
    #align(center)[
      #text(weight: "bold", size: 7.2pt)[#sec.fleet_minibuses Mini-Buses] \
      #text(size: 5.0pt, fill: rgb("#64748B"))[(at ₹4.80L/yr Opex)]
    ]
  ],
  rect(width: 100%, fill: rgb("#F1F5F9"), stroke: 0.5pt + rgb("#CBD5E1"), radius: 2pt, inset: 2.8pt)[
    #align(center)[
      #text(weight: "bold", size: 7.2pt)[#sec.fleet_feeder_vans Feeder Vans] \
      #text(size: 5.0pt, fill: rgb("#64748B"))[(at ₹3.00L/yr Opex)]
    ]
  ],
  rect(width: 100%, fill: rgb("#F1F5F9"), stroke: 0.5pt + rgb("#CBD5E1"), radius: 2pt, inset: 2.8pt)[
    #align(center)[
      #text(weight: "bold", size: 7.2pt)[₹#calc.round(sec.annual_transit_opex_cr, digits: 1) Cr/yr] \
      #text(size: 5.0pt, fill: rgb("#64748B"))[Fuel, repairs & chaperones]
    ]
  ],
  rect(width: 100%, fill: rgb("#F1F5F9"), stroke: 0.5pt + rgb("#CBD5E1"), radius: 2pt, inset: 2.8pt)[
    #align(center)[
      #text(weight: "bold", size: 7.2pt)[9,144 Teachers] \
      #text(size: 5.0pt, fill: rgb("#64748B"))[25% Hardship Allowance]
    ]
  ]
)

#v(1pt)
#text(size: 8.2pt, weight: "bold", fill: rgb("#1E3A8A"))[4. 5-Year Capital Rollout, Calibrated Economic ROI & Cabinet Directives]
#v(1pt)

#table(
  columns: (72pt, 160pt, 75pt, 45pt, 52pt, 50pt, 1fr),
  stroke: 0.4pt + rgb("#CBD5E1"),
  fill: (col, row) => if row == 0 { rgb("#1E3A8A") } else if calc.even(row) { rgb("#F8FAFC") } else { rgb("#FFFFFF") },
  align: (col, row) => (if col <= 1 { left } else { center }),
  inset: 2.2pt,
  
  table.header(
    [#text(weight: "bold", fill: white, size: 6.2pt)[Phase]],
    [#text(weight: "bold", fill: white, size: 6.2pt)[Target Corridors]],
    [#text(weight: "bold", fill: white, size: 6.2pt)[Outlay]],
    [#text(weight: "bold", fill: white, size: 6.2pt)[Upgrades]],
    [#text(weight: "bold", fill: white, size: 6.2pt)[New Sch.]],
    [#text(weight: "bold", fill: white, size: 6.2pt)[Transit]],
    [#text(weight: "bold", fill: white, size: 6.2pt)[Access Gain]]
  ),
  
  [#text(weight: "bold")[Phase 1 (Y1–Y2)]], [High Vulnerability Tribal Corridors (9 Dists)], [#text(weight: "bold")[₹2,704 Cr (45%)]], [981], [537], [644], [#text(weight: "bold", fill: rgb("#059669"))[+16.5%]],
  [#text(weight: "bold")[Phase 2 (Y3–Y4)]], [Mineral Belts & Western Plateaus (11 Dists)], [#text(weight: "bold")[₹2,103 Cr (35%)]], [763], [418], [351], [#text(weight: "bold", fill: rgb("#059669"))[+11.2%]],
  [#text(weight: "bold")[Phase 3 (Y5)]], [Coastal Deltas & Cyclone Retrofits (10 Dists)], [#text(weight: "bold")[₹1,202 Cr (20%)]], [436], [239], [175], [#text(weight: "bold", fill: rgb("#059669"))[+4.8%]],
)

#v(1pt)
- *Audited Economic ROI:* Retaining 184,000 secondary students generates *₹#calc.round(econ.net_present_value_gsdp_contribution_cr, digits: 0) Cr lifetime GSDP value* (0.75x informal labor discount), delivering a *#econ.benefit_cost_ratio_roi\x Benefit-Cost Ratio* on ₹#calc.round(sec.total_budget_cr, digits: 1) Cr capital outlay.
- *Immediate Cabinet Directives:* *1. Tribal Teacher Cadre:* Sanction 9,144 posts with 25% Remote Area Allowance & 3-yr bond. *2. PESA Land Fast-Track:* Transfer revenue wasteland via Gram Sabha consent (PESA Sec 4i). *3. SHG Transit Operations:* Partner with Mission Shakti SHGs for bus/feeder chaperones. *4. GIS-Linked Disbursals:* Require GPS validation prior to fund release.
