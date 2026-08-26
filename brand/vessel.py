#!/usr/bin/env python3
"""The Vessel — a crescent solid that cups a staged garden.

Round six of the mark, and the first that is not a mark. The brief changed:
not "a logo" but a small against-the-rules image that encapsulates the
business. So this is an OBJECT, rendered, in the forge layer — never a stroke,
never a flat vector. Form comes from adjacent planes at different values,
which is the one lesson that survived four rejected rounds.

Geometry:
    A large disc with a second disc subtracted, offset up and right. What is
    left is a crescent with real thickness that stands on a ground plane. Its
    concave inner face catches the light; its outer shoulder rolls away from
    it. That value break IS the edge — nothing is outlined.

    A ledge crosses the lower interior. On it: a rock mass, a windswept pine
    reaching out over the opening, and the Monk seated small beneath it.

One raking light, upper left, low (LIGHT_DEG / LIGHT_Z shared with strike.py).
Specular is a narrow near-white line, never gold, never a bloom.

    vessel.py [--night] [--px N] [--no-figure] [--out FILE]
"""
import argparse, os
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets")

# ── the house light — identical constants to strike.py ────────────────────
LIGHT_DEG = 214.0
LIGHT_Z   = 0.34
AMBIENT   = 0.15

DAY_GROUND   = (0xF4, 0xF5, 0xF2)
NIGHT_GROUND = (0x0A, 0x0A, 0x0B)

# ── ramps, straight out of tokens.css. Nothing picked by eye. ─────────────
# graphite — matte powder-coat, the body material. Long dark run: a ramp
# weighted toward its own mid tone renders as plastic.
GRAPHITE = [(0.00, (0x06, 0x07, 0x06)),   # graphite-void
            (0.34, (0x1A, 0x1A, 0x1A)),   # graphite-deep
            (0.66, (0x3F, 0x39, 0x37)),   # graphite
            (0.92, (0x81, 0x7C, 0x7A)),   # graphite-lit
            (1.00, (0xFE, 0xFE, 0xF5))]   # edge — near-white, NOT gold

# the pine. Imagery only — the lit-world gamut is permitted inside a plate
# and forbidden on type, tiles and rules.
FOLIAGE = [(0.00, (0x2A, 0x16, 0x0D)),
           (0.38, (0x5E, 0x32, 0x1F)),    # oxide
           (0.68, (0x7B, 0x49, 0x33)),    # rust
           (0.88, (0xCD, 0x79, 0x5C)),    # coral
           (1.00, (0xE5, 0x9E, 0x5D))]    # bronze


def ramp(t, stops):
    ts = np.array([s[0] for s in stops])
    cs = np.array([s[1] for s in stops], dtype=float)
    out = np.empty(t.shape + (3,), dtype=float)
    for c in range(3):
        out[..., c] = np.interp(t, ts, cs[:, c])
    return out


def box1d(a, r, axis):
    if r < 1:
        return a
    a = np.swapaxes(a, 0, axis)
    pad = np.pad(a, ((r + 1, r),) + ((0, 0),) * (a.ndim - 1), mode="edge")
    c = np.cumsum(pad, axis=0)
    out = (c[2 * r + 1:] - c[:-(2 * r + 1)]) / (2 * r + 1)
    return np.swapaxes(out, 0, axis)


def gblur(a, sigma, ax=None):
    """Gaussian in FLOAT as three box passes. PIL will not blur mode F here,
    and round-tripping a height field through uint8 quantises it into rings."""
    if sigma < 0.4:
        return a.astype(float)
    r = max(1, int(round((np.sqrt(4 * sigma * sigma + 1) - 1) / 2)))
    out = a.astype(float)
    axes = (0, 1) if ax is None else (ax,)
    for _ in range(3):
        for x in axes:
            out = box1d(out, r, x)
    return out


def light_vec():
    a = np.radians(LIGHT_DEG)
    L = np.array([np.cos(a), np.sin(a), LIGHT_Z])
    return L / np.linalg.norm(L)


def smoothstep(e0, e1, x):
    d = e1 - e0
    if abs(d) < 1e-9:
        d = 1e-9 if d >= 0 else -1e-9      # preserve the SIGN, not just magnitude
    t = np.clip((x - e0) / d, 0, 1)
    return t * t * (3 - 2 * t)


def draw_mask(px, fn):
    """Rasterise an organic shape with PIL, hand it back as a float mask."""
    im = Image.new("L", (px, px), 0)
    fn(ImageDraw.Draw(im))
    return np.asarray(im, dtype=float) / 255.0


# ── composition constants, in normalised frame coords (-.5 .. .5, y down) ──
R_OUT,  C_OUT = 0.345, ( 0.015,  0.030)
R_IN,   C_IN  = 0.275, (-0.045, -0.050)
LEDGE_Y       = 0.145


