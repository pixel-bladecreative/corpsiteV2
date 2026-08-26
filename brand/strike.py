#!/usr/bin/env python3
"""Strike a flat mark into a real material.

The mark we argued down to bare geometry is not the artwork — it is the DIE.
This takes that geometry and presses it into something: foil onto construction
paper, relief into a bronze coin, a blind deboss into cotton stock. Everything
here is lit by ONE raking light from the upper left, because two sources is a
bug (brand/tokens.css). Specular is near-white, never gold, and narrow.

    strike.py <mode> <mark.svg> <out.png> [--plate FILE] [options]

Modes
    foil      metal leaf stamped onto the plate — raised, hot, reflective
    deboss    pressed IN, no ink at all. The plate's own material, revealed
              only by the way light falls into the impression.
    emboss    pushed OUT from behind. Same material, opposite shadow.
    coin      struck relief on a bronze disc, laid on the plate with contact
              shadow and a little bounce.

Options
    --px N          render size, default 2048
    --bevel F       how far the edge ramps before the face goes flat (0.02)
    --depth F       relief height, drives how hard the light breaks (1.0)
    --rot D         rotate the light off the house angle, for a variant sheet
    --inset F       fraction of frame the mark occupies (0.62)
    --rim           coin only: add a raised rim
"""
import argparse, io, os, re, sys
import numpy as np
from PIL import Image, ImageFilter
import cairosvg

# ── the house light ───────────────────────────────────────────────────────
# Upper left, low. In array space row 0 is the top, so "up" is -y.
LIGHT_DEG = 214.0        # measured clockwise from +x, matching SVG convention
LIGHT_Z = 0.34           # lower = more raking, longer shadows in the relief
AMBIENT = 0.15

# ── ramps, straight out of tokens.css ─────────────────────────────────────
# Every stop is a token. Nothing here is a colour I picked by eye.
# The dark run is LONG on purpose. Metal spends most of its surface in shadow
# and earns its colour in a narrow band; a ramp weighted toward the mid tone
# renders as orange plastic, which is exactly what the first pass did.
BRONZE = [(0.00, (0x06, 0x07, 0x06)),   # graphite-void
          (0.24, (0x3F, 0x39, 0x37)),   # graphite
          (0.50, (0x9A, 0x7E, 0x67)),   # bronze-shade
          (0.76, (0xE5, 0x9E, 0x5D)),   # bronze
          (0.92, (0xEB, 0xA5, 0x64)),   # bronze-hi
          (1.00, (0xFE, 0xFE, 0xF5))]   # edge — near-white, NOT gold
OXIDE  = [(0.00, (0x2A, 0x16, 0x0D)),
          (0.35, (0x5E, 0x32, 0x1F)),   # day accent
          (0.70, (0x7B, 0x49, 0x33)),   # rust
          (1.00, (0xE8, 0xE3, 0xD6))]   # washi
STEEL  = [(0.00, (0x13, 0x25, 0x2C)),   # petrol-deep
          (0.40, (0x3F, 0x39, 0x37)),   # graphite
          (0.75, (0x81, 0x7C, 0x7A)),   # graphite-lit
          (1.00, (0xFE, 0xFE, 0xF5))]
RAMPS = {"bronze": BRONZE, "oxide": OXIDE, "steel": STEEL}


def ramp(t, stops):
    """Map 0..1 through a colour ramp. t is an array; returns H×W×3 float."""
    ts = np.array([s[0] for s in stops])
    cs = np.array([s[1] for s in stops], dtype=float)
    out = np.empty(t.shape + (3,), dtype=float)
    for c in range(3):
        out[..., c] = np.interp(t, ts, cs[:, c])
    return out


# ── geometry in, height field out ─────────────────────────────────────────
CREASE_RE = re.compile(r'<path[^>]*stroke="#0A0A0B"[^>]*/>')


