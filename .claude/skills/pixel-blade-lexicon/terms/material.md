# material

Tagged reference: `hex-relief`
Brand-native plates: `plates/material-swatch.png`, `plates/material-fold-relief.png`,
`plates/material-crane.png`
Tokens: `brand/tokens.css` (round two)

## What Spencer means by it

**A palette is not a list of colors. It is a set of materials.**

Each entry carries a base value, a surface behavior, and a rule for how it
responds to light. Texture is part of the token, not decoration added later. Ask
"what is this made of," not "what color is this."

This supersedes the round-one palette, which defined flat colors and was
therefore only half a system.

## The three materials

| | Surface | Behavior |
|---|---|---|
| **graphite** | Matte powder-coat, fine tooth | Non-reflective. Reads across a wide value ramp purely by angle to the light. The body material. Never carries text. |
| **bronze** | Brushed satin, visible directional grain | Warm orange-gold. Grain runs along each plane's long axis, one direction per plane. Catches light as a soft directional sheen, never a glossy point. |
| **petrol** | Deep satin blue-green | A second *ground*, not an accent. Dark enough to sit beside graphite, unmistakably green-blue. This is what keeps the palette off the law-firm shelf. |

## The signature: hot edges

Where two planes meet at a crease, a razor-thin brilliant highlight catches.

**The edge is near-white (`#FEFEF5`), not gold.** That was the surprise on
sampling — the specular blows past the material color entirely, and the bronze
sits just inboard of it. Getting this wrong (a thick gold line instead of a
hairline white one) is the difference between machined and plated.

One pixel. Never a glow, never a blur, never thicker.

## Value ramps, and why they exist

Every material lists several values. Those are not tints to pick from freely —
they are **the same material at different angles to a single hard raking light,
upper left, no fill.**

Two light sources anywhere in the system is a bug. This is also why shadows
crush clean to black rather than lifting into grey.

## The rule this replaced

Round one said *"gold is ink, not metal — the moment gold looks like metal, this
becomes a law firm."* That was an over-correction, and the `material-crane`
plate disproves it.

**The corrected rule: bronze is metal in the forge and ink in the livery.**
Brushed grain and hot edges on dimensional surfaces; dead flat for type, because
text has to be flat to stay readable.

The law-firm failure was never *metal*. It is **polished plated** gold — mirror
finish, bevels, a gradient standing in for a highlight. Brushed bronze under a
raking light is machined and industrial. A different object entirely.

## Borrow / don't borrow

**Borrow:** the three materials, the surface behaviors, the hot edge, the single
raking light, and the idea that a value ramp belongs to a material rather than
being free-floating tints.

**Do NOT borrow the hexagons.** The reference is a regular hexagonal
tessellation, which is one of the most exhausted motifs available — crypto,
gaming, generic tech. Our geometry is **origami folds**: irregular, asymmetric,
unequal angles, hand-derived. `material-fold-relief.png` is the reference's
materials rebuilt in our geometry, and it is the version to work from.

**Do not borrow:** any suggestion of chrome, silver, or rainbow reflection. Three
materials, one light.

## Relationship to the other layers

- **forge** (this term) — made. Dimensional surfaces, the 3-D world, the mark.
- **garden** — grown. Photography and light. See `night scene`, `brooding`.
- **livery** — said. Flat type and hairlines over the top of either.

Bronze appears in all three, but as brushed metal in the forge, as reflected
warm light in the garden, and as flat ink in the livery.
