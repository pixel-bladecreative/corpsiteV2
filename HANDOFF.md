# Pixel Blade — session handoff

**Branch:** `claude/pixel-blade-design-system-e4hviw` · everything below is committed and pushed.

Read this before touching anything. It exists so the next session does not
re-litigate settled decisions or re-draw rejected work.

---

## 1 · The plan, and where we are

Spencer set the order at the outset and it has not changed:

> **(1) brand / design system → (2) inspiration → (3) site assembly → (4) assets → (5) content**

We are in **phase 1**. It is nearly complete. **The logo is the one thing still open**,
and it is the reason phase 1 has not closed.

Load `.claude/skills/pixel-blade-lexicon` at the start of any design work. It is a
project skill in this repo, so it survives the container; it is not in `~/.claude`.

---

## 2 · Settled — do not re-open without being asked

**The three-layer architecture.** `forge` (made — dimensional surfaces, lit, **and the
mark**) · `garden` (staged — the constructed world) · `livery` (said — flat type and
hairlines). Bronze appears in all three: brushed metal, emitted light, flat ink.

**`brand/tokens.css` is the authority.** Every value in it was measured off a generated
asset, never picked off a swatch, and every text pair has a recorded WCAG ratio. Load
it before writing any colour anywhere.

**Day/night.** Roles hold, values swap. Bronze fails at 2.05:1 on paper — that
limitation *is* the switch mechanism, and oxide takes bronze's role in day mode.

**The `lit world` rule.** Saturated coral / ember / rust are permitted **inside imagery**
and forbidden in type, tiles and text sections. The ceiling is **coverage, not chroma**:
≤25% chroma coverage, ≥50% ground. Peak saturation is explicitly *not* a failure
condition. Bright plates feather and vignette into the ground — never a hard line.

**One raking light, low, upper left.** Two sources is a bug. Specular is a narrow
near-white `#FEFEF5` line, never gold, never a bloom around a whole silhouette.

**The three Warriors** — Monk, Samurai, Ninja — are done, and live in
`lexicon/warrior/`. They are a **separate element, loaded only when a figure is
actually needed**. There is no adversary on the site; the Oni is deferred until video.

---

## 3 · The logo — still open

Four full rounds, all rejected by Spencer. **The kill list matters more than the
survivors.** Do not walk back into these.

| Round | What was built | Verdict |
|---|---|---|
| 1 | Generated logo concepts via image models | Image models produce logo-*pictures*, not marks. Never ask one to draw the logo. |
| 2 | Cut ensō — a ring cut by a line, minor arc slid. Plus a pixel-decay variant | Spencer kept both, then scrapped them |
| 3 | Crane brought back inside the ensō, occluding it | *"Nah. No good."* |
| 4 | The same geometry struck into materials — foil, coin, deboss, cut paper, aperture | Right instinct, wrong object. He meant scrap the *design*, not re-render it |
| 5 | **The kerf** — a solid disc, cut once, the piece slid along the cut, the removed material left in the gap as pixels | *"nope"* |

**Everything above is rejected.** `brand/marks/` (rounds 2–4) and `brand/mark/` +
`brand/forms/` (round 5) are kept only as a record.

### What was learned, and is worth keeping

- **Outlines were the mistake, and it survived four rounds.** None of Spencer's
  references contain a stroke. They build form from *adjacent planes at different
  values*, where the edge is simply where two values meet. That is why a rendered
  origami crane reads as folded paper.
- **The mark belongs in the forge, not the livery.** It is a made, lit object. A flat
  one-colour vector is the die, not the deliverable.
- Solid reads with weight; stroked rings are all line weight and air, and die small.
- A near-equal split reads as *a cut*; a thin sliver reads as *a moon phase*.
- Sliding a cut piece **along** the cut is a slip; **across** just separates it and
  reads as an eclipse.
- Pixel decay must **coarsen as it leaves**. Run the other way it reads as healing over.
- Watch for accidental reads: pie chart, loading spinner, prohibition sign ∅, bomb
  with a fuse, moon phase, butterfly, checkmark, swoosh. Each of these killed a
  candidate.
- Filed in the lexicon as `struck`, with all five of Spencer's material references
  analysed and borrow / don't-borrow lines written.

### The one idea still alive and homeless

**The aperture** — a ring that stops containing and becomes a *hole*, with a world
behind the page. It was the strongest thing in Spencer's reference set. A solid mark
cannot carry it. Best guess: it survives as a **site device**, not a logo — the ring
as a hole in the homepage with the garden moving behind it. Raise it in phase 3.

---

## 4 · Tools — all deterministic, all repeatable

Every measurable rule got a tool, because enforcement beats memory. Three scope bugs
in `check-plate.py` were found by new image kinds rather than by inspection.

| File | Does |
|---|---|
| `brand/check-plate.py` | **The QA gate.** `[--day] [--figure] <image>…` Fails on chroma coverage and edge seam, never on saturation. Run it on every plate. |
| `brand/strike.py` | Presses flat geometry into material. Modes: `foil` `deboss` `emboss` `coin` `papercut` `aperture` `inlay`. Ramps read from `tokens.css`. |
| `brand/feather.py` | `[--day] <in> <out> [inset]` — vignette to page ground. Working inset 0.10–0.14. |
| `brand/pixelate.py` | The Ninja's dissolve. Blocks **grow** as they travel; a loose block is redrawn at the size of where it *lands*, not where it came from. |
| `brand/kie-gen.py` | `<slug> <aspect> <promptfile> [model]` |
| `brand/make-struck.sh` | Regenerates the whole material set from current geometry |

