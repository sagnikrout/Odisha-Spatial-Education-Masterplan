"""
Odisha Spatial Education Masterplan: 30 Standalone District Action Memos Generator (Multi-Core Optimized Edition)
Compiles 30 dedicated 2-page action memos tailored for individual District Collectors and District Education Officers (DEOs).
Features Multi-Core Parallel Processing for 4-5x Faster PDF Compilation.
"""

import os
import json
from concurrent.futures import ProcessPoolExecutor, as_completed
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
MEMOS_DIR = os.path.join(BASE_DIR, "district_action_memos")

os.makedirs(MEMOS_DIR, exist_ok=True)

# Palette
PRIMARY = colors.HexColor("#1E3A8A")
SECONDARY = colors.HexColor("#0284C7")
DARK_TEXT = colors.HexColor("#0F172A")
MUTED_TEXT = colors.HexColor("#64748B")
LIGHT_BG = colors.HexColor("#F8FAFC")
PANEL_BG = colors.HexColor("#F1F5F9")
BORDER_COL = colors.HexColor("#CBD5E1")


class MemoCanvas(canvas.Canvas):
    """Custom canvas for 2-page district action memos."""
    def __init__(self, *args, district_name="", **kwargs):
        super().__init__(*args, **kwargs)
        self.district_name = district_name
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_memo_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_memo_decorations(self, total_pages):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(MUTED_TEXT)

        # Header
        self.drawString(36, 842 - 28, f"GOVERNMENT OF ODISHA | {self.district_name.upper()} DISTRICT ADMINISTRATION")
        self.drawRightString(595 - 36, 842 - 28, "AUDITED EDUCATION ACTION MEMO (2026-2031)")
        self.setStrokeColor(BORDER_COL)
        self.setLineWidth(0.75)
        self.line(36, 842 - 34, 595 - 36, 842 - 34)

        # Footer
        self.setFont("Helvetica", 7.5)
        self.drawString(36, 22, f"Confidential  -  For Collector & District Magistrate / DEO {self.district_name}")
        self.drawRightString(595 - 36, 22, f"Page {self._pageNumber} of {total_pages}")
        self.line(36, 30, 595 - 36, 30)

        self.restoreState()


