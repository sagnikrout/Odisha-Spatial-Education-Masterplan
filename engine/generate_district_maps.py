"""High-precision 30-district cartographic plate generator for Odisha Map2Needs.

Renders LGD-aligned CD block parcels, Survey of India coastal/landmass separation,
interstate context, PMGSY habitation-weighted 1:1 facility placement with true-metric
5 km catchment buffers, and deterministic non-overlapping block label layouts.
"""

from concurrent.futures import ProcessPoolExecutor, as_completed
import gzip
import hashlib
import json
import math
import os
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.lines import Line2D
from matplotlib.patches import Ellipse, FancyBboxPatch, PathPatch, Polygon
from matplotlib.path import Path
import numpy as np


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEOJSON_PATH = os.path.join(BASE_DIR, "odisha_districts.geojson")
GEOPACK_PATH = os.path.join(BASE_DIR, "engine", "odisha_geodata.json.gz")
ASSESS_PATH = os.path.join(BASE_DIR, "odisha_statewide_assessment.json")
OUT_DIR = os.path.join(BASE_DIR, "assets", "district_maps")

# Shared 4-zone horizontal margins so every banner and map frame aligns flush.
ZONE_X = 0.045
ZONE_W = 0.910
FIG_W_IN = 10.0
FIG_H_IN = 11.2
MAP_BOX = [ZONE_X, 0.245, ZONE_W, 0.625]  # [left, bottom, width, height]

# Approximate WGS84 meridional arc length (km per degree latitude).
KM_PER_DEG_LAT = 110.574
BLOCK_SHADES = ("#FFFFFF", "#F8FAFC", "#F3F6FA")
SCALE_STEPS_KM = (5, 10, 15, 20, 25, 30, 40, 50, 60)

DISTRICT_NAME_ALIASES = {
    "Anugul": "Angul",
    "Baleshwar": "Balasore",
    "Boudh": "Boudh",
    "Bauda": "Boudh",
    "Debagarh": "Deogarh",
    "Jagatsinghapur": "Jagatsinghpur",
    "Jajapur": "Jajpur",
    "Kendujhar": "Kendujhar",
    "Keonjhar": "Kendujhar",
    "Khordha": "Khordha",
    "Khurda": "Khordha",
    "Nabarangapur": "Nabarangpur",
    "Nabarangpur": "Nabarangpur",
    "Sonapur": "Subarnapur",
    "Sonepur": "Subarnapur",
    "Subarnapur": "Subarnapur",
}


def point_in_poly(x, y, poly):
    """Pure-Python ray-casting point-in-polygon test kept fast for tight loops."""
    n = len(poly)
    inside = False
    p1x, p1y = poly[0][0], poly[0][1]
    for i in range(1, n + 1):
        p2x, p2y = poly[i % n][0], poly[i % n][1]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x if p1y != p2y else p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside


def _canon_district(raw_name):
    """Map raw GeoJSON/SOI district spellings to canonical assessment keys."""
    return DISTRICT_NAME_ALIASES.get(raw_name, raw_name)


def _signed_area(ring):
    """Compute signed shoelace area so exterior/hole windings stay consistent."""
    s = 0.0
    n = len(ring)
    for i in range(n):
        x1, y1 = ring[i][0], ring[i][1]
        x2, y2 = ring[(i + 1) % n][0], ring[(i + 1) % n][1]
        s += x1 * y2 - x2 * y1
    return 0.5 * s


def _ensure_winding(ring, ccw=True):
    """Orient closed ring vertices for crisp Matplotlib compound hole rendering."""
    pts = list(ring)
    if len(pts) < 3:
        return pts
    if pts[0] != pts[-1]:
        pts.append(pts[0])
    area = _signed_area(pts)
    if (ccw and area < 0) or (not ccw and area > 0):
        pts.reverse()
    return pts


def _rings_to_path(poly_records):
    """Build one Matplotlib compound Path supporting exterior shells and interior holes."""
    verts = []
    codes = []
    for rec in poly_records:
        ext = _ensure_winding(rec["ext"], ccw=True)
        if len(ext) < 4:
            continue
        verts.extend(ext)
        codes.extend([Path.MOVETO] + [Path.LINETO] * (len(ext) - 2) + [Path.CLOSEPOLY])
        for hole in rec.get("holes", []):
            h = _ensure_winding(hole, ccw=False)
            if len(h) < 4:
                continue
            verts.extend(h)
            codes.extend([Path.MOVETO] + [Path.LINETO] * (len(h) - 2) + [Path.CLOSEPOLY])
    if not verts:
        return None
    return Path(verts, codes)


def _extract_geojson_polys(geometry):
    """Convert GeoJSON Polygon/MultiPolygon geometry into normalized {'ext', 'holes'} dicts."""
    gtype = geometry.get("type")
    coords = geometry.get("coordinates", [])
    raw_polys = [coords] if gtype == "Polygon" else (coords if gtype == "MultiPolygon" else [])
    out = []
    for p in raw_polys:
        if not p or len(p[0]) < 4:
            continue
        out.append({"ext": p[0], "holes": [h for h in p[1:] if len(h) >= 4]})
    return out


def _poly_bbox(poly_records):
    """Compute bounding box (minx, miny, maxx, maxy) across polygon exterior rings."""
    xs = [pt[0] for rec in poly_records for pt in rec["ext"]]
    ys = [pt[1] for rec in poly_records for pt in rec["ext"]]
    return min(xs), min(ys), max(xs), max(ys)


def _stable_rng(key_str):
    """Create a deterministic numpy Generator seeded strictly from a district/block key."""
    digest = hashlib.sha256(key_str.encode("utf-8")).digest()
    return np.random.default_rng(int.from_bytes(digest[:8], "little"))


def _compute_viewport(minx, miny, maxx, maxy):
    """Compute exact (xlim, ylim, true_aspect) matching MAP_BOX aspect without shrinking axes."""
    cx = 0.5 * (minx + maxx)
    cy = 0.5 * (miny + maxy)
    dx = max(maxx - minx, 0.08)
    dy = max(maxy - miny, 0.08)

    km_per_deg_lon = KM_PER_DEG_LAT * math.cos(math.radians(cy))
    true_aspect = KM_PER_DEG_LAT / km_per_deg_lon

    box_w_in = MAP_BOX[2] * FIG_W_IN
    box_h_in = MAP_BOX[3] * FIG_H_IN
    box_ratio = box_w_in / box_h_in

    span_x = dx * 1.24
    span_y = dy * 1.24
    if span_x / (span_y * true_aspect) < box_ratio:
        span_x = box_ratio * span_y * true_aspect
    else:
        span_y = span_x / (box_ratio * true_aspect)

    return (
        (cx - 0.5 * span_x, cx + 0.5 * span_x),
        (cy - 0.5 * span_y, cy + 0.5 * span_y),
        true_aspect,
        km_per_deg_lon,
    )