def split_svg(path):
    """Separate the mark's body from its crease.

    The crease is drawn in the page ground so it reads as a fold on a flat
    page. In relief it must be a GROOVE cut into the face, not a hole through
    it — so it gets pulled out here and subtracted from the height later.
    """
    s = open(path).read()
    creases = CREASE_RE.findall(s)
    body = CREASE_RE.sub("", s)
    body = re.sub(r'(stroke|fill)="#[0-9A-Fa-f]{6}"', r'\1="#FFFFFF"', body)
    if not creases:
        return body, None
    head = s[:s.index(">") + 1]
    crease = head + "".join(c.replace("#0A0A0B", "#FFFFFF") for c in creases) + "</svg>"
    return body, crease


def alpha_of(svg_text, px):
    buf = cairosvg.svg2png(bytestring=svg_text.encode(), output_width=px,
                           output_height=px)
    im = Image.open(io.BytesIO(buf)).convert("RGBA")
    return np.asarray(im, dtype=float)[..., 3] / 255.0


def box1d(a, r, axis):
    """Moving average via cumulative sum. O(n) regardless of radius."""
    if r < 1:
        return a
    a = np.swapaxes(a, 0, axis)
    pad = np.pad(a, ((r + 1, r),) + ((0, 0),) * (a.ndim - 1), mode="edge")
    c = np.cumsum(pad, axis=0)
    out = (c[2 * r + 1:] - c[:-(2 * r + 1)]) / (2 * r + 1)
    return np.swapaxes(out, 0, axis)


def gblur(a, sigma, ax=None):
    """Gaussian in FLOAT, as three box passes.

    PIL will only blur 8-bit here, and round-tripping the height field through
    uint8 quantises it — a quantised height field differentiates into visible
    concentric rings, which is exactly what made the first coin look like a
    cheap render. Three boxes of width sqrt(4s^2+1) match a Gaussian closely
    enough for a normal map and cost nothing.
    """
    if sigma < 0.4:
        return a.astype(float)
    r = max(1, int(round((np.sqrt(4 * sigma * sigma + 1) - 1) / 2)))
    out = a.astype(float)
    axes = (0, 1) if ax is None else (ax,)
    for _ in range(3):
        for x in axes:
            out = box1d(out, r, x)
    return out


def height_field(a, bevel, px):
    """Blur, then push the interior back to full.

    A struck face is FLAT with a bevel only at the rim. A plain blur gives a
    dome, which reads as plastic. Clipping the blurred field above 1 and
    re-normalising is what keeps the plateau flat and confines the ramp to the
    edge — that is the whole difference between stamped metal and a gel button.
    """
    return np.clip(gblur(a, max(0.6, bevel * px)) * 2.9, 0, 1)


def light_vec(rot=0.0):
    a = np.radians(LIGHT_DEG + rot)
    L = np.array([np.cos(a), np.sin(a), LIGHT_Z])
    return L / np.linalg.norm(L)


def sheen(px, rot=0.0, span=0.42):
    """The broad falloff across a flat face.

    A plateau has a constant normal, so pure directional diffuse renders it as
    one flat colour — which is what made the first pass look like plastic. Real
    metal on a table is lit by a big soft source and reads as a GRADIENT across
    the face, brightest toward the light. This is that gradient.
    """
    L = light_vec(rot)
    y, x = np.mgrid[0:px, 0:px].astype(float) / px - 0.5
    t = -(x * L[0] + y * L[1]) / 0.72
    return np.clip(0.5 + t * span, 0.05, 1.0)


def grain(px, rot=0.0, amt=0.05, seed=7):
    """Unidirectional brush, running along the light. Anisotropy is most of
    what separates brushed metal from a gradient."""
    rng = np.random.default_rng(seed)
    n = rng.standard_normal((px, px))
    # long across, short down: the streaks run one way and one way only
    n = gblur(n, px * 0.009, ax=1)
    n = gblur(n, px * 0.0009, ax=0)
    n /= max(n.std(), 1e-6)
    return 1.0 + n * amt


