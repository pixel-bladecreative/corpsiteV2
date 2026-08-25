#!/usr/bin/env python3
"""Feather an image's edges down to the Pixel Blade page ground.

The boundary between the lit world and the room is a falloff, never a line.
This resolves an image's border to --pb-sumi (#0A0A0B) so it emerges from the
dark instead of being cut into it.

Usage: feather.py <in> <out> [inset]
  inset — fraction of the short edge over which the falloff runs (default .22)
"""
import sys, warnings
from PIL import Image, ImageDraw, ImageFilter

warnings.filterwarnings("ignore", category=DeprecationWarning)
GROUND = (0x0A, 0x0A, 0x0B)


def feather(src, dst, inset=0.22):
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

    ground = Image.new("RGB", (W, H), GROUND)
    Image.composite(im, ground, mask).save(dst)
    return dst


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    inset = float(sys.argv[3]) if len(sys.argv) > 3 else 0.22
    print("feathered ->", feather(sys.argv[1], sys.argv[2], inset))


main()
