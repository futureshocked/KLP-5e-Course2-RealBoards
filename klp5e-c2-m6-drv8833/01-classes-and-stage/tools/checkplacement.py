#!/usr/bin/env python3
"""Verify the Module 6 placement against the real footprint geometry.

Course 2's copy of Volume 2's tools/checkplacement.py (M6 P2, 2026-10-28). The geometry
code is the book's, unchanged: the s-expression reader, the courtyard and pad maths, the
outline arithmetic, the placement tables. What changed, and why:

  1. Footprint files. The book finds U1 in its own Libraries folder and everything else in
     KiCad's stock library. Here U1 comes from the stage's fp-lib-table (the nickname the
     board uses, `${KIPRJMOD}` = the board's folder, so Libraries/peters_custom_Library.pretty)
     and every other footprint from KiCad's stock library: KICAD10_FOOTPRINT_DIR if set,
     else /usr/share/kicad/footprints. The nickname each footprint carries in the board
     is used, as in the book; U1's is no longer hard-wired to `peter_footprints`.
  2. --board defaults to klp5e-c2-m6-drv8833.kicad_pcb, so the lecture runs it from a stage
     folder as `python3 tools/checkplacement.py --outline --fit --overlap --proximity`.
  3. Forgiving, with every tolerance in one place (below). The book compares to 0.001 mm
     everywhere except the proximity distances (0.15 mm). Here positions and the grid origin
     may be 0.05 mm out; rotations are exact.
  4. One OK or FAIL line per check, then one line per failing item. -v lists every item.
     Exit status 0 if every requested check passes, 1 otherwise.
  5. --fit also fails a courtyard that hangs over the outline. The book prints those as
     "informational" and passes, although its chapter says --fit confirms every courtyard
     is inside the outline; the course follows the chapter.
  6. New --positions: every part at its table position (0.05 mm) and rotation (exact). The
     book's tool never compares a position with its table (placeparts.py --check does), so
     a part typed wrongly but clear of everything else passed. New --block works on a board:
     the driver stage's courtyard box, 25.17 x 30.88 mm in the chapter.
     New --refs limits --fit, --overlap and --positions to a list of parts, for a stage
     where only the driver stage is placed.
  7. Left out: the book's spec-table mode (no --board), --table and --selftest. The course
     checks a board.

Nothing else is changed. In particular a part that is not on the board is skipped, never
failed, and said so on the way in, because a board with parts missing passes the part checks
trivially: read the "still to come" line.

Board coordinates (y down, origin on the outline's top-left corner), not page coordinates:
see from_board().

Run from the stage folder, with KiCad closed:

    python3 tools/checkplacement.py --board klp5e-c2-m6-drv8833.kicad_pcb \
        --outline --fit --overlap --proximity

S-expressions are walked with balanced parens, never regex: (pad ...) and (fp_poly ...)
nest, and a regex that looks right on one footprint quietly mis-parses the next.
Python 3 standard library only.
"""

import argparse
import math
import os
import sys

STOCK = os.environ.get("KICAD10_FOOTPRINT_DIR") or "/usr/share/kicad/footprints"
DEFAULT_BOARD = "klp5e-c2-m6-drv8833.kicad_pcb"

# ---------------------------------------------------------------------------
# tolerances: the one place to change them
# ---------------------------------------------------------------------------
POS_TOL = 0.05         # mm. Part positions (--positions) and the grid origin. One notch of
                       # the 0.05 mm grid passes, two do not; the table is typed to 0.01.
ROT_TOL = 0.001        # degrees. Rotations are exact; this only absorbs float noise.
OUTLINE_TOL = 0.01     # mm. Outline width, height and corner radius. A rectangle drawn by
                       # eye is out by tenths of a millimetre; one finished by typing is not.
PROXIMITY_TOL = 0.15   # mm. The book's band, kept: the chapter's five distances are quoted
                       # to 0.01, so the band is ~30x the rounding and under a quarter of
                       # one pin pitch (0.65 mm). A cap moved a whole pin over fails.
OVERLAP_TOL = 0.01     # mm. Courtyards may overlap by less than this and still pass:
                       # touching courtyards are legal, and 0.01 mm is below KiCad's
                       # own rounding of a courtyard line.
BLOCK_SIZE = (25.17, 30.88)    # mm, the chapter's driver stage
BLOCK_TOL = 0.05

