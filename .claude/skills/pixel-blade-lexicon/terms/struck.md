# `struck`

**A mark is not artwork. It is a die.**

The flat vector is the tool, not the deliverable. It gets pressed into
something — foil onto construction paper, relief onto a bronze blank, a blind
impression into cotton stock, a stack of cut sheets, a hole cut in the page
with a world behind it. What Spencer said, verbatim: *"If it doesn't look right
flat, emboss it in metallic foil on construction paper. Or make a coin out of
it resting on black marble."*

This term exists because of a category error. The mark was built in the
**livery** layer — flat, said, one colour, no dimension. It belongs in the
**forge**: made, surfaced, lit. Everything else in the brand already lived
there. The mark was the only thing still pretending to be a printer's problem
from 1974.

## Mechanics

**Depth comes from light and stacking, never from a gradient fill.** Every
reference in this set builds dimension the same way: real planes at real
offsets, throwing real shadows on each other. Nothing is shaded to *look*
three-dimensional; things are separated and then lit. A gradient poured into a
flat shape reads as a gradient. A shape lifted 4px off the one behind it reads
as an object.

**One raking light, low.** Already the brand's rule (`material`), and it is
what these references obey. Upper left, shallow. Two sources is a bug. The
lower the light, the longer the shoulder, the more physical the result.

**Specular is a narrow near-white line.** `--pb-edge #FEFEF5`, one pixel wide,
on the light side only. A wide white bloom around the whole outline is a bevel
filter, and it reads instantly as amateur. Metal that glows all the way round
its own silhouette is plastic.

**A flat raised face shades identically to the flat field around it** — same
normal, same light. This is the trap. Directional light alone cannot render
relief; what makes relief read is *occlusion in the field beside the shape*
plus a small lift because the raised face is nearer the source. Both are fakes
and both are mandatory.

**The face of metal is a gradient across it, not a flat fill.** A big soft
source in a room produces a broad sheen, brightest toward the light. Without
it a struck face renders as one flat colour.

**Anisotropy separates brushed metal from a coloured circle.** Fine streaks
running one direction only, along the light.

**The dark run in a metal ramp must be long.** Metal spends most of its surface
in shadow and earns its colour in a narrow band. A ramp weighted toward its own
mid tone renders as orange plastic.

**Cut paper is defined by its edge and its shadow.** The cut edge catches light
the face does not — a hairline lighter than the sheet. The shadow beneath is
short, soft, and directional. Those two details are the entire effect.

**A bright plate never meets the dark page at a hard line.** Spencer's rule
from `lit world`, and it applies to every aperture: feather in and vignette in,
so a lit world dissolves into the moonlit ground rather than being pasted onto
it.

## Borrow / don't borrow

**Borrow** — the aperture: a ring that stops containing and becomes a *hole*,
with an environment behind the page. This is the single strongest idea in the
set, and it is the company's argument in one image: what shows through our mark
is the world we build for a client.

**Borrow** — layered cut paper for the crane. The fold that one hairline
struggled to suggest reads instantly once it is a real edge throwing a real
shadow.

**Borrow** — blind deboss. No ink at all, the stock's own material revealed
only by how light falls into the impression. The quietest thing in the system
and the most expensive-looking.

**Borrow** — the disc behind the subject, breaking the frame.

**Don't borrow** — the saturated red at reference scale. Those discs run 35%+
chroma coverage and `check-plate.py` fails a night plate over 25%. A struck
plate is imagery, so `lit world` permits ember and coral **inside** it, but the
ceiling still binds. Size the disc to the budget: r≈0.60 of frame lands near
21% once the sheets cover part of it.

**Don't borrow** — cherry blossom, torii, calligraphy columns, hanko seals,
Mt Fuji. The references reach for Japan as *decor*. The brand's Japanese layer
is principle and surface, not iconography, and a torii gate in the mark would
be tourism.

**Don't borrow** — the drop-shadowed glossy bevel. Three of these references
are close to it and it is the failure mode this whole term is meant to avoid.

## The tool

`brand/strike.py` — modes `foil`, `deboss`, `emboss`, `coin`, `papercut`,
`aperture`, `inlay`. Everything above is enforced in code rather than
remembered: one light constant, ramps read from `tokens.css`, near-white
specular, float-precision height fields. Any mark, any material, repeatably.

Plates come from `brand/assets/mat-*.png` — empty materials, generated with
nothing on them. **Never ask an image model to draw the logo.** It produces
logo-*pictures*. Generate the material, strike the geometry into it with code.
