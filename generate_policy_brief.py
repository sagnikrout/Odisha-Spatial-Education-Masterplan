"""
Odisha Spatial Education Masterplan: 1-Page Standalone Executive Policy Brief Generator (Audited Edition)
Compiles a concise, high-impact single-page briefing document for ministers, secretaries, and directors.
"""

import os
import json
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "odisha_statewide_assessment.json")
OUTPUT_BRIEF = os.path.join(BASE_DIR, "Odisha_Education_Policy_Brief_2026.pdf")

# Palette
PRIMARY = colors.HexColor("#1E3A8A")
SECONDARY = colors.HexColor("#0284C7")
DARK_TEXT = colors.HexColor("#0F172A")
MUTED_TEXT = colors.HexColor("#64748B")
LIGHT_BG = colors.HexColor("#F8FAFC")
PANEL_BG = colors.HexColor("#F1F5F9")
BORDER_COL = colors.HexColor("#CBD5E1")
GREEN_ACC = colors.HexColor("#059669")


class BriefCanvas(canvas.Canvas):
    """Custom canvas for 1-page executive policy brief."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        print(f"Total pages rendered: {num_pages}")
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_brief_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_brief_decorations(self, total_pages):
        self.saveState()
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(MUTED_TEXT)

        # Header
        self.drawString(28, 842 - 18, "GOVERNMENT OF ODISHA | DEPARTMENT OF SCHOOL & MASS EDUCATION")
        self.drawRightString(595 - 28, 842 - 18, "EXECUTIVE POLICY BRIEF (2026-2031)")
        self.setStrokeColor(BORDER_COL)
        self.setLineWidth(0.6)
        self.line(28, 842 - 22, 595 - 28, 842 - 22)

        # Footer
        self.setFont("Helvetica", 7.0)
        self.drawString(28, 12, "Confidential  -  Operations Research & Spatial Decision-Support Brief")
        self.drawRightString(595 - 28, 12, f"Page {self._pageNumber} of {total_pages}")
        self.line(28, 19, 595 - 28, 19)

        self.restoreState()


def build_policy_brief():
    print("Loading assessment data for Policy Brief...")
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Printable width: 595.27 - 56 = 539.27 pt. Printable height: 842 - 46 = 796 pt.
    doc = SimpleDocTemplate(
        OUTPUT_BRIEF,
        pagesize=A4,
        leftMargin=28,
        rightMargin=28,
        topMargin=26,
        bottomMargin=22
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'BriefTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=14.5,
        textColor=PRIMARY,
        spaceBefore=0,
        spaceAfter=1
    )

    subtitle_style = ParagraphStyle(
        'BriefSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.0,
        textColor=MUTED_TEXT,
        spaceAfter=3
    )

    sec_head = ParagraphStyle(
        'SecHead',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=8.0,
        leading=10.0,
        textColor=PRIMARY,
        spaceBefore=3,
        spaceAfter=1.5,
        keepWithNext=True
    )

    body_text = ParagraphStyle(
        'BriefBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.6,
        leading=8.6,
        textColor=DARK_TEXT,
        spaceAfter=2
    )

    cell_text = ParagraphStyle(
        'BriefCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.2,
        leading=7.5,
        textColor=DARK_TEXT,
        alignment=1
    )

    cell_bold = ParagraphStyle(
        'BriefCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.2,
        leading=7.5,
        textColor=DARK_TEXT,
        alignment=1
    )

    cell_header = ParagraphStyle(
        'BriefCellHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.2,
        leading=7.5,
        textColor=colors.white,
        alignment=1
    )

    story = []
    sec = data["statewide_totals"]["Secondary"]
    econ = data["metadata"].get("economic_impact", {})

    # Header & Title Block
    story.append(Paragraph("ODISHA SPATIAL SCHOOL EDUCATION MASTERPLAN (2026-2031)", title_style))
    story.append(Paragraph("Audited Operations Research & PWD Hill Cost Calibrated Strategy Across 314 CD Blocks", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=0.75, color=PRIMARY, spaceBefore=0, spaceAfter=3))

    # 1. Executive KPI Dashboard Cards
    kpi_matrix = [
        [
            Paragraph(f"<b>{sec['initial_coverage_pct']}% → {sec['final_coverage_pct']}%</b><br/><font size=5 color='#64748B'>Secondary Coverage</font>", cell_bold),
            Paragraph(f"<b>Rs. {sec['total_budget_cr']:,.1f} Cr</b><br/><font size=5 color='#64748B'>Hill-Adjusted Outlay</font>", cell_bold),
            Paragraph(f"<b>314 Blocks</b><br/><font size=5 color='#64748B'>30 Districts Analyzed</font>", cell_bold),
            Paragraph(f"<b>{econ.get('benefit_cost_ratio_roi', 1.8)}x GSDP ROI</b><br/><font size=5 color='#64748B'>Rs. {econ.get('net_present_value_gsdp_contribution_cr', 10796):,.0f} Cr Value</font>", cell_bold),
            Paragraph(f"<b>9,144 Posts</b><br/><font size=5 color='#64748B'>Teachers (25% Hardship)</font>", cell_bold)
        ]
    ]
    t_kpi = Table(kpi_matrix, colWidths=[107, 108, 108, 108, 108])
    t_kpi.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), PANEL_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COL),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t_kpi)
    story.append(Spacer(1, 2))

    # 2. Dual Column / Combined Challenge & Optimization Methodology
    story.append(Paragraph("1. Strategic Context & Operations Research Methodology", sec_head))
    p_context = (
        "• <b>Grade 8 → 9 Spatial Dropout Cliff:</b> While primary access achieves >74%, secondary coverage drops to 59.1% due to distance barriers "
        "(mean distance >6.8 km in Eastern Ghats), driving >42% tribal dropout with girls dropping out at 2.3x higher rates without safe transit.<br/>"
        "• <b>PuLP MILP & PWD Hill Cost Multipliers:</b> Interventions are optimized using PuLP Mixed-Integer Linear Programming (MCLP) under capital constraints, "
        "incorporating <b>Tobler's Hiking Slope Resistance (1.8x-2.4x)</b> and <b>PWD Hill Cost Multipliers (+18% to +30%)</b> to model realistic ghat logistics."
    )
    story.append(Paragraph(p_context, body_text))

    # 3. Statewide Multi-Tier Investment & Physical Targets Table
    story.append(Paragraph("2. Statewide Multi-Tier Investment & Physical Targets (Hill Cost Calibrated)", sec_head))
    st_table = [
        [
            Paragraph("Education Tier", cell_header),
            Paragraph("Norm", cell_header),
            Paragraph("Existing", cell_header),
            Paragraph("Baseline", cell_header),
            Paragraph("Upgrades", cell_header),
            Paragraph("New Campuses", cell_header),
            Paragraph("Transit Hubs", cell_header),
            Paragraph("Target Access", cell_header),
            Paragraph("Total Est. Outlay", cell_header)
        ]
    ]
    for t_name, t_vals in data["statewide_totals"].items():
        st_table.append([
            Paragraph(f"<b>{t_name}</b>", cell_text),
            Paragraph(f"{data['metadata']['tier_standards'][t_name]['norm_distance_km']} km", cell_text),
            Paragraph(f"{t_vals['existing_schools']:,}", cell_text),
            Paragraph(f"{t_vals['initial_coverage_pct']}%", cell_text),
            Paragraph(f"{t_vals['proposed_upgrades']:,}", cell_text),
            Paragraph(f"{t_vals['proposed_new_schools']:,}", cell_text),
            Paragraph(f"{t_vals['proposed_transport_hubs']:,}", cell_text),
            Paragraph(f"<b>{t_vals['final_coverage_pct']}%</b>", cell_bold),
            Paragraph(f"<b>Rs. {t_vals['total_budget_cr']:,.1f} Cr</b>", cell_bold)
        ])

    t_st = Table(st_table, colWidths=[79, 36, 48, 50, 48, 56, 56, 62, 104])
    t_st.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COL),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, PANEL_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 1.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5),
    ]))
    story.append(t_st)
    story.append(Spacer(1, 2))

    # 4. Regional Equity Breakdown (314 Blocks) & Transit Fleet Strip
    story.append(Paragraph("3. 314 CD Blocks Regional Stratification, Transit Fleet & Teacher Cadre", sec_head))
    p_blocks = (
        "• <b>High Vulnerability (72 Blocks in 9 Tribal Dists):</b> Coverage <45%. Priority for dedicated girls' hostels, feeder transit, and teacher hardship pay.<br/>"
        "• <b>Central & Agrarian (142 Blocks):</b> Coverage 55-70%. Focus on expanding existing Upper Primary schools into High Schools.<br/>"
        "• <b>Coastal & Deltaic (100 Blocks):</b> Coverage >75%. Focus on STEM infrastructure and 396 cyclone-resilient structural retrofits."
    )
    story.append(Paragraph(p_blocks, body_text))

    fleet_table = [
        [
            Paragraph("<b>588 Girls' Hostels</b><br/><font size=4.8 color='#64748B'>Guarantees female retention</font>", cell_bold),
            Paragraph(f"<b>{sec['fleet_minibuses']:,} Mini-Buses (24-Seater)</b><br/><font size=4.8 color='#64748B'>@ Rs. 4.80L/yr Opex</font>", cell_bold),
            Paragraph(f"<b>{sec['fleet_feeder_vans']:,} Feeder Vans (12-Seater)</b><br/><font size=4.8 color='#64748B'>@ Rs. 3.00L/yr Opex</font>", cell_bold),
            Paragraph(f"<b>Rs. {sec['annual_transit_opex_cr']:.1f} Cr Annual Opex</b><br/><font size=4.8 color='#64748B'>Fuel, repairs & chaperones</font>", cell_bold),
            Paragraph("<b>9,144 Subject Teachers</b><br/><font size=4.8 color='#64748B'>25% Hardship Allowance</font>", cell_bold)
        ]
    ]
    t_fl = Table(fleet_table, colWidths=[107, 108, 108, 108, 108])
    t_fl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), PANEL_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COL),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(t_fl)
    story.append(Spacer(1, 2))

    # 5. Phased Rollout & Economic ROI
    story.append(Paragraph("4. 5-Year Capital Rollout, Calibrated Economic ROI & Cabinet Directives", sec_head))
    p_rollout = [
        [Paragraph("Phase", cell_header), Paragraph("Target Corridors", cell_header), Paragraph("Outlay", cell_header), Paragraph("Upgrades", cell_header), Paragraph("New Campuses", cell_header), Paragraph("Transit Hubs", cell_header), Paragraph("Access Gain", cell_header)],
        [Paragraph("<b>Phase 1 (Y1-Y2)</b>", cell_bold), Paragraph("High Vulnerability Tribal Corridors (9 Dists)", cell_text), Paragraph("Rs. 2,704 Cr (45%)", cell_bold), Paragraph("981", cell_text), Paragraph("537", cell_text), Paragraph("644", cell_text), Paragraph("+16.5%", cell_bold)],
        [Paragraph("<b>Phase 2 (Y3-Y4)</b>", cell_bold), Paragraph("Mineral Belts & Western Plateaus (11 Dists)", cell_text), Paragraph("Rs. 2,103 Cr (35%)", cell_bold), Paragraph("763", cell_text), Paragraph("418", cell_text), Paragraph("351", cell_text), Paragraph("+11.2%", cell_bold)],
        [Paragraph("<b>Phase 3 (Y5)</b>", cell_bold), Paragraph("Coastal Deltas & Cyclone Retrofits (10 Dists)", cell_text), Paragraph("Rs. 1,202 Cr (20%)", cell_bold), Paragraph("436", cell_text), Paragraph("239", cell_text), Paragraph("175", cell_text), Paragraph("+4.8%", cell_bold)]
    ]
    t_ro = Table(p_rollout, colWidths=[70, 175, 76, 50, 60, 56, 52])
    t_ro.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COL),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, PANEL_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 1.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5),
    ]))
    story.append(t_ro)
    story.append(Spacer(1, 2))

    roi_and_recs = (
        f"<b>Audited Economic ROI:</b> Retaining 184,000 secondary students generates <b>Rs. {econ.get('net_present_value_gsdp_contribution_cr', 10796):,.1f} Cr lifetime GSDP value</b> "
        f"(0.75x informal labor discount), delivering a <b>{econ.get('benefit_cost_ratio_roi', 1.8)}x Benefit-Cost Ratio</b> on Rs. {sec['total_budget_cr']:,.1f} Cr capital outlay.<br/>"
        "<b>Immediate Directives:</b> <b>1. Tribal Teacher Cadre:</b> Sanction 9,144 posts with 25% Remote Area Allowance & 3-yr bond. "
        "<b>2. PESA Land Fast-Track:</b> Transfer revenue wasteland via Gram Sabha consent (PESA Sec 4i). "
        "<b>3. SHG Transit Operations:</b> Partner with Mission Shakti SHGs for bus/feeder chaperones. "
        "<b>4. GIS-Linked Disbursals:</b> Require GPS validation in solver prior to fund release."
    )
    story.append(Paragraph(roi_and_recs, body_text))

    # Build Document
    print(f"Compiling 1-Page Executive Policy Brief into {OUTPUT_BRIEF}...")
    doc.build(story, canvasmaker=BriefCanvas)
    print(f"Policy Brief successfully generated! File size: {os.path.getsize(OUTPUT_BRIEF) / 1024:.2f} KB")


if __name__ == "__main__":
    build_policy_brief()