# ---------------------------------------------------------------------------
# the placement plan, from draft/ch08-layout-spec.md sections 2 and 4
# ---------------------------------------------------------------------------

BOARD_W, BOARD_H = 52.0, 48.0
CORNER_R = 2.0                 # spec section 2, corners filleted at 2 mm
EDGE_CLEARANCE = 0.5           # .kicad_pro rules.min_copper_edge_clearance
U1_AT = (26.0, 27.0)

# Where the board's top-left corner sits on the sheet, and therefore where the grid origin
# goes, is NOT the page origin; everything in this file works in board coordinates and
# from_board() converts, taking the offset from the outline itself.
BOARD_ORIGIN = (120.0, 80.0)

# ref -> (footprint id, x, y, rotation), y measured UP from the board's bottom-left
#
# Sides are dictated by where each pin lands once U1 is turned 90 deg, which is the
# mirror image of what the schematic's left-to-right order suggests:
#   supply row (above U1): VCP +0.975, VM +0.325, GND -0.325, VINT -0.975
#   motor  row (below U1): motor A at -x (pins 2, 3, 4), motor B at +x (pins 5, 6, 7)
BLOCK_OFFSETS = {
    "U1": ("peters_custom_Library:HTSSOP-16-1EP_DRV8833_PD", 0.00, 0.00, 90),
    # C2, C3 and C4 shifted slightly and C2 turned 180 deg during power routing, so that
    # VM arrives on the pad nearest the trunk instead of crossing the part to reach it.
    "C3": ("Capacitor_SMD:C_0603_1608Metric", +4.00, +5.50, 0),      # VCP, pin 11, right
    "C2": ("Capacitor_SMD:C_0805_2012Metric", +0.25, +5.80, 180),    # VM,  pin 12
    "C4": ("Capacitor_SMD:C_0603_1608Metric", -3.50, +5.50, 0),      # VINT, pin 14, left
    # R2 is turned 180 deg so its AISEN pad faces U1 rather than pointing away from it.
    # Both dropped 0.75 mm during the channel A and B redraw, because six current-carrying
    # nets escape U1's bottom row at 0.65 mm pitch and the fanout needs the room. That put
    # them 4.26 and 4.20 mm from their sense pins instead of 3.62; see PROXIMITY below.
    "R2": ("Resistor_SMD:R_1206_3216Metric", -3.60, -6.25, 180),     # AISEN, pin 3, left
    "R3": ("Resistor_SMD:R_1206_3216Metric", +3.50, -6.25, 0),       # BISEN, pin 6, right
    "J2": ("TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal", -9.50, -19.00, 0),   # motor A, left
    "J3": ("TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal", +4.50, -19.00, 0),   # motor B, right
}

# Anchors are not centres. The terminal block's origin is pin 1, 3.04 mm from its left
# edge and 8.13 mm from its right; the 1x08 header's origin is pin 1 at one END, with
# the body running 19.55 mm the other way; C1 and Q1 are offset too. Every number below
# is the anchor KiCad writes into (at x y), not the middle of the part.
SHARED = {
    "J1": ("TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal", 16.60, 42.00, 180),
    # Q1 and R4 are turned 180 deg so that Q1's drain tab faces J1 and its gate faces R4,
    # which lets VM_IN and VM run straight across the supply row.
    "Q1": ("Package_TO_SOT_SMD:TO-252-2", 26.50, 42.50, 180),
    "R4": ("Resistor_SMD:R_0603_1608Metric", 26.25, 36.00, 180),
    "C1": ("Capacitor_THT:CP_Radial_D6.3mm_P2.50mm", 36.90, 42.00, 0),
    # D1 and R5 moved in beside C1 during power routing, so that the VM trunk reaches R5's
    # pad 1 without doubling back. They are no longer a column with R1: R1 left it entirely
    # and now sits beside J4's pins 1 and 4, which are the only two nets it touches. The
    # old three-part column and its 2.50 mm R5-to-R1 gap (finding L10) no longer apply.
    "D1": ("LED_SMD:LED_0805_2012Metric", 39.75, 36.00, 180),
    "R5": ("Resistor_SMD:R_0603_1608Metric", 36.25, 36.00, 0),
    "R1": ("Resistor_SMD:R_0603_1608Metric", 49.50, 19.50, 270),
    "J4": ("Connector_PinHeader_2.54mm:PinHeader_1x08_P2.54mm_Vertical", 45.91, 15.11, 180),
    "H1": ("MountingHole:MountingHole_3.2mm_M3", 4.00, 4.00, 0),
    "H2": ("MountingHole:MountingHole_3.2mm_M3", 48.00, 4.00, 0),
    "H3": ("MountingHole:MountingHole_3.2mm_M3", 4.00, 44.00, 0),
    "H4": ("MountingHole:MountingHole_3.2mm_M3", 48.00, 44.00, 0),
}