def render(px=2048, night=False, figure=True):
    ground = NIGHT_GROUND if night else DAY_GROUND
    L = light_vec()

    y, x = np.mgrid[0:px, 0:px].astype(float) / px - 0.5

    d_out = np.hypot(x - C_OUT[0], y - C_OUT[1]) - R_OUT
    d_in  = np.hypot(x - C_IN[0],  y - C_IN[1])  - R_IN

    aa = 1.6 / px
    m_out  = smoothstep(aa, -aa, d_out)
    m_in   = smoothstep(aa, -aa, d_in)
    solid  = m_out * (1.0 - m_in)          # the crescent body
    mouth  = m_out * m_in                  # the lens-shaped opening

    # ── shade the crescent ────────────────────────────────────────────────
    # A REAL cross-section, not a plateau. `t` runs 0 at the outer boundary to
    # 1 at the inner one; the body is a rounded shoulder with a concave scoop
    # cut near the inner edge. That scoop is the whole point — its far wall
    # turns back into the light and becomes the pale band that says "vessel".
    # A plateau under one directional light renders as a single flat colour
    # with a gradient over it, which is the plastic failure `struck` names.
    a_out = np.clip(-d_out, 0, None)
    b_in  = np.clip(d_in,  0, None)
    t = a_out / (a_out + b_in + 1e-9)

    prof = np.clip(1.0 - (2.0 * t - 1.0) ** 2, 0, 1) ** 0.42
    prof = prof - 0.42 * np.exp(-(((t - 0.80) / 0.115) ** 2))   # the scoop
    h = np.clip(prof, 0, 1) * solid
    h = gblur(h, 0.0022 * px)

    gy, gx = np.gradient(h)
    gx *= px * 0.055
    gy *= px * 0.055
    nz = 1.0 / np.sqrt(gx * gx + gy * gy + 1.0)
    nx, ny = -gx * nz, -gy * nz
    lam = nx * L[0] + ny * L[1] + nz * L[2]
    diff = np.clip((lam + 0.35) / 1.35, 0, 1)      # wrap, not pure Lambert

    # broad sheen: even a curved face needs the big-soft-source falloff or the
    # dark side goes dead flat.
    t_sh = -((x * L[0] + y * L[1]) / 0.72)
    sheen = np.clip(0.62 + t_sh * 0.30, 0.10, 1.0)

    # concrete tooth — fine, isotropic. NOT the anisotropic brush; that belongs
    # to bronze. Without it the face renders as untextured CG.
    rng = np.random.default_rng(11)
    tooth = gblur(rng.standard_normal((px, px)), max(0.8, px * 0.0011))
    tooth /= max(tooth.std(), 1e-6)

    val = AMBIENT + 0.92 * diff * sheen
    val *= (1.0 + tooth * 0.055)

    # cavity: the scoop's own floor holds shadow
    val -= 0.16 * np.exp(-(((t - 0.845) / 0.075) ** 2)) * solid

    # narrow near-white specular on the light side only — one line, never a
    # bloom around the silhouette.
    grad = np.hypot(gx, gy)
    spec = smoothstep(0.55, 1.35, grad) * np.clip(diff, 0, 1) ** 6 * solid
    val = np.clip(val, 0, 1) * (1 - spec * 0.9) + spec * 0.9

    body = ramp(np.clip(val, 0, 1), GRAPHITE) / 255.0

    # ── the cup interior, below the ledge ────────────────────────────────
    below = smoothstep(-aa, aa, y - LEDGE_Y)
    cup = mouth * below
    cup_v = 0.05 + 0.13 * smoothstep(LEDGE_Y + 0.24, LEDGE_Y, y)
    # occlusion where the floor meets the inner wall
    cup_v -= 0.055 * np.exp(-((b_in / 0.055) ** 2))
    cup_rgb = ramp(np.clip(cup_v, 0, 1), GRAPHITE) / 255.0

    # ── canvas ────────────────────────────────────────────────────────────
    img = np.ones((px, px, 3)) * (np.array(ground) / 255.0)

    # a very soft floor gradient so the object is standing on something
    floor = smoothstep(0.16, 0.50, y) * 0.05
    img *= (1.0 - floor[..., None] * (0.9 if not night else -0.6))

    # contact shadow — short, soft, thrown down-right off the low left light
    sh = np.exp(-(((x - C_OUT[0] + 0.045) / 0.34) ** 2
                  + ((y - (C_OUT[1] + R_OUT + 0.020)) / 0.030) ** 2))
    sh = gblur(sh, 0.010 * px)
    img *= (1.0 - 0.30 * sh[..., None]) if not night else (1.0 + 0.10 * sh[..., None])

    img = img * (1 - cup[..., None]) + cup_rgb * cup[..., None]

    # the ledge lip — one hairline catching light, the cut edge of a plane
    lip = np.exp(-(((y - LEDGE_Y) / 0.0035) ** 2)) * mouth
    img = img * (1 - lip[..., None] * 0.85) + \
        (np.array([0x81, 0x7C, 0x7A]) / 255.0) * (lip * 0.85)[..., None]

    # ── the staged garden, struck onto the ledge ─────────────────────────
    if figure:
        img = stage(img, px, mouth, ground, night)

    img = img * (1 - solid[..., None]) + body * solid[..., None]
    return Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8))