def _select_inset_corner(blocks, xlim, ylim):
    """Pick the corner inside MAP_BOX overlapping the fewest district vertices and block centers."""
    xmin, xmax = xlim
    ymin, ymax = ylim
    dx = xmax - xmin
    dy = ymax - ymin

    # Normalized axes rectangles for candidate inset boxes (width=0.23, height=0.23).
    iw, ih = 0.235, 0.235
    candidates = {
        "top-left": (0.015, 1.0 - 0.015 - ih),
        "top-right": (1.0 - 0.015 - iw, 1.0 - 0.015 - ih),
        "bottom-right": (1.0 - 0.015 - iw, 0.015),
    }

    sample_pts = []
    for blk in blocks:
        sample_pts.append((blk["label_pt"][0], blk["label_pt"][1], 8.0))
        for rec in blk["polys"]:
            step = max(1, len(rec["ext"]) // 16)
            for pt in rec["ext"][::step]:
                sample_pts.append((pt[0], pt[1], 1.0))

    best_name = "top-left"
    best_score = float("inf")
    for name, (ax0, ay0) in candidates.items():
        rx0 = xmin + (ax0 - 0.02) * dx
        rx1 = xmin + (ax0 + iw + 0.02) * dx
        ry0 = ymin + (ay0 - 0.02) * dy
        ry1 = ymin + (ay0 + ih + 0.02) * dy
        score = sum(w for px, py, w in sample_pts if rx0 <= px <= rx1 and ry0 <= py <= ry1)
        if score < best_score:
            best_score = score
            best_name = name

    ax0, ay0 = candidates[best_name]
    return best_name, (ax0, ay0, iw, ih)


def _sample_block_facilities(habs, osm_pts, block_polys, n_exist, n_upg, n_new, n_trans, seed_key):
    """Assign exact 1:1 facility counts inside a block weighted by real PMGSY habitations."""
    rng = _stable_rng(seed_key)
    rings = [rec["ext"] for rec in block_polys if len(rec["ext"]) >= 4]
    xs_h = np.array([h[0] for h in habs], dtype=float)
    ys_h = np.array([h[1] for h in habs], dtype=float)
    weights = np.array([max(float(h[2]), 50.0) for h in habs], dtype=float)
    probs = weights / weights.sum()

    def _pick_spaced(n_need, avoid_pts, min_sep_deg):
        if n_need <= 0:
            return []
        chosen = []
        avail = list(range(len(habs)))
        # Draw high-population candidates first with progressive relaxation on min_sep.
        for sep in (min_sep_deg, min_sep_deg * 0.55, min_sep_deg * 0.25, 0.0):
            if len(chosen) >= n_need:
                break
            order = rng.choice(len(habs), size=min(len(habs), max(n_need * 5, len(habs))), replace=True, p=probs)
            for idx in order:
                if len(chosen) >= n_need:
                    break
                px, py = float(xs_h[idx]), float(ys_h[idx])
                if chosen or avoid_pts:
                    too_close = False
                    for ax, ay in chosen:
                        if (px - ax) ** 2 + (py - ay) ** 2 < sep * sep:
                            too_close = True
                            break
                    if too_close:
                        continue
                # Slight sub-village jitter verified inside block ring when reusing a busy hub.
                if (px, py) in avoid_pts or any(abs(px - cx) < 1e-4 and abs(py - cy) < 1e-4 for cx, cy in chosen):
                    for _ in range(8):
                        jx = px + float(rng.normal(0.0, 0.0055))
                        jy = py + float(rng.normal(0.0, 0.0055))
                        if any(point_in_poly(jx, jy, r) for r in rings):
                            px, py = jx, jy
                            break
                chosen.append((px, py))
                avoid_pts.add((round(px, 4), round(py, 4)))
        # Guarantee exact requested count even on ultra-small dense blocks.
        while len(chosen) < n_need and avail:
            idx = int(rng.choice(len(habs), p=probs))
            px = float(xs_h[idx]) + float(rng.normal(0.0, 0.004))
            py = float(ys_h[idx]) + float(rng.normal(0.0, 0.004))
            if rings and not any(point_in_poly(px, py, r) for r in rings):
                px, py = float(xs_h[idx]), float(ys_h[idx])
            chosen.append((px, py))
        return chosen

    occupied = set()
    exist_pts = []
    for ox, oy in osm_pts:
        if len(exist_pts) >= n_exist:
            break
        exist_pts.append((float(ox), float(oy)))
        occupied.add((round(float(ox), 4), round(float(oy), 4)))
    if len(exist_pts) < n_exist:
        exist_pts.extend(_pick_spaced(n_exist - len(exist_pts), occupied, 0.012))

    upg_pts = _pick_spaced(n_upg, occupied, 0.018)
    new_pts = _pick_spaced(n_new, occupied, 0.022)
    trans_pts = _pick_spaced(n_trans, occupied, 0.016)
    return exist_pts, upg_pts, new_pts, trans_pts


def _format_block_label(name):
    """Wrap multi-word block names onto two compact lines to reduce badge aspect width."""
    if " " in name and len(name) >= 12:
        parts = name.split(" ", 1)
        return f"{parts[0]}\n{parts[1]}"
    if "-" in name and len(name) >= 12:
        parts = name.split("-", 1)
        return f"{parts[0]}-\n{parts[1]}"
    return name


def _estimate_badge_size_deg(label_text, fontsize, xlim, ylim, true_aspect):
    """Estimate exact pill bounding box width and height in data degrees."""
    lines = label_text.split("\n")
    max_chars = max(len(line) for line in lines)
    n_lines = len(lines)

    w_pt = max_chars * fontsize * 0.56 + 9.0
    h_pt = n_lines * fontsize * 1.24 + 6.5

    box_w_pt = MAP_BOX[2] * FIG_W_IN * 72.0
    box_h_pt = MAP_BOX[3] * FIG_H_IN * 72.0

    deg_per_pt_x = (xlim[1] - xlim[0]) / box_w_pt
    deg_per_pt_y = (ylim[1] - ylim[0]) / box_h_pt
    return w_pt * deg_per_pt_x, h_pt * deg_per_pt_y


def solve_label_layout(blocks, xlim, ylim, true_aspect, obstacles_data, fontsize):
    """Deterministically resolve block badge collisions against peers and map obstacles."""
    xmin, xmax = xlim
    ymin, ymax = ylim
    dx = xmax - xmin
    dy = ymax - ymin

    items = []
    for blk in blocks:
        text = _format_block_label(blk["block_name"])
        bw, bh = _estimate_badge_size_deg(text, fontsize, xlim, ylim, true_aspect)
        ax_pt, ay_pt = float(blk["label_pt"][0]), float(blk["label_pt"][1])
        items.append({
            "name": blk["block_name"],
            "text": text,
            "ax": ax_pt,
            "ay": ay_pt,
            "x": ax_pt,
            "y": ay_pt,
            "w": bw * 1.10,
            "h": bh * 1.15,
        })

    pad_x = 0.015 * dx
    pad_y = 0.015 * dy

    # Deterministic relaxation: separate badge overlaps & push out of inset/scale obstacles.
    for step in range(280):
        spring = 0.035 * (1.0 - step / 360.0)
        forces = [[(it["ax"] - it["x"]) * spring, (it["ay"] - it["y"]) * spring] for it in items]

        # 1. Badge-to-badge rectangle overlap resolution.
        for i in range(len(items)):
            a = items[i]
            for j in range(i + 1, len(items)):
                b = items[j]
                req_x = 0.5 * (a["w"] + b["w"])
                req_y = 0.5 * (a["h"] + b["h"])
                ox = a["x"] - b["x"]
                oy = a["y"] - b["y"]
                pen_x = req_x - abs(ox)
                pen_y = req_y - abs(oy)
                if pen_x > 0.0 and pen_y > 0.0:
                    # Push along normalized axis proportional to penetration depth.
                    nx_p = pen_x / req_x
                    ny_p = pen_y / req_y
                    if nx_p < ny_p:
                        sgn = 1.0 if ox >= 0.0 else -1.0
                        if abs(ox) < 1e-6:
                            sgn = 1.0 if i % 2 == 0 else -1.0
                        push = 0.55 * pen_x * sgn
                        forces[i][0] += push
                        forces[j][0] -= push
                    else:
                        sgn = 1.0 if oy >= 0.0 else -1.0
                        if abs(oy) < 1e-6:
                            sgn = 1.0 if i % 2 == 0 else -1.0
                        push = 0.55 * pen_y * sgn
                        forces[i][1] += push
                        forces[j][1] -= push

        # 2. Keep clear of Odisha locator inset, scale bar, and north arrow obstacles.
        for i, a in enumerate(items):
            for ox0, oy0, ox1, oy1 in obstacles_data:
                ocx = 0.5 * (ox0 + ox1)
                ocy = 0.5 * (oy0 + oy1)
                ow = ox1 - ox0
                oh = oy1 - oy0
                req_x = 0.5 * (a["w"] + ow)
                req_y = 0.5 * (a["h"] + oh)
                ddx = a["x"] - ocx
                ddy = a["y"] - ocy
                pen_x = req_x - abs(ddx)
                pen_y = req_y - abs(ddy)
                if pen_x > 0.0 and pen_y > 0.0:
                    if pen_x / req_x < pen_y / req_y:
                        forces[i][0] += (1.0 if ddx >= 0.0 else -1.0) * pen_x * 0.85
                    else:
                        forces[i][1] += (1.0 if ddy >= 0.0 else -1.0) * pen_y * 0.85

        for i, a in enumerate(items):
            a["x"] += forces[i][0]
            a["y"] += forces[i][1]
            # Clamp cleanly within Zone 2 inner safe bounds.
            a["x"] = min(max(a["x"], xmin + 0.5 * a["w"] + pad_x), xmax - 0.5 * a["w"] - pad_x)
            a["y"] = min(max(a["y"], ymin + 0.5 * a["h"] + pad_y), ymax - 0.5 * a["h"] - pad_y)

    return items


def _rects_overlap(r1, r2):
    """Return True if two axis-aligned rectangles (x0, y0, x1, y1) intersect."""
    return r1[0] < r2[2] and r1[2] > r2[0] and r1[1] < r2[3] and r1[3] > r2[1]


def _find_clear_context_pt(candidate_polys, c_bbox, label_text, fontsize, xlim, ylim,
                           forbidden_rects, target_rings, require_all_in_poly=True):
    """Locate a collision-free context label point outside target district and UI cards."""
    xmin, xmax = xlim
    ymin, ymax = ylim
    dx = xmax - xmin
    dy = ymax - ymin

    lines = label_text.split("\n")
    max_chars = max(len(line) for line in lines)
    box_w_pt = MAP_BOX[2] * FIG_W_IN * 72.0
    box_h_pt = MAP_BOX[3] * FIG_H_IN * 72.0
    lw_deg = (max_chars * fontsize * 0.72 + 14.0) * (dx / box_w_pt)
    lh_deg = (len(lines) * fontsize * 1.45 + 10.0) * (dy / box_h_pt)

    ix0 = max(c_bbox[0], xmin + 0.55 * lw_deg + 0.015 * dx)
    ix1 = min(c_bbox[2], xmax - 0.55 * lw_deg - 0.015 * dx)
    iy0 = max(c_bbox[1], ymin + 0.55 * lh_deg + 0.015 * dy)
    iy1 = min(c_bbox[3], ymax - 0.55 * lh_deg - 0.015 * dy)
    if ix1 <= ix0 or iy1 <= iy0:
        return None

    # Bias search toward natural visible centroid of intersecting polygon slice.
    vcx = min(max(0.5 * (c_bbox[0] + c_bbox[2]), ix0), ix1)
    vcy = min(max(0.5 * (c_bbox[1] + c_bbox[3]), iy0), iy1)
    cands = [(vcx, vcy)]
    for gx in range(11):
        px = ix0 + (ix1 - ix0) * (gx + 0.5) / 11.0
        for gy in range(9):
            py = iy0 + (iy1 - iy0) * (gy + 0.5) / 9.0
            cands.append((px, py))
    cands.sort(key=lambda p: ((p[0] - vcx) / dx) ** 2 + ((p[1] - vcy) / dy) ** 2)

    cand_rings = [r["ext"] for r in candidate_polys]
    for px, py in cands:
        rect = (px - 0.55 * lw_deg, py - 0.55 * lh_deg, px + 0.55 * lw_deg, py + 0.55 * lh_deg)
        if any(_rects_overlap(rect, f) for f in forbidden_rects):
            continue
        # Sample padded 3x3 text footprint so edges/midpoints stay strictly clear of target border.
        p_x0, p_y0 = rect[0] - 0.015 * dx, rect[1] - 0.015 * dy
        p_x1, p_y1 = rect[2] + 0.015 * dx, rect[3] + 0.015 * dy
        border_samples = [
            (sx, sy)
            for sx in (p_x0, px, p_x1)
            for sy in (p_y0, py, p_y1)
        ]
        if any(point_in_poly(sx, sy, tr) for sx, sy in border_samples for tr in target_rings):
            continue
        samples = [
            (sx, sy)
            for sx in (rect[0], px, rect[2])
            for sy in (rect[1], py, rect[3])
        ]
        if not any(point_in_poly(px, py, cr) for cr in cand_rings):
            continue
        if require_all_in_poly:
            in_cnt = sum(1 for sx, sy in samples if any(point_in_poly(sx, sy, cr) for cr in cand_rings))
            if in_cnt < 7:
                continue
        return px, py, rect
    return None


def load_data():
    """Load district boundaries, compact LGD/PMGSY geodata pack, and statewide assessment JSON."""
    with open(GEOJSON_PATH, "r", encoding="utf-8") as f:
        geo_data = json.load(f)
    with gzip.open(GEOPACK_PATH, "rt", encoding="utf-8") as f:
        geopack = json.load(f)
    with open(ASSESS_PATH, "r", encoding="utf-8") as f:
        assess_data = json.load(f)
    return {"geojson": geo_data, "geopack": geopack}, assess_data


def _prepare_task_payloads(geo_bundle, assess_data):
    """Slice geodata cleanly per district so worker processes only pickle relevant geometries."""
    geo_json = geo_bundle["geojson"]
    geopack = geo_bundle["geopack"]

    # Prefer exact LGD-consistent district polygons precomputed from all 314 CD blocks.
    dist_polys = dict(geopack.get("dist_polys", {}))
    if len(dist_polys) != 30:
        for feat in geo_json["features"]:
            dn = _canon_district(feat["properties"].get("dtname") or feat["properties"].get("Dist"))
            dist_polys.setdefault(dn, _extract_geojson_polys(feat["geometry"]))
    dist_bboxes = {dn: _poly_bbox(polys) for dn, polys in dist_polys.items()}

    # Compact state outline tuple list for inset locator map.
    all_dist_paths = {dn: dist_polys[dn] for dn in dist_polys}

    tasks = []
    for d_assess in assess_data["districts"]:
        d_name = d_assess["district_name"]
        target_polys = dist_polys[d_name]
        minx, miny, maxx, maxy = _poly_bbox(target_polys)
        xlim, ylim, true_aspect, km_per_lon = _compute_viewport(minx, miny, maxx, maxy)

        # Collect intersecting adjacent Odisha districts and their bbox centers for labels.
        neighbors = []
        for other_dn, obbox in dist_bboxes.items():
            if other_dn == d_name:
                continue
            ominx, ominy, omaxx, omaxy = obbox
            if omaxx >= xlim[0] and ominx <= xlim[1] and omaxy >= ylim[0] and ominy <= ylim[1]:
                neighbors.append((other_dn, dist_polys[other_dn], obbox))

        d_blocks = geopack["blocks_by_district"][d_name]
        d_habs = {}
        d_osm = {}
        for blk in d_blocks:
            k = f"{d_name}|{blk['block_name']}"
            d_habs[blk["block_name"]] = geopack["habitations"].get(k, [[blk["label_pt"][0], blk["label_pt"][1], 250]])
            d_osm[blk["block_name"]] = geopack["osm_schools"].get(k, [])

        tasks.append({
            "d_assess": d_assess,
            "target_polys": target_polys,
            "target_bbox": (minx, miny, maxx, maxy),
            "xlim": xlim,
            "ylim": ylim,
            "true_aspect": true_aspect,
            "km_per_lon": km_per_lon,
            "neighbors": neighbors,
            "east_india_land": geopack["east_india_land"],
            "neighbor_states": geopack["neighbor_states"],
            "all_dist_paths": all_dist_paths,
            "blocks": d_blocks,
            "habs": d_habs,
            "osm": d_osm,
        })
    return tasks


def render_single_district_map(task):
    """Render one publication-grade district cartographic plate to PNG."""
    d_assess = task["d_assess"]
    d_name = d_assess["district_name"]
    prof = d_assess["profile"]
    t_sec = d_assess["tiers"]["Secondary"]
    hill_mult = d_assess["pwd_hill_cost_multiplier"]

    xlim = task["xlim"]
    ylim = task["ylim"]
    true_aspect = task["true_aspect"]
    km_per_lon = task["km_per_lon"]
    xmin, xmax = xlim
    ymin, ymax = ylim
    dx = xmax - xmin
    dy = ymax - ymin

    clean_name = d_name.lower().replace(" ", "_")
    out_path = os.path.join(OUT_DIR, f"dist_{clean_name}.png")

    fig = plt.figure(figsize=(FIG_W_IN, FIG_H_IN), facecolor="#FFFFFF")

    # =========================================================================
    # ZONE 1: STRUCTURED HEADER BANNER (0.885 - 0.970)
    # =========================================================================
    hdr_ax = fig.add_axes([ZONE_X, 0.885, ZONE_W, 0.085])
    hdr_ax.set_xlim(0, 1)
    hdr_ax.set_ylim(0, 1)
    hdr_ax.axis("off")

    hdr_card = FancyBboxPatch(
        (0.0, 0.0), 1.0, 1.0, boxstyle="round,pad=0.0,rounding_size=0.04",
        facecolor="#F8FAFC", edgecolor="#CBD5E1", linewidth=1.2, clip_on=False,
    )
    hdr_ax.add_patch(hdr_card)
    hdr_accent = FancyBboxPatch(
        (0.0, 0.0), 0.011, 1.0, boxstyle="round,pad=0.0,rounding_size=0.01",
        facecolor="#1E3A8A", edgecolor="none", clip_on=False,
    )
    hdr_ax.add_patch(hdr_accent)

    hdr_ax.text(
        0.505, 0.72,
        f"ODISHA MICRO-PLANNING: {d_name.upper()} DISTRICT",
        ha="center", va="center", fontsize=15.0, fontweight="bold", color="#0F172A",
    )
    hdr_ax.text(
        0.505, 0.41,
        f"{prof['category']} Zone  |  {prof['terrain']} Terrain  |  Vulnerability: {prof['vulnerability']}/100  |  PWD Cost: {hill_mult:.3f}x",
        ha="center", va="center", fontsize=9.2, fontweight="bold", color="#334155",
    )
    hdr_ax.text(
        0.505, 0.16,
        f"Census Pop: {prof['population']:,}  |  ST Share: {prof['tribal_pct']:.1f}%  |  Gender Parity (GPI): {prof['gpi']:.2f}  |  Cyclone Risk: {prof['cyclone_risk']}  |  LGD Blocks: {len(task['blocks'])}",
        ha="center", va="center", fontsize=8.3, color="#475569",
    )

    # =========================================================================
    # ZONE 2: MAIN CARTOGRAPHIC FRAME (0.245 - 0.870)
    # =========================================================================
    ax = fig.add_axes(MAP_BOX)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect(true_aspect, adjustable="box")
    ax.set_facecolor("#D6EAF8")  # Ocean / Bay of Bengal tint
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_edgecolor("#1E293B")
        spine.set_linewidth(1.5)

    # Compute corner inset, north arrow, and scale card rectangles upfront so labels avoid all UI panels.
    inset_corner, inset_rel = _select_inset_corner(task["blocks"], xlim, ylim)
    ix0_ax, iy0_ax, iw_ax, ih_ax = inset_rel
    inset_data_rect = (
        xmin + (ix0_ax - 0.015) * dx,
        ymin + (iy0_ax - 0.015) * dy,
        xmin + (ix0_ax + iw_ax + 0.015) * dx,
        ymin + (iy0_ax + ih_ax + 0.015) * dy,
    )

    view_km = dx * km_per_lon
    target_km = 0.19 * view_km
    scale_km = min(SCALE_STEPS_KM, key=lambda k: abs(k - target_km))
    scale_deg = scale_km / km_per_lon
    bar_x0 = xmin + 0.032 * dx
    bar_x1 = bar_x0 + scale_deg
    bar_y = ymin + 0.042 * dy
    scale_card_rect = (
        bar_x0 - 0.015 * dx, bar_y - 0.025 * dy,
        bar_x1 + 0.032 * dx, bar_y + 0.055 * dy,
    )

    nx_frac = 0.945 if inset_corner == "top-left" else 0.055
    nx = xmin + nx_frac * dx
    ny = ymin + 0.915 * dy
    north_card = (nx - 0.034 * dx, ny - 0.048 * dy, nx + 0.034 * dx, ny + 0.055 * dy)

    # 2A. Landmass base (viewport-culled for speed; Bay of Bengal stays coastal blue #D6EAF8)
    vis_land_polys = []
    for rec in task["east_india_land"]:
        xs_l = [p[0] for p in rec["ext"]]
        ys_l = [p[1] for p in rec["ext"]]
        if max(xs_l) >= xmin and min(xs_l) <= xmax and max(ys_l) >= ymin and min(ys_l) <= ymax:
            vis_land_polys.append(rec)
    land_path = _rings_to_path(vis_land_polys)
    if land_path is not None:
        ax.add_patch(PathPatch(land_path, facecolor="#FAF7F0", edgecolor="#7CA5C4", linewidth=0.8, zorder=1))

    # 2B. Neighboring Indian states (muted sand wash + interstate border line)
    vis_states = []
    for sname, spolys in task["neighbor_states"].items():
        sminx, sminy, smaxx, smaxy = _poly_bbox(spolys)
        if smaxx < xmin or sminx > xmax or smaxy < ymin or sminy > ymax:
            continue
        sp = _rings_to_path(spolys)
        if sp is not None:
            ax.add_patch(PathPatch(
                sp, facecolor="#EFECE4", edgecolor="#788496", linewidth=1.0, linestyle=(0, (5, 3)), zorder=2
            ))
            vis_states.append((sname, spolys, (sminx, sminy, smaxx, smaxy)))

    # 2C. Adjacent Odisha districts (muted stone fill + subtle boundary)
    for ndn, npolys, nbbox in task["neighbors"]:
        np_path = _rings_to_path(npolys)
        if np_path is not None:
            ax.add_patch(PathPatch(np_path, facecolor="#E8ECEF", edgecolor="#94A3B8", linewidth=0.75, zorder=3))

    # Place neighbor district & state labels strictly outside target district and UI cards.
    target_rings = [r["ext"] for r in task["target_polys"]]
    ctx_forbidden = [inset_data_rect, scale_card_rect, north_card]

    for ndn, npolys, nbbox in task["neighbors"]:
        res = _find_clear_context_pt(
            npolys, nbbox, ndn.upper(), 7.2, xlim, ylim, ctx_forbidden, target_rings, require_all_in_poly=True
        )
        if res is not None:
            lx_n, ly_n, lrect = res
            ctx_forbidden.append(lrect)
            ax.text(
                lx_n, ly_n, ndn.upper(), ha="center", va="center",
                fontsize=7.2, fontweight="bold", color="#64748B", alpha=0.85, zorder=4.9,
            )

    for sname, spolys, sbbox in vis_states:
        res = _find_clear_context_pt(
            spolys, sbbox, sname.upper(), 7.2, xlim, ylim, ctx_forbidden, target_rings, require_all_in_poly=False
        )
        if res is not None:
            lx_s, ly_s, lrect = res
            ctx_forbidden.append(lrect)
            ax.text(
                lx_s, ly_s, sname.upper(), ha="center", va="center",
                fontsize=7.2, style="italic", fontweight="bold", color="#64748B", alpha=0.85, zorder=4.9,
            )

    # Label Bay of Bengal if any visible open-ocean box stays completely clear of landmass, islands, and cards.
    land_rings = [r["ext"] for r in vis_land_polys] + target_rings
    for ox_f, oy_f in ((0.82, 0.14), (0.72, 0.10), (0.88, 0.44), (0.85, 0.28), (0.85, 0.85), (0.15, 0.15), (0.50, 0.10)):
        ox_p = xmin + ox_f * dx
        oy_p = ymin + oy_f * dy
        w_rect = (ox_p - 0.095 * dx, oy_p - 0.03 * dy, ox_p + 0.095 * dx, oy_p + 0.03 * dy)
        ocean_samples = [(sx, sy) for sx in (w_rect[0], ox_p, w_rect[2]) for sy in (w_rect[1], oy_p, w_rect[3])]
        if not any(point_in_poly(sx, sy, r) for sx, sy in ocean_samples for r in land_rings):
            if not any(_rects_overlap(w_rect, f) for f in ctx_forbidden):
                ax.text(
                    ox_p, oy_p, "BAY OF BENGAL", ha="center", va="center",
                    fontsize=8.2, style="italic", fontweight="bold", color="#2B6CB0", alpha=0.85, zorder=3,
                )
                break

    # 2D. Target District polygon path (used for interior crisp fill + buffer clipping)
    target_path = _rings_to_path(task["target_polys"])
    target_clip_patch = PathPatch(target_path, facecolor="none", edgecolor="none", transform=ax.transData)
    ax.add_patch(target_clip_patch)

    ax.add_patch(PathPatch(target_path, facecolor="#FFFFFF", edgecolor="none", zorder=4))

    # Subtle alternating micro-fills per LGD block so adjoining CD blocks separate cleanly.
    for idx_b, blk in enumerate(task["blocks"]):
        bp = _rings_to_path(blk["polys"])
        if bp is not None:
            ax.add_patch(PathPatch(
                bp, facecolor=BLOCK_SHADES[idx_b % len(BLOCK_SHADES)], edgecolor="none", zorder=4.2
            ))

    # 2E. True-metric 5 km catchments + 1:1 ground facility allocation per block
    blocks_by_name = {b["block_name"]: b for b in d_assess["blocks"]}
    all_hab_pts = []
    all_exist_pts = []
    all_upg_pts = []
    all_new_pts = []
    all_trans_pts = []

    for blk in task["blocks"]:
        all_hab_pts.extend(task["habs"][blk["block_name"]])

    total_dist_hab_pop = sum(h[2] for h in all_hab_pts) or 1
    exact_exist_total = t_sec["existing_schools"]
    raw_allocs = []
    for blk in task["blocks"]:
        b_pop = sum(h[2] for h in task["habs"][blk["block_name"]])
        raw_allocs.append(exact_exist_total * (b_pop / total_dist_hab_pop))

    # Largest remainder integer apportionment so sum(exist per block) == t_sec['existing_schools'].
    floors = [int(math.floor(x)) for x in raw_allocs]
    rem_need = exact_exist_total - sum(floors)
    remainders = sorted(range(len(raw_allocs)), key=lambda i: raw_allocs[i] - floors[i], reverse=True)
    for i in remainders[:rem_need]:
        floors[i] += 1

    for idx_b, blk in enumerate(task["blocks"]):
        b_name = blk["block_name"]
        b_assess = blocks_by_name[b_name]
        ex, up, nw, tr = _sample_block_facilities(
            task["habs"][b_name],
            task["osm"][b_name],
            blk["polys"],
            floors[idx_b],
            b_assess["proposed_upgrades"],
            b_assess["proposed_new_schools"],
            b_assess["proposed_transport_hubs"],
            seed_key=f"{d_name}|{b_name}",
        )
        all_exist_pts.extend(ex)
        all_upg_pts.extend(up)
        all_new_pts.extend(nw)
        all_trans_pts.extend(tr)

    # Layer 1 of Catchment: uniform solid pale-teal fill for 5 km walking circles (no alpha stacking).
    diam_lon = (2.0 * 5.0) / km_per_lon
    diam_lat = (2.0 * 5.0) / KM_PER_DEG_LAT
    exist_bufs = [Ellipse(pt, width=diam_lon, height=diam_lat) for pt in all_exist_pts]
    if exist_bufs:
        pc_ex = PatchCollection(exist_bufs, facecolor="#E2F2EE", edgecolor="#B7DDD4", linewidths=0.35, zorder=4.4)
        pc_ex.set_clip_path(target_clip_patch)
        ax.add_collection(pc_ex)

    # Proposed school 5 km catchment expansion (warm ivory-amber halo).
    prop_bufs = [Ellipse(pt, width=diam_lon, height=diam_lat) for pt in (all_upg_pts + all_new_pts)]
    if prop_bufs:
        pc_pr = PatchCollection(prop_bufs, facecolor="#FEF3C7", edgecolor="#F59E0B", linewidths=0.45, linestyle=":", alpha=0.55, zorder=4.6)
        pc_pr.set_clip_path(target_clip_patch)
        ax.add_collection(pc_pr)

    # Subtle PMGSY settlement texture dots (up to 1,200 evenly strided real habitations).
    if all_hab_pts:
        stride = max(1, len(all_hab_pts) // 1200)
        sub_h = all_hab_pts[::stride]
        hx = [p[0] for p in sub_h]
        hy = [p[1] for p in sub_h]
        ax.scatter(hx, hy, s=3.2, c="#94A3B8", alpha=0.45, edgecolors="none", rasterized=True, zorder=4.8)

    # Draw official LGD CD block outlines on top of catchment wash so internal topology reads cleanly.
    for blk in task["blocks"]:
        bp = _rings_to_path(blk["polys"])
        if bp is not None:
            ax.add_patch(PathPatch(bp, facecolor="none", edgecolor="#64748B", linewidth=0.80, linestyle="--", zorder=5.2))

    # Bold outer district boundary (double-stroke halo + dark navy/slate outline).
    ax.add_patch(PathPatch(target_path, facecolor="none", edgecolor="#0F172A", linewidth=3.4, alpha=0.14, zorder=5.4))
    ax.add_patch(PathPatch(target_path, facecolor="none", edgecolor="#0F172A", linewidth=1.85, zorder=5.5))

    # Plot 1:1 markers with adaptive sizing scaled to district density.
    n_interventions = len(all_upg_pts) + len(all_new_pts) + len(all_trans_pts)
    dens_scale = 0.76 if n_interventions > 220 else (0.88 if n_interventions > 110 else 1.0)
    ms_ex = 12.0 if len(all_exist_pts) > 220 else 17.0

    if all_exist_pts:
        ax.scatter(
            [p[0] for p in all_exist_pts], [p[1] for p in all_exist_pts],
            s=ms_ex, c="#0F766E", marker="o", edgecolors="#FFFFFF", linewidths=0.4, alpha=0.85, zorder=6.0,
        )
    if all_trans_pts:
        ax.scatter(
            [p[0] for p in all_trans_pts], [p[1] for p in all_trans_pts],
            s=36.0 * dens_scale, c="#2563EB", marker="D", edgecolors="#FFFFFF", linewidths=0.5, alpha=0.92, zorder=6.2,
        )
    if all_new_pts:
        ax.scatter(
            [p[0] for p in all_new_pts], [p[1] for p in all_new_pts],
            s=50.0 * dens_scale, c="#DC2626", marker="^", edgecolors="#FFFFFF", linewidths=0.55, alpha=0.95, zorder=6.4,
        )
    if all_upg_pts:
        ax.scatter(
            [p[0] for p in all_upg_pts], [p[1] for p in all_upg_pts],
            s=72.0 * dens_scale, c="#F59E0B", marker="*", edgecolors="#78350F", linewidths=0.45, alpha=0.98, zorder=6.6,
        )

    # 2F. Dynamic Scale Bar (bottom-left) + North Arrow (opposite upper corner from Inset)
    ax.add_patch(FancyBboxPatch(
        (scale_card_rect[0], scale_card_rect[1]),
        scale_card_rect[2] - scale_card_rect[0],
        scale_card_rect[3] - scale_card_rect[1],
        boxstyle="round,pad=0.0,rounding_size=0.008",
        facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=0.9, alpha=0.94, zorder=8.0,
    ))
    half_x = 0.5 * (bar_x0 + bar_x1)
    bar_h = 0.010 * dy
    ax.add_patch(plt.Rectangle((bar_x0, bar_y), half_x - bar_x0, bar_h, facecolor="#0F172A", edgecolor="#0F172A", lw=0.6, zorder=8.2))
    ax.add_patch(plt.Rectangle((half_x, bar_y), bar_x1 - half_x, bar_h, facecolor="#FFFFFF", edgecolor="#0F172A", lw=0.8, zorder=8.2))
    ax.text(bar_x0, bar_y + 0.017 * dy, "0", ha="center", va="bottom", fontsize=7.6, fontweight="bold", color="#0F172A", zorder=8.3)
    ax.text(half_x, bar_y + 0.017 * dy, f"{scale_km / 2:g}", ha="center", va="bottom", fontsize=7.6, fontweight="bold", color="#0F172A", zorder=8.3)
    ax.text(bar_x1, bar_y + 0.017 * dy, f"{scale_km:g} km", ha="center", va="bottom", fontsize=7.6, fontweight="bold", color="#0F172A", zorder=8.3)
    ax.text(half_x, bar_y - 0.018 * dy, "True Ground Scale", ha="center", va="bottom", fontsize=6.2, color="#475569", zorder=8.3)

    # Compact North Arrow placed away from inset
    ax.add_patch(FancyBboxPatch(
        (north_card[0], north_card[1]), north_card[2] - north_card[0], north_card[3] - north_card[1],
        boxstyle="round,pad=0.0,rounding_size=0.008",
        facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=0.9, alpha=0.94, zorder=8.0,
    ))
    ax.annotate(
        "", xy=(nx, ny + 0.032 * dy), xytext=(nx, ny - 0.018 * dy),
        arrowprops=dict(arrowstyle="-|>", color="#0F172A", lw=1.8, mutation_scale=13), zorder=8.3,
    )
    ax.text(nx, ny - 0.032 * dy, "N", ha="center", va="center", fontsize=8.8, fontweight="bold", color="#0F172A", zorder=8.3)

    # 2G. Odisha State Locator Inset (smart free corner with true Odisha projection)
    inset_ax = ax.inset_axes([ix0_ax, iy0_ax, iw_ax, ih_ax], zorder=9)
    inset_ax.set_facecolor("#F8FAFC")
    inset_aspect = KM_PER_DEG_LAT / (KM_PER_DEG_LAT * math.cos(math.radians(20.25)))
    inset_box_ratio = (iw_ax * MAP_BOX[2] * FIG_W_IN) / (ih_ax * MAP_BOX[3] * FIG_H_IN)
    in_span_y = 5.35
    in_span_x = inset_box_ratio * in_span_y * inset_aspect
    inset_ax.set_xlim(84.42 - 0.5 * in_span_x, 84.42 + 0.5 * in_span_x)
    inset_ax.set_ylim(20.22 - 0.5 * in_span_y, 20.22 + 0.5 * in_span_y)
    inset_ax.set_aspect(inset_aspect, adjustable="box")
    inset_ax.set_xticks([])
    inset_ax.set_yticks([])
    for sp in inset_ax.spines.values():
        sp.set_edgecolor("#475569")
        sp.set_linewidth(1.0)

    for od_dn, od_polys in task["all_dist_paths"].items():
        op = _rings_to_path(od_polys)
        if op is None:
            continue
        is_tgt = (od_dn == d_name)
        inset_ax.add_patch(PathPatch(
            op,
            facecolor="#1E40AF" if is_tgt else "#E2E8F0",
            edgecolor="#FFFFFF" if is_tgt else "#94A3B8",
            linewidth=0.7 if is_tgt else 0.35,
            zorder=3 if is_tgt else 2,
        ))
    inset_ax.text(0.94, 0.06, "ODISHA", transform=inset_ax.transAxes, ha="right", va="bottom",
                  fontsize=6.8, fontweight="bold", color="#334155")

    # 2H. Collision-free LGD Block Badges + Leader Lines
    n_blk = len(task["blocks"])
    badge_fs = 6.8 if n_blk >= 20 else (7.3 if n_blk >= 11 else 7.9)
    obstacles = [inset_data_rect, scale_card_rect, north_card]
    placed = solve_label_layout(task["blocks"], xlim, ylim, true_aspect, obstacles, badge_fs)

    for it in placed:
        dist_moved = math.hypot((it["x"] - it["ax"]) / dx, (it["y"] - it["ay"]) / dy)
        if dist_moved > 0.022:
            ax.scatter([it["ax"]], [it["ay"]], s=10.0, c="#0F172A", zorder=8.8)
            ax.plot([it["ax"], it["x"]], [it["ay"], it["y"]], color="#334155", linewidth=0.80, zorder=8.7)
        ax.text(
            it["x"], it["y"], it["text"], ha="center", va="center",
            fontsize=badge_fs, fontweight="bold", color="#0F172A", linespacing=0.95,
            bbox=dict(boxstyle="round,pad=0.18", facecolor="#FFFFFF", edgecolor="#64748B", linewidth=0.75, alpha=0.92),
            zorder=9.2,
        )

    # =========================================================================
    # ZONE 3: SYMBOLOGY LEGEND PANEL (0.108 - 0.228)
    # =========================================================================
    leg_ax = fig.add_axes([ZONE_X, 0.108, ZONE_W, 0.120])
    leg_ax.set_xlim(0, 1)
    leg_ax.set_ylim(0, 1)
    leg_ax.axis("off")

    leg_card = FancyBboxPatch(
        (0.0, 0.0), 1.0, 1.0, boxstyle="round,pad=0.0,rounding_size=0.03",
        facecolor="#F8FAFC", edgecolor="#CBD5E1", linewidth=1.1, clip_on=False,
    )
    leg_ax.add_patch(leg_card)

    legend_handles = [
        Line2D([0], [0], marker="o", color="w", label=f"Existing Secondary ({t_sec['existing_schools']:,})",
               markerfacecolor="#0F766E", markeredgecolor="#FFFFFF", markersize=6.8),
        Line2D([0], [0], marker="*", color="w", label=f"Upgrade → Secondary ({t_sec['proposed_upgrades']:,})",
               markerfacecolor="#F59E0B", markeredgecolor="#78350F", markeredgewidth=0.6, markersize=10.5),
        Line2D([0], [0], marker="^", color="w", label=f"New Secondary School ({t_sec['proposed_new_schools']:,})",
               markerfacecolor="#DC2626", markeredgecolor="#FFFFFF", markersize=8.5),
        Line2D([0], [0], marker="D", color="w", label=f"Transit / Bus Hub ({t_sec['proposed_transport_hubs']:,})",
               markerfacecolor="#2563EB", markeredgecolor="#FFFFFF", markersize=7.2),
        Line2D([0], [0], marker="o", color="w", label="5 km Walking Service Radius",
               markerfacecolor="#E2F2EE", markeredgecolor="#64748B", markeredgewidth=0.8, markersize=10.5),
        Line2D([0], [0], color="#F59E0B", lw=1.4, ls=":", label="Proposed 5 km Catchment Halo"),
        Line2D([0], [0], color="#64748B", lw=1.1, ls="--", label=f"CD Block Boundary (LGD {n_blk})"),
        Line2D([0], [0], marker=".", color="w", label="PMGSY Rural Habitation Cluster",
               markerfacecolor="#94A3B8", markeredgecolor="none", markersize=8.5),
    ]
    leg_ax.legend(
        handles=legend_handles, loc="center", ncol=4, frameon=False,
        fontsize=7.9, columnspacing=1.2, handletextpad=0.5, borderaxespad=0.2,
    )

    # =========================================================================
    # ZONE 4: DARK STRATEGIC ACTION RIBBON (0.025 - 0.095)
    # =========================================================================
    ft_ax = fig.add_axes([ZONE_X, 0.025, ZONE_W, 0.070])
    ft_ax.set_xlim(0, 1)
    ft_ax.set_ylim(0, 1)
    ft_ax.axis("off")

    ft_card = FancyBboxPatch(
        (0.0, 0.0), 1.0, 1.0, boxstyle="round,pad=0.0,rounding_size=0.03",
        facecolor="#0F172A", edgecolor="#0F172A", linewidth=1.0, clip_on=False,
    )
    ft_ax.add_patch(ft_card)
    ft_accent = FancyBboxPatch(
        (0.0, 0.0), 0.011, 1.0, boxstyle="round,pad=0.0,rounding_size=0.01",
        facecolor="#F59E0B", edgecolor="none", clip_on=False,
    )
    ft_ax.add_patch(ft_accent)

    cyc_cnt = t_sec["cyclone_resilient_upgrades"]
    cyc_str = f"CYCLONE RETROFITS: {cyc_cnt} Coastal Units" if cyc_cnt > 0 else "TERRAIN SPEC: All-Weather Rural Grade"
    kpi_line = (
        f"SECONDARY OUTLAY: Rs. {t_sec['total_budget_cr']:.2f} Cr  |  "
        f"COVERAGE: {t_sec['initial_coverage_pct']:.1f}% → {t_sec['final_coverage_pct']:.1f}%  |  "
        f"TEACHERS: +{t_sec['teachers_required']:,}  |  GIRLS HOSTELS: +{t_sec['girls_hostels_proposed']:,}"
    )
    ft_ax.text(
        0.505, 0.67, kpi_line, ha="center", va="center",
        fontsize=8.3, fontweight="bold", color="#FDE68A",
    )
    ft_ax.text(
        0.505, 0.28,
        f"FLEET: {t_sec['fleet_minibuses']} Minibuses + {t_sec['fleet_feeder_vans']} Feeder Vans (OpEx Rs. {t_sec['annual_transit_opex_cr']:.2f} Cr/yr)  |  {cyc_str}",
        ha="center", va="center", fontsize=8.0, color="#E2E8F0",
    )

    fig.savefig(out_path, dpi=200, facecolor="#FFFFFF")
    plt.close(fig)
    return out_path


def generate_all_district_maps_parallel(geo_bundle, assess_data):
    """Generate all 30 Odisha district cartographic plates concurrently."""
    os.makedirs(OUT_DIR, exist_ok=True)
    tasks = _prepare_task_payloads(geo_bundle, assess_data)
    t0 = time.time()
    max_workers = min(8, os.cpu_count() or 4)
    out_files = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(render_single_district_map, t) for t in tasks]
        for fut in as_completed(futures):
            out_files.append(fut.result())
    print(f"Rendered {len(out_files)} district cartographic plates in {time.time() - t0:.2f}s.")
    return out_files


if __name__ == "__main__":
    geo_bundle, assess_data = load_data()
    generate_all_district_maps_parallel(geo_bundle, assess_data)
