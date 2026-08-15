"""
Odisha Spatial Education Masterplan: Publication-Grade PDF Assembly Engine (Advanced OR & 314-Block Edition)
Assembles a comprehensive, publication-quality masterplan report featuring:
- Two-pass canvas for dynamic "Page X of Y" numbering and running headers/footers
- Undistorted 1:1 square district map embeds
- Mathematical OR formulation and proofs
- Multi-tier data tables with calculated analytical metrics
- Complete 314 Community Development Block Appendix Table
- Social equity, teacher staffing, and cyclone resilience framework
"""

import os
import json
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "odisha_statewide_assessment.json")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
MAPS_DIR = os.path.join(ASSETS_DIR, "district_maps")
OUTPUT_PDF = os.path.join(BASE_DIR, "Odisha_Spatial_School_Education_Masterplan.pdf")

# Palette
PRIMARY = colors.HexColor("#1E3A8A")     # Deep Royal Navy
SECONDARY = colors.HexColor("#0284C7")   # Slate Cyan
ACCENT_RED = colors.HexColor("#DC2626")  # Accent Coral
DARK_TEXT = colors.HexColor("#0F172A")   # Dark Slate
MUTED_TEXT = colors.HexColor("#64748B")  # Medium Gray
LIGHT_BG = colors.HexColor("#F8FAFC")    # Soft Slate 50
PANEL_BG = colors.HexColor("#F1F5F9")    # Slate 100
BORDER_COL = colors.HexColor("#CBD5E1")  # Border Line
GREEN_ACC = colors.HexColor("#059669")   # Emerald Green
PINK_ACC = colors.HexColor("#EC4899")    # Magenta Pink


class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and stamp total page count
    and render running headers and footers.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        if self._pageNumber == 1:
            return  # Suppress headers/footers on cover page

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(MUTED_TEXT)

        # Running Header
        header_text_left = "GOVERNMENT OF ODISHA | DEPARTMENT OF SCHOOL & MASS EDUCATION"
        header_text_right = "SPATIAL EDUCATION MASTERPLAN (2026–2031)"
        self.drawString(36, 842 - 32, header_text_left)
        self.drawRightString(595 - 36, 842 - 32, header_text_right)
        
        self.setStrokeColor(BORDER_COL)
        self.setLineWidth(0.75)
        self.line(36, 842 - 38, 595 - 36, 842 - 38)

        # Running Footer
        footer_text_left = "OPERATIONS RESEARCH & SPATIAL DECISION SUPPORT FRAMEWORK"
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawString(36, 32, footer_text_left)
        self.drawRightString(595 - 36, 32, page_str)
        
        self.setStrokeColor(BORDER_COL)
        self.setLineWidth(0.75)
        self.line(36, 42, 595 - 36, 42)

        self.restoreState()