def shade(h, depth, rot=0.0, shine=44.0):
    """One directional light on a height field. Returns diffuse, specular, cavity."""
    gy, gx = np.gradient(h * depth * 40.0)
    nz = np.ones_like(h)
    n = np.stack([-gx, -gy, nz], -1)
    n /= np.linalg.norm(n, axis=-1, keepdims=True)

    L = light_vec(rot)
    diff = np.clip(n @ L, 0, 1)

    H = L + np.array([0, 0, 1.0])
    H /= np.linalg.norm(H)
    spec = np.clip(n @ H, 0, 1) ** shine

    # cavity: darken where the surface sits below its own neighbourhood
    wide = gblur(h, h.shape[0] * 0.02)
    cav = np.clip(1.0 - (wide - h) * 2.2, 0.35, 1.0)
    return diff, spec, cav


def occlude(relief, px, r=0.009, k=1.15):
    """Darken the field where it sits in the shadow of raised metal.

    A directional light alone cannot render relief: the flat top of a raised
    shape and the flat field around it share the same normal, so they shade
    identically and the mark vanishes into the face. What actually makes relief
    read is occlusion in the field beside it, plus a small lift because the
    raised face is nearer the source. Both are faked here, deliberately.
    """
    return np.clip(1.0 - (gblur(relief, px * r) - relief) * k, 0.30, 1.0)


# ── plates ────────────────────────────────────────────────────────────────
def load_plate(path, px, fallback=(0x1A, 0x1A, 0x1A)):
    if path and os.path.exists(path):
        im = Image.open(path).convert("RGB")
        s = min(im.size)
        im = im.crop(((im.width - s) // 2, (im.height - s) // 2,
                      (im.width + s) // 2, (im.height + s) // 2)).resize((px, px), Image.LANCZOS)
        return np.asarray(im, dtype=float)
    g = np.zeros((px, px, 3), dtype=float)
    g[:] = fallback
    return g


def place(arr, px, inset):
    """Drop a px-square field into the frame at the requested coverage."""
    w = int(px * inset)
    im = Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8))
    im = im.resize((w, w), Image.LANCZOS)
    out = np.zeros((px, px), dtype=float)
    o = (px - w) // 2
    out[o:o + w, o:o + w] = np.asarray(im, dtype=float) / 255.0
    return out


def soft(a, r):
    return gblur(np.clip(a, 0, 1), r)


def offset(a, dx, dy):
    return np.roll(np.roll(a, dy, axis=0), dx, axis=1)


# ══ MODES ═════════════════════════════════════════════════════════════════
def mode_foil(h, crease, plate, args):
    """Metal leaf stamped onto the plate. Sits on top, catches the light hard."""
    diff, spec, cav = shade(h, args.depth, args.rot, shine=args.shine)
    lit = AMBIENT + diff * 0.46 + sheen(args.px, args.rot, 0.36) * 0.30 + h * 0.16
    lit *= cav * occlude(h, args.px) * grain(args.px, args.rot, args.grain)
    lit = np.clip(lit - crease * 0.18, 0, 1)             # the fold, incised
    metal = ramp(lit, RAMPS[args.ramp])
    metal = np.clip(metal + spec[..., None] * 255.0 * args.spec, 0, 255)

    m = (h > 0.02).astype(float)
    # foil is not perfectly opaque — the sheet's tooth prints through it
    tooth = plate.mean(-1, keepdims=True) / 255.0
    metal = metal * (0.86 + 0.14 * (tooth / max(tooth.mean(), 1e-6)))

    drop = soft(offset(m, int(args.px * .006), int(args.px * .008)), args.px * .010)
    out = plate * (1 - drop[..., None] * 0.55)
    return out * (1 - m[..., None]) + metal * m[..., None]


