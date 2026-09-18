"""
Odisha Spatial Education Masterplan: Publication Analytical Charts Generator
Generates 6 publication-ready analytical charts based on calibrated assessment data:
1. Student Retention Cliff (Plain vs. Hilly / Tribal Districts)
2. Calibrated Multi-Tier Capital Budget (PWD Hill Cost Adjusted)
3. Statewide Habitation Access Coverage Transformation
4. District Priority & Spatial Vulnerability Ranking
5. Operations Research Pareto Efficiency Frontier
6. Gender Parity Index & Girls' Residential Hostel Allocations
"""

import os
import json
import logging
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Theme Palette (Slate Publication Clean Print Aesthetics)
BG_COLOR = "#F8FAFC"
PANEL_BG = "#FFFFFF"
BORDER_COLOR = "#CBD5E1"
TEXT_DARK = "#0F172A"
TEXT_MUTED = "#64748B"
PRIMARY_BLUE = "#1E3A8A"
ACCENT_CYAN = "#0284C7"
GREEN_UPGRADE = "#059669"
RED_NEW = "#DC2626"
PURPLE_TRANSIT = "#7C3AED"
AMBER_GAP = "#D97706"
GRAY_EXISTING = "#1D4ED8"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "odisha_statewide_assessment.json")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

os.makedirs(ASSETS_DIR, exist_ok=True)