# ref -> (U1 pad number, claimed centre-to-pad distance in mm) from spec section 4
PROXIMITY = {
    "C2": ("12", 2.90),   # VM
    "C3": ("11", 3.99),   # VCP
    "C4": ("14", 3.62),   # VINT
    "R2": ("3", 4.26),    # AISEN, 3.62 until the bottom-row fanout needed the room
    "R3": ("6", 4.20),    # BISEN, the same
}


def placement(to_kicad=True, height=BOARD_H):
    """The whole board, block offsets resolved into absolute coordinates.

    The spec's tables are written in the frame a person reasons in: origin at the
    board's bottom-left corner, y increasing upward. KiCad's board file is the
    other way up, y increasing downward from the top-left. With to_kicad set,
    positions come back in KiCad's frame, which is the only frame the geometry
    below can be compared against footprint data.
    """
    out = dict(SHARED)
    for ref, (fp, dx, dy, rot) in BLOCK_OFFSETS.items():
        out[ref] = (fp, U1_AT[0] + dx, U1_AT[1] + dy, rot)
    if to_kicad:
        out = {r: (fp, x, height - y, rot) for r, (fp, x, y, rot) in out.items()}
    return out


# ---------------------------------------------------------------------------
# s-expression reader
# ---------------------------------------------------------------------------

def parse(text):
    """Parse one s-expression into nested lists. Atoms stay strings."""
    tok, i, n = [], 0, len(text)
    while i < n:
        c = text[i]
        if c == '"':
            j = i + 1
            buf = []
            while j < n and text[j] != '"':
                if text[j] == "\\":
                    buf.append(text[j + 1])
                    j += 2
                else:
                    buf.append(text[j])
                    j += 1
            tok.append(("str", "".join(buf)))
            i = j + 1
        elif c in "()":
            tok.append(("p", c))
            i += 1
        elif c.isspace():
            i += 1
        else:
            j = i
            while j < n and not text[j].isspace() and text[j] not in '()"':
                j += 1
            tok.append(("sym", text[i:j]))
            i = j

    def build(pos):
        node = []
        while pos < len(tok):
            kind, val = tok[pos]
            if kind == "p" and val == "(":
                child, pos = build(pos + 1)
                node.append(child)
            elif kind == "p" and val == ")":
                return node, pos + 1
            else:
                node.append(val)
                pos += 1
        return node, pos

    assert tok and tok[0] == ("p", "("), "not an s-expression"
    node, _ = build(1)
    return node


def find_all(node, head):
    """Every sub-list whose first atom is `head`, at any depth."""
    out = []
    if isinstance(node, list):
        if node and node[0] == head:
            out.append(node)
        for child in node:
            if isinstance(child, list):
                out += find_all(child, head)
    return out


def kv(node, key):
    for child in node:
        if isinstance(child, list) and child and child[0] == key:
            return child
    return None


# ---------------------------------------------------------------------------
# footprint geometry
# ---------------------------------------------------------------------------



# ---------------------------------------------------------------------------
# footprint geometry
# ---------------------------------------------------------------------------

_cache = {}
PROJECT_DIR = "."          # set by main(): the board's folder, which is ${KIPRJMOD}
_lib_table = None


def project_libs():
    """nickname -> .pretty folder, from the fp-lib-table beside the board, or {}."""
    global _lib_table
    if _lib_table is None:
        _lib_table = {}
        path = os.path.join(PROJECT_DIR, "fp-lib-table")
        if os.path.exists(path):
            for lib in find_all(parse(open(path, encoding="utf-8").read()), "lib"):
                name, uri = kv(lib, "name"), kv(lib, "uri")
                if not (name and uri):
                    continue
                folder = uri[1].replace("${KIPRJMOD}", PROJECT_DIR)
                for var, val in os.environ.items():
                    folder = folder.replace("${%s}" % var, val)
                _lib_table[name[1]] = folder
    return _lib_table


