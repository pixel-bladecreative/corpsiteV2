# Layout patterns

Spencer's references carry reusable *structure* as well as mood. Mood lives in
`terms/`; this is the structural half — the beginnings of the component system.

Each pattern names where it came from and whether it transfers whole.

---

## `tracked-stack`
**From:** `focus-poster`

Three or four short caps words stacked, at nearly the same type size, separated
only by **letter-spacing and opacity**. First line widest-tracked and in the
accent color; each subsequent line tighter and dimmer.

Use for: a values statement, a section opener, a chapter card. Do **not** use for
navigation — it is slow to read by design.

Implementation: same `font-size`, step `letter-spacing` down (e.g. `.42em` →
`.30em` → `.22em`) and `color` from `--pb-kin` → `--pb-washi` → `--pb-washi-dim`.

---

## `accent-word`
**From:** `auraplan`

A large headline in `--pb-washi` with exactly **one word** in `--pb-kin`. The
gold word carries the argument's turn — the noun the sentence is actually about.

Hard rule: one accent word per view. If the page has two, one of them is not the
point.

---

## `gold-ghost-pair`
**From:** `auraplan`

Primary: solid `--pb-kin`, text in `--pb-sumi` (7.99:1, verified), no radius or
minimal, no shadow. Secondary: transparent, 1px `--pb-hair` border, text in
`--pb-washi`. Equal height, sitting side by side.

Third-tier action, when needed: plain text link with a chevron and no border —
`quietlab`'s "Discover Our Process ›".

---

## `corner-brackets`
**From:** `quietlab`

Frame a region by drawing four thin L-shaped marks at its corners and nothing
else. Marks the boundary without enclosing it — a viewfinder rather than a box.

This is the brand-correct alternative to a card: it satisfies "hairlines over
boxes, no shadows, one elevation step" while still grouping content.

---

## `instrument-marks`
**From:** `focus-poster`

Plumb lines with dot nodes, edge tick scales, contour arcs, dot-matrix grids.
They read as measurement and navigation instruments — directly on-thesis for the
precision half of this brand.

**Guardrail (repeated from `terms/dark-elegance.md` because it is the one that
gets violated):** a mark must encode something true or be structurally
load-bearing. A tick scale marking real section positions, a plumb line that is
an actual scroll-progress indicator, a node at a real anchor. Sprinkled for
texture, these are the loudest tell of generated design. If it can't be
explained, delete it.

---

## `feature-strip`
**From:** `auraplan`

A horizontal row of three or four `icon + label` pairs, separated by thin
vertical rules, sitting at the bottom of the hero. Line icons only, single
weight, matching the hairline system. Labels in small tracked caps, two lines
max.

---

## `numbered-grid`
**From:** `glasshaven` — **structure only**

A row of four items, each with an image, a large outlined numeral, a short title
and two lines of copy. Numerals are large and set in outline or low-opacity fill
so they read as position markers, not headings.

Only use numerals when the items are **genuinely ordinal** — a real sequence or
ranked set. Four parallel services are not a sequence; numbering them is
decoration.

**Do not carry over** from this reference: the rounded-corner card, the slate
ground, or the ultra-bold wide display face. All three contradict rules already
set.

---

## `data-rows`
**From:** `glasshaven`

Label left, figure right, thin hairline between rows, no vertical rules, no
zebra striping. Figures set with `font-variant-numeric: tabular-nums` so the
column aligns.

This is the **proof register** — where the evidence voice lives. Set in
`--pb-mono`.

---

## `dark-half-type`
**From:** `auraplan`, `focus-poster`, `quietlab`

Compose or crop the photograph so a genuinely unlit region exists, and put the
type there. **Never** a scrim, a gradient overlay, or a blur-behind panel — those
are the admission that the image and the type were not designed together.

This is why `night-scene` specifies 70–85% of frame with no detail. The empty
region is not wasted photograph; it is the type's home.
