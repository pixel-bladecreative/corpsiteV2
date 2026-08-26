# Pixel Blade — corporate site

**Before any design, art-direction, image-generation or site work, load the
`pixel-blade-lexicon` skill and read `brand/system/SYSTEM.md`.**

## The design system is five accepted parts. Nothing else.

| Part | Where |
|---|---|
| Foundations — three layers, tokens, one light | `brand/tokens.css` |
| The Dreamed Garden — the staged world, lit world, the ceiling | lexicon `terms/dreamed-garden.md`, `terms/lit-world.md` |
| Daylight Mode — `tech`, day/night switch | lexicon `terms/tech.md` |
| The Monk · The Samurai · The Ninja | lexicon `warrior/` — **load only when a figure is needed** |

Combined and canonical: **`brand/system/design-system.html`** →
https://claude.ai/code/artifact/7b3a9ec8-6548-4ccf-a503-4f64c7b97919

## What is NOT the system

`brand/marks/`, `brand/mark/`, `brand/forms/`, `brand/struck/` and the boards
`logo.html`, `struck.html`, `kerf.html`, `direction.html`, `materials.html`,
`dark-elegance-hero.html` are **archive**. Five logo rounds were proposed and all
five were rejected. They are kept so the same ground is not walked twice — see
`HANDOFF.md` for the kill list. **Do not treat any of it as approved.**

## Hard rules

- **`brand/tokens.css` is the authority on colour.** Never introduce a value that
  is not in it.
- **One raking light, low, upper left.** Two sources is a bug. Specular is a
  narrow near-white `#FEFEF5` line — never gold, never a bloom.
- **The lit-world boundary.** Saturated warm colour lives inside imagery only,
  and is forbidden in type, tiles, buttons, rules, borders and text sections.
- **The ceiling is coverage, not chroma.** ≤25% chroma coverage, ≥50% ground.
  Peak saturation is not a failure condition.
- **Run `brand/check-plate.py` on every generated plate.** `--day` for day mode,
  `--figure` for a Warrior portrait.
- **Feather and vignette every bright plate** into the page ground. A hard line
  of light against the night is wrong.
- Generate material plates **empty** and strike geometry into them in code.
  Image models produce logo-*pictures*, never marks.

## Working agreements

- Develop, commit and push **only** to `claude/pixel-blade-design-system-e4hviw`.
- **Do not open a pull request unless explicitly asked.**
- Prior work — the KAGE repo, "The Twig Snaps", the old corpsite, the original
  gold wireframe crane — is **inspiration only, never assets**.
- Standing instruction on `tech`: **stay in the dream**.
- Client accounts are read-only by default.
- `.git` is ~400 MB from early full-resolution PNG commits. Commit new imagery as
  JPEG. **Do not rewrite history without an explicit instruction.**