def mode_deboss(h, crease, plate, args, up=False):
    """Pressed in, no ink. The plate's own material, revealed only by light.

    This is the quietest thing in the system and probably the most expensive
    looking. Nothing is added — a shape is simply pushed below the surface, and
    the raking light does the rest.
    """
    sgn = 1.0 if up else -1.0
    diff, spec, cav = shade(h * sgn, args.depth * 1.25, args.rot, shine=18.0)
    base = np.clip(AMBIENT + diff * 0.95, 0, 1) * cav
    base = np.clip(base - crease * sgn * 0.30, 0, 1)
    edge = (h > 0.02) & (h < 0.985)
    # the fibre compresses at the shoulder and goes very slightly darker
    shoulder = soft(edge.astype(float), args.px * 0.004)
    out = plate * (0.52 + 0.95 * base)[..., None]
    out *= (1 - shoulder[..., None] * 0.10)
    return np.clip(out + spec[..., None] * 40.0, 0, 255)


def mode_coin(h, crease, plate, args):
    """Relief struck on a disc, laid on the plate.

    Three things have to be true at once or it reads as a render: the face has
    a broad sheen across it, the brush runs one way, and the specular is a NARROW
    near-white line rather than a wide white blob. The last one is the brand's
    own rule — one hot pixel, not gold.
    """
    px = args.px
    y, x = np.mgrid[0:px, 0:px].astype(float)
    r = np.hypot(x - px / 2, y - px / 2) / (px / 2)

    disc = np.clip((args.face - r) * px * 0.09, 0, 1)     # hard edge, tiny AA
    edge_ramp = np.clip((args.face - r) * 26, 0, 1)       # the chamfer at the rim
    field = edge_ramp * 0.30
    if args.rim:
        band = np.clip(1 - np.abs(r - (args.face - 0.045)) * 44, 0, 1) * disc
        field = np.clip(field + band * 0.30, 0, 1)
    field = np.clip(field + h * disc * 0.62, 0, 1.4)

    relief = h * disc
    diff, spec, cav = shade(field, args.depth, args.rot, shine=args.shine)
    lit = AMBIENT + diff * 0.46 + sheen(px, args.rot) * 0.30 + relief * 0.15
    lit *= cav * occlude(relief, px) * grain(px, args.rot, args.grain)
    lit = np.clip(lit - crease * disc * 0.16, 0, 1)
    metal = ramp(lit, RAMPS[args.ramp])
    metal = np.clip(metal + spec[..., None] * 255.0 * args.spec, 0, 255)

    m = np.clip(disc, 0, 1)
    d = int(px * 0.013)
    cast = soft(offset(m, d, int(d * 1.4)), px * 0.026) * 0.80
    contact = soft(m, px * 0.005) * 0.55                 # the tight dark line at the base
    out = plate * (1 - np.clip(cast + contact, 0, 0.94))[..., None]
    # a little of the metal bounces back into the stone
    out += ramp(np.full((px, px), 0.55), RAMPS[args.ramp]) * (soft(m, px * 0.05) * 0.09)[..., None]
    return np.clip(out * (1 - m[..., None]) + metal * m[..., None], 0, 255)


# ── layered paper ─────────────────────────────────────────────────────────
MASK_RE = re.compile(r"<mask\b.*?</mask>", re.S)
DRAW_RE = re.compile(r"<(?:path|circle|rect)\b[^>]*/>")


def layer_svgs(path):
    """One SVG per drawable, in draw order.

    The marks are already written back to front — ring first, then the bird —
    so element order IS depth order and nothing needs annotating. Anything
    inside a <mask> is held aside: it is machinery, not a plane.
    """
    s = open(path).read()
    masks = MASK_RE.findall(s)
    body = MASK_RE.sub("@@MASK@@", s)
    hits = list(DRAW_RE.finditer(body))
    out = []
    for i in range(len(hits)):
        v = body
        for j, m in reversed(list(enumerate(hits))):
            if j != i:
                v = v[:m.start()] + m.group().replace("/>", ' opacity="0"/>') + v[m.end():]
        for mk in masks:
            v = v.replace("@@MASK@@", mk, 1)
        v = re.sub(r'(stroke|fill)="#[0-9A-Fa-f]{6}"', r'\1="#FFFFFF"', v)
        out.append(v)
    return out