def load_footprint(fpid):
    if fpid in _cache:
        return _cache[fpid]
    lib, name = fpid.split(":", 1)
    folders = []
    if lib in project_libs():
        folders.append(project_libs()[lib])
    folders.append(os.path.join(STOCK, lib + ".pretty"))
    for folder in folders:
        path = os.path.join(folder, name + ".kicad_mod")
        if os.path.exists(path):
            _cache[fpid] = parse(open(path, encoding="utf-8").read())
            return _cache[fpid]
    raise SystemExit(f"footprint not found: {fpid}  (looked in: {', '.join(folders)})")


def courtyard_points(fp):
    """Every point on F.CrtYd / B.CrtYd, in the footprint's own frame."""
    pts = []
    for tag in ("fp_line", "fp_rect", "fp_poly", "fp_circle", "fp_arc"):
        for item in find_all(fp, tag):
            layer = kv(item, "layer")
            if not layer or "CrtYd" not in layer[1]:
                continue
            if tag == "fp_circle":
                c = kv(item, "center")
                e = kv(item, "end")
                if c and e:
                    cx, cy = float(c[1]), float(c[2])
                    ex, ey = float(e[1]), float(e[2])
                    r = math.hypot(ex - cx, ey - cy)
                    pts += [(cx - r, cy - r), (cx + r, cy + r)]
                continue
            if tag == "fp_poly":
                p = kv(item, "pts")
                if p:
                    pts += [(float(x[1]), float(x[2])) for x in p if isinstance(x, list) and x[0] == "xy"]
                continue
            for key in ("start", "end", "mid", "center"):
                k = kv(item, key)
                if k:
                    pts.append((float(k[1]), float(k[2])))
    return pts


def pad_centre(fp, number):
    for pad in find_all(fp, "pad"):
        if len(pad) > 1 and pad[1] == number:
            at = kv(pad, "at")
            if at:
                return float(at[1]), float(at[2])
    return None


def xform(pt, x, y, rot):
    """KiCad footprint frame -> board frame. Rotation is anticlockwise on screen,
    and the footprint's own y axis already points down, so a positive rotation
    maps (px, py) -> (px cos + py sin, -px sin + py cos)."""
    a = math.radians(rot)
    ca, sa = math.cos(a), math.sin(a)
    px, py = pt
    return (x + px * ca + py * sa, y - px * sa + py * ca)


def bbox(fpid, x, y, rot):
    pts = [xform(p, x, y, rot) for p in courtyard_points(load_footprint(fpid))]
    if not pts:
        return None
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return (min(xs), min(ys), max(xs), max(ys))


# ---------------------------------------------------------------------------
# board outline
# ---------------------------------------------------------------------------
def edge_shapes(root):
    """The board's own Edge.Cuts graphics, as (tag, node) pairs.

    Only top-level gr_* shapes are read. A footprint carries its own fp_line and
    fp_arc, and some of them do sit on Edge.Cuts, so find_all over the whole tree
    would collect a slot or a cutout belonging to a part and report it as outline.
    """
    out = []
    for item in root:
        if not (isinstance(item, list) and item):
            continue
        if item[0] not in ("gr_line", "gr_arc", "gr_rect", "gr_poly", "gr_circle"):
            continue
        layer = kv(item, "layer")
        if layer and len(layer) > 1 and layer[1] == "Edge.Cuts":
            out.append((item[0], item))
    return out


def shape_points(tag, node):
    """One outline shape's defining points, in page coordinates and in order."""
    keys = {
        "gr_line": ("start", "end"),
        "gr_arc": ("start", "mid", "end"),
        "gr_rect": ("start", "end"),
        "gr_circle": ("center", "end"),
    }.get(tag, ("start", "end"))
    pts = []
    for key in keys:
        k = kv(node, key)
        if k:
            pts.append((float(k[1]), float(k[2])))
    return pts


def edge_extents(root):
    """Bounding box of the board outline, in page coordinates.

    An arc contributes its start, mid and end points. That is exact for a quarter
    arc whose two endpoints are its own extremes in x and y, which is what every
    filleted corner is and what this outline is made of. A half turn or a reflex arc
    would need its centre and radius instead, so if the outline ever grows one of
    those this function has to grow with it.
    """
    pts = []
    for tag, node in edge_shapes(root):
        pts += shape_points(tag, node)
    if not pts:
        return None
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return (min(xs), min(ys), max(xs), max(ys))


