# Pixel Blade — Brand Inventory & Open Tensions

Working document. Captures what already exists, what it implies, and the
decisions that have to be made before a style guide can become a design system.

Status: **discussion draft** — nothing here is settled.

---

## 1. What already exists

### 1.1 The mark (email signature)
Gold wireframe origami crane, black field, wordmark below in light-weight
letterspaced caps: `PIXEL BLADE`.

| Property | Observed | Note |
|---|---|---|
| Construction | Line only — no fills, no gradient, no metallic shading | Fold lines drawn as edges |
| Color | Warm gold, approx `#E5A823` (needs sampling from source) | Not sampled — estimated from raster |
| Field | Near-black, approx `#0A0A0A` | |
| Wordmark | Geometric sans, ~300 weight, wide tracking (~0.15em), all caps | Typeface unidentified |
| Format | Raster only | No vector master exists yet |

### 1.2 Prior draft — "Pixel Blade" (artifact, 2026-08-18)
The **rational / corporate** register. Single static page, no trackers.

- Type: Instrument Serif (display) · Inter (sans) · IBM Plex Mono (meta)
- Palette: `--ink #06070A` · `--bone #E9E7E2` · `--signal #FF5C35` · `--cold #7E93C4`
- Structure: 00 Index · 01 The shift · 02 Method · 03 Work · 04 Engagement · 05 Contact
- Positioning: GEO-led. "Search stopped listing and started answering."
- Closing line: **"We would rather be the source than the result."**
- Eight service lines, four-step method, "six clients, room for two"

### 1.3 Prior draft — "The Twig Snaps" (artifact, 2026-08-19)
The **emotional / manifesto** register. three.js scene, image collage, kanji rail.

- Type: Onest (variable 300–800) · Noto JP
- Palette: `--ink #080B0A` · `--bone #DFE7E0` · sage `#AAB4AD` / `#78837C` / `#4A534E`
  · `--blade #E24E2B` · `--ember #FF7A4D`
- Chapters: 00 The twig snaps · 01 Empathic · 02 Influence · 03 Feeling ·
  04 Cutting · 05 Warfare · 06 Begin
- Pillars (separate list): Focus · Authority · Emotion · Tribe
- Core parable: two men walk past the same bush for years; a twig snaps and the
  bush has their whole attention. *"Nothing you say matters until that happens."*
- Japanese layer: `創造者歓迎` ("builders welcome") as a decorative rail

---

## 2. The unifying idea (proposed)

**Fold lines.**

Classical origami reaches the form by folding, not cutting — kirigami is the
one that cuts. A crane drawn as a *wireframe* is the folds made visible: the
decisions, exposed. That is the same operation the agency sells — cut the
message back until one true thing stands, and show the reasoning that got there.

This reconciles the three parts that currently don't obviously belong together:

| Part | Reading under "fold lines" |
|---|---|
| The crane (mark) | The finished form — reached by removing, not adding |
| The blade (name) | The instrument. A pixel is the smallest unit of a screen; a blade acts at the smallest scale |
| "Cutting — until the truth shows" (ch. 04) | The method, stated |
| Senbazuru (1,000 cranes) | Patience and repetition — the same fold, done well, many times |

**Design consequences if adopted:**
- Line-first, never fill-first. 1px strokes are the default material.
- Geometry comes from folding: facets, hard vertices, straight runs. No blobs.
  Gradients are atmosphere only, never structure.
- Negative space is the material, not the leftover.
- Every stroke justifies itself. A component that can lose a rule, loses it.

---

## 3. Open tensions

### T1 — Gold vs. orange  *(blocking; everything downstream depends on it)*
The mark is gold. Both site drafts are orange-red. These are different brands.

| | Gold `#E5A823` | Signal orange `#FF5C35` |
|---|---|---|
| Reads as | Craft, permanence, patience | Heat, urgency, alarm |
| Contrast on `#0A0A0A` | **9.4:1** | 6.4:1 |
| Thin-stroke behavior on near-black | Glows, holds | Vibrates, muddies |
| Print / foil / physical | Excellent range | Poor |
| Saturation in market | Rare | The default "modern agency" accent |
| Risk | Luxury/crypto/law-firm cliché | Voiceless, indistinguishable |

Recommendation: **gold, single hue family.** Escape the luxury cliché by
treating gold as *ink*, not *metal* — flat, thin, no gloss, no bevel, no
gradient. Where a hotter interaction state is needed, push the same hue warmer
(amber → ember) rather than introducing a second competing accent.

### T2 — Two voices
"Twig Snaps" is belief. "Pixel Blade" is proof. Currently they read as two
brands. Proposal: one argument, two **registers**, with explicit rules —

| | Register A — Belief | Register B — Proof |
|---|---|---|
| Job | Earn attention, state the thesis | Substantiate it, price it |
| Density | Low | High |
| Type | Display serif, large | Sans + mono, small |
| Motion | Present | Minimal |
| Where | Opening, chapter heads | Services, method, engagement |

Belief opens, proof closes. Same page, same palette, declared transition.

### T3 — Taxonomy collision
Chapters (Empathic, Influence, Feeling, Cutting, Warfare, Begin) and pillars
(Focus, Authority, Emotion, Tribe) overlap and compete. One canonical set is
needed — it becomes the site IA, the deck sections, and the proposal structure.

Proposed five, as a sequence that mirrors the buyer's path:

1. **Attention** — the twig snaps. Nothing happens before it.
2. **Empathy** — be them.
3. **Emotion** — no one ever decided anything logically.
4. **Reduction** — cut until the truth shows.
5. **Tribe** — name the opponent; the buyer learns which side they're on.

Two items get reassigned rather than dropped:
- **"Influence, never manipulation"** — an *ethic that governs all five*, not a
  step among them. It is a constraint, so it should read as one.
- **Authority** — belongs to the proof register (GEO, citation, being the
  source), not the belief register.

### T4 — The Japanese layer
Crane, `創造者歓迎`, Noto JP, KAGE (影, "shadow") from the earlier repo.

The *principles* — ma, reduction, fold geometry — are load-bearing and already
doing work. The decorative kanji rail is the weak version: costume unless there
is a real reason behind it. Recommendation: keep the principles, cut the rail,
unless there is a specific reason to keep it (open question for Spencer).

### T5 — No vector master
The mark exists only as a raster. Before any system work: rebuild the crane as
clean vector geometry, at minimum three lockups (full, horizontal, glyph-only)
and a favicon-scale reduction that survives at 16px.

---

## 4. Unresolved / needs Spencer

- [ ] T1 — gold or orange
- [ ] T4 — keep or cut the Japanese surface layer
- [ ] Wordmark typeface — identify the existing one, or replace it deliberately
- [ ] Primary line: "We'd rather be the source than the result" (positioning)
      vs. "Builders welcome" (invitation) — can coexist; which leads?
- [ ] Real domain and contact (drafts use `pixelblade.example`)
- [ ] Client-facing scope: is this system for the site only, or also decks,
      proposals, reports, and email?
