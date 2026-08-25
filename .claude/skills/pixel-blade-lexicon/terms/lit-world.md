# lit world

Brand-native plates: `plates/litworld-aperture.png`, `plates/litworld-columns.png`,
`plates/litworld-enso.png`
Tokens: `brand/tokens.css` — the LIT WORLD block and the two-gamut rule.

Spencer's framing, verbatim: *"we're in a dark room, looking into a bright
world"* — and *"we're in the dark, comfy room, reading a fantastical tale of
surreal dreamy exploration."*

## What it establishes

**Two gamuts with a hard boundary at the image edge.**

| | |
|---|---|
| **Interface gamut** — the dark room | sumi, graphite, petrol, bronze, washi. Narrow, disciplined, contrast-verified. |
| **Image gamut** — the lit world | all of the above, plus ember, coral, blush, rust, oxide. |

Saturated warm color is **permitted inside imagery** and **forbidden in type,
tiles, buttons, rules, borders, backgrounds, and any text section**.

This supersedes the `dreamed garden` instruction to cut coral and red outright.
That was too blunt — the distinction is not *whether* those colors appear but
*which side of the frame they appear on*.

## Two findings from sampling the plates

**1. This is not a foreign palette.** The warm range lands at **hue 12–20**,
directly adjacent to bronze at hue 29. It is the same hue family — the interface
holds it restrained, the world runs it hot. That is why a fully saturated plate
still reads as this brand rather than a different one.

**2. There is no pink.** Sampling found nothing above hue 340 — no true pink, no
magenta. What reads as pink is a **desaturated coral** (`--pb-blush` #F3AF96).
Worth knowing before someone reaches for an actual pink and breaks the family.

## Enforcing the boundary

The edge is **hard, never a gradient**:

- No full-bleed saturated image behind or beneath type.
- No glow, bloom, halo, or colored spill crossing the frame.
- No colored ambient light landing on an interface surface.
- No saturated hue in a border, rule, tile, chip, button, or label.

A reflection **inside** the frame may carry color — a reflection is part of the
world. A shadow **outside** it may not.

**Bronze is the only color that crosses.** It lives in both gamuts, and it is
what stitches them together. Nothing else gets that privilege.

## Why the discipline buys something

The interface is monastic so the images can be lush. Rationing the saturated
range by confining it is exactly what gives it force. Spend it in the room and it
stops being an event — the same logic as `accent-word`, applied at the scale of
the whole page.

## Layout consequence

This gives the page a natural rhythm without anyone having to invent one: long
quiet dark passages of interface, punctuated by contained saturated apertures.
The image sections are the exhalations. `corner-brackets` and `dark-half-type`
matter more than ever, because the image edge is now where the gamut changes.

## Reading the plates

- `litworld-aperture` — the metaphor stated literally. A near-black room, one
  hairline bronze reveal, a figure in silhouette, and a coral valley through the
  opening. The color stops dead at the frame.
- `litworld-columns` — the site environment with the world turned up. Bronze
  columns and black mirror floor hold the interface gamut; only the far landscape
  is saturated. The floor reflection carries color, correctly.
- `litworld-enso` — the disc as a lit transparency. Most "fantastical tale" of
  the three; the void around it stays pure black.
