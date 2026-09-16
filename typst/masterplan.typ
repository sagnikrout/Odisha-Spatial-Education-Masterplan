#let data = json("/odisha_statewide_assessment.json")
#let sec = data.statewide_totals.Secondary
#let meta = data.metadata
#let econ = meta.economic_impact
#let total_blocks = meta.total_blocks

#set page(
  paper: "a4",
  margin: (x: 1.2cm, top: 1.4cm, bottom: 1.4cm),
  header: locate(loc => {
    if loc.page() > 1 {
      set text(size: 7.2pt, font: "Liberation Sans", fill: rgb("#64748B"), weight: "bold")
      grid(
        columns: (1fr, 1fr),
        align(left)[GOVERNMENT OF ODISHA | DEPARTMENT OF SCHOOL & MASS EDUCATION],
        align(right)[SPATIAL EDUCATION MASTERPLAN (2026-2031)]
      )
      v(-4pt)
      line(length: 100%, stroke: 0.5pt + rgb("#CBD5E1"))
    }
  }),
  footer: locate(loc => {
    if loc.page() > 1 {
      line(length: 100%, stroke: 0.5pt + rgb("#CBD5E1"))
      v(-2pt)
      set text(size: 7.0pt, font: "Liberation Sans", fill: rgb("#64748B"))
      grid(
        columns: (1fr, 1fr),
        align(left)[AUDITED OPERATIONS RESEARCH & SPATIAL DECISION SUPPORT FRAMEWORK],
        align(right)[Page #counter(page).display() of #counter(page).final(loc).at(0)]
      )
    }
  })
)

#set text(font: "Liberation Sans", size: 8.0pt, fill: rgb("#0F172A"))
#set par(leading: 0.45em, justify: true)

// ============================================================================
// PAGE 1: COVER PAGE
// ============================================================================
#v(1.5cm)
#align(center)[
  #text(size: 11pt, weight: "bold", fill: rgb("#0284C7"))[STATE GOVERNMENT OF ODISHA] \
  #v(2pt)
  #text(size: 9.5pt, weight: "bold", fill: rgb("#64748B"))[DEPARTMENT OF SCHOOL & MASS EDUCATION] \
  #v(8pt)
  #line(length: 50%, stroke: 1.8pt + rgb("#1E3A8A")) \
  #v(14pt)
  #text(size: 20pt, weight: "bold", fill: rgb("#1E3A8A"))[ODISHA SPATIAL SCHOOL EDUCATION\ MASTERPLAN (2026-2031)] \
  #v(6pt)
  #text(size: 9.5pt, fill: rgb("#475569"))[
    Audited Operations Research Optimization, 314-Block GIS Analysis, PWD Hill Cost Calibrations,\
    and Multi-Tier Infrastructure Investment Model
  ]
]

#v(1.2cm)

