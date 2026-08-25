# Ninja

Plates: `plates/ninja-blend.png` (day ground), `plates/ninja-dark.png`,
`plates/ninja-myth.png` — feathered, verified with `check-plate.py --figure`.
References: six images supplied 2026-08-25. Not stored on disk.

Spencer: *"Shinji Aramaki style anime in texture, movement, execution. Warriors
that might be myth. Until you get back to your hideout, and everyone's dead."*

## The register

That second sentence is the character. He is not the hero of the scene — he is
**the thing that already happened**. Rumour that turns out to have been true.
Everything about him is past tense and unhurried.

**The stillness is the threat.** No action poses, no crescendo, no confrontation.
He is standing in a crowd doing nothing, or crouched watching, or standing in a
corridor where it is already over. `night-myth.png` shows the aftermath with **no
bodies, no damage and no gore** — only dust, emptiness and him. That is the
correct way to render it and it should stay that way.

## Rendering — and what this proves about the cast

**Shinji Aramaki anime.** Hard-surface mechanical design, crisp panel lines,
cel-shaded flat colour zones with sharp specular edges. Engineered, not painterly.
Explicitly **not** photoreal.

Which surfaces the real structure of this namespace:

| Figure | Rendered as |
|---|---|
| Monk | photoreal cloth |
| Samurai | photoreal, then ink |
| Night warrior | cel-shaded anime, then ink |

**Three different rendering modes on purpose. The only constant is the ink
dissolution.** That is what makes them one cast — not a shared drawing style.
Worth stating plainly because the instinct is to unify the technique, and
unifying the technique would flatten three distinct figures into one.

## Mechanics

1. **No hat. Hood up. A cyber mask, never a face.** The hat belongs to the other
   two; the hood is this figure's silhouette. Under it, a hard-surface plated
   mask with lit line channels or a single glowing optic — see *The face is a
   mask* below. No skin, no hair, no human features at any angle.
2. **Reads young.** Lighter build, casual weight, unhurried posture.
3. **HEAVILY LAYERED, and LONG.** A first pass cropped the jacket short and that
   was wrong. The parka is oversized with the hem falling **well below the hip,
   toward the knee**, worn open over a second offset mid-layer jacket, over a
   high-collared under-layer, over stacked cargo trousers. **Each hem visible at
   a different length.** Sealed seams, magnetic closures, webbing straps, small
   hard-shell panels at shoulder and forearm, over matte black articulated
   plating. Nothing cropped, ever — the bulk is the silhouette.
4. **Cybernetic appendage.** One matte black prosthetic arm or hand with
   articulated joints and fine seam lines. He carries **no drawn weapon** in any
   plate — his hands are the weapon. Worth keeping.
5. **Adaptive colour — see below.**
6. **Kindle channels.** Narrow cyan-turquoise light along plating, spine and
   knuckles. **Hairline only** — measured at 0.4–1.0% of frame coverage. Never a
   glow-suit.
7. **The common thread — see the section below.** This took three passes to get
   right and it is the most important thing on this page.
8. **Future Tokyo, desaturated.** Signage is dim and near-grey, never a neon
   blaze. No magenta, no hot pink, no orange neon. The city stays dark so he can
   be the only lit thing.

## The effect — HE COMES APART AS PIXELS

**The Ninja does not dissolve into ink. Ink belongs to the Monk and the Samurai.**

His edges come apart as **16-bit pixels** — large flat opaque squares of the
cloth they left, drifting upward and outward as if lifted on a breeze rising from
below. Only ever on **one side**: the side nearest a wall or a shadow.

That is not a variation for its own sake. **The company is called Pixel Blade,
and the line is already on record — "blades are no longer steel, pixels."** The
ancient figures come apart in ink, the modern one in pixels. Same event, the
medium changed with the era.

### The blocks GROW as they travel

This is the part that makes it read. **Fine, almost sub-pixel speckle right
against the body; big chunky low-res squares far out.**

It is not confetti coming off him — it is **resolution loss**. He is not shedding
particles, he is losing definition, and the further a block gets the less of him
it remembers. A uniform block size reads as an effect; a graduated one reads as
degradation.

`pixelate.py` implements it with `--b0` (block size at the body), `--b1` (at the
outer edge) and `--bk` (how fast it coarsens). Working values: **b0 4, b1 44–52,
bk 1.7** at 2K. A loose block is redrawn at the size of **where it lands**, not
where it came from, so travelling further coarsens it further.

### Rules

- **Square blocks.** Hard right angles, flat solid colour, no anti-aliasing, no
  rotation, no blur.
- **The garment is genuinely eaten.** Its outline becomes a stepped staircase of
  missing bites, and square holes appear punched through the cloth a little way
  in from the edge. He is visibly incomplete on that side.
