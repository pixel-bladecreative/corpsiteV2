#!/usr/bin/env python3
"""Pixel Blade candidate marks, built as real geometry.

Generation gives concepts; it does not give marks. These are constructed so
they are flat, single-colour, exact at any size, and legible at favicon scale.
"""
import math, os, cairosvg

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "marks")
os.makedirs(OUT, exist_ok=True)
S = 200                      # viewbox
C = S / 2


def svg(body, stroke="#C6A664", extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" '
            f'fill="none" stroke="{stroke}" stroke-linecap="butt" '
            f'stroke-linejoin="miter">{extra}{body}</svg>')


def pt(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def arc(cx, cy, r, a0, a1, w):
    x0, y0 = pt(cx, cy, r, a0)
    x1, y1 = pt(cx, cy, r, a1)
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return (f'<path d="M{x0:.2f} {y0:.2f} A{r} {r} 0 {large} 1 {x1:.2f} {y1:.2f}" '
            f'stroke-width="{w}"/>')


def sq(x, y, s, fill="#C6A664"):
    return f'<rect x="{x:.2f}" y="{y:.2f}" width="{s:.2f}" height="{s:.2f}" fill="{fill}" stroke="none"/>'


# ── 01 · CUT ENSO ─────────────────────────────────────────────────────────
# A circle interrupted by a straight cut, the smaller piece slid along it.
# The slip has to be decisive or it reads as a drawing error.
def cut_enso(slip=11.0, gap=9, cut_deg=-38, w=7, r=74):
    a0, a1 = cut_deg + gap / 2, cut_deg - gap / 2 + 360
    major = arc(C, C, r, a0, a1, w)
    dx = slip * math.cos(math.radians(cut_deg + 90))
    dy = slip * math.sin(math.radians(cut_deg + 90))
    minor = arc(C + dx, C + dy, r, cut_deg - gap / 2, cut_deg + gap / 2, w)
    return svg(major + minor)


# ── 02 · CUT ENSO, LOSING RESOLUTION ──────────────────────────────────────
# Solid for most of its length, then the ring coarsens into blocks and stops.
# The decay runs in ONE direction only; the far end of the gap is a clean cut.
def cut_enso_pixel(cut_deg=-38, gap=14, w=7, r=74, decay=72, n=11):
    a_clean = cut_deg + gap / 2          # clean square-cut end
    a_decay = cut_deg - gap / 2 + 360    # the end that falls apart
    body = arc(C, C, r, a_clean, a_decay - decay, w)
    blocks = ""
    for i in range(n):
        t = i / (n - 1)                              # 0 at the solid ring, 1 at the cut
        a = a_decay - decay * (1 - t)
        size = w * (0.60 + 1.55 * t ** 1.9)          # fine -> coarse
        # spread them as they coarsen so the run never fuses into a lump
        a += (t ** 2) * 7
        x, y = pt(C, C, r, a)
        blocks += sq(x - size / 2, y - size / 2, size)
    # three coarse squares carried past the cut, drifting off the arc
    for k, (da, dr) in enumerate([(13, 1.05), (24, 1.12), (37, 1.21)]):
        size = w * (2.0 + 0.85 * k)
        x, y = pt(C, C, r * dr, a_decay + da)
        blocks += sq(x - size / 2, y - size / 2, size)
    return svg(body + blocks)


# ── 03 · PIXEL ENSO ───────────────────────────────────────────────────────
# No stroke at all. The whole circle is built from squares that coarsen
# toward the cut — fully committed to the brand's own medium.
def pixel_enso(cut_deg=-38, gap=26, r=74, n=54, w=7):
    a0 = cut_deg + gap / 2
    sweep = 360 - gap
    out = ""
    for i in range(n):
        t = i / (n - 1)
        a = a0 + sweep * t
        size = w * (0.62 + 1.9 * t ** 2.4)
        if t > 0.80 and i % 2:                       # thin out near the break
            continue
        x, y = pt(C, C, r, a)
        out += sq(x - size / 2, y - size / 2, size)
    for k, (da, dr) in enumerate([(6, 1.04), (14, 1.11), (23, 1.19)]):
        size = w * (2.0 + 0.75 * k)
        x, y = pt(C, C, r * dr, a0 + sweep + da)
        out += sq(x - size / 2, y - size / 2, size)
    return svg(out)


# ── 04 · CUT ENSO + BLADE ─────────────────────────────────────────────────
# The circle, and the stroke that cut it, left in frame.
def enso_blade(w=7, r=72, cut_deg=-38, gap=13):
    a0, a1 = cut_deg + gap / 2, cut_deg - gap / 2 + 360
    ring = arc(C, C, r, a0, a1, w)
    x0, y0 = pt(C, C, r * 1.46, cut_deg + 180)
    x1, y1 = pt(C, C, r * 1.46, cut_deg)
    blade = f'<path d="M{x0:.1f} {y0:.1f} L{x1:.1f} {y1:.1f}" stroke-width="{w}"/>'
    return svg(ring + blade)


MARKS = {
    "01-cut-enso": cut_enso(),
    "02-cut-enso-pixel": cut_enso_pixel(),
    "03-pixel-enso": pixel_enso(),
    "04-enso-blade": enso_blade(),
}

for name, s in MARKS.items():
    open(f"{OUT}/{name}.svg", "w").write(s)
    for px, tag in ((800, ""), (64, "-64"), (32, "-32"), (16, "-16")):
        cairosvg.svg2png(bytestring=s.encode(), write_to=f"{OUT}/{name}{tag}.png",
                         output_width=px, output_height=px,
                         background_color="#0A0A0B")
    # day mode: oxide on paper
    day = s.replace("#C6A664", "#5E321F")
    open(f"{OUT}/{name}-day.svg", "w").write(day)
    cairosvg.svg2png(bytestring=day.encode(), write_to=f"{OUT}/{name}-day.png",
                     output_width=800, output_height=800, background_color="#F4F5F2")
    print(f"{name}: svg + 800/64/16 night + day")


# ── LOCKUPS ───────────────────────────────────────────────────────────────
def lockup(mark_svg, ink="#C6A664", word="#E8E3D6", w=760, h=200):
    inner = mark_svg.split(">", 1)[1].rsplit("</svg>", 1)[0]
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" fill="none">'
        f'<g transform="translate(8,0) scale(1.0)" stroke="{ink}" '
        f'stroke-linecap="butt" stroke-linejoin="miter">{inner}</g>'
        f'<text x="238" y="112" font-family="Archivo, Helvetica, Arial, sans-serif" '
        f'font-size="46" font-weight="300" letter-spacing="15" fill="{word}" '
        f'stroke="none">PIXEL BLADE</text>'
        f'<text x="242" y="146" font-family="JetBrains Mono, monospace" '
        f'font-size="15" letter-spacing="7" fill="{ink}" stroke="none" '
        f'opacity="0.85">ADVERTISING</text></svg>')