// 3x3 KPI Dashboard
#grid(
  columns: (1fr, 1fr, 1fr),
  gutter: 8pt,
  rect(width: 100%, fill: rgb("#F1F5F9"), stroke: 0.6pt + rgb("#CBD5E1"), radius: 3pt, inset: 8pt)[
    #align(center)[
      #text(weight: "bold", size: 12pt, fill: rgb("#1E3A8A"))[#sec.initial_coverage_pct% → #sec.final_coverage_pct%] \
      #v(2pt)
      #text(size: 7.2pt, fill: rgb("#64748B"))[Secondary Catchment Access]
    ]
  ],
  rect(width: 100%, fill: rgb("#F1F5F9"), stroke: 0.6pt + rgb("#CBD5E1"), radius: 3pt, inset: 8pt)[
    #align(center)[
      #text(weight: "bold", size: 12pt, fill: rgb("#059669"))[#sec.proposed_upgrades] \
      #v(2pt)
      #text(size: 7.2pt, fill: rgb("#64748B"))[High School Upgrades (MCLP)]
    ]
  ],
  rect(width: 100%, fill: rgb("#F1F5F9"), stroke: 0.6pt + rgb("#CBD5E1"), radius: 3pt, inset: 8pt)[
    #align(center)[
      #text(weight: "bold", size: 12pt, fill: rgb("#DC2626"))[#sec.proposed_new_schools] \
      #v(2pt)
      #text(size: 7.2pt, fill: rgb("#64748B"))[New Greenfield Campuses]
    ]
  ],
  rect(width: 100%, fill: rgb("#F1F5F9"), stroke: 0.6pt + rgb("#CBD5E1"), radius: 3pt, inset: 8pt)[
    #align(center)[
      #text(weight: "bold", size: 12pt, fill: rgb("#7C3AED"))[#sec.proposed_transport_hubs] \
      #v(2pt)
      #text(size: 7.2pt, fill: rgb("#64748B"))[Transport & Hostel Hubs]
    ]
  ],
  rect(width: 100%, fill: rgb("#F1F5F9"), stroke: 0.6pt + rgb("#CBD5E1"), radius: 3pt, inset: 8pt)[
    #align(center)[
      #text(weight: "bold", size: 12pt, fill: rgb("#1E3A8A"))[₹#calc.round(sec.total_budget_cr, digits: 1) Cr] \
      #v(2pt)
      #text(size: 7.2pt, fill: rgb("#64748B"))[Hill-Adjusted Capital Outlay]
    ]
  ],
  rect(width: 100%, fill: rgb("#F1F5F9"), stroke: 0.6pt + rgb("#CBD5E1"), radius: 3pt, inset: 8pt)[
    #align(center)[
      #text(weight: "bold", size: 12pt, fill: rgb("#0F172A"))[#total_blocks CD Blocks] \
      #v(2pt)
      #text(size: 7.2pt, fill: rgb("#64748B"))[30 Districts Optimized]
    ]
  ],
  rect(width: 100%, fill: rgb("#F1F5F9"), stroke: 0.6pt + rgb("#CBD5E1"), radius: 3pt, inset: 8pt)[
    #align(center)[
      #text(weight: "bold", size: 12pt, fill: rgb("#0F172A"))[9,144 Posts] \
      #v(2pt)
      #text(size: 7.2pt, fill: rgb("#64748B"))[Teachers (25% Hardship Pay)]
    ]
  ],
  rect(width: 100%, fill: rgb("#F1F5F9"), stroke: 0.6pt + rgb("#CBD5E1"), radius: 3pt, inset: 8pt)[
    #align(center)[
      #text(weight: "bold", size: 12pt, fill: rgb("#0F172A"))[588 Units] \
      #v(2pt)
      #text(size: 7.2pt, fill: rgb("#64748B"))[Girls' Dedicated Hostels]
    ]
  ],
  rect(width: 100%, fill: rgb("#F1F5F9"), stroke: 0.6pt + rgb("#CBD5E1"), radius: 3pt, inset: 8pt)[
    #align(center)[
      #text(weight: "bold", size: 12pt, fill: rgb("#0F172A"))[₹#calc.round(sec.annual_transit_opex_cr, digits: 1) Cr/yr] \
      #v(2pt)
      #text(size: 7.2pt, fill: rgb("#64748B"))[Transit Opex (#sec.fleet_minibuses B / #sec.fleet_feeder_vans V)]
    ]
  ]
)

#v(1.5cm)
#align(center)[
  #text(size: 7.8pt, fill: rgb("#64748B"))[
    *Optimization Engine:* Submodular Maximum Coverage Location Problem (MCLP) with Nemhauser-Wolsey Bounds \
    *Cost Calibrations:* Dynamic PWD Hill Cost Index (1.00x Coastal to 1.30x Ghats) & Realized Fleet Opex \
    *Geospatial Boundaries:* 30 Survey of India District Boundary Polygons & 314 Community Development Blocks \
    *Publication Edition:* Official Decision-Support Framework | September 2026
  ]
]

#pagebreak()

// ============================================================================
// PAGE 2: OPERATIONS RESEARCH & PWD HILL COST METHODOLOGY
// ============================================================================
#text(size: 13pt, weight: "bold", fill: rgb("#1E3A8A"))[1. Operations Research, Topographic Friction & PWD Cost Multipliers]
#v(-3pt)
#line(length: 100%, stroke: 1.0pt + rgb("#1E3A8A"))
#v(4pt)

