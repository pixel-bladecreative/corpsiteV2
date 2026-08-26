#!/usr/bin/env python3
"""THE KERF — the Pixel Blade mark.

A kerf is the material a blade removes as it passes. That is the whole mark: a
solid disc, cut once, the lower piece slid along the cut, and in the gap the
material the blade took — as pixels, coarsening and scattering as it leaves.

    Blades are no longer steel. Pixels.

Everything before this was drawn with outlines, and outlines were the mistake.
Every reference Spencer supplied builds form the opposite way: adjacent planes
at different values, and the edge is simply where two values meet. There is not
one stroke in this file.

Why this and not the others: it is solid, so it has weight; it is asymmetric,
so it has a direction of travel; it is not a picture of anything, so it cannot
date and cannot be read as decor; and it survives to 16px, where the kerf drops
out and leaves a cut disc — the same two-density system, earned rather than
imposed.
"""
import math, os, cairosvg

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mark")
os.makedirs(OUT, exist_ok=True)
S, C = 200, 100

# Two values for the two pieces, one for the kerf. The slid piece is the raised
# one, so it is the lighter one — that is the only reason it is lighter.
NIGHT = {"static": "#9A7E67", "slid": "#EBA564", "grit": "#C98B52",
         "grit2": "#9A7E67", "ground": "#0A0A0B"}
DAY = {"static": "#7B4933", "slid": "#5E321F", "grit": "#7B4933",
       "grit2": "#9A5C42", "ground": "#F4F5F2"}

CUT, SPLIT, GAP, OFF, R = -28, 0.46, 5.0, 15.0, 78.0


def d_of(p):
    return "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in p) + " Z"


def face(p, fill, op=1.0, lift=0.0):
    o = f' opacity="{op:.3f}"' if op < 1 else ""
    sh = ""
    if lift:
        off = [(x + lift * 0.72, y + lift) for x, y in p]
        sh = f'<path d="{d_of(off)}" fill="#000" opacity="0.42"/>'
    return sh + f'<path d="{d_of(p)}" fill="{fill}"{o}/>'


def pt(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def pieces(r=R, cut=CUT, split=SPLIT, gap=GAP, off=OFF):
    """The two halves, the second slid ALONG the cut.

    Along, not across. Sliding across just separates them and reads as an
    eclipse; sliding along leaves a notch at one end and an overhang at the
    other, which is what a cut piece of material actually does.
    """
    sweep, n = 360 * split, 64
    mi = [pt(C, C, r, cut + sweep * i / n) for i in range(n + 1)]
    ma = [pt(C, C, r, cut + sweep + (360 - sweep) * i / n) for i in range(n + 1)]
    p0, p1 = pt(C, C, r, cut), pt(C, C, r, cut + sweep)
    ax = math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0]))
    dx, dy = off * math.cos(math.radians(ax)), off * math.sin(math.radians(ax))
    g = gap / 2
    hx, hy = g * math.cos(math.radians(ax + 90)), g * math.sin(math.radians(ax + 90))
    return ([(x + dx - hx, y + dy - hy) for x, y in mi],
            [(x + hx, y + hy) for x, y in ma], p0, p1)


def kerf(p0, p1, pal, n=17, lo=2.2, hi=16.0, push=4.0, over=1.24):
    """The material the blade took.

    Fine and tight where the cut is still closed, coarsening and scattering as
    it opens and leaves the silhouette. Run the other way it reads as the cut
    healing over, which is the opposite of the point.
    """
    L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    ux, uy = (p0[0] - p1[0]) / L, (p0[1] - p1[1]) / L      # enters at p1
    nx, ny = -uy, ux
    out = ""
    for i in range(n):
        t = i / (n - 1)
        s = lo + (hi - lo) * t ** 2.3
        d = L * (0.05 + over * t ** 0.94)
        k = push * (t ** 1.7) * (1 if i % 2 else -0.62)
        x, y = p1[0] + ux * d + nx * k - s / 2, p1[1] + uy * d + ny * k - s / 2
        out += face([(x, y), (x + s, y), (x + s, y + s), (x, y + s)],
                    pal["grit"] if i % 3 else pal["grit2"], 1 - 0.40 * t ** 1.7)
    return out


def mark(pal, lift=0.0, grit=True, **kw):
    mi, ma, p0, p1 = pieces(**kw)
    body = face(ma, pal["static"]) + face(mi, pal["slid"], lift=lift)
    if grit:
        body += kerf(p0, p1, pal)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" '
            f'fill="none">{body}</svg>')


def lockup(pal, w=780, h=200):
    inner = mark(pal, lift=0).split(">", 1)[1].rsplit("</svg>", 1)[0]
    ink = pal["slid"] if pal is NIGHT else pal["static"]
    word = "#E8E3D6" if pal is NIGHT else "#13252C"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" fill="none">'
            f'<g transform="translate(4,0)">{inner}</g>'
            f'<text x="246" y="112" font-family="Archivo, Helvetica, Arial, sans-serif" '
            f'font-size="46" font-weight="300" letter-spacing="15" fill="{word}">PIXEL BLADE</text>'
            f'<text x="250" y="146" font-family="JetBrains Mono, monospace" font-size="15" '
            f'letter-spacing="7" fill="{ink}" opacity="0.85">ADVERTISING</text></svg>')


BUILD = {
    "kerf":        (NIGHT, dict(lift=0)),
    "kerf-lift":   (NIGHT, dict(lift=8)),      # the dimensional presentation
    "kerf-quiet":  (NIGHT, dict(lift=0, grit=False)),   # below ~24px the grit is noise
    "kerf-day":    (DAY,   dict(lift=0)),
    "kerf-day-lift": (DAY, dict(lift=8)),
    "kerf-day-quiet": (DAY, dict(lift=0, grit=False)),
}

for name, (pal, kw) in BUILD.items():
    s = mark(pal, **kw)
    open(f"{OUT}/{name}.svg", "w").write(s)
    for px, tag in ((1000, ""), (64, "-64"), (32, "-32"), (16, "-16")):
        cairosvg.svg2png(bytestring=s.encode(), write_to=f"{OUT}/{name}{tag}.png",
                         output_width=px, output_height=px,
                         background_color=pal["ground"])
    print(name)

for nm, pal in (("lockup", NIGHT), ("lockup-day", DAY)):
    s = lockup(pal)
    open(f"{OUT}/{nm}.svg", "w").write(s)
    cairosvg.svg2png(bytestring=s.encode(), write_to=f"{OUT}/{nm}.png",
                     output_width=1560, background_color=pal["ground"])
    print(nm)