**Gotchas already paid for:**
- PIL in this container **cannot blur float** — `GaussianBlur` rejects mode `F`.
  `strike.py` ships a float box-Gaussian. Do not round-trip a height field through
  8-bit; it quantises, and a quantised height field differentiates into visible rings.
- Kie: **seedream needs `image_size`** (e.g. `portrait_4_3`), *not* `aspect_ratio`,
  plus `image_resolution: "2K"` — capital K. `google/imagen4-ultra` errors
  consistently on this account. `nano-banana-2` is the workhorse.
- Generate material plates **empty**, then strike geometry into them in code.
- Background jobs die when the parent shell exits — always `( … & … & wait )`.
- Never put backticks in a commit message. Write it to a file and use `git commit -F`.
- `cd` inside a Bash call persists into the next call. Use absolute paths.

---

## 5 · Boards

**The system is five of these.** `brand/system/SYSTEM.md` is the manifest and
`brand/system/design-system.html` is the combined book:
https://claude.ai/code/artifact/7b3a9ec8-6548-4ccf-a503-4f64c7b97919


| Board | Status | Link |
|---|---|---|
| **Pixel Blade Design System — the book** | **canonical** | https://claude.ai/code/artifact/7b3a9ec8-6548-4ccf-a503-4f64c7b97919 |
| Livery Over Garden — round one | superseded | https://claude.ai/code/artifact/45f9c3e5-d4a7-4e96-b8be-9ddcada20cb0 |
| Dark Elegance Hero | superseded | https://claude.ai/code/artifact/9ef045f1-e169-420c-989b-c7c5254da3de |
| Forge Garden Livery — materials | superseded | https://claude.ai/code/artifact/ef2ec1fb-453e-4e59-94da-2242bd1f7eda |
| The Dreamed Garden — lit world, the ceiling | **IN THE SYSTEM** | https://claude.ai/code/artifact/46cd9cc9-d350-4a4c-a60f-847e298160c8 |
| Daylight Mode — `tech`, day/night switch | **IN THE SYSTEM** | https://claude.ai/code/artifact/5adc3660-9ccf-4a91-9aef-1fad06a2aa80 |
| The Monk | **IN THE SYSTEM** | https://claude.ai/code/artifact/47004346-cafc-4379-9bbf-acb41fcd6075 |
| The Samurai | **IN THE SYSTEM** | https://claude.ai/code/artifact/313ab567-ddb3-4fb5-b916-6b7bcc34c994 |
| The Ninja | **IN THE SYSTEM** | https://claude.ai/code/artifact/59c9e511-1170-47fc-9898-21d2b44f74d2 |
| The Cut Circle — mark, rounds 2–4 *(rejected)* | rejected | https://claude.ai/code/artifact/50710d23-310f-44cf-88f1-a3e5d82e2407 |
| Struck — the material argument | archive | https://claude.ai/code/artifact/5b5fe414-b926-42ee-b0ae-dbff880fed9e |
| The Kerf — fresh start *(rejected)* | rejected | https://claude.ai/code/artifact/3850e4b2-fb34-4668-b488-0f5073a30504 |

To update one, pass its URL as `url` — publishing without it makes a second artifact.

---

## 6 · Open

1. **The logo.** Five rounds rejected. Before drawing anything, ask Spencer what he is
   reacting *against* — the written record above shows what has failed, not what he
   wants. Consider showing rough directions early and cheap rather than one polished
   proposal per round; each of the five rounds spent a lot of effort before he could
   react to it.
2. **Typography is unargued.** Bodoni Moda / Archivo 300 / JetBrains Mono was a
   round-one proposal that has never been defended. It is the oldest unexamined thing
   in the system.
3. **No component specs** — button, nav, card — beyond one hero comp.
4. **No motion spec**, despite parallax, pixel dissolve and day↔night all being implied.
5. **Repo weight.** `.git` is ~400 MB from full-resolution PNGs committed in early
   rounds. New plates go in as JPEG. Clearing the existing weight needs a history
   rewrite — destructive, so **do not do it without an explicit instruction**.

---

## 7 · Working with Spencer

- He is direct and fast. Short, plain answers. No preamble.
- He gives references and expects the *mechanic* extracted, not the mood.
- Prior work — the KAGE repo, "The Twig Snaps", the old corpsite, the original gold
  wireframe crane — is **inspiration only, never assets**.
- Standing instruction on `tech`: **Stay in the Dream.**
- He wants "that layered, 3-D feel of moving through an environment", deferred to
  site-design mode.
- Kie for asset generation; premium tools allowed in moderation.
- Claude cannot write conversation attachments to disk. If a source image must be kept
  verbatim, Spencer commits it; otherwise the written analysis plus a brand-native
  plate *are* the record.
- Develop, commit and push **only** to `claude/pixel-blade-design-system-e4hviw`.
  Never push elsewhere without explicit permission. **Do not open a PR unless asked.**
- Client accounts are read-only by default — state exactly what will change and get an
  explicit yes before any write against one.
