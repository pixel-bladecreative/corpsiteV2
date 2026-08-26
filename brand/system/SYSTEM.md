# Pixel Blade Design System — accepted core

**Status: phase one, five parts accepted.** Confirmed by Spencer 2026-08-26.

Canonical combined document: `design-system.html` →
https://claude.ai/code/artifact/7b3a9ec8-6548-4ccf-a503-4f64c7b97919

---

## In the system

| # | Part | Board of record | Source of truth |
|---|---|---|---|
| 00 | **Foundations** — three layers (forge / garden / livery), the material palette, one raking light, the day↔night switch | — | `brand/tokens.css` |
| 01 | **The Dreamed Garden** — the world, built not found; the two-gamut lit-world rule; the coverage ceiling; the feathered edge | [garden](https://claude.ai/code/artifact/46cd9cc9-d350-4a4c-a60f-847e298160c8) | lexicon `terms/dreamed-garden.md`, `terms/lit-world.md` |
| 02 | **Daylight Mode** — `tech`; ninety degrees; lines that overshoot and fade; diorama not building; the day palette | [daylight](https://claude.ai/code/artifact/5adc3660-9ccf-4a91-9aef-1fad06a2aa80) | lexicon `terms/tech.md` |
| 03 | **The Monk** — final form, photoreal cloth, hands empty, crosses both modes without adaptation | [monk](https://claude.ai/code/artifact/47004346-cafc-4379-9bbf-acb41fcd6075) | lexicon `warrior/monk.md` |
| 03 | **The Samurai** — the Day warrior; hyper-real where solid, ink where not; always hatted, face always shadowed | [samurai](https://claude.ai/code/artifact/313ab567-ddb3-4fb5-b916-6b7bcc34c994) | lexicon `warrior/samurai.md` |
| 03 | **The Ninja** — Aramaki anime; hood and cyber mask, never a face; graduated pixel dissolution | [ninja](https://claude.ai/code/artifact/59c9e511-1170-47fc-9898-21d2b44f74d2) | lexicon `warrior/ninja.md` |

The three Warriors are **one part, loaded on demand**. They are not a mode, a
palette or a term, and they are never loaded for ordinary design or layout work.

### Enforcement

`check-plate.py` (the gate) · `feather.py` (the edge) · `pixelate.py` (the
dissolve) · `tokens.css` (the authority). Every measurable rule is executable.

### Figures

`fig/` holds the approved plates, extracted from the five boards of record. They
are the only imagery that carries system approval.

---

## Not in the system

Kept for the record only. **Nothing below is approved.**

| Item | Status |
|---|---|
| `brand/marks/` · `brand/mark/` · `brand/forms/` | Five rejected logo rounds |
| `brand/struck/` | Material studies of a rejected mark |
| `brand/board/logo.html` · `struck.html` · `kerf.html` | Rejected mark boards |
| `brand/board/direction.html` · `materials.html` · `dark-elegance-hero.html` | Superseded. Their surviving conclusions live in `tokens.css` and in the lexicon terms above. |
| Oni / adversary | Struck. No enemy is shown. Revisit only with video. |

**Load-bearing note.** The `material` lexicon term (palette-as-materials, the
single raking light) originated on a board now listed as superseded. The term
itself is still load-bearing for all five accepted parts, and its conclusions are
carried in `tokens.css`. Superseding the *board* does not retire the *rule*.

---

## Open

The mark · typography · component specs · a motion spec · the homeless aperture
idea · site design. See `HANDOFF.md`.
