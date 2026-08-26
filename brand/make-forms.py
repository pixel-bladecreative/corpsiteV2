#!/usr/bin/env python3
"""Fresh marks, built from PLANES instead of strokes.

Every previous round drew outlines. Every reference Spencer supplied builds
form the opposite way: adjacent facets sit at different angles to one light and
land at different VALUES, and the fold is simply where two values meet. Nothing
is outlined. That is the whole difference between a logo drawing of paper and a
piece of paper.

So there are no strokes in this file. Each mark is a list of polygons with a
value taken from the bronze ramp, lit consistently from the upper left.
"""
import math, os, cairosvg

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "forms")
os.makedirs(OUT, exist_ok=True)
S = 200
C = S / 2

# One light, upper left. A facet's value is decided by how it faces that light —
# never by what would look nice. Five steps is the whole range; a sixth reads as
# a gradient and the object stops looking folded.
V = {"deep": "#3F3937", "shade": "#9A7E67", "mid": "#C98B52",
     "lit": "#E59E5D", "hi": "#EBA564", "hot": "#FEFEF5",
     "void": "#0A0A0B", "petrol": "#13252C"}


def svg(body, w=S, h=S):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'fill="none">{body}</svg>')


def d_of(pts):
    return "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in pts) + " Z"


def f(pts, v, op=1.0, lift=0):
    """One facet. No stroke — ever.

    A stroke around a plane is a drawing of a plane; the plane itself is just
    the plane. `lift` throws a shadow behind this facet onto whatever sits
    under it — the way the references separate their sheets. Never a gradient.
    """
    o = f' opacity="{op}"' if op < 1 else ""
    sh = ""
    if lift:
        off = [(x + lift * 0.72, y + lift) for x, y in pts]
        sh = f'<path d="{d_of(off)}" fill="#000" opacity="0.42"/>'
    return sh + f'<path d="{d_of(pts)}" fill="{V.get(v, v)}"{o}/>'