for nm, base in (("01-cut-enso", MARKS["01-cut-enso"]),
                 ("02-cut-enso-pixel", MARKS["02-cut-enso-pixel"])):
    n = lockup(base)
    open(f"{OUT}/lockup-{nm}.svg", "w").write(n)
    cairosvg.svg2png(bytestring=n.encode(), write_to=f"{OUT}/lockup-{nm}.png",
                     output_width=1520, background_color="#0A0A0B")
    d = lockup(base, ink="#5E321F", word="#13252C")
    open(f"{OUT}/lockup-{nm}-day.svg", "w").write(d)
    cairosvg.svg2png(bytestring=d.encode(), write_to=f"{OUT}/lockup-{nm}-day.png",
                     output_width=1520, background_color="#F4F5F2")
    print(f"lockup-{nm}: night + day")


# ══ CRANE × ENSO ══════════════════════════════════════════════════════════
# The crane returns — but it does not sit politely inside the ring. It crosses
# in front of it, and where it crosses, the ring is not there. The occlusion IS
# the interaction: the bird is defined as much by what it interrupts as by what
# it draws, which is what lets it stay this reduced.
#
# Four parts, one axis. One wing, not two — two wings read as a butterfly. The
# neck is a stroked line with a kink in it, because a taper reads as a spear
# and a bend reads as a head. Straight edges only: paper folds, it does not
# curve. Drawn facing left in the 200 box, then mirrored and banked by CRANE_TF.
CRANE_FILL = {
    "wing": [(80, 128), (130, 2), (166, 48), (122, 118)],   # the plane that carries it
    "tail": [(162, 80), (116, 108), (112, 130)],            # short blunt wedge
    "keel": [(92, 128), (116, 122), (104, 152)],            # the body, hanging
}
CRANE_LINE = {"neck": ([(104, 122), (26, 96), (2, 66)], 7.5)}