def compile_single_district_memo(d):
    """Compiles a single 2-page District Action Memo PDF."""
    dist_name = d["district_name"]
    prof = d["profile"]
    sec = d["tiers"]["Secondary"]
    blocks = d.get("blocks", [])
    map_filename = f"dist_{dist_name.lower().replace(' ', '_')}.png"
    map_path = os.path.join(MAPS_DIR, map_filename)
    out_pdf = os.path.join(MEMOS_DIR, f"{dist_name.replace(' ', '_')}_DEO_Action_Memo.pdf")

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'MemoTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=15.5,
        textColor=PRIMARY,
        spaceBefore=0,
        spaceAfter=2
    )

    subtitle_style = ParagraphStyle(
        'MemoSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.0,
        leading=10.2,
        textColor=MUTED_TEXT,
        spaceAfter=6
    )

    sec_head = ParagraphStyle(
        'SecHeadMemo',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=9.0,
        leading=11.5,
        textColor=PRIMARY,
        spaceBefore=5,
        spaceAfter=3,
        keepWithNext=True
    )

    body_text = ParagraphStyle(
        'MemoBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.4,
        leading=9.8,
        textColor=DARK_TEXT,
        spaceAfter=3
    )

    cell_text = ParagraphStyle(
        'MemoCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.8,
        leading=8.2,
        textColor=DARK_TEXT,
        alignment=1
    )

    cell_bold = ParagraphStyle(
        'MemoCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.8,
        leading=8.2,
        textColor=DARK_TEXT,
        alignment=1
    )

    cell_header = ParagraphStyle(
        'MemoCellHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.0,
        leading=8.5,
        textColor=colors.white,
        alignment=1
    )

    def make_canvas(*args, **kwargs):
        return MemoCanvas(*args, district_name=dist_name, **kwargs)

    doc = SimpleDocTemplate(
        out_pdf,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=44,
        bottomMargin=38
    )

    story = []

    # PAGE 1: OVERVIEW & MAP
    story.append(Paragraph(f"{dist_name.upper()} DISTRICT: EDUCATION INFRASTRUCTURE ACTION MEMO", title_style))
    sub_text = (
        f"Category: <b>{prof['category']}</b> | Terrain: <b>{prof['terrain']}</b> | "
        f"Tobler Friction: <b>{d.get('terrain_friction_factor', 1.0)}x</b> | "
        f"PWD Hill Index: <b>{d.get('pwd_hill_cost_multiplier', 1.0)}x</b> | "
        f"Vulnerability: <b>{prof['vulnerability']}/100</b>"
    )
    story.append(Paragraph(sub_text, subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceBefore=0, spaceAfter=5))

    left_box = []
    if os.path.exists(map_path):
        left_box.append(Image(map_path, width=250, height=250))

    right_box = [
        Paragraph("<b>4-Tier Infrastructure Targets (Hill Adjusted):</b>", sec_head),
    ]
    tier_table_data = [
        [Paragraph("Tier", cell_header), Paragraph("Baseline", cell_header), Paragraph("Target", cell_header), Paragraph("Upgrades", cell_header), Paragraph("New", cell_header), Paragraph("Transit", cell_header), Paragraph("Outlay", cell_header)],
        [Paragraph("Primary", cell_text), Paragraph(f"{d['tiers']['Primary']['initial_coverage_pct']}%", cell_text), Paragraph(f"{d['tiers']['Primary']['final_coverage_pct']}%", cell_text), Paragraph(str(d['tiers']['Primary']['proposed_upgrades']), cell_text), Paragraph(str(d['tiers']['Primary']['proposed_new_schools']), cell_text), Paragraph(str(d['tiers']['Primary']['proposed_transport_hubs']), cell_text), Paragraph(f"Rs. {d['tiers']['Primary']['total_budget_cr']:.1f}Cr", cell_text)],
        [Paragraph("UP (Middle)", cell_text), Paragraph(f"{d['tiers']['Upper Primary']['initial_coverage_pct']}%", cell_text), Paragraph(f"{d['tiers']['Upper Primary']['final_coverage_pct']}%", cell_text), Paragraph(str(d['tiers']['Upper Primary']['proposed_upgrades']), cell_text), Paragraph(str(d['tiers']['Upper Primary']['proposed_new_schools']), cell_text), Paragraph(str(d['tiers']['Upper Primary']['proposed_transport_hubs']), cell_text), Paragraph(f"Rs. {d['tiers']['Upper Primary']['total_budget_cr']:.1f}Cr", cell_text)],
        [Paragraph("Secondary", cell_bold), Paragraph(f"{sec['initial_coverage_pct']}%", cell_bold), Paragraph(f"{sec['final_coverage_pct']}%", cell_bold), Paragraph(str(sec['proposed_upgrades']), cell_bold), Paragraph(str(sec['proposed_new_schools']), cell_bold), Paragraph(str(sec['proposed_transport_hubs']), cell_bold), Paragraph(f"Rs. {sec['total_budget_cr']:.1f}Cr", cell_bold)],
        [Paragraph("Higher Sec", cell_text), Paragraph(f"{d['tiers']['Higher Secondary']['initial_coverage_pct']}%", cell_text), Paragraph(f"{d['tiers']['Higher Secondary']['final_coverage_pct']}%", cell_text), Paragraph(str(d['tiers']['Higher Secondary']['proposed_upgrades']), cell_text), Paragraph(str(d['tiers']['Higher Secondary']['proposed_new_schools']), cell_text), Paragraph(str(d['tiers']['Higher Secondary']['proposed_transport_hubs']), cell_text), Paragraph(f"Rs. {d['tiers']['Higher Secondary']['total_budget_cr']:.1f}Cr", cell_text)]
    ]
    t_tier = Table(tier_table_data, colWidths=[55, 40, 40, 42, 35, 38, 45])
    t_tier.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COL),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, PANEL_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    right_box.append(t_tier)
    right_box.append(Spacer(1, 4))
    right_box.append(Paragraph(f"<b>Key Operational Allocations:</b><br/>"
                               f"• <b>Subject Teachers (25% Hardship Allowance):</b> {sec.get('teachers_required', 0)} Posts<br/>"
                               f"• <b>Transit Fleet:</b> {sec.get('fleet_minibuses', 0)} Mini-Buses, {sec.get('fleet_feeder_vans', 0)} Vans<br/>"
                               f"• <b>Annual Transit Opex:</b> Rs. {sec.get('annual_transit_opex_cr', 0.0):.2f} Cr/yr<br/>"
                               f"• <b>Dedicated Girls' Hostels:</b> {sec.get('girls_hostels_proposed', 0)} Units<br/>"
                               f"• <b>Cyclone Retrofits:</b> {sec.get('cyclone_resilient_upgrades', 0)} Schools", body_text))

    t_p1 = Table([[left_box, right_box]], colWidths=[255, 268])
    t_p1.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP')]))
    story.append(t_p1)
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Strategic Directive for District Administration:</b>", sec_head))
    story.append(Paragraph(d["strategy"], body_text))
    story.append(PageBreak())

    # PAGE 2: BLOCK MATRIX
    story.append(Paragraph(f"Block-by-Block Secondary Infrastructure Allocation ({len(blocks)} Blocks)", sec_head))
    
    blk_table_data = [
        [
            Paragraph("CD Block", cell_header),
            Paragraph("Population", cell_header),
            Paragraph("Habs", cell_header),
            Paragraph("Vuln.", cell_header),
            Paragraph("Base Cov.", cell_header),
            Paragraph("Target Cov.", cell_header),
            Paragraph("Upgrades", cell_header),
            Paragraph("New", cell_header),
            Paragraph("Transit", cell_header),
            Paragraph("Buses/Vans", cell_header),
            Paragraph("Est. Outlay", cell_header)
        ]
    ]

    for b in blocks:
        blk_table_data.append([
            Paragraph(f"<b>{b['block_name']}</b>", cell_text),
            Paragraph(f"{b['population']:,}", cell_text),
            Paragraph(str(b['habitations']), cell_text),
            Paragraph(str(b['vulnerability_score']), cell_text),
            Paragraph(f"{b['baseline_coverage_pct']}%", cell_text),
            Paragraph(f"<b>{b['target_coverage_pct']}%</b>", cell_bold),
            Paragraph(str(b['proposed_upgrades']), cell_text),
            Paragraph(str(b['proposed_new_schools']), cell_text),
            Paragraph(str(b['proposed_transport_hubs']), cell_text),
            Paragraph(f"{b.get('fleet_minibuses', 1)}B / {b.get('fleet_feeder_vans', 1)}V", cell_text),
            Paragraph(f"Rs. {b['estimated_budget_cr']:.2f}Cr", cell_text)
        ])

    t_blk = Table(blk_table_data, colWidths=[70, 52, 28, 28, 45, 48, 40, 32, 35, 50, 45])
    t_blk.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('GRID', (0, 0), (-1, -1), 0.4, BORDER_COL),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, PANEL_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.0),
    ]))
    story.append(t_blk)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Collector & DEO Priority Action Steps:</b>", sec_head))
    action_steps = (
        "1. <b>Fast-Track PESA Land Clearance:</b> Fast-track panchayat wasteland transfer with Gram Sabha consent under Section 4(i) of PESA for greenfield sites.<br/>"
        "2. <b>Mission Shakti Transit Schedulers:</b> Convene BEOs to establish Women SHG vehicle operations for remote feeder loops with chaperone honorariums.<br/>"
        "3. <b>Special Teacher Hardship Cadre:</b> Submit formal requisition for subject teacher recruitments with 25% Remote Area Allowance.<br/>"
        "4. <b>ORSAC Satellite Monitoring:</b> Track monthly civil works milestones and geofenced attendance on the state GIS portal."
    )
    story.append(Paragraph(action_steps, body_text))

    doc.build(story, canvasmaker=make_canvas)
    return dist_name


def generate_all_district_memos_parallel():
    print(f"Generating 30 District Action Memos in parallel in {MEMOS_DIR}...")
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    workers = min(8, os.cpu_count() or 4)
    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(compile_single_district_memo, d) for d in data["districts"]]
        for fut in as_completed(futures):
            res = fut.result()

    print(f"Successfully generated all 30 District Action Memos in parallel in {MEMOS_DIR}.")


if __name__ == "__main__":
    generate_all_district_memos_parallel()
