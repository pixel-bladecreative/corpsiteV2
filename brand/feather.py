#!/usr/bin/env python3
"""Feather an image's edges down to the Pixel Blade page ground.

The boundary between the lit world and the room is a falloff, never a line.
This resolves an image's border to --pb-sumi (#0A0A0B) so it emerges from the
dark instead of being cut into it.

Usage: feather.py [--day] <in> <out> [inset]
  inset — fraction of the short edge over which the falloff runs (default .22)
"""
import sys, warnings
from PIL import Image, ImageDraw, ImageFilter

warnings.filterwarnings("ignore", category=DeprecationWarning)
NIGHT_GROUND = (0x0A, 0x0A, 0x0B)
DAY_GROUND = (0xF4, 0xF5, 0xF2)


def feather(src, dst, inset=0.22, day=False):
    im = Image.open(src).convert("RGB")
    W, H = im.size
    pad = int(min(W, H) * inset)

    # A hard white core inset from every edge, blurred into a soft ramp. The
    # blur radius sets how gradual the falloff is; the inset sets where it
    # starts. Corners fall off on both axes at once, which is what kills a
    # cropped bright element at the frame edge.
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).rectangle([pad, pad, W - pad, H - pad], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(pad * 0.55))

    ground = Image.new("RGB", (W, H), DAY_GROUND if day else NIGHT_GROUND)
    Image.composite(im, ground, mask).save(dst)
    return dst


def main():
    args = [a for a in sys.argv[1:] if a != "--day"]
    day = "--day" in sys.argv
    if len(args) < 2:
        sys.exit(__doc__)
    inset = float(args[2]) if len(args) > 2 else 0.22
    print("feathered ->", feather(args[0], args[1], inset, day))


main()
