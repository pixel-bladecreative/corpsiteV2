#!/usr/bin/env python3
"""Pixel dissolution — the Ninja's signature effect.

His garment edge is eaten away into blocks that GROW as they travel — fine, almost
sub-pixel detail right against the body, coarsening into big chunky low-res squares
further out. It reads as resolution loss rather than as confetti: he is not shedding
particles, he is losing definition.

The loose squares drift upward and outward as if lifted on a breeze from below.

Done procedurally rather than by generation: image models reliably render this
as an adjacent object beside the figure instead of a property of the garment.
In code the edge is genuinely chewed, the blocks are genuinely pieces of the
cloth they left, and the whole thing is deterministic and repeatable.

Usage:
  pixelate.py <in> <out> [options]

Options (fractions of image width/height unless noted):
  --edge left|right      side that dissolves            (default right)
  --x0 F                 inner edge of the dissolve band, on the figure
  --x1 F                 outer edge — full dissolution by here
  --drift F              how far loose blocks travel beyond x1
  --b0 N                 block size AT THE BODY, px at 2K (default 5)
  --b1 N                 block size AT THE OUTER EDGE     (default 46)
  --bk F                 how fast blocks coarsen          (default 1.6)
  --srcx F               column to copy clean background from
  --y0 F  --y1 F         vertical extent of the effect    (default whole frame)
  --gamma F              falloff curve; higher = tighter to the edge (default 2.2)
  --seed N
"""
import random, sys
from PIL import Image


def frac(args, key, default):
    return float(args[key]) if key in args else default


def main():
    a = sys.argv[1:]
    if len(a) < 2:
        sys.exit(__doc__)
    src, dst = a[0], a[1]
    args = {}
    i = 2
    while i < len(a):
        if a[i].startswith("--"):
            args[a[i][2:]] = a[i + 1]
            i += 2
        else:
            i += 1

    im = Image.open(src).convert("RGB")
    W, H = im.size
    px = im.load()
    out = im.copy()
    op = out.load()

    edge = args.get("edge", "right")
    SC = W / 2048.0
    b0 = max(2, int(float(args.get("b0", 5)) * SC))
    b1 = max(b0 + 2, int(float(args.get("b1", 46)) * SC))
    bk = frac(args, "bk", 1.6)
    x0, x1 = frac(args, "x0", .58), frac(args, "x1", .80)
    drift = frac(args, "drift", .14)
    srcx = frac(args, "srcx", .95)
    y0, y1 = frac(args, "y0", 0.0), frac(args, "y1", 1.0)
    gamma = frac(args, "gamma", 2.2)
    rng = random.Random(int(args.get("seed", 7)))

    X0, X1 = int(W * x0), int(W * x1)
    Y0, Y1 = int(H * y0), int(H * y1)
    DR = int(W * drift)
    SX = int(W * srcx)
    if edge == "left":
        X0, X1 = int(W * (1 - x0)), int(W * (1 - x1))
        SX = int(W * (1 - srcx))

    step = 1 if edge == "right" else -1
    span = abs(X1 - X0) or 1

    def t_at(x):
        return min(max(abs(x - X0) / span, 0.0), 1.0)

    def block_at(t):
        """Fine against the body, coarse further out. This is the whole effect."""
        return max(2, int(b0 + (b1 - b0) * (t ** bk)))

    def bg_patch(bx, by, B):
        """A clean block of background, copied from a column outside the figure."""
        sx = min(max(SX + (bx - X0) % max(B * 3, 1), 0), W - B)
        return im.crop((sx, by, sx + B, by + B))

    def block_colour(bx, by, B):
        r = g = b = n = 0
        st = max(1, B // 6)
        for y in range(by, min(by + B, H), st):
            for x in range(bx, min(bx + B, W), st):
                c = px[x, y]; r += c[0]; g += c[1]; b += c[2]; n += 1
        return (r // n, g // n, b // n) if n else (0, 0, 0)

    def put(bx, by, B, colour):
        for y in range(max(by, 0), min(by + B, H)):
            for x in range(max(bx, 0), min(bx + B, W)):
                op[x, y] = colour

    # Walk OUTWARD in columns, letting the block size grow as we go. The column
    # grid changes with it, which is what produces the mip-level cascade.
    loose = []
    bx = X0
    while (bx < X1 if step > 0 else bx > X1):
        t = t_at(bx)
        B = block_at(t)
        cx = bx if step > 0 else bx - B
        by = Y0
        while by < Y1:
            if rng.random() < t ** gamma:
                col = block_colour(cx, by, B)
                out.paste(bg_patch(cx, by, B), (cx, by))
                if rng.random() < 0.55:
                    loose.append((cx, by, col))
            by += B
        bx += B * step

    # Loose squares drift up and outward. A block is redrawn at the size of WHERE
    # IT LANDS, not where it came from — so travelling further coarsens it.
    for bx, by, col in loose:
        d = rng.random() ** 1.6
        nx = bx + step * int(DR * d * (0.35 + t_at(bx)))
        ny = by - int(H * 0.30 * d * (0.4 + rng.random()))
        if rng.random() < 0.85 - 0.55 * d:
            put(nx, ny, block_at(t_at(nx)), col)

    # A sparse tail further out — the coarsest blocks in the image.
    pal = [c for _, _, c in loose] or [(200, 200, 200)]
    for _ in range(int(len(loose) * 0.35)):
        d = rng.random()
        nx = X1 + step * int(DR * (0.2 + d))
        ny = rng.randint(Y0 - int(H * .18), Y1)
        if rng.random() < 0.30 * (1 - d):
            put(nx + rng.randint(-b1, b1), ny, block_at(1.0), rng.choice(pal))

    out.save(dst)
    print(f"pixelated -> {dst}  block={B}px  loose={len(loose)}")


main()
