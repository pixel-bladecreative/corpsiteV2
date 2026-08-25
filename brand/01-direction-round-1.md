> **SUPERSEDED (round two, 2026-08-25).** The palette section below is
> replaced by the material system in `tokens.css` and
> `board/materials.html`. Colors became materials; flat gold became
> brushed bronze; petrol teal was added as a second ground. The
> livery-over-garden thesis survives and gains a third layer (forge).
> Everything else here still stands.

# Round one — direction

Board: https://claude.ai/code/artifact/45f9c3e5-d4a7-4e96-b8be-9ddcada20cb0

## The thesis: livery over garden

Two layers, kept separate on purpose.

- **Garden** — warm, deep, emotional. What the visitor *moves through*.
- **Livery** — flat gold on dead black, exact to the hairline. What the visitor *reads*.

This replaces the "two brands" problem from round zero. Per Spencer: the split
*is* the product. Advertising is the emotional act; execution is the precise one.
*"Blades are no longer steel. Pixels."*

The warrior in the garden is the same structure: the garden is the discipline,
the warrior is the capability.

## Palette

Sampled from the generated assets. Tokens in `tokens.css`, contrast verified.

The load-bearing research detail: JPS ran **gold mylar** pinstripes and logos over
a **non-metallic** black body, with car numbers in **tan paint** — "more tan than
gold." That is what separates this from law-firm black-and-gold. Flat black,
warm dull gold, and the moss green from the garden layer keeping it off the shelf.

Key numbers:

| | |
|---|---|
| `--pb-kin` #C5A05F on ground | **7.99:1** — AAA, carries body text (rare for a gold) |
| `--pb-kin-deep` #6F582F | 2.90:1 — hairlines only, never text |
| `--pb-kin` on `--pb-washi` | **1.91:1** — unusable. The brand is dark-only |

## Marks

Four studies generated (Kie / nano-banana-2), prompts in `prompts/`, output in `assets/`.

| | Verdict | Note |
|---|---|---|
| **A · coachline** | Keep | Crane as pure fold lines at one hairline weight. Most on-thesis. Needs symmetry pass + true single-stroke redraw. |
| **D · blade-wing** | Keep | Best idea: reads blade first, crane second. Needs flattening (has gradients) and de-swooshing. |
| **C · kamon** | Hold | Real crest authority, but reads phoenix, too much gold mass, abandons fold lines. Drawer it as a seal/favicon. |
| **B · facet** | Cut | Generic gallery origami. Says nothing specific. |

**Recommendation:** D's idea in A's hand — the blade-wing double-read redrawn at a
single uniform pinstripe weight, flat, straight segments only. Then rebuilt as real
vector geometry. Everything currently in `assets/` is a raster comp.

## World plates

| | Job |
|---|---|
| `world-a-warrior` | Mood reference. Figure small and back-turned; skyline belongs. |
| `world-b-layers` | **The site's environment.** Three clean parallax planes. |
| `world-c-texture` | Texture/discipline plate. Raked gravel under grazing light. |

~80% of each frame is black — which is what leaves room for gold linework on top.

## Rules inherited by the system

1. **Two layers.** Garden colors never touch interface chrome; livery colors never appear inside photography.
2. **Gold is ink, not metal.** No gloss, bevel, gradient, or sheen.
3. **Line before fill.** Hairlines are the default material. Filled surfaces argue for themselves.
4. **No shadows.** One elevation step. Depth comes from the photographic layer behind.
5. **Dark by default.** Light contexts get a declared substitute.
6. **Straight segments.** Hard vertices, no blobs, in any brand-level drawing.
7. **Amber is light.** Never a background, button, or fill.

## Open

1. Is #C5A05F the right gold — richer, or closer to leaf?
2. A, D, or the hybrid?
3. Does the warrior ever appear, or only his garden?
4. Wordmark typeface — Bodoni Moda over Archivo is a proposal, not a decision.
5. How far does the Japanese surface go — kanji in the interface, or only environment and mark?

## Reproducing

```
export KIE_API_KEY=...
brand/kie-gen.py <slug> <aspect> brand/prompts/<file>.txt
```
Writes `brand/assets/<slug>.png` plus the CDN url. Model: `nano-banana-2`, 2K PNG.
