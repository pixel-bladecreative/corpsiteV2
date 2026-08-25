# Night warrior

Plates: `plates/night-blend.png` (day ground), `plates/night-dark.png`,
`plates/night-myth.png` — feathered, verified with `check-plate.py --figure`.
Reference: four images supplied 2026-08-25. Not stored on disk.
Name still open — filed by role until one lands.

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

1. **No hat. Hood up. The face is a COMPLETE VOID.** The hat belongs to the
   other two; the hood is this figure's silhouette. Inside it there is
   **nothing** — pure flat black. No skin, no jaw, no chin, no eyes, no features
   of any kind. A first pass let a jaw and an eye band catch light and Spencer
   cut it: *"no exposed skin on his face. Only suggestion, silhouette, shadow."*
   This is absolute, and it matches the Samurai after all.
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
7. **The common thread — SUBTRACTIVE, not emissive.** Whole **regions** of him
   are simply gone and replaced by churning wet black ink: half a torso, an
   entire arm, the whole lower body. The boundary runs raggedly through him.

   A first pass had smoke rising from a single point on his shoulder and Spencer
   named it: *"too on the nose. Whole parts of him need to look like they are
   dissolving into the shadows from which he works."* The failure mode is drawing
   him whole and adding an effect. He is not emitting shadow — **he is missing**,
   and shadow is what is there instead.
8. **Future Tokyo, desaturated.** Signage is dim and near-grey, never a neon
   blaze. No magenta, no hot pink, no orange neon. The city stays dark so he can
   be the only lit thing.

## Adaptive colour — he is the day/night switch

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
