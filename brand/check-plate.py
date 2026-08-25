#!/usr/bin/env python3
"""Pixel Blade image QA — enforces the `lit world` rule.

The ceiling is COVERAGE, not chroma. Peak saturation is unbounded; what is
bounded is how much of the frame carries it, and how much dark ground remains.

Also checks the feather: an image's edge value must resolve to the page ground
(--pb-sumi #0A0A0B) or the vignette reveals itself as a seam.

Usage: check-plate.py <image> [<image> ...]
"""
import colorsys, sys, warnings
from PIL import Image

warnings.filterwarnings("ignore", category=DeprecationWarning)

GROUND = (0x0A, 0x0A, 0x0B)
MAX_CHROMA_COVERAGE = 25.0   # % of frame at sat>.35, val>.30
MIN_DARK_GROUND     = 50.0   # % of frame at val<.18
MAX_EDGE_DELTA      = 12     # per-channel distance from GROUND at the corners


def measure(path):
    im = Image.open(path).convert("RGB")
    W, H = im.size
    small = im.copy(); small.thumbnail((260, 260))
    px = list(small.getdata()); n = len(px)

    chroma = dark = 0; peak = 0.0
    for r, g, b in px:
        _, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        if s > .35 and v > .30:
            chroma += 1
            peak = max(peak, s)
        if v < .18:
            dark += 1

    k = max(6, W // 40)
    boxes = [(0, 0, k, k), (W - k, 0, W, k), (0, H - k, k, H), (W - k, H - k, W, H)]
    vals = []
    for box in boxes:
        cp = list(im.crop(box).getdata()); m = len(cp)
        vals.append(tuple(sum(p[i] for p in cp) // m for i in range(3)))
    edge = tuple(sum(v[i] for v in vals) // 4 for i in range(3))
    delta = max(abs(edge[i] - GROUND[i]) for i in range(3))

    return {
        "chroma": 100 * chroma / n,
        "dark": 100 * dark / n,
        "peak": 100 * peak,
        "edge": "#%02X%02X%02X" % edge,
        "delta": delta,
    }


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    fail = False
    print(f"{'plate':26s} {'chroma':>8} {'dark':>7} {'peak':>6} {'edge':>9} {'d':>4}  verdict")
    for path in sys.argv[1:]:
        m = measure(path)
        notes = []
        if m["chroma"] > MAX_CHROMA_COVERAGE:
            notes.append(f"chroma coverage {m['chroma']:.0f}% > {MAX_CHROMA_COVERAGE:.0f}%")
        if m["dark"] < MIN_DARK_GROUND:
            notes.append(f"dark ground {m['dark']:.0f}% < {MIN_DARK_GROUND:.0f}%")
        if m["delta"] > MAX_EDGE_DELTA:
            notes.append(f"edge seam — needs a vignette to reach {'#%02X%02X%02X' % GROUND}")
        verdict = "PASS" if not notes else "; ".join(notes)
        if notes:
            fail = True
        name = path.rsplit("/", 1)[-1]
        print(f"{name:26s} {m['chroma']:7.1f}% {m['dark']:6.1f}% {m['peak']:5.0f} "
              f"{m['edge']:>9} {m['delta']:4d}  {verdict}")
    print("\nPeak saturation is NOT a failure condition — chroma is unbounded by design.")
    sys.exit(1 if fail else 0)


main()
