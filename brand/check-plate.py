#!/usr/bin/env python3
"""Pixel Blade image QA — enforces the `lit world` rule in either mode.

The ceiling is COVERAGE, not chroma. Peak saturation is unbounded; what is
bounded is how much of the frame carries it, and how much GROUND remains.

Also checks the feather: an image's edge value must resolve to the page ground
of its mode, or the vignette reveals itself as a seam.

Usage: check-plate.py [--day] <image> [<image> ...]
  default   night mode — ground #0A0A0B, requires >=50% dark
  --day     day mode   — ground #F4F5F2, requires >=50% light

A Warrior plate is checked in whichever mode it is destined for; the figure's
own value ramp carries him on both, so the mode is a placement decision.
"""
import colorsys, sys, warnings
from PIL import Image

warnings.filterwarnings("ignore", category=DeprecationWarning)

NIGHT_GROUND = (0x0A, 0x0A, 0x0B)
DAY_GROUND   = (0xF4, 0xF5, 0xF2)
MAX_CHROMA_COVERAGE = 25.0   # % of frame at sat>.35, val>.30
MIN_GROUND          = 50.0   # % of frame at the mode's ground end of the ramp
MAX_EDGE_DELTA      = 12     # per-channel distance from GROUND at the corners


def measure(path, day=False):
    im = Image.open(path).convert("RGB")
    W, H = im.size
    small = im.copy(); small.thumbnail((260, 260))
    px = list(small.getdata()); n = len(px)

    ground_rgb = DAY_GROUND if day else NIGHT_GROUND
    chroma = ground = 0; peak = 0.0
    for r, g, b in px:
        _, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        if s > .35 and v > .30:
            chroma += 1
            peak = max(peak, s)
        # "ground" is the quiet end of the value ramp for this mode
        if (v > .88 and s < .12) if day else (v < .18):
            ground += 1

    k = max(6, W // 40)
    boxes = [(0, 0, k, k), (W - k, 0, W, k), (0, H - k, k, H), (W - k, H - k, W, H)]
    vals = []
    for box in boxes:
        cp = list(im.crop(box).getdata()); m = len(cp)
        vals.append(tuple(sum(p[i] for p in cp) // m for i in range(3)))
    edge = tuple(sum(v[i] for v in vals) // 4 for i in range(3))
    delta = max(abs(edge[i] - ground_rgb[i]) for i in range(3))

    return {
        "chroma": 100 * chroma / n,
        "ground": 100 * ground / n,
        "peak": 100 * peak,
        "edge": "#%02X%02X%02X" % edge,
        "delta": delta,
    }


def main():
    args = [a for a in sys.argv[1:] if a != "--day"]
    day = "--day" in sys.argv
    if not args:
        sys.exit(__doc__)
    ground_rgb = DAY_GROUND if day else NIGHT_GROUND
    fail = False
    label = "light" if day else "dark"
    print(f"mode: {'DAY' if day else 'NIGHT'}  ground {'#%02X%02X%02X' % ground_rgb}\n")
    print(f"{'plate':26s} {'chroma':>8} {label:>7} {'peak':>6} {'edge':>9} {'d':>4}  verdict")
    for path in args:
        m = measure(path, day)
        notes = []
        if m["chroma"] > MAX_CHROMA_COVERAGE:
            notes.append(f"chroma coverage {m['chroma']:.0f}% > {MAX_CHROMA_COVERAGE:.0f}%")
        if m["ground"] < MIN_GROUND:
            notes.append(f"{label} ground {m['ground']:.0f}% < {MIN_GROUND:.0f}%")
        if m["delta"] > MAX_EDGE_DELTA:
            notes.append(f"edge seam — needs a vignette to reach {'#%02X%02X%02X' % ground_rgb}")
        verdict = "PASS" if not notes else "; ".join(notes)
        if notes:
            fail = True
        name = path.rsplit("/", 1)[-1]
        print(f"{name:26s} {m['chroma']:7.1f}% {m['ground']:6.1f}% {m['peak']:5.0f} "
              f"{m['edge']:>9} {m['delta']:4d}  {verdict}")
    print("\nPeak saturation is NOT a failure condition — chroma is unbounded by design.")
    sys.exit(1 if fail else 0)


main()