# The crease. One line, wing root to wing tip, drawn in the PAGE GROUND so it
# cuts the plane in two. A flat shape with a fold in it reads as paper; without
# it the wing reads as a feather. This one line is the whole origami cue.
CRANE_CREASE = [(100, 124), (131, 10)]

# Banked, mirrored, and sized so the wing tip and the head break the ring while
# the lower-left arc stays whole. The bank is what keeps a circular container
# from going heraldic; the whole arc is what keeps it a seal.
CRANE_TF = (f"translate({2 * C},0) scale(-1,1) rotate(-10 {C} {C}) "
            f"translate({C},{C}) scale(0.86) translate({-C},{-C})")

GROUND = "#0A0A0B"
CUT_LL = 145                 # the crane version cuts its ring in the quiet quadrant


def poly(pts, close=True):
    return "M" + " L".join(f"{x} {y}" for x, y in pts) + (" Z" if close else "")


def crane_paths(fill="#C6A664", w=7, only=None, crease=True):
    """The bird. fill=None draws it in outline instead of solid."""
    fills = {k: v for k, v in CRANE_FILL.items() if not only or k in only}
    lines = {k: v for k, v in CRANE_LINE.items() if not only or k in only}
    out = ""
    for pts in fills.values():
        out += (f'<path d="{poly(pts)}" fill="{fill or "none"}" '
                f'stroke="{fill or "#C6A664"}" stroke-width="{1.2 if fill else w * .62}" '
                f'stroke-linejoin="round"/>')
    for pts, lw in lines.values():
        out += (f'<path d="{poly(pts, False)}" fill="none" stroke="#C6A664" '
                f'stroke-width="{lw if fill else lw * .72}"/>')
    if crease and "wing" in fills and fill:
        out += (f'<path d="{poly(CRANE_CREASE, False)}" fill="none" '
                f'stroke="{GROUND}" stroke-width="{w * 0.48}"/>')
    return f'<g transform="{CRANE_TF}">{out}</g>'


def crane_mask(mid, grow=11, only=None):
    """A dilated crane silhouette, used to knock the ring out behind it.

    The dilation is clearance: the ring stops short of the bird rather than
    touching it, so the two never fuse into one blob as the mark scales down.
    """
    body = "".join(f'<path d="{poly(p)}" fill="#000" stroke="#000" '
                   f'stroke-width="{grow}" stroke-linejoin="round"/>'
                   for k, p in CRANE_FILL.items() if not only or k in only)
    body += "".join(f'<path d="{poly(p, False)}" fill="none" stroke="#000" '
                    f'stroke-width="{lw + grow}" stroke-linejoin="round" '
                    f'stroke-linecap="round"/>'
                    for k, (p, lw) in CRANE_LINE.items() if not only or k in only)
    return (f'<mask id="{mid}" maskUnits="userSpaceOnUse" x="0" y="0" '
            f'width="{S}" height="{S}"><rect width="{S}" height="{S}" fill="#fff"/>'
            f'<g transform="{CRANE_TF}">{body}</g></mask>')