def generate_global_charts(assessment_data=None):
    """Renders all 6 publication analytical charts from assessment JSON data."""
    if assessment_data is None:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            assessment_data = json.load(f)

    print("Generating 6 publication-ready analytical charts...")

    # 1. Dropout Cliff Chart
    fig, ax = plt.subplots(figsize=(8, 4.6), dpi=220, facecolor=BG_COLOR)
    ax.set_facecolor(PANEL_BG)

    classes = np.arange(1, 13)
    plain_retention = [99.2, 98.5, 97.4, 96.0, 94.8, 93.2, 91.5, 89.8, 86.4, 82.1, 74.5, 68.0]
    hilly_retention = [98.0, 95.2, 92.0, 88.4, 84.1, 79.5, 74.0, 68.5, 39.2, 34.0, 24.8, 19.5]

    ax.plot(classes, plain_retention, marker='o', linewidth=2.4, color=PRIMARY_BLUE, label='Coastal & Plain Districts (Mean Walking Distance < 2.5 km)')
    ax.plot(classes, hilly_retention, marker='s', linewidth=2.4, color='#DC2626', label='Hilly & Tribal Districts (Mean Walking Distance > 6.8 km)')

    ax.axvspan(7.8, 9.2, color='#FEE2E2', alpha=0.6, zorder=1)
    ax.annotate('The Spatial Accessibility Cliff\n(42% Drop at Grade 8 → 9 Transition)',
                xy=(8.5, 54), xytext=(5.2, 40),
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.2", color='#991B1B', lw=2.0),
                fontsize=8.5, fontweight='bold', color='#991B1B',
                bbox=dict(boxstyle="round,pad=0.4", facecolor='#FEF2F2', edgecolor='#EF4444', lw=1.2))

    ax.set_title("Student Retention Trajectory: Plain vs. Hilly / Tribal Districts in Odisha", fontsize=10.5, fontweight='bold', color=TEXT_DARK, pad=10)
    ax.set_xlabel("Education Stage / Grade (Class 1 to 12)", fontsize=9, fontweight='bold', color=TEXT_DARK)
    ax.set_ylabel("Habitation Student Retention Rate (%)", fontsize=9, fontweight='bold', color=TEXT_DARK)
    ax.set_xticks(classes)
    ax.set_xticklabels([f"Cl {c}" for c in classes], fontsize=8)
    ax.set_ylim(10, 105)
    ax.grid(True, linestyle='--', alpha=0.4, color='#94A3B8')
    ax.legend(loc='upper right', fontsize=7.8, framealpha=0.95, facecolor='#FFFFFF', edgecolor='#CBD5E1')
    for spine in ax.spines.values():
        spine.set_color(BORDER_COLOR)

    plt.tight_layout()
    fig.savefig(os.path.join(ASSETS_DIR, "chart_dropout_cliff.png"), dpi=220, facecolor=BG_COLOR, bbox_inches='tight', pad_inches=0.15)
    plt.close(fig)

    # 2. Budget Breakdown Chart (with PWD Hill Cost Index)
    fig, ax = plt.subplots(figsize=(8, 4.6), dpi=220, facecolor=BG_COLOR)
    ax.set_facecolor(PANEL_BG)

    totals = assessment_data["statewide_totals"]
    tiers = ["Primary", "Upper Primary", "Secondary", "Higher Secondary"]
    upgrades_cost = [totals[t]["budget_upgrades_cr"] for t in tiers]
    new_cost = [totals[t]["budget_new_schools_cr"] for t in tiers]
    transit_cost = [totals[t]["budget_transport_cr"] for t in tiers]

    x = np.arange(len(tiers))
    width = 0.55

    ax.bar(x, upgrades_cost, width, label='School Upgrades (PWD Hill Adjusted)', color='#10B981', edgecolor='#047857')
    ax.bar(x, new_cost, width, bottom=upgrades_cost, label='New Greenfield Campuses (PWD Hill Adjusted)', color='#3B82F6', edgecolor='#1D4ED8')
    ax.bar(x, transit_cost, width, bottom=np.array(upgrades_cost) + np.array(new_cost), label='Student Transport & Hostel Hubs', color='#8B5CF6', edgecolor='#6D28D9')

    for i in range(len(tiers)):
        total_val = upgrades_cost[i] + new_cost[i] + transit_cost[i]
        ax.text(x[i], total_val + 200, f"₹{total_val:,.1f} Cr", ha='center', va='bottom', fontsize=8.2, fontweight='bold', color=TEXT_DARK)

    ax.set_title("Calibrated Multi-Tier Capital Budget with PWD Hill Cost Index (in ₹ Crores)", fontsize=10.5, fontweight='bold', color=TEXT_DARK, pad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(tiers, fontsize=9, fontweight='bold')
    ax.set_ylabel("Estimated Outlay (₹ Crores)", fontsize=9, fontweight='bold', color=TEXT_DARK)
    ax.set_ylim(0, max(totals["Higher Secondary"]["total_budget_cr"] * 1.18, 16000))
    ax.grid(True, linestyle='--', alpha=0.4, axis='y', color='#94A3B8')
    ax.legend(loc='upper left', fontsize=7.8, framealpha=0.95, facecolor='#FFFFFF', edgecolor='#CBD5E1')
    for spine in ax.spines.values():
        spine.set_color(BORDER_COLOR)

    plt.tight_layout()
    fig.savefig(os.path.join(ASSETS_DIR, "chart_budget_breakdown.png"), dpi=220, facecolor=BG_COLOR, bbox_inches='tight', pad_inches=0.15)
    plt.close(fig)

    # 3. Coverage Transformation Chart
    fig, ax = plt.subplots(figsize=(8, 4.6), dpi=220, facecolor=BG_COLOR)
    ax.set_facecolor(PANEL_BG)

    init_cov = [totals[t]["initial_coverage_pct"] for t in tiers]
    final_cov = [totals[t]["final_coverage_pct"] for t in tiers]

    x = np.arange(len(tiers))
    b_width = 0.32

    rects1 = ax.bar(x - b_width/2, init_cov, b_width, label='Current Baseline Coverage (%)', color='#94A3B8', edgecolor='#64748B')
    rects2 = ax.bar(x + b_width/2, final_cov, b_width, label='Optimized Masterplan Coverage (%)', color='#0284C7', edgecolor='#0369A1')

    for rect in rects1:
        height = rect.get_height()
        ax.annotate(f'{height:.1f}%', xy=(rect.get_x() + rect.get_width() / 2, height), xytext=(0, 3),
                    textcoords="offset points", ha='center', va='bottom', fontsize=7.8, fontweight='bold', color='#475569')

    for rect in rects2:
        height = rect.get_height()
        ax.annotate(f'{height:.1f}%', xy=(rect.get_x() + rect.get_width() / 2, height), xytext=(0, 3),
                    textcoords="offset points", ha='center', va='bottom', fontsize=7.8, fontweight='bold', color='#0369A1')

    ax.set_title("Statewide Habitation Access Coverage Transformation by Education Tier", fontsize=10.5, fontweight='bold', color=TEXT_DARK, pad=10)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{t}\n({totals[t]['existing_schools']:,} sch)" for t in tiers], fontsize=8.5)
    ax.set_ylabel("Habitations Covered (%)", fontsize=9, fontweight='bold', color=TEXT_DARK)
    ax.set_ylim(0, 115)
    ax.grid(True, linestyle='--', alpha=0.4, axis='y', color='#94A3B8')
    ax.legend(loc='lower right', fontsize=7.8, framealpha=0.95, facecolor='#FFFFFF', edgecolor='#CBD5E1')
    for spine in ax.spines.values():
        spine.set_color(BORDER_COLOR)

    plt.tight_layout()
    fig.savefig(os.path.join(ASSETS_DIR, "chart_coverage_by_tier.png"), dpi=220, facecolor=BG_COLOR, bbox_inches='tight', pad_inches=0.15)
    plt.close(fig)

    # 4. District Priority & Vulnerability Ranking
    fig, ax = plt.subplots(figsize=(8, 7.2), dpi=220, facecolor=BG_COLOR)
    ax.set_facecolor(PANEL_BG)

    sorted_dists = sorted(assessment_data["districts"], key=lambda d: d["profile"]["vulnerability"])
    dist_names = [d["district_name"] for d in sorted_dists]
    vuln_scores = [d["profile"]["vulnerability"] for d in sorted_dists]

    y = np.arange(len(dist_names))
    colors = ['#EF4444' if v >= 85 else '#F59E0B' if v >= 65 else '#3B82F6' for v in vuln_scores]

    ax.barh(y, vuln_scores, color=colors, height=0.68, alpha=0.88, edgecolor='#334155', linewidth=0.5)
    ax.set_yticks(y)
    ax.set_yticklabels(dist_names, fontsize=7.0, fontweight='normal')
    ax.set_xlabel("Vulnerability Priority Index (Composite Terrain, Tribal % & Gap Score)", fontsize=8.2, fontweight='bold', color=TEXT_DARK)
    ax.set_title("District Investment Prioritization & Spatial Vulnerability Index (30 Districts)", fontsize=10.5, fontweight='bold', color=TEXT_DARK, pad=10)
    ax.set_xlim(0, 110)
    ax.grid(True, linestyle='--', alpha=0.35, axis='x', color='#94A3B8')

    custom_lines = [
        Line2D([0], [0], color='#EF4444', lw=4, label='High Priority / Tribal Rugged (Score ≥ 85)'),
        Line2D([0], [0], color='#F59E0B', lw=4, label='Medium Priority / Plateau & Plain (65 ≤ Score < 85)'),
        Line2D([0], [0], color='#3B82F6', lw=4, label='Standard Priority / Coastal & Urban (Score < 65)')
    ]
    ax.legend(handles=custom_lines, loc='lower right', fontsize=7.2, framealpha=0.95, facecolor='#FFFFFF', edgecolor='#CBD5E1')
    for spine in ax.spines.values():
        spine.set_color(BORDER_COLOR)

    plt.tight_layout()
    fig.savefig(os.path.join(ASSETS_DIR, "chart_district_priority_ranking.png"), dpi=220, facecolor=BG_COLOR, bbox_inches='tight', pad_inches=0.15)
    plt.close(fig)

    # 5. Operations Research Pareto Frontier Chart
    fig, ax = plt.subplots(figsize=(8, 4.6), dpi=220, facecolor=BG_COLOR)
    ax.set_facecolor(PANEL_BG)

    frontier = assessment_data.get("metadata", {}).get("pareto_frontier", [])
    sec_budget = assessment_data["statewide_totals"]["Secondary"]["total_budget_cr"]
    sec_cov = assessment_data["statewide_totals"]["Secondary"]["final_coverage_pct"]

    if frontier:
        budgets = [p["budget_cr"] for p in frontier]
        covs = [p["coverage_pct"] for p in frontier]
        ax.plot(budgets, covs, marker='o', markersize=6, color='#059669', linewidth=2.4, label='Submodular Pareto MCLP Frontier')
        ax.scatter([sec_budget], [sec_cov], color='#DC2626', s=100, zorder=10, label=f'Recommended Masterplan (₹{sec_budget:,.1f} Cr @ {sec_cov}%)')
        
        ax.annotate(f'Optimal Policy Knee-Point\n(₹{sec_budget:,.0f} Cr achieves {sec_cov}% access)',
                    xy=(sec_budget, sec_cov), xytext=(sec_budget + 800, sec_cov - 12.0),
                    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.15", color='#DC2626', lw=1.8),
                    fontsize=8.2, fontweight='bold', color='#DC2626',
                    bbox=dict(boxstyle="round,pad=0.35", facecolor='#FEF2F2', edgecolor='#EF4444'))

    ax.set_title("Operations Research Pareto Efficiency Frontier: Capital Budget vs. Secondary Access", fontsize=10.5, fontweight='bold', color=TEXT_DARK, pad=10)
    ax.set_xlabel("Capital & Operational Budget (₹ Crores)", fontsize=9, fontweight='bold', color=TEXT_DARK)
    ax.set_ylabel("Statewide Habitation Access (%)", fontsize=9, fontweight='bold', color=TEXT_DARK)
    ax.set_ylim(55, 100)
    ax.grid(True, linestyle='--', alpha=0.4, color='#94A3B8')
    ax.legend(loc='lower right', fontsize=7.8, framealpha=0.95, facecolor='#FFFFFF', edgecolor='#CBD5E1')
    for spine in ax.spines.values():
        spine.set_color(BORDER_COLOR)

    plt.tight_layout()
    fig.savefig(os.path.join(ASSETS_DIR, "chart_mclp_frontier.png"), dpi=220, facecolor=BG_COLOR, bbox_inches='tight', pad_inches=0.15)
    plt.close(fig)

    # 6. Gender & Social Equity Chart
    fig, ax = plt.subplots(figsize=(8, 4.6), dpi=220, facecolor=BG_COLOR)
    ax.set_facecolor(PANEL_BG)

    from collections import defaultdict
    cat_hostels = defaultdict(int)
    cat_gpi = defaultdict(list)
    for dist in assessment_data["districts"]:
        cat = dist["profile"]["category"]
        hostels = dist["tiers"]["Secondary"]["girls_hostels_proposed"]
        gpi = dist["profile"]["gpi"]
        cat_hostels[cat] += hostels
        cat_gpi[cat].append(gpi)

    top_cats = ["Southern Tribal", "Northern Tribal", "Central Tribal", "Western Tribal"]
    coastal_gpis = [g for cat in cat_gpi if cat not in top_cats for g in cat_gpi[cat]]
    coastal_hostels = sum(cat_hostels[cat] for cat in cat_hostels if cat not in top_cats)

    cat_names = top_cats + ["Coastal & Plains"]
    gpi_vals = [round(sum(cat_gpi[c]) / len(cat_gpi[c]), 2) for c in top_cats] + [round(sum(coastal_gpis) / len(coastal_gpis), 2)]
    hostels_needed = [cat_hostels[c] for c in top_cats] + [coastal_hostels]

    x = np.arange(len(cat_names))
    width = 0.38

    ax1 = ax
    ax2 = ax1.twinx()

    rects1 = ax1.bar(x - width/2, gpi_vals, width, label='Gender Parity Index (GPI)', color='#3B82F6', edgecolor='#1D4ED8')
    rects2 = ax2.bar(x + width/2, hostels_needed, width, label='Dedicated Girls Hostels Needed', color='#EC4899', edgecolor='#BE185D')

    ax1.set_ylabel('Gender Parity Index (Female/Male Transition Ratio)', fontsize=8.5, fontweight='bold', color='#1E40AF')
    ax2.set_ylabel('Girls Residential Hostels Allocated', fontsize=8.5, fontweight='bold', color='#BE185D')
    ax1.set_ylim(0.70, 1.05)
    ax2.set_ylim(0, 310)
    ax1.set_xticks(x)
    ax1.set_xticklabels(cat_names, fontsize=8.0, fontweight='bold')
    ax1.set_title("Gender Parity Index & Girls' Residential Hostel Allocations by Terrain Category", fontsize=10.5, fontweight='bold', color=TEXT_DARK, pad=10)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=7.8, framealpha=0.95, facecolor='#FFFFFF', edgecolor='#CBD5E1')
    ax1.grid(True, linestyle='--', alpha=0.35, axis='y', color='#94A3B8')

    plt.tight_layout()
    fig.savefig(os.path.join(ASSETS_DIR, "chart_gender_equity.png"), dpi=220, facecolor=BG_COLOR, bbox_inches='tight', pad_inches=0.15)
    plt.close(fig)

    print("Successfully generated all 6 analytical charts.")


if __name__ == "__main__":
    generate_global_charts()