def arc_centre(a, b, c):
    """Centre of the circle through three points, or None if they are collinear."""
    (ax, ay), (bx, by), (cx, cy) = a, b, c
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if abs(d) < 1e-12:
        return None
    sa, sb, sc = ax * ax + ay * ay, bx * bx + by * by, cx * cx + cy * cy
    ux = (sa * (by - cy) + sb * (cy - ay) + sc * (ay - by)) / d
    uy = (sa * (cx - bx) + sb * (ax - cx) + sc * (bx - ax)) / d
    return (ux, uy)


def grid_origin(root):
    """The stored grid origin, or None if the board has never had one set."""
    for g in find_all(root, "grid_origin"):
        return (float(g[1]), float(g[2]))
    return None


def pad_bbox(fpid, x, y, rot):
    """Extent of the footprint's copper pads only. This, not the courtyard, is what
    the board-edge clearance rule measures: a courtyard hanging over the edge is
    untidy but raises nothing, while copper over the edge is an error."""
    fp = load_footprint(fpid)
    pts = []
    for pad in find_all(fp, "pad"):
        layers = kv(pad, "layers")
        if layers and not any("Cu" in str(t) or t == "*" or "*.Cu" in str(t) for t in layers[1:]):
            continue
        at = kv(pad, "at")
        size = kv(pad, "size")
        if not at or not size:
            continue
        px, py = float(at[1]), float(at[2])
        sw, sh = float(size[1]) / 2, float(size[2]) / 2
        prot = float(at[3]) if len(at) > 3 else 0.0
        for cx, cy in ((-sw, -sh), (sw, -sh), (-sw, sh), (sw, sh)):
            a = math.radians(prot)
            rx = px + cx * math.cos(a) + cy * math.sin(a)
            ry = py - cx * math.sin(a) + cy * math.cos(a)
            pts.append(xform((rx, ry), x, y, rot))
    if not pts:
        return None
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return (min(xs), min(ys), max(xs), max(ys))



# ---------------------------------------------------------------------------
# checks. Each returns (summary, [failing items], [every item, for -v]); the
# summary starts with the verdict's reason, main() prints OK or FAIL.
# ---------------------------------------------------------------------------

def check_outline(path):
    """The board outline on a real board, against spec section 2.

    Five assertions, and the last is the one that earns this function its place. A
    grid origin sitting one grid step off the corner looks identical on screen, and
    puts every part typed through "Position Relative To..." out by that same amount,
    on every part, without a single DRC violation to show for it.
    """
    root = parse(open(path, encoding="utf-8").read())
    shapes = edge_shapes(root)
    bad, every = [], []

    counts = {}
    for tag, _ in shapes:
        counts[tag] = counts.get(tag, 0) + 1
    want = {"gr_line": 4, "gr_arc": 4}
    msg = f"a filleted rectangle: {counts or 'nothing on Edge.Cuts'}, expected {want}"
    (every if counts == want else bad).append(msg)

    ext = edge_extents(root)
    if ext is None:
        return "no outline on Edge.Cuts", bad + ["nothing to measure, the board has no outline"], every
    x0, y0, x1, y1 = ext
    w, h = x1 - x0, y1 - y0
    ok = abs(w - BOARD_W) <= OUTLINE_TOL and abs(h - BOARD_H) <= OUTLINE_TOL
    msg = f"{w:.3f} x {h:.3f} mm, expected {BOARD_W:g} x {BOARD_H:g} (within {OUTLINE_TOL} mm)"
    every.append(msg)
    if not ok:
        bad.append(msg)

    off = 0
    for tag, node in shapes:
        if tag != "gr_arc":
            continue
        pts = shape_points(tag, node)
        if len(pts) != 3:
            off += 1
            continue
        c = arc_centre(*pts)
        if c is None:
            off += 1
            bad.append("an arc's three points are collinear")
            continue
        r = math.hypot(pts[0][0] - c[0], pts[0][1] - c[1])
        a0 = math.atan2(pts[0][1] - c[1], pts[0][0] - c[0])
        a1 = math.atan2(pts[2][1] - c[1], pts[2][0] - c[0])
        sweep = abs(math.degrees(a1 - a0)) % 360
        if sweep > 180:
            sweep = 360 - sweep
        good = abs(r - CORNER_R) <= OUTLINE_TOL and abs(sweep - 90) < 0.01
        off += not good
        msg = (f"corner at ({pts[0][0] - x0:5.2f}, {pts[0][1] - y0:5.2f}) "
               f"radius {r:.3f} mm, sweep {sweep:.2f} deg, expected {CORNER_R:g} mm and 90")
        every.append(msg)
        if not good:
            bad.append(msg)
    if off:
        bad.append(f"{off} corner arc(s) are not a {CORNER_R:g} mm quarter turn")

    ends = {}
    for tag, node in shapes:
        pts = shape_points(tag, node)
        if not pts:
            continue
        for p in (pts[0], pts[-1]):
            key = (round(p[0], 4), round(p[1], 4))
            ends[key] = ends.get(key, 0) + 1
    loose = sorted(k for k, n in ends.items() if n != 2)
    if loose:
        bad.append(f"the outline does not close, {len(loose)} loose end(s): {loose}")
    else:
        every.append("the loop closes")

    g = grid_origin(root)
    ok = g is not None and abs(g[0] - x0) <= POS_TOL and abs(g[1] - y0) <= POS_TOL
    where = "never set" if g is None else f"({g[0]:g}, {g[1]:g})"
    msg = (f"grid origin {where}, outline's top-left corner is ({x0:g}, {y0:g}) "
           f"(within {POS_TOL} mm)")
    every.append(msg)
    if not ok:
        bad.append(msg)

    summary = (f"{w:.1f} x {h:.1f} mm, corners {CORNER_R:g} mm, loop closed, "
               f"grid origin on the corner") if not bad else f"{len(bad)} problem(s)"
    return summary, bad, every


