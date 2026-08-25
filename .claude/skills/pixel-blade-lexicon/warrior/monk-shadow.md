# Monk — shadow form

Plates: `plates/monk-stand.png`, `plates/monk-enso.png`, `plates/monk-dissolve.png`
— all feathered to the day ground, all passing.
Reference: three images supplied 2026-08-25. Not stored on disk.

Spencer: *"Inky, shadowed, the hat hides him from a sun he's not worthy of
receiving. He's learning to dance, but carries too much shadow. Watercolor made
motion. Sumi-e inkblot mainly, with bursts of color behind his weapon that
reveals what he might be once he's done learning."*

## This is the Monk, earlier

Spencer introduced this figure as "the Day warrior." Filed here as an **earlier
form of the same character** — the slot left open in the roster — on the strength
of the briefs read side by side:

| Shadow form | Final form |
|---|---|
| *"the hat hides him from a sun he's not worthy of receiving"* | *"He's no longer hiding from the sun"* |
| *"He's learning to dance"* | the pose reads as dance as much as strike |
| *"carries too much shadow"* | dissolves into light and dust |
| **carries a sword** | **hands empty and open, always** |

The last row is the one that settles it, and neither brief stated it. **Empty
hands are the graduation.** The student needs a blade to show what he might be;
the master no longer needs one to be it.

Spencer also said the final form would make sense *"when we see the other
forms."* This is one.

If he is meant as a separate character rather than an earlier form, this file
splits cleanly — the mechanics below do not depend on the reading.

## Two findings, one of which killed a better-sounding guess

### 1. He has no colour at all

Expected: his ink would be petrol, the way the Monk's cloth is bronze. It is not.

Sampled across all three plates his ink returns `#171714` / `#1B1B18` / `#1C1C19`
— **hue 60, saturation 11–13%.** That is warm-neutral sumi black. No brand hue
whatsoever.

Which is a better answer than the one expected. The final form is **the bronze
family desaturated** — he is made of the brand. The shadow form is made of
**nothing**. He has not earned a hue yet. He is colourless because he has not
become anything.

### 2. The blade burst belongs to no gamut

Sampled at hue **174–177**, saturation **76–82%**, value **81–86%** — settled as
`--pb-kindle` **#2AD4C8**.

Petrol is hue 197. This sits 22° warmer and far hotter. It is not petrol, not
bronze, and not in the day or night palette. **It is the brightest and most
saturated value anywhere in the system, and it appears in exactly one place.**

That is correct rather than a problem. It is the only colour in the brand that
belongs to **potential** rather than to a material or a mode — which is precisely
what Spencer asked it to mean.

**Absolute rules:** image gamut only (1.69:1 on paper). Only ever behind a blade.
It never touches the figure carrying it. Kindle anywhere else is a bug.

## Mechanics

1. **ALWAYS the hat.** A wide conical kasa, and it completely conceals the head.
   **No face, ever, at any angle.** Non-negotiable — Spencer's word was "always."
2. **Sumi-e inkblot body.** He is brush-painted, not rendered: wet pooling
   blacks, grey wash bleeding into damp paper, dry-brush bristle streaks, flicked
   splatter. Silhouette first.
3. **Solid and unresolved at once.** Some edges hard and confidently painted —
   hat brim, one shoulder, the line of the back. Others trailing into raw brush
   strokes: the hem breaking into dry tongues and curling tendrils, a sleeve
   dissolving to splatter, the feet never quite landing. **He is a person and a
   brush mark simultaneously.**
4. **The weapon carries the colour.** Kindle bleeds and splashes behind the blade
   only. The figure himself stays black and grey.
5. **Dance, not violence.** Sweeping, extended, unhurried — even mid-cut.
6. **Transit is dissolution.** To move he becomes a rushing spiral of inky wisp
   and re-forms elsewhere, leaving a slow-turning vortex of swirls and drifting
   droplets where he was. `monk-dissolve.png` documents it: residue left, current
   between, figure re-coalescing hat-first.

## What he shares with the final form, and what he breaks

**Shares:** face never readable, dissolution at the edges, motion living around
the figure rather than in blur, dance before strike, layered and indistinct.

**Breaks:** he carries a weapon. He carries no brand hue. He is bound to the
light ground, where the final form crosses both.

## Borrow / don't borrow

**Do not borrow the armour** from the second reference. He is a traveller in a
coat, not a warlord in plate.

**Do not borrow the orange sun disc.** Bronze holds the warm role and this figure
holds none of it.

**Do not resolve him.** The temptation under generation is a clean, complete,
well-drawn character. Half of him must stay unfinished — that is the character.

## Verified

| Plate | Mode | Chroma | Light ground | Edge |
|---|---|---|---|---|
| `monk-stand` | day | 2.1% | 62.1% | delta 0 |
| `monk-enso` | day | 1.4% | 72.5% | delta 1 |
| `monk-dissolve` | day | 0.2% | 56.6% | delta 1 |

His ink reads **16.41:1** on paper. Kindle reads **1.69:1** — which is why it is
image-only and always will be.