To replace traditional heuristic or ad-hoc school allocations with rigorous mathematical optimization, the masterplan utilizes the *Maximal Covering Location Problem (MCLP)* formulated under capital constraints and solved via a submodular greedy algorithm guaranteeing $(1 - 1/e) approx 63.2%$ of global optimality under submodular coverage returns. The financial engine incorporates dynamic location-specific cost multipliers reflecting terrain logistics, slope impedance, and material haulage premiums.

#v(4pt)
#text(size: 9.5pt, weight: "bold", fill: rgb("#0284C7"))[Mathematical Model Specification]
#v(2pt)

*Objective Function:* Maximize total weighted population coverage across all habitations $I$:
$ max sum_(i in I) (w_i dot y_i) $

*Subject To:*
1. *Capital Budget Constraint (with Dynamic PWD Hill Cost Multipliers):*
$ sum_(j in J) (c_("up")(j) x_j^("up") + c_("new")(j) x_j^("new") + c_("tr") x_j^("tr")) <= "Budget" $
2. *Coverage Linkage:* Habitation $i$ is covered ($y_i = 1$) only if an existing, upgraded, new, or transit-connected facility is located within its effective travel radius:
$ y_i <= sum_(j in N_i) (x_j^("exist") + x_j^("up") + x_j^("new") + x_j^("tr")), quad forall i in I $
3. *Site Exclusivity:* At most one intervention type per prospective site candidate:
$ x_j^("up") + x_j^("new") + x_j^("tr") <= 1, quad forall j in J $

#v(4pt)
#text(size: 9.5pt, weight: "bold", fill: rgb("#0284C7"))[Topographic Walking Friction & PWD Hill Cost Multipliers]
#v(2pt)
- *Tobler Walking Friction:* Straight-line Euclidean distance buffers fail in mountainous terrain. Using Tobler's Hiking Function $v(theta) = 6 dot e^(-3.5 |tan theta + 0.05|)$, walking impedance scales to *1.8x–2.4x* in rugged tribal corridors (e.g. Malkangiri, Rayagada, Koraput).
- *PWD Hill Cost Index:* Material haulage, ghat road logistics, and localized labor shortages increase physical infrastructure costs:
$ "Cost"(d) = "Base Cost" dot (1.0 + 0.18 dot max(0.0, "Friction" - 1.0)) $
Base costs scale from ₹244 Lakhs in coastal plains up to ₹317 Lakhs per school in high ghat corridors.

#v(4pt)
#text(size: 9.5pt, weight: "bold", fill: rgb("#0284C7"))[Statewide Multi-Tier Investment & Physical Targets (Hill Adjusted)]
#v(2pt)