def chosen(place, refs):
    return {r: v for r, v in place.items() if refs is None or r in refs}


def check_fit(place, w, h, clr, refs):
    place = chosen(place, refs)
    bad, every = [], []
    for ref in sorted(place):
        fpid, x, y, rot = place[ref]
        b = pad_bbox(fpid, x, y, rot)
        if b is None:
            every.append(f"{ref:4} no copper (mechanical part)")
        else:
            x0, y0, x1, y1 = b
            margin = min(x0 - clr, y0 - clr, (w - clr) - x1, (h - clr) - y1)
            msg = (f"{ref:4} copper x {x0:6.2f}..{x1:6.2f}  y {y0:6.2f}..{y1:6.2f}  "
                   f"margin {margin:+.2f} mm to the {clr:g} mm keep-in")
            every.append(msg)
            if margin < -1e-6:
                bad.append(f"{ref:4} copper {-margin:.2f} mm closer to the edge than "
                           f"{clr:g} mm  (x {x0:.2f}..{x1:.2f}, y {y0:.2f}..{y1:.2f})")
        b = bbox(fpid, x, y, rot)
        if b is not None:
            x0, y0, x1, y1 = b
            m = min(x0, y0, w - x1, h - y1)
            every.append(f"{ref:4} courtyard margin to the outline {m:+.2f} mm")
            if m < -1e-6:
                bad.append(f"{ref:4} courtyard hangs {-m:.2f} mm over the outline")
    n = len(place)
    return (f"{n} parts: copper {clr:g} mm clear of the edge, courtyards inside the outline"
            if not bad else f"{len(bad)} problem(s) in {n} parts"), bad, every


def check_overlap(place, refs):
    place = chosen(place, refs)
    refs_ = sorted(place)
    boxes = {r: bbox(*place[r]) for r in refs_}
    bad = []
    for i, a in enumerate(refs_):
        for b in refs_[i + 1:]:
            ba, bb = boxes[a], boxes[b]
            if ba is None or bb is None:
                continue
            ox = min(ba[2], bb[2]) - max(ba[0], bb[0])
            oy = min(ba[3], bb[3]) - max(ba[1], bb[1])
            if ox > OVERLAP_TOL and oy > OVERLAP_TOL:
                bad.append(f"{a} / {b} courtyards overlap {ox:.2f} x {oy:.2f} mm")
    n = len(refs_)
    return (f"no two of {n} courtyards intersect" if not bad
            else f"{len(bad)} collision(s)"), bad, []