def P(px, u, v):
    return ((u + 0.5) * px, (v + 0.5) * px)


def stage(img, px, mouth, ground, night):
    """Rock, pine and the Monk — the built world inside the vessel.

    The garden is STAGED, not found: it sits on a ledge inside a made object.
    That is the brand's argument — an agency builds a model of the buyer's
    world rather than photographing the world.
    """
    # rock mass, right of centre, rising off the ledge
    def rock(d):
        d.polygon([P(px, -.006, .145), P(px, .022, .100), P(px, .058, .080),
                   P(px, .094, .094), P(px, .122, .122), P(px, .134, .145)],
                  fill=255)
        d.polygon([P(px, .068, .145), P(px, .098, .112), P(px, .126, .104),
                   P(px, .140, .128), P(px, .142, .145)], fill=255)
    m_rock = draw_mask(px, rock) * mouth

    # the pine — grows out of the rock and sweeps LEFT, leaving through the
    # crescent's mouth. Deliberately NOT clipped to the opening: the disc
    # broken by its own subject is the one move `struck` said to borrow.
    def trunk(d):
        pts = [(.060, .128), (.050, .086), (.028, .046), (-.004, .012),
               (-.038, -.018), (-.070, -.040)]
        for i in range(len(pts) - 1):
            w = max(2, int(px * (0.0062 - 0.0009 * i)))
            d.line([P(px, *pts[i]), P(px, *pts[i + 1])], fill=255, width=w)
        for a, b, w in [((.028, .046), (-.016, .038), .0028),
                        ((-.004, .012), (-.054, .006), .0024),
                        ((-.038, -.018), (-.086, -.026), .0021),
                        ((.050, .086), (.092, .074), .0022)]:
            d.line([P(px, *a), P(px, *b)], fill=255, width=max(2, int(px * w)))
    m_trunk = draw_mask(px, trunk)

    # foliage — flat horizontal pads, each built from a scatter of small
    # ellipses. A single solid ellipse reads as a cartoon cloud; the pad has to
    # be ragged and shallow before it reads as needles catching light.
    PADS = [(-.042, .036, .050, .0105, .40),
            (-.080, .004, .054, .0110, .56),
            (-.108, -.028, .046, .0098, .70),
            (.100, .072, .038, .0090, .46),
            (-.074, -.044, .038, .0088, .64),
            (-.014, .012, .034, .0082, .52),
            (-.130, .034, .032, .0078, .44),
            (.040, .040, .030, .0075, .38)]

    def pad_cluster(cx, cy, rw, rh, seed):
        def f(d):
            rng = np.random.default_rng(seed)
            for _ in range(34):
                u, v = rng.uniform(-1, 1), rng.uniform(-1, 1)
                if u * u + v * v > 1.0:
                    continue
                ex, ey = cx + u * rw * 0.98, cy + v * rh * 0.98
                sw = rw * rng.uniform(0.14, 0.26)
                sh = rh * rng.uniform(0.42, 0.80)
                d.ellipse([P(px, ex - sw, ey - sh), P(px, ex + sw, ey + sh)],
                          fill=255)
        return f

    pad_masks = [(draw_mask(px, pad_cluster(cx, cy, rw, rh, 31 + i)), v)
                 for i, (cx, cy, rw, rh, v) in enumerate(PADS)]

    # the Monk — seated, small, at the left of the ledge. Kasa for silhouette:
    # at this size his wardrobe, his hue family and his empty hands are all
    # invisible, and the hat is the only thing that survives the reduction.
    def monk(d):
        d.polygon([P(px, -.196, .145), P(px, -.186, .112), P(px, -.166, .102),
                   P(px, -.146, .112), P(px, -.136, .145)], fill=255)   # robe
        d.ellipse([P(px, -.1735, .0865), P(px, -.1585, .1015)], fill=255)  # head
        d.polygon([P(px, -.212, .0855), P(px, -.166, .0695), P(px, -.120, .0855),
                   P(px, -.166, .0800)], fill=255)                       # kasa
    m_monk = draw_mask(px, monk) * mouth

    dark = np.array([0x06, 0x07, 0x06]) / 255.0
    mid  = np.array([0x1A, 0x1A, 0x1A]) / 255.0

    m = np.clip(m_rock, 0, 1)[..., None]
    img = img * (1 - m) + mid * m

    for pm, v in pad_masks:
        rgb = np.array(ramp(np.array([v]), FOLIAGE)[0]) / 255.0
        pm = np.clip(pm, 0, 1)[..., None]
        img = img * (1 - pm) + rgb * pm

    for mk in (m_trunk, m_monk):
        mk = np.clip(mk, 0, 1)[..., None]
        img = img * (1 - mk) + dark * mk
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--night", action="store_true")
    ap.add_argument("--px", type=int, default=2048)
    ap.add_argument("--no-figure", action="store_true")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    im = render(a.px, a.night, not a.no_figure)
    out = a.out or os.path.join(OUT, "vessel-%s.png" % ("night" if a.night else "day"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.save(out)
    print(out)


if __name__ == "__main__":
    main()