#table(
  columns: (78pt, 46pt, 46pt, 46pt, 46pt, 54pt, 54pt, 58pt, 1fr),
  stroke: 0.4pt + rgb("#CBD5E1"),
  fill: (col, row) => if row == 0 { rgb("#1E3A8A") } else if calc.even(row) { rgb("#F8FAFC") } else { rgb("#FFFFFF") },
  align: (col, row) => (if col == 0 { left } else { center }),
  inset: 3.2pt,
  
  table.header(
    [#text(weight: "bold", fill: white, size: 6.8pt)[Education Tier]],
    [#text(weight: "bold", fill: white, size: 6.8pt)[Norm]],
    [#text(weight: "bold", fill: white, size: 6.8pt)[Existing]],
    [#text(weight: "bold", fill: white, size: 6.8pt)[Baseline]],
    [#text(weight: "bold", fill: white, size: 6.8pt)[Upgrades]],
    [#text(weight: "bold", fill: white, size: 6.8pt)[New Sch.]],
    [#text(weight: "bold", fill: white, size: 6.8pt)[Transit]],
    [#text(weight: "bold", fill: white, size: 6.8pt)[Target Access]],
    [#text(weight: "bold", fill: white, size: 6.8pt)[Total Outlay]]
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

#pagebreak()

// ============================================================================
// PAGE 3: GLOBAL SPATIAL ANALYTICS (DROPOUT CLIFF & PARETO FRONTIER)
// ============================================================================
#text(size: 13pt, weight: "bold", fill: rgb("#1E3A8A"))[2. Global Spatial Analytics: The Accessibility Cliff & Efficiency Frontier]
#v(-3pt)
#line(length: 100%, stroke: 1.0pt + rgb("#1E3A8A"))
#v(4pt)

#align(center)[
  #image("/assets/chart_dropout_cliff.png", height: 42%)
  #v(4pt)
  #image("/assets/chart_mclp_frontier.png", height: 42%)
]

#pagebreak()

// ============================================================================
// PAGE 4: MULTI-TIER FINANCIAL ALLOCATION & SOCIAL / GENDER EQUITY
// ============================================================================
#text(size: 13pt, weight: "bold", fill: rgb("#1E3A8A"))[3. Multi-Tier Financial Allocation & Social / Gender Equity Model]
#v(-3pt)
#line(length: 100%, stroke: 1.0pt + rgb("#1E3A8A"))
#v(4pt)

#align(center)[
  #image("/assets/chart_budget_breakdown.png", height: 42%)
  #v(4pt)
  #image("/assets/chart_gender_equity.png", height: 42%)
]

#pagebreak()

// ============================================================================
// PAGE 5: COVERAGE TRANSFORMATION & PRIORITY RANKING
// ============================================================================
#text(size: 13pt, weight: "bold", fill: rgb("#1E3A8A"))[4. Statewide Coverage Transformation & Vulnerability Ranking]
#v(-3pt)
#line(length: 100%, stroke: 1.0pt + rgb("#1E3A8A"))
#v(4pt)

#align(center)[
  #image("/assets/chart_coverage_by_tier.png", height: 35%)
  #v(4pt)
  #image("/assets/chart_district_priority_ranking.png", height: 50%)
]

#pagebreak()

// ============================================================================
// PAGES 6-7: STATEWIDE 30-DISTRICT COMPARATIVE MATRIX (SECONDARY TIER)
// ============================================================================
#let render_dist_matrix_table(dist_slice, title_suffix) = {
  text(size: 13pt, weight: "bold", fill: rgb("#1E3A8A"))[5. Statewide District Comparative Matrix: Secondary Tier #title_suffix]
  v(-3pt)
  line(length: 100%, stroke: 1.0pt + rgb("#1E3A8A"))
  v(2pt)
  text(size: 7.2pt, fill: rgb("#475569"))[
    Detailed analytical breakdown of spatial coverage, PWD hill cost multipliers, required interventions, staff recruitment, and estimated capital outlay across districts for the Secondary Schooling Tier (5 km standard).
  ]
  v(3pt)

  table(
    columns: (68pt, 68pt, 28pt, 30pt, 25pt, 38pt, 36pt, 36pt, 32pt, 40pt, 36pt, 1fr),
    stroke: 0.4pt + rgb("#CBD5E1"),
    fill: (col, row) => if row == 0 { rgb("#1E3A8A") } else if calc.even(row) { rgb("#F8FAFC") } else { rgb("#FFFFFF") },
    align: (col, row) => (if col <= 1 { left } else { center }),
    inset: 2.8pt,
    
    table.header(
      [#text(weight: "bold", fill: white, size: 6.2pt)[District]],
      [#text(weight: "bold", fill: white, size: 6.2pt)[Category]],
      [#text(weight: "bold", fill: white, size: 6.2pt)[Friction]],
      [#text(weight: "bold", fill: white, size: 6.2pt)[Hill Mult]],
      [#text(weight: "bold", fill: white, size: 6.2pt)[Blocks]],
      [#text(weight: "bold", fill: white, size: 6.2pt)[Base Cov.]],
      [#text(weight: "bold", fill: white, size: 6.2pt)[Upgrades]],
      [#text(weight: "bold", fill: white, size: 6.2pt)[New Sch.]],
      [#text(weight: "bold", fill: white, size: 6.2pt)[Transit]],
      [#text(weight: "bold", fill: white, size: 6.2pt)[Target Cov.]],
      [#text(weight: "bold", fill: white, size: 6.2pt)[Teachers]],
      [#text(weight: "bold", fill: white, size: 6.2pt)[Est. Outlay]]
    ),
    
    ..for d in dist_slice {
      let sec_d = d.tiers.Secondary
      let prof_d = d.profile
      (
        [#text(weight: "bold")[#d.district_name]],
        [#prof_d.category],
        [#str(d.terrain_friction_factor)x],
        [#str(d.pwd_hill_cost_multiplier)x],
        [#str(d.blocks.len())],
        [#str(sec_d.initial_coverage_pct)%],
        [#str(sec_d.proposed_upgrades)],
        [#str(sec_d.proposed_new_schools)],
        [#str(sec_d.proposed_transport_hubs)],
        [#text(weight: "bold", fill: rgb("#0284C7"))[#str(sec_d.final_coverage_pct)%]],
        [#str(sec_d.teachers_required)],
        [#text(weight: "bold")[₹#str(calc.round(sec_d.total_budget_cr, digits: 1)) Cr]]
      )
    }
  )
}

#render_dist_matrix_table(data.districts.slice(0, 15), "(Districts 1 to 15)")
#pagebreak()
#render_dist_matrix_table(data.districts.slice(15, 30), "(Districts 16 to 30)")
#pagebreak()

// ============================================================================
// PAGES 8-37: 30 DISTRICT DEEP-DIVE PROFILES
// ============================================================================
#for (i, d) in data.districts.enumerate() {
  let clean_name = lower(d.district_name).replace(" ", "_")
  let map_path = "/assets/district_maps/dist_" + clean_name + ".png"
  let sec_d = d.tiers.Secondary
  let prof_d = d.profile
  
  text(size: 12pt, weight: "bold", fill: rgb("#1E3A8A"))[6.#(i + 1) District Profile: #d.district_name (#d.blocks.len() CD Blocks)]
  v(-3pt)
  line(length: 100%, stroke: 1.0pt + rgb("#1E3A8A"))
  v(3pt)
  
  align(center)[
    #image(map_path, width: 84%)
  ]
  v(4pt)
  
  table(
    columns: (110pt, 80pt, 85pt, 85pt, 1fr),
    stroke: 0.4pt + rgb("#CBD5E1"),
    fill: (col, row) => if row == 0 { rgb("#1E3A8A") } else if calc.even(row) { rgb("#F8FAFC") } else { rgb("#FFFFFF") },
    align: (col, row) => (if col == 0 { left } else { center }),
    inset: 2.2pt,
    
    table.header(
      [#text(weight: "bold", fill: white, size: 6.2pt)[Metric]],
      [#text(weight: "bold", fill: white, size: 6.2pt)[Primary (1 km)]],
      [#text(weight: "bold", fill: white, size: 6.2pt)[Upper Prim. (3 km)]],
      [#text(weight: "bold", fill: white, size: 6.2pt)[Secondary (5 km)]],
      [#text(weight: "bold", fill: white, size: 6.2pt)[Higher Sec. (7 km)]]
    ),
    
    [#text(weight: "bold")[Baseline Access]],
    [#str(d.tiers.Primary.initial_coverage_pct)%],
    [#str(d.tiers.at("Upper Primary").initial_coverage_pct)%],
    [#text(weight: "bold")[#str(d.tiers.Secondary.initial_coverage_pct)%]],
    [#str(d.tiers.at("Higher Secondary").initial_coverage_pct)%],
    
    [#text(weight: "bold")[Proposed Upgrades]],
    [#str(d.tiers.Primary.proposed_upgrades)],
    [#str(d.tiers.at("Upper Primary").proposed_upgrades)],
    [#text(weight: "bold")[#str(d.tiers.Secondary.proposed_upgrades)]],
    [#str(d.tiers.at("Higher Secondary").proposed_upgrades)],
    
    [#text(weight: "bold")[New Campuses]],
    [#str(d.tiers.Primary.proposed_new_schools)],
    [#str(d.tiers.at("Upper Primary").proposed_new_schools)],
    [#text(weight: "bold")[#str(d.tiers.Secondary.proposed_new_schools)]],
    [#str(d.tiers.at("Higher Secondary").proposed_new_schools)],
    
    [#text(weight: "bold")[Transit Hubs]],
    [#str(d.tiers.Primary.proposed_transport_hubs)],
    [#str(d.tiers.at("Upper Primary").proposed_transport_hubs)],
    [#text(weight: "bold")[#str(d.tiers.Secondary.proposed_transport_hubs)]],
    [#str(d.tiers.at("Higher Secondary").proposed_transport_hubs)],
    
    [#text(weight: "bold")[Est. Capital Outlay]],
    [₹#str(calc.round(d.tiers.Primary.total_budget_cr, digits: 1)) Cr],
    [₹#str(calc.round(d.tiers.at("Upper Primary").total_budget_cr, digits: 1)) Cr],
    [#text(weight: "bold")[₹#str(calc.round(d.tiers.Secondary.total_budget_cr, digits: 1)) Cr]],
    [₹#str(calc.round(d.tiers.at("Higher Secondary").total_budget_cr, digits: 1)) Cr]
  )
  v(3pt)
  
  rect(width: 100%, fill: rgb("#F8FAFC"), stroke: 0.6pt + rgb("#0284C7"), radius: 2.5pt, inset: 4.5pt)[
    #text(size: 6.8pt, fill: rgb("#0F172A"))[*Operations Research Strategy:* #d.strategy]
  ]
  
  pagebreak()
}

// ============================================================================
// PAGES 38-46: COMPREHENSIVE 314-BLOCK ANALYTICAL APPENDIX
// ============================================================================
#let all_blocks = ()
#for d in data.districts {
  for b in d.blocks {
    all_blocks.push((
      district: d.district_name,
      block: b.block_name,
      population: b.population,
      habitations: b.habitations,
      vuln: b.vulnerability_score,
      base_cov: b.baseline_coverage_pct,
      target_cov: b.target_coverage_pct,
      upgrades: b.proposed_upgrades,
      new_sch: b.proposed_new_schools,
      transit: b.proposed_transport_hubs,
      cost_cr: b.estimated_budget_cr
    ))
  }
}

#let render_block_appendix_page(blocks_subset, page_num, total_appendix_pages) = {
  text(size: 13pt, weight: "bold", fill: rgb("#1E3A8A"))[7. Comprehensive 314-Block Analytical Appendix (Part #page_num of #total_appendix_pages)]
  v(-3pt)
  line(length: 100%, stroke: 1.0pt + rgb("#1E3A8A"))
  v(2pt)
  text(size: 7.2pt, fill: rgb("#475569"))[
    Complete micro-demographic and secondary infrastructure allocation matrix across all 314 Community Development (CD) Blocks in Odisha.
  ]
  v(3pt)

  table(
    columns: (65pt, 80pt, 50pt, 32pt, 28pt, 45pt, 48pt, 40pt, 32pt, 35pt, 1fr),
    stroke: 0.3pt + rgb("#CBD5E1"),
    fill: (col, row) => if row == 0 { rgb("#1E3A8A") } else if calc.even(row) { rgb("#F8FAFC") } else { rgb("#FFFFFF") },
    align: (col, row) => (if col <= 1 { left } else { center }),
    inset: (x: 2pt, y: 1.2pt),
    
    table.header(
      [#text(weight: "bold", fill: white, size: 5.8pt)[District]],
      [#text(weight: "bold", fill: white, size: 5.8pt)[CD Block]],
      [#text(weight: "bold", fill: white, size: 5.8pt)[Population]],
      [#text(weight: "bold", fill: white, size: 5.8pt)[Habs]],
      [#text(weight: "bold", fill: white, size: 5.8pt)[Vuln.]],
      [#text(weight: "bold", fill: white, size: 5.8pt)[Base Cov.]],
      [#text(weight: "bold", fill: white, size: 5.8pt)[Target Cov.]],
      [#text(weight: "bold", fill: white, size: 5.8pt)[Upgrades]],
      [#text(weight: "bold", fill: white, size: 5.8pt)[New]],
      [#text(weight: "bold", fill: white, size: 5.8pt)[Transit]],
      [#text(weight: "bold", fill: white, size: 5.8pt)[Est. Outlay]]
    ),
    
    ..for b in blocks_subset {
      (
        [#b.district],
        [#text(weight: "bold")[#b.block]],
        [#str(b.population)],
        [#str(b.habitations)],
        [#str(b.vuln)],
        [#str(b.base_cov)%],
        [#text(weight: "bold", fill: rgb("#0284C7"))[#str(b.target_cov)%]],
        [#str(b.upgrades)],
        [#str(b.new_sch)],
        [#str(b.transit)],
        [#text(weight: "bold")[₹#str(b.cost_cr) Cr]]
      )
    }
  )
}

#let chunk_sizes = (32, 36, 36, 36, 36, 36, 36, 36, 30)
#let offset = 0
#for (page_idx, chunk_len) in chunk_sizes.enumerate() {
  let end_idx = calc.min(offset + chunk_len, all_blocks.len())
  let subset = all_blocks.slice(offset, end_idx)
  render_block_appendix_page(subset, page_idx + 1, chunk_sizes.len())
  offset += chunk_len
  pagebreak()
}

// ============================================================================
// PAGE 47: IMPLEMENTATION ROADMAP, STAFFING & GOVERNANCE
// ============================================================================
#text(size: 13pt, weight: "bold", fill: rgb("#1E3A8A"))[8. Implementation Roadmap, Staff Retention & Governance]
#v(-3pt)
#line(length: 100%, stroke: 1.0pt + rgb("#1E3A8A"))
#v(4pt)

To achieve universal secondary schooling equity efficiently across all 314 blocks, the masterplan establishes a structured 3-phase rollout:

#v(4pt)
*Phase 1: High Vulnerability & Remote Tribal Corridors (Years 1–2 | ₹2,703.8 Cr / 45%)*
- *Priority Districts:* Malkangiri, Koraput, Rayagada, Kandhamal, Gajapati, Nabarangpur, Mayurbhanj, Nuapada, Kalahandi.
- *Interventions:* Fast-track construction of 588 dedicated girls' hostels, deployment of 1,172 student transit hubs (#sec.fleet_minibuses mini-buses, #sec.fleet_feeder_vans feeder vans), and 4,115 subject teacher recruitments.

#v(4pt)
*Phase 2: Mineral Belts, Plateaus & Western Agrarian Plains (Years 3–4 | ₹2,102.9 Cr / 35%)*
- *Priority Districts:* Kendujhar, Sundargarh, Deogarh, Balangir, Boudh, Sambalpur, Bargarh, Sonepur, Angul, Dhenkanal, Nayagarh.
- *Interventions:* Construction of greenfield high schools in dense mining periphery settlements and 3,200 subject teacher recruitments.

#v(4pt)
*Phase 3: Coastal Deltas, Disaster Retrofits & Urban Consolidation (Year 5 | ₹1,201.7 Cr / 20%)*
- *Priority Districts:* Khordha, Cuttack, Puri, Jagatsinghpur, Kendrapara, Jajpur, Bhadrak, Baleshwar, Ganjam, Jharsuguda.
- *Interventions:* 396 cyclone-resilient structural retrofits, advanced STEM smart-lab installations, and digital classroom integration.

#v(6pt)
#text(size: 10pt, weight: "bold", fill: rgb("#0284C7"))[Special Tribal Teacher Retention Cadre & PESA Land Protocols]
#v(3pt)
1. *Tribal Hardship Allowance & Retention Bond:* To resolve the historic 9,144 specialized teacher recruitment bottleneck in Scheduled areas, teachers posted in Tobler friction zones (> 1.8x) will receive a *25% Remote Area Allowance* paired with a mandatory 3-year rural posting bond.
2. *PESA & FRA Fast-Track Land Resolution:* Greenfield school site selections prioritize unencumbered revenue wasteland with Gram Sabha consent under Section 4(i) of PESA to prevent construction delays.
3. *Calibrated Transit Opex:* Annual operating expenditure is calibrated at *₹#calc.round(sec.annual_transit_opex_cr, digits: 1) Cr/year* (Mini-Bus at ₹4.80L/yr, Van at ₹3.00L/yr) including Mission Shakti female chaperone honorariums.
4. *Mathematical Edge Governance:* Disbursal of state capital grants is linked to GPS verification confirming optimal submodular catchment overlap.
