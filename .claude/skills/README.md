# Project skills

## taste-skill (vendored)

Thirteen frontend design / art-direction skills from
[Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill), MIT licensed
(see `LICENSE.taste-skill`).

Vendored into this repo rather than installed as a plugin so they load
automatically in every session on `corpsiteV2` — including ephemeral remote
containers, where `~/.claude/skills` does not persist.

**Source commit:** `72e2995` (2026-08-22)

Each skill is a single self-contained `SKILL.md` — no scripts, assets, or
relative file dependencies. Directory names use the skill's frontmatter `name`,
which differs from the upstream folder name in several cases.

### Runs here (instruction-only skills)

| Skill | Use |
|---|---|
| `design-taste-frontend` | Main anti-slop skill. Reads brief, infers direction, ships non-templated interfaces. 87KB — the substantial one. |
| `design-taste-frontend-v1` | Preserved v1 behavior. Only for backward compatibility. |
| `redesign-existing-projects` | Audit-first upgrade of an existing site. Identifies generic AI patterns. |
| `high-end-visual-design` | Fonts, spacing, shadows, card structure, animation — what makes a site feel expensive. |
| `minimalist-ui` | Warm monochrome, typographic contrast, flat bento. No gradients or heavy shadows. |
| `industrial-brutalist-ui` | Swiss print × military terminal. Rigid grids, extreme type scale contrast, analog degradation. |
| `gpt-taste` | GSAP motion engineering, AIDA structure, wide editorial type, strict ScrollTriggers. |
| `stitch-design-taste` | Emits a `DESIGN.md` semantic design system for agent consumption. |
| `full-output-enforcement` | Bans truncation and placeholder patterns. Utility, composes with the others. |

### Needs an image-generation tool (not available in this session)

`brandkit` · `imagegen-frontend-web` · `imagegen-frontend-mobile` ·
`image-to-code`

These are prompt/art-direction systems that assume the host can render images.
Without a generation tool they still produce usable art direction and prompts,
but cannot produce the boards themselves.

### Pruning

All thirteen descriptions load into the skill listing every session. If that
becomes noise, delete the directories that aren't earning their place —
`design-taste-frontend-v1` and the mobile/stitch skills are the first cuts for
this project.