def pt(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def ring_pts(cx, cy, r0, r1, a0, a1, n=48):
    """An annulus sector as a polygon, so a ring is made of planes too."""
    outer = [pt(cx, cy, r1, a0 + (a1 - a0) * i / n) for i in range(n + 1)]
    inner = [pt(cx, cy, r0, a1 - (a1 - a0) * i / n) for i in range(n + 1)]
    return outer + inner


FORMS = {}

# ══ ROUND TWO ═════════════════════════════════════════════════════════════
# Round one produced a pyramid, a pie chart and a torii — decor and clip art.
# Two things survived, and they are the two things the company actually is: a
# folded plane, and a cut that turns into pixels. Everything below pushes on
# those and abandons the rest.

# ── WING ──────────────────────────────────────────────────────────────────
# Two planes, one crease. Blade and wing at once, which is the whole company
# in the fewest marks it can be made from.
def wing(lift=0):
    return (f([(30, 176), (118, 14), (118, 138)], "hi", lift=lift) +
            f([(118, 14), (172, 116), (118, 138)], "shade", lift=lift) +
            f([(30, 176), (118, 138), (118, 166)], "deep"))
FORMS["a-wing"] = wing()
FORMS["a-wing-lift"] = wing(lift=7)

# ── WING, COMING APART ────────────────────────────────────────────────────
# The trailing edge stops being paper and becomes the medium we actually cut
# with. The blocks are part of the plane's own boundary, not a tail stuck on
# the back — that was the mistake in round one.
def wing_px(n=13):
    out = f([(30, 176), (118, 14), (118, 138)], "hi")
    out += f([(118, 14), (160, 92), (128, 132), (118, 138)], "shade")
    for i in range(n):
        t = i / (n - 1)
        s = 4 + 17 * t ** 1.8
        x = 122 + 44 * t ** 0.75
        y = 128 - 104 * t ** 1.05 + 8 * t
        out += f([(x, y), (x + s, y), (x + s, y + s), (x, y + s)],
                 "mid" if i % 3 else "shade", 1 - 0.5 * t ** 1.4)
    out += f([(30, 176), (118, 138), (118, 166)], "deep")
    return out
FORMS["b-wing-pixel"] = wing_px()

# ── SLIP ──────────────────────────────────────────────────────────────────
# A solid disc, cut, the smaller piece slid along the cut. Solid instead of
# stroked is a completely different weight, and it survives much further down.
def slip(r=76, cut=-32, gap=6.0, off=15.0, lift=0):
    dx = off * math.cos(math.radians(cut + 90))
    dy = off * math.sin(math.radians(cut + 90))
    g = gap / 2
    hx, hy = g * math.cos(math.radians(cut + 90)), g * math.sin(math.radians(cut + 90))
    top = [pt(C, C, r, cut + 180 * i / 40) for i in range(41)]
    bot = [pt(C - dx, C - dy, r, cut + 180 + 180 * i / 40) for i in range(41)]
    return (f([(x - hx, y - hy) for x, y in bot], "shade") +
            f([(x + hx, y + hy) for x, y in top], "lit", lift=lift))
FORMS["c-slip"] = slip()
FORMS["c-slip-lift"] = slip(lift=8)

# ── CHEVRON ───────────────────────────────────────────────────────────────
# The fold seen edge on. Two planes, one crease, nothing else — the absolute
# floor of what can still read as a folded object.
FORMS["d-chevron"] = (
    f([(22, 128), (100, 40), (100, 92), (52, 146)], "hi") +
    f([(100, 40), (178, 128), (148, 146), (100, 92)], "shade"))

# ── LIFT ──────────────────────────────────────────────────────────────────
# One sheet, one corner peeled off the surface. Depth from a single gesture
# and a single shadow. The most restrained thing in the set.
FORMS["e-lift"] = (
    '<path d="M 52 62 L 158 48 L 152 158 L 46 152 Z" fill="#000" opacity="0.38"/>' +
    f([(44, 54), (150, 40), (144, 150), (38, 144)], "shade") +
    f([(44, 54), (150, 40), (96, 96)], "lit") +
    f([(150, 40), (144, 150), (96, 96)], "hi"))

# ── SLIT ──────────────────────────────────────────────────────────────────
# The cut as light rather than as absence: a dark field opened once, and the
# halves have moved. Not a picture of a blade — the result of one.
FORMS["f-slit"] = (
    f([(30, 30), (170, 30), (170, 92), (30, 92)], "petrol") +
    f([(30, 108), (170, 108), (170, 170), (30, 170)], "petrol") +
    f([(30, 94), (170, 94), (170, 100), (30, 100)], "hot") +
    f([(46, 100), (186, 100), (186, 106), (46, 106)], "lit"))

# ── APERTURE ──────────────────────────────────────────────────────────────
# Three concentric arcs at stepped depths. Not a ring — something you move
# through, which is the brief for the entire site.
def aperture():
    out = ""
    for r0, r1, a0, a1, v in [(78, 92, 118, 402, "deep"),
                              (58, 72, 152, 424, "shade"),
                              (36, 50, 196, 452, "lit")]:
        out += f(ring_pts(C, C, r0, r1, a0, a1, 40), v)
    return out
FORMS["g-aperture"] = aperture()

# ── SHARD ─────────────────────────────────────────────────────────────────
# Three facets, every edge straight, nothing symmetrical. A struck flake
# rather than a folded sheet — the blade half of the name with none of the wing.
FORMS["h-shard"] = (
    f([(38, 152), (126, 20), (108, 120)], "lit") +
    f([(126, 20), (166, 150), (108, 120)], "shade") +
    f([(38, 152), (108, 120), (166, 150), (96, 182)], "deep"))


for name, body in FORMS.items():
    s = svg(body)
    open(f"{OUT}/{name}.svg", "w").write(s)
    for px, tag in ((800, ""), (64, "-64"), (32, "-32"), (16, "-16")):
        cairosvg.svg2png(bytestring=s.encode(), write_to=f"{OUT}/{name}{tag}.png",
                         output_width=px, output_height=px, background_color="#0A0A0B")
    print(name)
