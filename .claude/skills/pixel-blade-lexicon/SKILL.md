---
name: pixel-blade-lexicon
description: Spencer's private visual vocabulary for the Pixel Blade brand — a growing set of shorthand words ("surreal", "scale", and others added over time) each anchored to real reference images and to the extracted mechanics that make those images work. Load this WHENEVER a Pixel Blade design, art-direction, image-generation, or site-build task is in play, and ALWAYS the moment Spencer uses one of the indexed terms below, so the word resolves to its actual referent instead of a generic reading. Also load when adding a new term or reference to the vocabulary.
---

# Pixel Blade visual lexicon

Spencer supplies reference images and tags each with one or more words. Those
words then become precise shorthand between him and Claude. This skill is where
the words live.

**The point:** when Spencer says "make it more surreal," that must not resolve
to a generic idea of surreal. It resolves to *this* mechanic, extracted from
*these* images.

## Protocol

**Using a term.** When Spencer uses an indexed word in a design context, read
`terms/<term>.md` before acting. The one-line summaries below are an index, not
the definition — they are too compressed to design from.

**Adding a term.** When Spencer supplies new references:

1. Look at the image. Name what is *mechanically* happening — composition,
   scale relationships, light behavior, palette, depth construction. Not mood
   words. A mechanic is something that can be executed.
2. Write or extend `terms/<term>.md` with those mechanics, plus explicit
   **borrow / don't borrow** lines. References are almost never adopted whole;
   say which part transfers.
3. Write `refs/<ref-id>.md` describing that specific image and tagging it.
4. Generate a **brand-native exemplar plate** — the same mechanic executed in
   the Pixel Blade palette — into `plates/`. This matters: a foreign reference
   shows the mechanic in someone else's colors, and the plate proves it survives
   translation into ours.
5. Add the one-liner to the index below.

**Storing sources.** Claude cannot write conversation attachments to disk. If a
source image should be kept verbatim, Spencer puts it in Drive or commits it to
`brand/refs/`, and the ref file records the path. Otherwise the written analysis
plus the brand-native plate *are* the record.

## Index

| Term | One line |
|---|---|
| `surreal` | Familiar objects of intimate scale, rendered monumentally, suspended in void with no explanation of support. Not fantasy — dislocation. |
| `scale` | A tiny human figure as the ruler that proves everything else is impossible. 1–3% of frame height, never more. |

## Standing constraints

Everything in this lexicon is subordinate to `brand/tokens.css` and the
livery-over-garden rule. A reference's *structure* transfers; its *palette*
usually does not. When a reference is more saturated than the brand, take the
composition and discard the color — and say so out loud rather than quietly
drifting the palette.