def create_masterplan_pdf():
    print("Loading assessment data for PDF assembly...")
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        assessment_data = json.load(f)

    # Document Template with strict margin buffers
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=52,
        bottomMargin=55
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=23,
        leading=27,
        textColor=PRIMARY,
        alignment=1,
        spaceAfter=10
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=MUTED_TEXT,
        alignment=1,
        spaceAfter=18
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=PRIMARY,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=SECONDARY,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=DARK_TEXT,
        spaceAfter=5
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=DARK_TEXT
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.0,
        textColor=DARK_TEXT
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9.0,
        textColor=DARK_TEXT
    )

    table_cell_header = ParagraphStyle(
        'TableCellHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white,
        alignment=1
    )

    story = []

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("STATE GOVERNMENT OF ODISHA", ParagraphStyle('GovtHeader', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=SECONDARY, alignment=1, spaceAfter=6)))
    story.append(Paragraph("DEPARTMENT OF SCHOOL & MASS EDUCATION", ParagraphStyle('DeptHeader', fontName='Helvetica-Bold', fontSize=9.5, leading=12, textColor=MUTED_TEXT, alignment=1, spaceAfter=20)))
    
    story.append(HRFlowable(width="60%", thickness=2, color=PRIMARY, spaceBefore=4, spaceAfter=20))
    
    story.append(Paragraph("ODISHA SPATIAL SCHOOL EDUCATION<br/>MASTERPLAN (2026–2031)", title_style))
    story.append(Paragraph("A Statewide Operations Research Optimization, 314-Block GIS Analysis, Universal Secondary Access Strategy,<br/>and Multi-Tier Infrastructure Investment Model", subtitle_style))
    
    story.append(Spacer(1, 10))

    sec_totals = assessment_data["statewide_totals"]["Secondary"]
    total_blocks = assessment_data["metadata"].get("total_blocks", 314)
    
    kpi_data = [
        [
            Paragraph(f"<b>{sec_totals['initial_coverage_pct']}% → {sec_totals['final_coverage_pct']}%</b><br/><font size=6.5 color='#64748B'>Statewide Secondary Access</font>", table_cell_bold),
            Paragraph(f"<b>{sec_totals['proposed_upgrades']:,}</b><br/><font size=6.5 color='#64748B'>High School Upgrades</font>", table_cell_bold),
            Paragraph(f"<b>{sec_totals['proposed_new_schools']:,}</b><br/><font size=6.5 color='#64748B'>New Greenfield Campuses</font>", table_cell_bold)
        ],
        [
            Paragraph(f"<b>{sec_totals['proposed_transport_hubs']:,}</b><br/><font size=6.5 color='#64748B'>Transport/Hostel Hubs</font>", table_cell_bold),
            Paragraph(f"<b>₹{sec_totals['total_budget_cr']:,.1f} Cr</b><br/><font size=6.5 color='#64748B'>Est. Secondary Outlay</font>", table_cell_bold),
            Paragraph(f"<b>{total_blocks} CD Blocks</b><br/><font size=6.5 color='#64748B'>30 Districts Analyzed</font>", table_cell_bold)
        ],
        [
            Paragraph(f"<b>{sec_totals['teachers_required']:,} Posts</b><br/><font size=6.5 color='#64748B'>Subject Teachers (PTR 1:30)</font>", table_cell_bold),
            Paragraph(f"<b>{sec_totals['girls_hostels_proposed']:,} Units</b><br/><font size=6.5 color='#64748B'>Girls' Dedicated Hostels</font>", table_cell_bold),
            Paragraph(f"<b>{sec_totals['cyclone_resilient_upgrades']:,} Schools</b><br/><font size=6.5 color='#64748B'>Coastal Cyclone Retrofits</font>", table_cell_bold)
        ]
    ]
    t_kpi = Table(kpi_data, colWidths=[165, 165, 165])
    t_kpi.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), PANEL_BG),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.8, BORDER_COL),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_kpi)

    story.append(Spacer(1, 35))

    meta_text = (
        "<b>Mathematical Modeling:</b> Mixed-Integer Linear Programming (PuLP MILP / MCLP Facility Location)<br/>"
        "<b>Terrain Analytics:</b> Tobler's Hiking Function & Topographic Walking Friction Modeling<br/>"
        "<b>Geospatial Boundaries:</b> 30 District Polygons & 314 Community Development Blocks of Odisha<br/>"
        "<b>Published:</b> August 2026 | Bhubaneswar, Odisha"
    )
    story.append(Paragraph(meta_text, ParagraphStyle('MetaStyle', fontName='Helvetica', fontSize=8.0, leading=11.5, textColor=MUTED_TEXT, alignment=1)))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: OPERATIONS RESEARCH & MATHEMATICAL FORMULATION
    # =========================================================================
    story.append(Paragraph("1. Mathematical Formulation & Operations Research Methodology", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceBefore=2, spaceAfter=8))

    or_intro = (
        "To replace traditional heuristic or ad-hoc school allocations with rigorous mathematical optimization, "
        "the masterplan utilizes the <b>Maximal Covering Location Problem (MCLP)</b> formulated as a Mixed-Integer Linear Program (MILP) "
        "solved using the open-source CBC / PuLP optimization engine. The model optimizes the exact spatial placement of school upgrades, "
        "greenfield campuses, and student transit hubs to maximize covered student population subject to a fixed capital budget constraint."
    )
    story.append(Paragraph(or_intro, body_style))

    story.append(Paragraph("Mathematical Model Specification", h2_style))
    math_desc = (
        "<b>Objective Function:</b> Maximize total weighted population coverage across all habitations $I$:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>Maximize</b> &Sigma;<sub>i &isin; I</sub> (w<sub>i</sub> &times; y<sub>i</sub>)<br/>"
        "<b>Subject To:</b><br/>"
        "1. <b>Capital Budget Constraint:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&Sigma;<sub>j &isin; J</sub> (c<sub>up</sub> &times; x<sub>j</sub><sup>up</sup> + c<sub>new</sub> &times; x<sub>j</sub><sup>new</sup> + c<sub>tr</sub> &times; x<sub>j</sub><sup>tr</sup>) &le; Budget<br/>"
        "2. <b>Coverage Logical Linkage:</b> Habitation i is covered (y<sub>i</sub>=1) only if at least one facility is located within its effective walking radius:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;y<sub>i</sub> &le; &Sigma;<sub>j &isin; N<sub>i</sub></sub> (x<sub>j</sub><sup>up</sup> + x<sub>j</sub><sup>new</sup> + x<sub>j</sub><sup>tr</sup>), &forall; i &isin; I<br/>"
        "3. <b>Site Exclusivity:</b> At most one facility intervention per candidate location:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;x<sub>j</sub><sup>up</sup> + x<sub>j</sub><sup>new</sup> + x<sub>j</sub><sup>tr</sup> &le; 1, &forall; j &isin; J"
    )
    story.append(Paragraph(math_desc, body_style))

    story.append(Paragraph("Topographic Walking Friction & Tobler's Hiking Model", h2_style))
    tobler_text = (
        "Straight-line Euclidean distances significantly underestimate walking effort across the Eastern Ghats and dense forest basins. "
        "The spatial engine applies <b>Tobler's Hiking Function</b> to calculate terrain slope resistance:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;v(&theta;) = 6 &times; e<sup>-3.5 &times; |tan(&theta;) + 0.05|</sup> (km/h)<br/>"
        "In high-altitude districts like Malkangiri, Koraput, and Kandhamal, terrain walking friction multipliers reach <b>1.8x to 2.4x</b>, "
        "necessitating transport and hostel hubs for habitations situated beyond 3.0 effective walking kilometers."
    )
    story.append(Paragraph(tobler_text, body_style))

    story.append(Paragraph("Statewide Multi-Tier Investment & Physical Targets", h2_style))
    st_table_data = [
        [
            Paragraph("Education Tier", table_cell_header),
            Paragraph("Distance Norm", table_cell_header),
            Paragraph("Existing Schools", table_cell_header),
            Paragraph("Baseline Coverage", table_cell_header),
            Paragraph("Proposed Upgrades", table_cell_header),
            Paragraph("Proposed New", table_cell_header),
            Paragraph("Transport Hubs", table_cell_header),
            Paragraph("Target Coverage", table_cell_header),
            Paragraph("Total Est. Budget", table_cell_header)
        ]
    ]

    for t_name, t_vals in assessment_data["statewide_totals"].items():
        st_table_data.append([
            Paragraph(f"<b>{t_name}</b>", table_cell),
            Paragraph(f"{assessment_data['metadata']['tier_standards'][t_name]['norm_distance_km']} km", table_cell),
            Paragraph(f"{t_vals['existing_schools']:,}", table_cell),
            Paragraph(f"{t_vals['initial_coverage_pct']}%", table_cell),
            Paragraph(f"{t_vals['proposed_upgrades']:,}", table_cell),
            Paragraph(f"{t_vals['proposed_new_schools']:,}", table_cell),
            Paragraph(f"{t_vals['proposed_transport_hubs']:,}", table_cell),
            Paragraph(f"<b>{t_vals['final_coverage_pct']}%</b>", table_cell_bold),
            Paragraph(f"<b>₹{t_vals['total_budget_cr']:,.1f} Cr</b>", table_cell_bold)
        ])

    t_st = Table(st_table_data, colWidths=[70, 52, 52, 54, 54, 52, 54, 58, 77])
    t_st.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COL),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, PANEL_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    story.append(t_st)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: GLOBAL ANALYTICS SPREAD (PART 1: RETENTION & PARETO FRONTIER)
    # =========================================================================
    story.append(Paragraph("2. Global Spatial Analytics: The Accessibility Cliff & Efficiency Frontier", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceBefore=2, spaceAfter=8))

    chart1 = os.path.join(ASSETS_DIR, "chart_dropout_cliff.png")
    chart5 = os.path.join(ASSETS_DIR, "chart_mclp_frontier.png")

    if os.path.exists(chart1):
        story.append(Image(chart1, width=500, height=260))
        story.append(Spacer(1, 4))
    if os.path.exists(chart5):
        story.append(Image(chart5, width=500, height=260))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: GLOBAL ANALYTICS SPREAD (PART 2: BUDGET & GENDER EQUITY)
    # =========================================================================
    story.append(Paragraph("3. Multi-Tier Financial Allocation & Social / Gender Equity Model", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceBefore=2, spaceAfter=8))

    chart2 = os.path.join(ASSETS_DIR, "chart_budget_breakdown.png")
    chart6 = os.path.join(ASSETS_DIR, "chart_gender_equity.png")

    if os.path.exists(chart2):
        story.append(Image(chart2, width=500, height=260))
        story.append(Spacer(1, 4))
    if os.path.exists(chart6):
        story.append(Image(chart6, width=500, height=260))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: COVERAGE TRANSFORMATION & PRIORITY RANKING
    # =========================================================================
    story.append(Paragraph("4. Statewide Coverage Transformation & Vulnerability Ranking", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceBefore=2, spaceAfter=8))

    chart3 = os.path.join(ASSETS_DIR, "chart_coverage_by_tier.png")
    chart4 = os.path.join(ASSETS_DIR, "chart_district_priority_ranking.png")

    if os.path.exists(chart3):
        story.append(Image(chart3, width=500, height=230))
        story.append(Spacer(1, 4))
    if os.path.exists(chart4):
        story.append(Image(chart4, width=500, height=360))

    story.append(PageBreak())

    # =========================================================================
    # PAGES 6-7: STATEWIDE 30-DISTRICT COMPARATIVE MATRIX (SECONDARY TIER)
    # =========================================================================
    story.append(Paragraph("5. Statewide District Comparative Matrix (Secondary Tier)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceBefore=2, spaceAfter=6))
    story.append(Paragraph("Detailed analytical breakdown of spatial coverage, required interventions, staff recruitment, and estimated capital outlay across all 30 districts of Odisha for the Secondary Schooling Tier (5 km catchment standard).", body_style))

    dists = assessment_data["districts"]
    for page_idx, dist_slice in enumerate([dists[:15], dists[15:]]):
        dist_table_data = [
            [
                Paragraph("District", table_cell_header),
                Paragraph("Terrain / Category", table_cell_header),
                Paragraph("Friction", table_cell_header),
                Paragraph("Blocks", table_cell_header),
                Paragraph("Existing", table_cell_header),
                Paragraph("Base Cov.", table_cell_header),
                Paragraph("Upgrades", table_cell_header),
                Paragraph("New Sch.", table_cell_header),
                Paragraph("Transit", table_cell_header),
                Paragraph("Target Cov.", table_cell_header),
                Paragraph("Teachers", table_cell_header),
                Paragraph("Est. Outlay", table_cell_header)
            ]
        ]

        for d in dist_slice:
            sec = d["tiers"]["Secondary"]
            prof = d["profile"]
            dist_table_data.append([
                Paragraph(f"<b>{d['district_name']}</b>", table_cell),
                Paragraph(prof['category'], table_cell),
                Paragraph(f"{d.get('terrain_friction_factor', 1.0)}x", table_cell),
                Paragraph(str(len(d.get('blocks', []))), table_cell),
                Paragraph(f"{sec['existing_schools']:,}", table_cell),
                Paragraph(f"{sec['initial_coverage_pct']}%", table_cell),
                Paragraph(str(sec['proposed_upgrades']), table_cell),
                Paragraph(str(sec['proposed_new_schools']), table_cell),
                Paragraph(str(sec['proposed_transport_hubs']), table_cell),
                Paragraph(f"<b>{sec['final_coverage_pct']}%</b>", table_cell_bold),
                Paragraph(str(sec.get('teachers_required', 0)), table_cell),
                Paragraph(f"<b>₹{sec['total_budget_cr']:.2f} Cr</b>", table_cell_bold)
            ])

        t_dist = Table(dist_table_data, colWidths=[62, 75, 28, 26, 34, 40, 36, 36, 34, 44, 38, 48])
        t_dist.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
            ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COL),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, PANEL_BG]),
            ('TOPPADDING', (0, 0), (-1, -1), 3.5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ]))
        story.append(t_dist)
        story.append(PageBreak())

    # =========================================================================
    # PAGES 8-37: 30 DISTRICT DEEP-DIVE PROFILES
    # =========================================================================
    print("Assembling 30 district deep-dive profile pages...")
    for i, d in enumerate(dists):
        dist_name = d["district_name"]
        prof = d["profile"]
        sec = d["tiers"]["Secondary"]
        map_filename = f"dist_{dist_name.lower().replace(' ', '_')}.png"
        map_path = os.path.join(MAPS_DIR, map_filename)

        dist_flowables = []

        header_text = f"6.{i+1} District Profile: {dist_name} ({len(d.get('blocks', []))} CD Blocks)"
        dist_flowables.append(Paragraph(header_text, h1_style))
        dist_flowables.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceBefore=1, spaceAfter=5))

        if os.path.exists(map_path):
            dist_flowables.append(Image(map_path, width=370, height=370))
            dist_flowables.append(Spacer(1, 5))

        # KPI Table
        kpi_table_data = [
            [
                Paragraph("Metric", table_cell_header),
                Paragraph("Primary (1km)", table_cell_header),
                Paragraph("Upper Primary (3km)", table_cell_header),
                Paragraph("Secondary (5km)", table_cell_header),
                Paragraph("Higher Sec. (7km)", table_cell_header),
            ],
            [
                Paragraph("<b>Baseline Access</b>", table_cell),
                Paragraph(f"{d['tiers']['Primary']['initial_coverage_pct']}%", table_cell),
                Paragraph(f"{d['tiers']['Upper Primary']['initial_coverage_pct']}%", table_cell),
                Paragraph(f"<b>{d['tiers']['Secondary']['initial_coverage_pct']}%</b>", table_cell_bold),
                Paragraph(f"{d['tiers']['Higher Secondary']['initial_coverage_pct']}%", table_cell),
            ],
            [
                Paragraph("<b>Proposed Upgrades</b>", table_cell),
                Paragraph(str(d['tiers']['Primary']['proposed_upgrades']), table_cell),
                Paragraph(str(d['tiers']['Upper Primary']['proposed_upgrades']), table_cell),
                Paragraph(f"<b>{d['tiers']['Secondary']['proposed_upgrades']}</b>", table_cell_bold),
                Paragraph(str(d['tiers']['Higher Secondary']['proposed_upgrades']), table_cell),
            ],
            [
                Paragraph("<b>New Greenfield Campuses</b>", table_cell),
                Paragraph(str(d['tiers']['Primary']['proposed_new_schools']), table_cell),
                Paragraph(str(d['tiers']['Upper Primary']['proposed_new_schools']), table_cell),
                Paragraph(f"<b>{d['tiers']['Secondary']['proposed_new_schools']}</b>", table_cell_bold),
                Paragraph(str(d['tiers']['Higher Secondary']['proposed_new_schools']), table_cell),
            ],
            [
                Paragraph("<b>Transport & Hostel Hubs</b>", table_cell),
                Paragraph(str(d['tiers']['Primary']['proposed_transport_hubs']), table_cell),
                Paragraph(str(d['tiers']['Upper Primary']['proposed_transport_hubs']), table_cell),
                Paragraph(f"<b>{d['tiers']['Secondary']['proposed_transport_hubs']}</b>", table_cell_bold),
                Paragraph(str(d['tiers']['Higher Secondary']['proposed_transport_hubs']), table_cell),
            ],
            [
                Paragraph("<b>Est. Capital Outlay</b>", table_cell),
                Paragraph(f"₹{d['tiers']['Primary']['total_budget_cr']:.2f} Cr", table_cell),
                Paragraph(f"₹{d['tiers']['Upper Primary']['total_budget_cr']:.2f} Cr", table_cell),
                Paragraph(f"<b>₹{d['tiers']['Secondary']['total_budget_cr']:.2f} Cr</b>", table_cell_bold),
                Paragraph(f"₹{d['tiers']['Higher Secondary']['total_budget_cr']:.2f} Cr", table_cell),
            ]
        ]

        t_kpi = Table(kpi_table_data, colWidths=[123, 100, 100, 100, 100])
        t_kpi.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
            ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COL),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, PANEL_BG]),
            ('TOPPADDING', (0, 0), (-1, -1), 2.0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2.0),
        ]))
        dist_flowables.append(t_kpi)
        dist_flowables.append(Spacer(1, 4))

        # Strategic Brief
        strategy_box = [
            [Paragraph(f"<b>Operations Research Strategy:</b> {d['strategy']}", body_style)]
        ]
        t_box = Table(strategy_box, colWidths=[523])
        t_box.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), LIGHT_BG),
            ('BOX', (0, 0), (-1, -1), 0.8, SECONDARY),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 7),
            ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ]))
        dist_flowables.append(t_box)

        story.append(KeepTogether(dist_flowables))
        story.append(PageBreak())

    # =========================================================================
    # PAGES 38+: 314-BLOCK COMPREHENSIVE APPENDIX MATRIX
    # =========================================================================
    print("Assembling 314-block comprehensive appendix tables...")
    story.append(Paragraph("7. Comprehensive 314-Block Analytical Appendix", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceBefore=2, spaceAfter=6))
    story.append(Paragraph("Complete micro-demographic and secondary infrastructure allocation matrix across all 314 Community Development (CD) Blocks in Odisha.", body_style))

    all_blocks_flat = []
    for d in dists:
        for b in d.get("blocks", []):
            all_blocks_flat.append({
                "district": d["district_name"],
                "block": b["block_name"],
                "population": b["population"],
                "habitations": b["habitations"],
                "vuln": b["vulnerability_score"],
                "base_cov": b["baseline_coverage_pct"],
                "target_cov": b["target_coverage_pct"],
                "upgrades": b["proposed_upgrades"],
                "new_sch": b["proposed_new_schools"],
                "transit": b["proposed_transport_hubs"],
                "cost_cr": b["estimated_budget_cr"]
            })

    # Chunk blocks ~35 per page
    chunk_size = 35
    for start_idx in range(0, len(all_blocks_flat), chunk_size):
        chunk = all_blocks_flat[start_idx:start_idx + chunk_size]
        block_table_data = [
            [
                Paragraph("District", table_cell_header),
                Paragraph("CD Block", table_cell_header),
                Paragraph("Population", table_cell_header),
                Paragraph("Habs", table_cell_header),
                Paragraph("Vuln.", table_cell_header),
                Paragraph("Base Cov.", table_cell_header),
                Paragraph("Target Cov.", table_cell_header),
                Paragraph("Upgrades", table_cell_header),
                Paragraph("New", table_cell_header),
                Paragraph("Transit", table_cell_header),
                Paragraph("Est. Outlay", table_cell_header)
            ]
        ]

        for b in chunk:
            block_table_data.append([
                Paragraph(b["district"], table_cell),
                Paragraph(f"<b>{b['block']}</b>", table_cell),
                Paragraph(f"{b['population']:,}", table_cell),
                Paragraph(str(b['habitations']), table_cell),
                Paragraph(str(b['vuln']), table_cell),
                Paragraph(f"{b['base_cov']}%", table_cell),
                Paragraph(f"<b>{b['target_cov']}%</b>", table_cell_bold),
                Paragraph(str(b['upgrades']), table_cell),
                Paragraph(str(b['new_sch']), table_cell),
                Paragraph(str(b['transit']), table_cell),
                Paragraph(f"₹{b['cost_cr']:.2f} Cr", table_cell)
            ])

        t_blk = Table(block_table_data, colWidths=[65, 80, 50, 32, 28, 45, 48, 40, 32, 35, 50])
        t_blk.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
            ('GRID', (0, 0), (-1, -1), 0.4, BORDER_COL),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, PANEL_BG]),
            ('TOPPADDING', (0, 0), (-1, -1), 2.5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ]))
        story.append(t_blk)
        story.append(PageBreak())

    # =========================================================================
    # FINAL SECTION: IMPLEMENTATION ROADMAP & STAFFING
    # =========================================================================
    story.append(Paragraph("8. Implementation Roadmap, Staff Recruitment & Governance", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceBefore=2, spaceAfter=8))

    roadmap_text = (
        "To achieve universal secondary schooling equity efficiently across all 314 blocks, the masterplan establishes a structured 3-phase rollout:<br/><br/>"
        "<b>Phase 1: High Vulnerability & Remote Tribal Corridors (Years 1–2 | 45% Outlay)</b><br/>"
        "• <b>Priority Districts:</b> Malkangiri, Koraput, Rayagada, Kandhamal, Gajapati, Nabarangpur, Mayurbhanj, Nuapada, Kalahandi.<br/>"
        "• <b>Interventions:</b> Fast-track construction of 588 dedicated girls' hostels, deployment of 1,172 student transit hubs, and 4,115 subject teacher recruitments.<br/><br/>"
        "<b>Phase 2: Mineral Belts, Plateaus & Western Agrarian Plains (Years 3–4 | 35% Outlay)</b><br/>"
        "• <b>Priority Districts:</b> Kendujhar, Sundargarh, Deogarh, Balangir, Boudh, Sambalpur, Bargarh, Subarnapur, Angul, Dhenkanal, Nayagarh.<br/>"
        "• <b>Interventions:</b> Construction of greenfield high schools in dense mining periphery settlements and 3,200 subject teacher recruitments.<br/><br/>"
        "<b>Phase 3: Coastal Deltas, Disaster Retrofits & Urban Consolidation (Year 5 | 20% Outlay)</b><br/>"
        "• <b>Priority Districts:</b> Khordha, Cuttack, Puri, Jagatsinghpur, Kendrapara, Jajpur, Bhadrak, Balasore, Ganjam, Jharsuguda.<br/>"
        "• <b>Interventions:</b> 396 cyclone-resilient structural retrofits, advanced STEM smart-lab installations, and digital classroom integration."
    )
    story.append(Paragraph(roadmap_text, body_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Secondary Subject Teacher Staffing & Quality Framework (1:30 PTR)", h2_style))
    staff_text = (
        "Physical infrastructure expansion must be matched with academic personnel to ensure educational quality:<br/>"
        "• <b>Total Secondary Subject Teachers Required:</b> <b>9,144 Posts</b> (4 per new school: Math, Science, English, Social Science; 2 per school upgrade).<br/>"
        "• <b>Special Tribal Area Allowances:</b> Hardship and transport allowances for teachers posted in Tobler friction zones (&gt;1.8x terrain impedance).<br/>"
        "• <b>Real-Time GIS Performance Dashboard:</b> Sat-verified construction milestone audits and biometric student attendance across 5km catchment corridors."
    )
    story.append(Paragraph(staff_text, body_style))

    # Build Document
    print(f"Compiling advanced publication-grade PDF into {OUTPUT_PDF}...")
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Masterplan PDF successfully generated! File size: {os.path.getsize(OUTPUT_PDF) / (1024 * 1024):.2f} MB")


if __name__ == "__main__":
    create_masterplan_pdf()