def edge_of(a, px, r=0.0035):
    """The cut edge of a sheet, which catches light the face does not."""
    return np.clip(a - gblur(a, px * r), 0, 1)


def mode_papercut(h, crease, plate, args):
    """Every part of the mark as its own sheet, at its own depth.

    This is the mechanic in three of the five references, and it is the one
    that most directly answers "we are digital, not flat": nothing is drawn in
    a colour — shapes are CUT, stacked, and separated by the shadows they throw
    on each other. Depth comes from the light, not from a gradient.
    """
    px = args.px
    ground = np.zeros((px, px, 3)) + (DAY if args.day else NIGHT)
    out = ground.copy()

    if args.sun:                                          # the disc at the back
        # Sized by the ceiling, not by taste: check-plate.py fails a night
        # plate over 25% chroma coverage, and a disc this saturated eats that
        # budget fast. r=0.60 lands near 21% once the sheets cover part of it.
        d = disc_mask(px, args.sun, 0.004)
        d = np.roll(np.roll(d, int(-px * .05), 0), int(px * .04), 1)
        sun = np.zeros((px, px, 3)) + (0xCD, 0x79, 0x5C) if args.day else \
              np.zeros((px, px, 3)) + (0xF2, 0x76, 0x56)
        out = out * (1 - d[..., None]) + sun * d[..., None]

    sheets = layer_svgs(args.svg)
    # Night: white sheets on sumi. Day: petrol sheets on paper — the day-panel
    # token. Graphite sheets on white went muddy, because a mid-value sheet on a
    # light ground has nothing to throw its shadow against.
    paper = np.array((0x13, 0x25, 0x2C) if args.day else DAY, dtype=float)
    lift = int(px * args.rise)
    for i, sv in enumerate(sheets):
        a = place(alpha_of(sv, px), px, args.inset)
        if a.max() < 0.02:
            continue
        z = 1 + i                                         # each sheet a little higher
        sh = soft(offset(a, lift * z, int(lift * z * 1.35)), px * 0.006 * z) * 0.80
        out *= (1 - sh[..., None])
        face = paper[None, None, :] * (0.80 + 0.30 * sheen(px, args.rot, 0.34))[..., None]
        face += (40.0 if args.day else 60.0) * edge_of(a, px)[..., None]   # the cut edge
        m = np.clip(a, 0, 1)[..., None]
        out = out * (1 - m) + np.clip(face, 0, 255) * m
    return np.clip(out, 0, 255)


NIGHT = (0x0A, 0x0A, 0x0B)
DAY = (0xF4, 0xF5, 0xF2)


def disc_mask(px, face, feather):
    """A circle whose edge is a FALLOFF, not a line.

    Spencer's rule, and it is the one that keeps a bright plate from looking
    pasted onto the dark page: we feather in and vignette in the edges so it is
    never a hard line of light against a moonlit candle night.
    """
    y, x = np.mgrid[0:px, 0:px].astype(float)
    r = np.hypot(x - px / 2, y - px / 2) / (px / 2)
    return np.clip((face - r) / max(feather, 1e-3), 0, 1)


