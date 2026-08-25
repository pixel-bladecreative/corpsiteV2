#!/usr/bin/env python3
"""Pixel dissolution — the Ninja's signature effect.

His garment edge is eaten away into 16-bit blocks, and the loose squares drift
upward and outward as if lifted on a breeze from below.

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
  --block N              block size in pixels at 2K       (default 26)
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
    B = int(args.get("block", 26)) * W // 2048 or 8
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
    span = abs(X1 - X0)

    def bg_patch(bx, by):
        """A clean block of background, copied from a column outside the figure."""
        sx = min(max(SX + (bx - X0) % (B * 3), 0), W - B)
        return im.crop((sx, by, sx + B, by + B))

    def block_colour(bx, by):
        r = g = b = n = 0
        for y in range(by, min(by + B, H), 3):
            for x in range(bx, min(bx + B, W), 3):
                c = px[x, y]; r += c[0]; g += c[1]; b += c[2]; n += 1
        return (r // n, g // n, b // n) if n else (0, 0, 0)

    def put(bx, by, colour):
        for y in range(by, min(by + B, H)):
            for x in range(max(bx, 0), min(bx + B, W)):
                op[x, y] = colour

    loose = []
    by = Y0
    while by < Y1:
        bx = X0
        while (bx < X1 if step > 0 else bx > X1):
            t = abs(bx - X0) / span if span else 1.0          # 0 at body, 1 at outer
            if rng.random() < t ** gamma:
                col = block_colour(bx, by)
                # eat the block out of the garment
                out.paste(bg_patch(bx, by), (bx, by))
                # some of what came loose is still in flight
                if rng.random() < 0.55:
                    loose.append((bx, by, col, t))
            bx += B * step
        by += B

    # loose squares drift up and outward, thinning as they go
    for bx, by, col, t in loose:
        d = rng.random() ** 1.6
        nx = bx + step * int(DR * d * (0.35 + t))
        ny = by - int(H * 0.30 * d * (0.4 + rng.random()))
        if rng.random() < 0.85 - 0.55 * d:
            put(nx, ny, col)

    # a sparse scatter further out, so the falloff has a tail
    pal = [c for _, _, c, _ in loose] or [(200, 200, 200)]
    for _ in range(int(len(loose) * 0.5)):
        d = rng.random()
        nx = X1 + step * int(DR * (0.2 + d))
        ny = rng.randint(Y0 - int(H * .18), Y1)
        if rng.random() < 0.30 * (1 - d):
            put(nx + rng.randint(-B, B), ny, rng.choice(pal))

    out.save(dst)
    print(f"pixelated -> {dst}  block={B}px  loose={len(loose)}")


main()
