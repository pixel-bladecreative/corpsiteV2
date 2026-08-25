# Samurai — the Day warrior

Plates: `plates/samurai-stand.png`, `plates/samurai-strike.png`,
`plates/samurai-dissolve.png`, `plates/samurai-enso.png` — feathered to the day
ground, verified with `check-plate.py --day --figure`.
Reference: four images supplied 2026-08-25. Not stored on disk.

Spencer: *"Inky, shadowed, the hat hides him from a sun he's not worthy of
receiving. He's learning to dance, but carries too much shadow... Sumi-e inkblot
mainly, with bursts of color behind his weapon that reveals what he might be once
he's done learning."*

And the correction that defines him: *"the parts of him that are complete need to
be HYPER-real, to lend solidity to the suggestion of his form. Act as if this is
a different warrior, whose solid parts are drawn by the same artist as the Monk."*

## The governing rule

**Where he is solid, he is a photograph. Where he is not, he is a brush stroke.**

The first pass got this wrong — the whole figure was rendered as flat sumi-e
silhouette, and Spencer's note names why that fails: *if everything is ink,
nothing is lost.* The dissolution only carries weight because what remains is
photographically real.

So the solid parts must hold **total material fidelity**, the same standard as
the Monk: every straw fibre and split in the hat, the coarse broken weave of the
outer robe, the real sheen and drape of the silk, individually grained prayer
beads, real weathered skin with sharp tendons, fibrous cord wrappings. Nothing
illustrated. Nothing painted.

The dissolution is the **only** stylised element in the image.

## Correction: he is not colourless

An earlier version of this file recorded that he carried no brand hue at all —
sampled at hue 60, saturation 11–13%. **That was an artifact of the failed first
prompt**, which asked for a pure ink silhouette and unsurprisingly returned a
neutral one. It described my mistake, not the character.

Measured properly, his cloth returns:

| | hue | saturation | reading |
|---|---|---|---|
| **Samurai** — student | 24–29 | **63–79** | **louder than the brand** |
| bronze — the brand itself | 29 | 59 | — |
| **Monk** — master | 28–34 | **5–45** | **quieter than the brand** |

**Same hue family throughout. Only the volume changes.**

The student is *over*-saturated — hotter than bronze itself. He is trying too
hard. The master has worn it down below the brand's own level. **Mastery is
turning it down**, which is the same argument the agency makes about advertising:
cut it back until the truth shows.

That is a far better finding than "he has no colour," and it only surfaced
because the first version was wrong.

## Mechanics

1. **ALWAYS the hat, and the face is ALWAYS shadowed.** Wide conical woven kasa.
   Beneath it, total black — no features at any angle, ever. Spencer was explicit
   that the reference's visible face is wrong.
2. **One amber coal.** A single small dim warm light inside the face shadow. It is
   the only warm light on him, and it is a **light source**, not a hue — the same
   rule as `--pb-andon`. It is the one thing he carries of what he will become.
3. **Hyper-real solids.** See the governing rule. This is what separates him from
   an illustration.
4. **Ragged transition.** The boundary where photograph becomes ink is uneven —
   abrupt in places, gradual in others. Never a clean line, never a soft fade
   applied uniformly.
5. **Layered.** Coarse black outer robe torn at the shoulder, warm ochre-mustard
   silk beneath, heavy wooden prayer beads, cord wrappings. Same layering logic
   as the Monk, different register.
6. **The weapon holds the colour.** `--pb-kindle` #2AD4C8 bleeds behind the blade
   only. Never on the figure.
7. **Dance, not violence.** Sweeping, unhurried, even mid-cut.
8. **Transit is dissolution.** `samurai-dissolve.png`: real from the ribs up, a
   churning column of wet ink below, a residue vortex where he was, a current
   between. He re-forms **hat first**.

## Relationship to the Monk

Spencer introduced him as "the Day warrior" and said to treat him as a different
warrior. That is how he is filed. But the two briefs do rhyme, and it is worth
recording rather than asserting:

| Samurai | Monk |
|---|---|
| hides from a sun he is not worthy of | *"no longer hiding from the sun"* |
| *"learning to dance"* | the movement **is** dance |
| *"carries too much shadow"* | dissolves into light |
| saturation 63–79 | saturation 5–45 |
| **carries a blade** | **hands empty, always** |

Whether that makes him an earlier form of the same man or a separate figure on a
parallel path is **Spencer's call, not an inference to act on.** Nothing in the
mechanics depends on the answer.

## Borrow / don't borrow

**Do not borrow the respirator or gas mask** from the reference. It reads as
cyber, which `tech` explicitly excludes.

**Do not borrow the visible face.** Spencer named it directly.

**Do not resolve him.** The pull under generation is toward a complete,
well-drawn character. Part of him must always be missing.

**Do not let the ochre creep past the cloth.** He runs hotter than bronze on
purpose; that heat belongs to his robes, not to anything around him.

## Verified

`check-plate.py --day --figure` — all four plates PASS at edge delta 0–1.

The figure flag exists because of these plates: a portrait legitimately fills more
frame than an environment, so the 50% ground floor was the wrong test for it. The
floor drops to 35% for figures; chroma and edge checks are unchanged.