def check_block(place):
    """The driver stage's courtyard box, measured on the board.

    Measured in the frame the board is built in: the Phoenix terminal's courtyard runs 5.71 mm
    one side of its pad row and 5.10 mm the other, so a mirrored frame reports a different height.
    """
    missing = [r for r in BLOCK_OFFSETS if r not in place]
    if missing:
        return None, [], [f"not on the board: {', '.join(missing)}"]
    xs, ys = [], []
    for ref in BLOCK_OFFSETS:
        b = bbox(*place[ref])
        if b:
            xs += [b[0], b[2]]
            ys += [b[1], b[3]]
    w, h = max(xs) - min(xs), max(ys) - min(ys)
    ok = abs(w - BLOCK_SIZE[0]) <= BLOCK_TOL and abs(h - BLOCK_SIZE[1]) <= BLOCK_TOL
    bad = [] if ok else [f"driver stage {w:.2f} x {h:.2f} mm, expected "
                         f"{BLOCK_SIZE[0]} x {BLOCK_SIZE[1]} (within {BLOCK_TOL} mm)"]
    return (f"driver stage {w:.2f} x {h:.2f} mm, two side by side need {2 * w:.2f} mm",
            bad, [f"x {min(xs):.2f}..{max(xs):.2f}  y {min(ys):.2f}..{max(ys):.2f}"])


def check_proximity(place):
    missing = [r for r in ["U1"] + sorted(PROXIMITY) if r not in place]
    if missing:
        return None, [], [f"not on the board: {', '.join(missing)}"]
    u1 = load_footprint(place["U1"][0])
    _, ux, uy, urot = place["U1"]
    bad, every = [], []
    for ref, (padnum, claimed) in sorted(PROXIMITY.items()):
        pc = pad_centre(u1, padnum)
        if pc is None:
            bad.append(f"{ref}: U1 pad {padnum} not found in {place['U1'][0]}")
            continue
        pad_xy = xform(pc, ux, uy, urot)
        _, px, py, _ = place[ref]
        d = math.hypot(px - pad_xy[0], py - pad_xy[1])
        msg = (f"{ref} to U1 pad {padnum:>2}: {d:.2f} mm, chapter says {claimed:.2f} mm "
               f"(within {PROXIMITY_TOL} mm)")
        every.append(msg)
        if abs(d - claimed) > PROXIMITY_TOL:
            bad.append(msg)
    return ("all five distances match the chapter" if not bad
            else f"{len(bad)} distance(s) off"), bad, every


def norm(deg):
    return round(float(deg) % 360.0, 6)


def check_positions(place, refs):
    """Each part at the table's position (POS_TOL) and rotation (exact)."""
    table = placement(to_kicad=True)
    bad, every = [], []
    n = 0
    for ref in sorted(table):
        if ref not in place or (refs is not None and ref not in refs):
            continue
        n += 1
        _, tx, ty, trot = table[ref]
        _, x, y, rot = place[ref]
        dx, dy = x - tx, y - ty
        drot = abs((norm(rot) - norm(trot) + 180) % 360 - 180)
        msg = (f"{ref:4} at ({x:6.2f}, {y:6.2f}) {rot:g} deg, table ({tx:.2f}, {ty:.2f}) "
               f"{trot:g} deg")
        every.append(msg)
        if abs(dx) > POS_TOL or abs(dy) > POS_TOL or drot > ROT_TOL:
            bad.append(f"{msg}: off by ({dx:+.2f}, {dy:+.2f}) mm"
                       + (f", rotation off by {drot:g} deg" if drot > ROT_TOL else ""))
    return (f"{n} parts at their table positions (within {POS_TOL} mm), rotations exact"
            if not bad else f"{len(bad)} of {n} parts off the table"), bad, every


# U1 pin groups, to prove the chip is the right way up rather than assume it
SUPPLY_PINS = {"11": "VCP", "12": "VM", "13": "GND", "14": "VINT"}
MOTOR_PINS = {"2": "AOUT1", "3": "AISEN", "4": "AOUT2", "5": "BOUT2", "6": "BISEN", "7": "BOUT1"}


def check_orientation(place, height):
    """Supply pins must end up nearer the top edge, motor pins nearer the bottom."""
    if "U1" not in place:
        return None, [], ["U1 is not on the board"]
    u1 = load_footprint(place["U1"][0])
    _, ux, uy, urot = place["U1"]
    groups = {}
    for name, pins in (("supply", SUPPLY_PINS), ("motor", MOTOR_PINS)):
        ys = [xform(pad_centre(u1, num), ux, uy, urot)[1] for num in pins if pad_centre(u1, num)]
        groups[name] = sum(ys) / len(ys)
    ok = groups["supply"] < groups["motor"]      # smaller y is nearer the top
    return ("supply pins up, motor pins down" if ok else "U1 is upside down",
            [] if ok else [f"supply pins mean y {groups['supply']:.2f}, motor pins "
                           f"{groups['motor']:.2f}: the chip is turned the wrong way"],
            [f"supply pins mean y {groups['supply']:.2f}, motor {groups['motor']:.2f}"])