- **No gap.** The loose squares begin exactly where the cloth ends.
- **They are pieces of his coat.** Each square carries the colour it came from —
  bone, sand, grey, charcoal, black. They do not glow. At most one or two in a
  hundred carry the cyan of the plating beneath.
- **Upward and outward**, densest at the edge, thinning as they rise, the
  furthest few sparse and scattered. Many are lost in the shadow they drift into.
- **One side only.** The other side is completely intact — smooth cloth, clean
  unbroken outline.
- **Never** smoke, mist, ink, tendrils, embers or sparks. And never glitch art —
  no RGB splitting, scan lines, chromatic aberration, digital noise or holograms.

### The face is a mask

**No face, no skin, and no hair.** Inside the hood is a hard-surface angular mask
of matte black plating covering the entire head — faceted panels, fine seam
lines, a low sculpted brow, a flat lower jaw guard. Set into it either a few
narrow glowing cyan line channels or **one small round glowing optic**, slightly
off centre.

Nothing hangs out of the hood. No strands, no fringe, nothing framing the mask —
an earlier pass had cyan hair-like strands and they were cut. The head is a
machined object, entirely covered.

### Produce it in code, not by generation

`brand/pixelate.py`.

Four generation attempts put the pixels **beside** the figure — a field on the
wall next to an intact character — rather than eating the garment. Image models
consistently read this as an adjacent object.

The pipeline that works:

1. Generate a **clean, fully intact** figure. No dissolution requested at all —
   models render that reliably.
2. Run `pixelate.py` over the dissolving side.

```
pixelate.py <in> <out> --edge right --x0 0.54 --x1 0.82 \
            --drift 0.17 --block 30 --srcx 0.93 --gamma 1.9 --seed 5
```

The tool blocks the band, removes blocks with probability rising toward the outer
edge, fills the holes with clean background copied from a column outside the
figure, then redraws a fraction of what came loose at a rising offset with
density falling off.

This is better than a lucky generation for three reasons: the edge is genuinely
chewed rather than suggested; every block is provably a piece of the cloth it
left; and it is **deterministic and repeatable** — same seed, same result, which
is what a design system needs. It is also the basis for the site animation, since
the same algorithm runs in canvas.

### Tuning notes

- Dark coat against a dark wall reads faintly. Widen the band inward (`--x0`
  lower) so it eats into the lighter under-layers too, and raise `--drift`.
- `--gamma` controls how tightly the dissolution hugs the edge. 1.7–2.2 is the
  useful range; higher keeps the body more intact.
- `--b1` around 44–52px at 2K for the coarse end. Much larger reads as damage
  rather than degradation.
- `--b0` at 3–5px. If the fine end is too large the gradient disappears and it
  goes back to reading as confetti.

## Adaptive colour — he is the day/night switch## Adaptive colour — he is the day/night switch

Spencer: *"Light colors to blend walking through a crowd that can change to dark
to suit his needs."*

Measured across the same garment:

| | dominant values |
|---|---|
| **Light mode** | `#BBBFC1` · `#737B7E` · `#373837` |
| **Dark mode** | `#2A2D30` · `#17191A` · `#020303` |

Same silhouette, swung from value ~76% down to ~19%.

**He does in one figure what the site does across pages.** That makes him the
natural transition device between the light pages and the dark ones — the only
element in the whole system that legitimately belongs to both modes at once and
changes on purpose rather than by placement.

## Kindle, and the rule it changed

His light measured **hue 181–189** against kindle's 175 — the same colour, drifting
a few degrees cooler through cel shading.

Kindle was previously "blades only." That rule is now restated by **meaning**
rather than location: **kindle marks what is not proven yet.** The Samurai's
blade is ability he has not earned; the Night warrior's channels are a myth
nobody has confirmed. The Monk, who has arrived, carries none of it.

## Borrow / don't borrow

**Do not borrow the neon** from the reference board. Those images run hot magenta,
crimson and lime against black. Ours stays desaturated with kindle as the only
saturated note — otherwise he becomes generic cyberpunk, which `tech` already
rules out.

**Do not borrow the lime green.** Kindle covers the role and adding a second
bright hue halves it.

**Do not draw a weapon.** He has not needed one in three plates and it is
stronger that way.

**Do not crop the jacket.** The layering and the length are the silhouette.

**Do not let any skin show above the neck.** Not a jaw, not a chin, not an eye.

**Do not show the aftermath.** No bodies, no blood, no wreckage. Emptiness and
dust carry it; anything explicit makes him ordinary.

## Verified

| Plate | Mode | Chroma | Ground | Edge |
|---|---|---|---|---|
| `night-blend` | day · figure | 0.5% | 37.1% light | delta 1 |
| `night-dark` | night · figure | 0.6% | 74.7% dark | delta 0 |
| `night-myth` | night · figure | 1.1% | 46.5% dark | delta 0 |
