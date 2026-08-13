"""
Odisha Spatial Education Masterplan: Publication-Grade PDF Assembly Engine
Assembles a unified, publication-quality masterplan report featuring:
- Two-pass canvas for dynamic "Page X of Y" numbering and running headers/footers
- Undistorted 1:1 square district map embeds
- Untruncated strategic briefs
- Multi-tier data tables with calculated analytical metrics
- Structured executive and global analytics spreads
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
        header_text_right = "SPATIAL SCHOOL EDUCATION MASTERPLAN"
        self.drawString(36, 842 - 32, header_text_left)
        self.drawRightString(595 - 36, 842 - 32, header_text_right)
        
        self.setStrokeColor(BORDER_COL)
        self.setLineWidth(0.75)
        self.line(36, 842 - 38, 595 - 36, 842 - 38)

        # Running Footer
        footer_text_left = "CONFIDENTIAL & PROPRIETARY — GIS SPATIAL OPTIMIZATION STUDY"
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

    # Custom Clean Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=PRIMARY,
        alignment=1, # Center
        spaceAfter=10
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=MUTED_TEXT,
        alignment=1,
        spaceAfter=20
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=PRIMARY,
        spaceBefore=12,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=SECONDARY,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=DARK_TEXT,
        spaceAfter=6
    )

    body_bold = ParagraphStyle(
        'Body_Bold_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=DARK_TEXT,
        spaceAfter=6
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=DARK_TEXT
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=DARK_TEXT
    )

    table_cell_header = ParagraphStyle(
        'TableCellHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=1
    )

    story = []

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 30))
    story.append(Paragraph("STATE GOVERNMENT OF ODISHA", ParagraphStyle('GovtHeader', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=SECONDARY, alignment=1, spaceAfter=8)))
    story.append(Paragraph("DEPARTMENT OF SCHOOL & MASS EDUCATION", ParagraphStyle('DeptHeader', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=MUTED_TEXT, alignment=1, spaceAfter=25)))
    
    story.append(HRFlowable(width="60%", thickness=2, color=PRIMARY, spaceBefore=5, spaceAfter=25))
    
    story.append(Paragraph("ODISHA SPATIAL SCHOOL EDUCATION<br/>MASTERPLAN (2026–2031)", title_style))
    story.append(Paragraph("A Comprehensive Data-Driven GIS Optimization, Universal Secondary Access Framework,<br/>and Multi-Tier Capital Outlay Estimation for All 30 Districts", subtitle_style))
    
    story.append(Spacer(1, 15))

    # Executive Key Highlights Block
    sec_totals = assessment_data["statewide_totals"]["Secondary"]
    total_schools_proposed = sec_totals["proposed_upgrades"] + sec_totals["proposed_new_schools"] + sec_totals["proposed_transport_hubs"]
    
    kpi_data = [
        [
            Paragraph(f"<b>{sec_totals['initial_coverage_pct']}% → {sec_totals['final_coverage_pct']}%</b><br/><font size=7 color='#64748B'>Statewide Secondary Access</font>", table_cell_bold),
            Paragraph(f"<b>{sec_totals['proposed_upgrades']:,}</b><br/><font size=7 color='#64748B'>High School Upgrades</font>", table_cell_bold),
            Paragraph(f"<b>{sec_totals['proposed_new_schools']:,}</b><br/><font size=7 color='#64748B'>New Greenfield Campuses</font>", table_cell_bold)
        ],
        [
            Paragraph(f"<b>{sec_totals['proposed_transport_hubs']:,}</b><br/><font size=7 color='#64748B'>Transport/Hostel Hubs</font>", table_cell_bold),
            Paragraph(f"<b>₹{sec_totals['total_budget_cr']:,.1f} Cr</b><br/><font size=7 color='#64748B'>Est. Secondary Outlay</font>", table_cell_bold),
            Paragraph(f"<b>30 Districts</b><br/><font size=7 color='#64748B'>Universal State Coverage</font>", table_cell_bold)
        ]
    ]
    t_kpi = Table(kpi_data, colWidths=[165, 165, 165])
    t_kpi.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), PANEL_BG),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.8, BORDER_COL),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_kpi)

    story.append(Spacer(1, 45))

    meta_text = (
        "<b>Prepared By:</b> Directorate of Spatial Planning & Educational Infrastructure<br/>"
        "<b>Geospatial Engine:</b> GIS Micro-Demographic Catchment Buffer Model (RTE / RMSA Norms)<br/>"
        "<b>Published:</b> August 2026 | Bhubaneswar, Odisha"
    )
    story.append(Paragraph(meta_text, ParagraphStyle('MetaStyle', fontName='Helvetica', fontSize=8.5, leading=12, textColor=MUTED_TEXT, alignment=1)))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: EXECUTIVE SUMMARY & METHODOLOGY
    # =========================================================================
    story.append(Paragraph("1. Executive Summary & Spatial Optimization Methodology", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceBefore=2, spaceAfter=10))

    exec_summary_p1 = (
        "The <b>Odisha Spatial School Education Masterplan</b> represents an evidence-based, geospatial planning roadmap designed to eliminate "
        "structural access barriers across all 30 districts of Odisha. While foundational primary schooling achieves widespread geographic penetration, "
        "the secondary education tier (Grades 9–10) suffers from severe spatial dropouts, particularly across the rugged Eastern Ghats and dense tribal hinterlands. "
        "This masterplan utilizes high-resolution habitation mapping and polygon boundary modeling to accurately identify every unserved community cluster "
        "and establish the true capital and operational budget required for universal education access."
    )
    story.append(Paragraph(exec_summary_p1, body_style))

    story.append(Paragraph("Spatial Buffer Standards & Policy Framework", h2_style))
    method_text = (
        "In accordance with the <b>Right to Education (RTE) Act</b>, <b>Samagra Shiksha Abhiyan</b>, and <b>National Education Policy (NEP 2020)</b>, "
        "the geospatial model implements rigorous distance thresholds for each tier:<br/>"
        "• <b>Primary Tier (Grades 1–5):</b> 1.0 km walking radius benchmark.<br/>"
        "• <b>Upper Primary Tier (Grades 6–8):</b> 3.0 km radius benchmark.<br/>"
        "• <b>Secondary Tier (Grades 9–10):</b> 5.0 km catchment radius benchmark.<br/>"
        "• <b>Higher Secondary Tier (Grades 11–12):</b> 7.0 km radius benchmark."
    )
    story.append(Paragraph(method_text, body_style))

    story.append(Paragraph("Tri-Pillar Spatial Allocation Strategy", h2_style))
    strategy_text = (
        "Rather than relying on blanket or arbitrary school construction, the engine applies an optimized 3-pillar decision framework:<br/>"
        "1. <b>Infrastructure Upgrades (₹85.0L per school):</b> Existing Upper Primary schools situated near unserved secondary clusters are expanded into integrated High Schools.<br/>"
        "2. <b>Greenfield High School Campuses (₹244.0L per school):</b> State-of-the-art new secondary campuses are constructed in densely populated habitations lacking nearby infrastructure.<br/>"
        "3. <b>Transport & Residential Hostel Hubs (₹30.0L per hub):</b> In sparse, rugged tribal topographies where daily walking is impeded by terrain and dense forests, dedicated transit networks and residential hostels are funded to ensure 100% access without redundant construction."
    )
    story.append(Paragraph(strategy_text, body_style))

    story.append(Paragraph("Statewide Financial & Physical Investment Summary", h2_style))
    
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
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_st)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: GLOBAL ANALYTICS & INSIGHTS
    # =========================================================================
    story.append(Paragraph("2. Global Spatial Analytics & Systemic Insights", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("The Spatial Accessibility Cliff & Budget Breakdown", h2_style))
    
    chart1_path = os.path.join(ASSETS_DIR, "chart_dropout_cliff.png")
    chart2_path = os.path.join(ASSETS_DIR, "chart_budget_breakdown.png")

    if os.path.exists(chart1_path):
        story.append(Image(chart1_path, width=500, height=270))
        story.append(Spacer(1, 6))

    if os.path.exists(chart2_path):
        story.append(Image(chart2_path, width=500, height=270))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: COVERAGE TRANSFORMATION & PRIORITY RANKING
    # =========================================================================
    story.append(Paragraph("3. Statewide Access Transformation & Vulnerability Ranking", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceBefore=2, spaceAfter=10))

    chart3_path = os.path.join(ASSETS_DIR, "chart_coverage_by_tier.png")
    chart4_path = os.path.join(ASSETS_DIR, "chart_district_priority_ranking.png")

    if os.path.exists(chart3_path):
        story.append(Image(chart3_path, width=500, height=240))
        story.append(Spacer(1, 6))

    if os.path.exists(chart4_path):
        story.append(Image(chart4_path, width=500, height=360))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5-6: STATEWIDE 30-DISTRICT COMPARATIVE MATRIX (SECONDARY TIER)
    # =========================================================================
    story.append(Paragraph("4. Statewide District Comparative Matrix (Secondary Tier)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceBefore=2, spaceAfter=8))
    story.append(Paragraph("Detailed analytical breakdown of spatial coverage, required interventions, and estimated capital outlay across all 30 districts of Odisha for the Secondary Schooling Tier (5 km catchment standard).", body_style))

    # Split 30 districts into 2 tables of 15 each for perfect page fitting
    dists = assessment_data["districts"]
    
    for page_idx, dist_slice in enumerate([dists[:15], dists[15:]]):
        dist_table_data = [
            [
                Paragraph("District", table_cell_header),
                Paragraph("Terrain / Category", table_cell_header),
                Paragraph("Vuln.", table_cell_header),
                Paragraph("Habitations", table_cell_header),
                Paragraph("Existing", table_cell_header),
                Paragraph("Base Cov.", table_cell_header),
                Paragraph("Upgrades", table_cell_header),
                Paragraph("New Sch.", table_cell_header),
                Paragraph("Trans. Hubs", table_cell_header),
                Paragraph("Final Cov.", table_cell_header),
                Paragraph("Est. Outlay", table_cell_header)
            ]
        ]

        for d in dist_slice:
            sec = d["tiers"]["Secondary"]
            prof = d["profile"]
            dist_table_data.append([
                Paragraph(f"<b>{d['district_name']}</b>", table_cell),
                Paragraph(prof['category'], table_cell),
                Paragraph(str(prof['vulnerability']), table_cell),
                Paragraph(f"{sec['habitations_total']:,}", table_cell),
                Paragraph(f"{sec['existing_schools']:,}", table_cell),
                Paragraph(f"{sec['initial_coverage_pct']}%", table_cell),
                Paragraph(str(sec['proposed_upgrades']), table_cell),
                Paragraph(str(sec['proposed_new_schools']), table_cell),
                Paragraph(str(sec['proposed_transport_hubs']), table_cell),
                Paragraph(f"<b>{sec['final_coverage_pct']}%</b>", table_cell_bold),
                Paragraph(f"<b>₹{sec['total_budget_cr']:.2f} Cr</b>", table_cell_bold)
            ])

        t_dist = Table(dist_table_data, colWidths=[65, 80, 28, 48, 38, 45, 42, 42, 45, 45, 45])
        t_dist.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
            ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COL),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, PANEL_BG]),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(t_dist)
        story.append(PageBreak())

    # =========================================================================
    # PAGES 7+: 30 DISTRICT DEEP-DIVE PROFILES
    # =========================================================================
    print("Assembling 30 district deep-dive profile pages...")

    for i, d in enumerate(dists):
        dist_name = d["district_name"]
        prof = d["profile"]
        sec = d["tiers"]["Secondary"]
        map_filename = f"dist_{dist_name.lower().replace(' ', '_')}.png"
        map_path = os.path.join(MAPS_DIR, map_filename)

        dist_flowables = []

        # District Header with Category & Vulnerability Badge
        header_text = f"5.{i+1} District Profile: {dist_name}"
        dist_flowables.append(Paragraph(header_text, h1_style))
        dist_flowables.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceBefore=1, spaceAfter=6))

        # Undistorted Square Map Image (370 x 370 pt)
        if os.path.exists(map_path):
            dist_flowables.append(Image(map_path, width=370, height=370))
            dist_flowables.append(Spacer(1, 6))

        # District KPI Table
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
            ('TOPPADDING', (0, 0), (-1, -1), 2.5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ]))
        dist_flowables.append(t_kpi)
        dist_flowables.append(Spacer(1, 5))

        # Strategic Brief
        strategy_box = [
            [Paragraph(f"<b>Strategic Roadmap & Recommendations:</b> {d['strategy']}", body_style)]
        ]
        t_box = Table(strategy_box, colWidths=[523])
        t_box.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), LIGHT_BG),
            ('BOX', (0, 0), (-1, -1), 0.8, SECONDARY),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        dist_flowables.append(t_box)

        # Wrap in KeepTogether to ensure cohesive single-page presentation
        story.append(KeepTogether(dist_flowables))
        story.append(PageBreak())

    # =========================================================================
    # FINAL SECTION: IMPLEMENTATION ROADMAP & CAPITAL ROLLOUT
    # =========================================================================
    story.append(Paragraph("6. Implementation Roadmap & Phased Capital Rollout", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceBefore=2, spaceAfter=10))

    roadmap_text = (
        "To maximize systemic impact and address acute inequities swiftly, the masterplan establishes a 3-phase capital deployment schedule:<br/><br/>"
        "<b>Phase 1: High Vulnerability & Remote Tribal Districts (Years 1–2 | 45% Capital Outlay)</b><br/>"
        "• Target Districts: Malkangiri, Koraput, Rayagada, Kandhamal, Gajapati, Nabarangpur, Mayurbhanj, Nuapada, Kalahandi.<br/>"
        "• Strategic Focus: Immediate rollout of residential hostel hubs and critical high school upgrades in inaccessible forest valleys to halt the Class 8–9 dropout cliff.<br/><br/>"
        "<b>Phase 2: Mineral Belts, Plateaus & Semi-Arid Plains (Years 3–4 | 35% Capital Outlay)</b><br/>"
        "• Target Districts: Kendujhar, Sundargarh, Deogarh, Balangir, Boudh, Sambalpur, Bargarh, Subarnapur, Angul, Dhenkanal, Nayagarh.<br/>"
        "• Strategic Focus: Construction of greenfield high schools in dense mining/industrial periphery habitations and transport route expansion.<br/><br/>"
        "<b>Phase 3: Coastal Plains, River Deltas & Urban Consolidations (Year 5 | 20% Capital Outlay)</b><br/>"
        "• Target Districts: Khordha, Cuttack, Puri, Jagatsinghpur, Kendrapara, Jajpur, Bhadrak, Balasore, Ganjam, Jharsuguda.<br/>"
        "• Strategic Focus: School modernization, smart lab integration, digital connectivity, and transport network optimization for high-density coastal belts."
    )
    story.append(Paragraph(roadmap_text, body_style))
    story.append(Spacer(1, 15))

    story.append(Paragraph("Monitoring, GIS Auditing & Governance Protocol", h2_style))
    gov_text = (
        "1. <b>Real-Time GIS Portal:</b> Every proposed upgrade and greenfield asset will be geofenced and monitored via satellite imagery and geo-tagged milestone verification.<br/>"
        "2. <b>Habitation-Level Tracking:</b> Block Education Officers (BEOs) will maintain real-time student tracking across 5km catchment corridors to measure retention gains.<br/>"
        "3. <b>Dynamic Route Rationalization:</b> Transport fleet allocations will be continuously re-routed using road-network graph algorithms to ensure zero unserved habitations."
    )
    story.append(Paragraph(gov_text, body_style))

    # Build Document
    print(f"Compiling publication-grade PDF into {OUTPUT_PDF}...")
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Masterplan PDF successfully generated! File size: {os.path.getsize(OUTPUT_PDF) / (1024 * 1024):.2f} MB")


if __name__ == "__main__":
    create_masterplan_pdf()