def from_board(path):
    """Read placement out of a real .kicad_pcb.

    The file stores page coordinates and every table in this script is in board
    coordinates, so the outline's top-left corner comes off on the way out. Taking
    that offset from the outline itself, rather than from BOARD_ORIGIN, means moving
    the board on the sheet can never shift every reported position by the same amount
    while the checks carry on passing.
    """
    root = parse(open(path, encoding="utf-8").read())
    ext = edge_extents(root)
    if ext is None:
        print("  note: no Edge.Cuts outline, so positions are page coordinates and "
              "the fit check will not mean anything", file=sys.stderr)
        ox, oy = 0.0, 0.0
    else:
        ox, oy = ext[0], ext[1]
    out = {}
    for fp in find_all(root, "footprint"):
        at = kv(fp, "at")
        ref = None
        for prop in find_all(fp, "property"):
            if len(prop) > 2 and prop[1] == "Reference":
                ref = prop[2]
        if ref and at:
            rot = float(at[3]) if len(at) > 3 else 0.0
            out[ref] = (fp[1], float(at[1]) - ox, float(at[2]) - oy, rot)
    return out


def main():
    global PROJECT_DIR
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--board", default=DEFAULT_BOARD, help="the .kicad_pcb to check "
                    f"(default {DEFAULT_BOARD})")
    ap.add_argument("--width", type=float, default=BOARD_W)
    ap.add_argument("--height", type=float, default=BOARD_H)
    ap.add_argument("--clearance", type=float, default=EDGE_CLEARANCE)
    ap.add_argument("--outline", action="store_true", help="outline and grid origin")
    ap.add_argument("--fit", action="store_true", help="copper and courtyards against the edge")
    ap.add_argument("--overlap", action="store_true", help="no two courtyards intersect")
    ap.add_argument("--proximity", action="store_true", help="the five distances")
    ap.add_argument("--positions", action="store_true", help="every part at its table position")
    ap.add_argument("--block", action="store_true", help="the driver stage's size")
    ap.add_argument("--orientation", action="store_true", help="U1 the right way up")
    ap.add_argument("--refs", help="limit --fit, --overlap and --positions to these parts, "
                    "comma-separated, or 'driver' for the eight driver-stage parts "
                    "(a stage where only those are placed)")
    ap.add_argument("-v", "--verbose", action="store_true", help="list every item checked")
    a = ap.parse_args()

    if not os.path.exists(a.board):
        ap.error(f"no board {a.board}: run from the stage folder or pass --board")
    PROJECT_DIR = os.path.dirname(os.path.abspath(a.board))
    refs = set(a.refs.replace(" ", "").split(",")) if a.refs else None
    if refs == {"driver"}:
        refs = set(BLOCK_OFFSETS)

    if not (a.fit or a.outline or a.overlap or a.block or a.proximity or a.positions
            or a.orientation):
        a.fit = a.overlap = a.proximity = a.positions = a.orientation = a.outline = True

    place = from_board(a.board)
    print(f"placement source: {a.board}   ({len(place)} parts)")
    absent = sorted(set(placement(to_kicad=True)) - set(place))
    if absent:
        print(f"  {len(place)} of {len(placement())} of the plan's parts are on the board; "
              f"still to come: {', '.join(absent)}")

    bad = 0

    def report(name, result):
        nonlocal bad
        summary, problems, every = result
        if summary is None:
            print(f"SKIP {name}: " + "; ".join(every))
            return
        print(f"{'FAIL' if problems else 'OK  '} {name}: {summary}")
        for p in problems:
            print(f"       {p}")
        if a.verbose:
            for e in every:
                print(f"       . {e}")
        bad += len(problems)

    if a.outline:
        report("outline", check_outline(a.board))
    if a.fit:
        report("fit", check_fit(place, a.width, a.height, a.clearance, refs))
    if a.overlap:
        report("overlap", check_overlap(place, refs))
    if a.orientation:
        report("orientation", check_orientation(place, a.height))
    if a.block:
        report("block", check_block(place))
    if a.proximity:
        report("proximity", check_proximity(place))
    if a.positions:
        report("positions", check_positions(place, refs))

    print("PASS" if not bad else f"FAIL ({bad} problem{'s' if bad != 1 else ''})")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