def enso_crane(mid, solid=True, w=7, r=74, grow=11, slip=0, gap=0,
               cut_deg=CUT_LL, only=None):
    """Ring behind, crane in front, ring absent where the crane crosses it."""
    if gap:
        ring = arc(C, C, r, cut_deg + gap / 2, cut_deg - gap / 2 + 360, w)
        if slip:
            dx = slip * math.cos(math.radians(cut_deg + 90))
            dy = slip * math.sin(math.radians(cut_deg + 90))
            ring += arc(C + dx, C + dy, r, cut_deg - gap / 2, cut_deg + gap / 2, w)
    else:
        ring = f'<circle cx="{C}" cy="{C}" r="{r}" stroke-width="{w}"/>'
    body = (f'<g mask="url(#{mid})">{ring}</g>'
            + crane_paths(fill="#C6A664" if solid else None, w=w, only=only))
    return svg(body, extra=crane_mask(mid, grow, only))


def enso_crane_pixel(mid="kp", w=7, r=74, grow=11, decay=72, n=11,
                     cut_deg=CUT_LL, gap=14):
    """Crane occluding the ring, and the ring losing resolution as it leaves.

    The end state of the animation 02 describes: the seal comes apart into the
    medium it cuts with, and the bird is what stays.
    """
    a_clean, a_decay = cut_deg + gap / 2, cut_deg - gap / 2 + 360
    out = arc(C, C, r, a_clean, a_decay - decay, w)
    for i in range(n):
        t = i / (n - 1)
        a = a_decay - decay * (1 - t) + (t ** 2) * 7
        size = w * (0.60 + 1.55 * t ** 1.9)
        x, y = pt(C, C, r, a)
        out += sq(x - size / 2, y - size / 2, size)
    for k, (da, dr) in enumerate([(13, 1.05), (24, 1.12), (37, 1.21)]):
        size = w * (2.0 + 0.85 * k)
        x, y = pt(C, C, r * dr, a_decay + da)
        out += sq(x - size / 2, y - size / 2, size)
    return svg(f'<g mask="url(#{mid})">{out}</g>' + crane_paths(),
               extra=crane_mask(mid, grow))


CRANE_MARKS = {
    "05-enso-crane":       enso_crane("ka"),
    "06-enso-crane-cut":   enso_crane("kb", slip=11.0, gap=9),
    "07-enso-crane-line":  enso_crane("kc", solid=False),
    "08-enso-crane-wing":  enso_crane("kd", only=("wing", "neck")),
    "09-enso-crane-pixel": enso_crane_pixel(),
}
MARKS.update(CRANE_MARKS)

for name in CRANE_MARKS:
    s = MARKS[name]
    open(f"{OUT}/{name}.svg", "w").write(s)
    for px, tag in ((800, ""), (64, "-64"), (32, "-32"), (16, "-16")):
        cairosvg.svg2png(bytestring=s.encode(), write_to=f"{OUT}/{name}{tag}.png",
                         output_width=px, output_height=px, background_color=GROUND)
    # day mode: oxide on paper — the crease follows the ground, not the ink
    day = s.replace("#C6A664", "#5E321F").replace(GROUND, "#F4F5F2")
    open(f"{OUT}/{name}-day.svg", "w").write(day)
    cairosvg.svg2png(bytestring=day.encode(), write_to=f"{OUT}/{name}-day.png",
                     output_width=800, output_height=800, background_color="#F4F5F2")
    print(f"{name}: built")

for nm in ("05-enso-crane", "06-enso-crane-cut"):
    n = lockup(MARKS[nm])
    open(f"{OUT}/lockup-{nm}.svg", "w").write(n)
    cairosvg.svg2png(bytestring=n.encode(), write_to=f"{OUT}/lockup-{nm}.png",
                     output_width=1520, background_color=GROUND)
    d = lockup(MARKS[nm], ink="#5E321F", word="#13252C").replace(GROUND, "#F4F5F2")
    open(f"{OUT}/lockup-{nm}-day.svg", "w").write(d)
    cairosvg.svg2png(bytestring=d.encode(), write_to=f"{OUT}/lockup-{nm}-day.png",
                     output_width=1520, background_color="#F4F5F2")
    print(f"lockup-{nm}: night + day")