def mode_aperture(h, crease, plate, args):
    """The world, seen through the mark.

    The ring stops being a container and becomes a hole in the page. What shows
    through is the environment we build for a client — which is the whole
    argument of the company in one image, and it is why this mark cannot live
    as flat vector alone.
    """
    px = args.px
    ground = np.zeros((px, px, 3)) + (DAY if args.day else NIGHT)
    d = disc_mask(px, args.face, args.feather)
    world = plate * (0.62 + 0.38 * d)[..., None]          # falls off toward its own edge
    out = ground * (1 - d[..., None]) + world * d[..., None]

    diff, spec, cav = shade(h, args.depth * 0.7, args.rot, shine=args.shine)
    lit = AMBIENT + diff * 0.42 + sheen(px, args.rot, 0.30) * 0.32 + h * 0.20
    lit = np.clip(lit * cav * occlude(h, px), 0, 1)
    lit = np.clip(lit - crease * 0.20, 0, 1)
    metal = np.clip(ramp(lit, RAMPS[args.ramp]) + spec[..., None] * 255.0 * args.spec, 0, 255)

    m = np.clip(h * 2.6, 0, 1)
    cast = soft(offset((h > 0.02).astype(float), int(px * .004), int(px * .006)), px * .008)
    out *= (1 - cast[..., None] * 0.45)
    return np.clip(out * (1 - m[..., None]) + metal * m[..., None], 0, 255)


def mode_inlay(h, crease, plate, args):
    """The mark itself is the window. Nothing else of the plate survives.

    Reference five does this with a torus full of cloud. It is the most
    reduced version of the same idea as `aperture`: the shape is not drawn in a
    colour, it is CUT, and a world is behind the page.
    """
    px = args.px
    out = np.zeros((px, px, 3)) + (DAY if args.day else NIGHT)
    diff, spec, cav = shade(h, args.depth * 0.5, args.rot, shine=args.shine)
    lit = 0.72 + diff * 0.34 + h * 0.10
    inner = np.clip(plate * (lit * cav)[..., None], 0, 255)
    m = np.clip(h * 2.6, 0, 1)
    halo = soft(m, px * 0.012) * 0.30                     # the page glows a little around the cut
    out += ramp(np.full((px, px), 0.62), RAMPS[args.ramp]) * (halo * 0.16)[..., None]
    out = out * (1 - m[..., None]) + inner * m[..., None]
    return np.clip(out + spec[..., None] * 90.0 * args.spec, 0, 255)


MODES = {"foil": mode_foil, "coin": mode_coin, "papercut": mode_papercut,
         "aperture": mode_aperture, "inlay": mode_inlay,
         "deboss": lambda h, c, p, a: mode_deboss(h, c, p, a, up=False),
         "emboss": lambda h, c, p, a: mode_deboss(h, c, p, a, up=True)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=sorted(MODES))
    ap.add_argument("svg"); ap.add_argument("out")
    ap.add_argument("--plate"); ap.add_argument("--px", type=int, default=2048)
    ap.add_argument("--bevel", type=float, default=0.0045)
    ap.add_argument("--depth", type=float, default=1.0)
    ap.add_argument("--rot", type=float, default=0.0)
    ap.add_argument("--inset", type=float, default=0.62)
    ap.add_argument("--face", type=float, default=0.86)
    ap.add_argument("--ramp", default="bronze", choices=sorted(RAMPS))
    ap.add_argument("--shine", type=float, default=340.0)
    ap.add_argument("--spec", type=float, default=0.30)
    ap.add_argument("--grain", type=float, default=0.026)
    ap.add_argument("--rim", action="store_true")
    ap.add_argument("--day", action="store_true")
    ap.add_argument("--feather", type=float, default=0.16)
    ap.add_argument("--sun", type=float, default=0.0)
    ap.add_argument("--rise", type=float, default=0.006)
    args = ap.parse_args()

    body, crease_svg = split_svg(args.svg)
    a = place(alpha_of(body, args.px), args.px, args.inset)
    h = height_field(a, args.bevel, args.px)
    c = np.zeros_like(h)
    if crease_svg:
        c = height_field(place(alpha_of(crease_svg, args.px), args.px, args.inset),
                         args.bevel * 0.45, args.px)

    plate = load_plate(args.plate, args.px)
    out = MODES[args.mode](h, c, plate, args)
    Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(args.out)
    print(f"{args.out}  {args.mode}  {args.px}px  light {LIGHT_DEG + args.rot:.0f}°")


if __name__ == "__main__":
    main()
