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
    for px, tag in ((800, ""), (64, "-64"), (16, "-16")):
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
