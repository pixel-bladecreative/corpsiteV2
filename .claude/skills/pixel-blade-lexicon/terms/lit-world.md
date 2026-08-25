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

## The ceiling is coverage, not chroma

Spencer: *"there is no upper ceiling"* on imagery — and if one is needed,
`lantern-scrolls` is the limit. Measuring the ladder proved why both halves of
that are true.

| Plate | Chroma coverage | Dark ground | Peak sat |
|---|---|---|---|
| `garden-columns` — restrained | 21.7% | 62.8% | 70 |
| `litworld-columns` — warm | 33.6% | 53.8% | 79 |
| `litworld-enso` — hot | 36.1% | 45.6% | 92 |
| **`litworld-ceiling`** | **21.4%** | **50.9%** | **89** |
| `litworld-aperture` | 19.5% | 62.4% | 95 |

The ceiling plate has among the **lowest** coverage in the set while running near
the top on saturation. It reads as maximal because it is **jewelled** — intense
chroma in small discrete objects separated by void — not because it is bright.

So the bounds are on area, not intensity:

- **saturated coverage ≤ ~25%** of frame (sat > .35, val > .30)
- **dark ground ≥ ~50%** of frame (val < .18)
- **peak saturation: unbounded**

A large continuous saturated field breaks this at far lower saturation than a
field of small brilliant ones. By that measure the `litworld-enso` and
`litworld-columns` plates are already **past** the limit and the ceiling plate is
comfortably inside it — the opposite of how they look.

Run `brand/check-plate.py <image>` to verify. It fails on coverage and on the
edge seam below, and never on saturation.

## The boundary is a falloff, not a line

I originally wrote "hard edge, never a gradient." Spencer corrected it:

> *"we feather in, and vignette in the edges so it's not a hard line of light
> against our moonlit candle night."*

He is right, and it makes the containment stronger rather than weaker. Images
**vignette out**; their own darkness is the boundary. The image **emerges from**
the dark instead of being cut into it — a hard rectangle would read as a pasted-in
photograph. The color dies to nothing *before* it reaches any interface element.

What still holds:

- No saturated hue in a border, rule, tile, chip, button, or label.
- No colored ambient light landing on an interface surface.
- No type sitting on any part of an image still carrying chroma.

A reflection **inside** the frame may carry color — a reflection is part of the
world. A shadow **outside** it may not.

**Bronze is the only color that crosses.** It lives in both gamuts, and it is
what stitches them together. Nothing else gets that privilege.

## Why the discipline buys something

The interface is monastic so the images can be lush. Rationing the saturated
range by confining it is exactly what gives it force. Spend it in the room and it
stops being an event — the same logic as `accent-word`, applied at the scale of
the whole page.

## Consequence for `corner-brackets`

Feathering revises an earlier note. I had said the image edge is where the gamut
changes, so `corner-brackets` matter more. With a feathered edge the opposite is
true for saturated passages: brackets would draw a line exactly where the design
says there should not be one.

**Brackets belong on contained, framed content** — a data panel, a quote, a
still. Not on a feathered image passage, which has no edge to mark.

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
  the three; the void around it stays pure black. **Measures past the coverage
  limit** (36% chroma, 46% dark) — beautiful, and would need tightening before
  it carried a page.
- `litworld-ceiling` — the calibration limit, `lantern-scrolls` rebuilt in our
  world. Vermilion, coral, cyan-teal, amber and ivory panels at many depths over
  a dominant dark void. **Fails the edge check** (corners #4B3525, delta 65)
  because lit panels crop the frame — precisely the case where the vignette is
  mandatory rather than optional.
