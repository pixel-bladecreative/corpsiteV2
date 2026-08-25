# Warrior

**A separate element. Load only when a figure is needed.**

Not a mode, not a palette, not a term in the main lexicon. Warrior is the cast —
figures called on when the work needs a person to make a point, and silent the
rest of the time. Nothing here is loaded for ordinary design or layout work.

Spencer's instruction: *"Don't integrate this into either Day or Night. Treat as
a separate element called Warrior, loaded only when we need it."*

## Why it is separable — and why it still belongs

The Monk crosses both modes without adaptation, and the reason is measurable
rather than aesthetic. See `monk.md` for the numbers; in short, his wardrobe
spans the full value range, so on a dark ground his light layers carry him and on
a light ground his dark layers do.

He is also not a foreign body. His cloth quantizes at **hue 28–34** — bronze is
hue 29. He is the brand's own hue family, worn down and desaturated. That is why
he never looks pasted into these environments.

## Roster

| Figure | Status |
|---|---|
| **Monk** — final form | `monk.md`. Three plates, both modes verified. Hue 28–34 at saturation 5–45. Hands empty. |
| **Samurai** — the Day warrior | `samurai.md`. Four plates, day mode verified. Hue 24–29 at saturation 63–79. Always hatted, face always shadowed, carries a blade. |
| **Oni** — adversary | Pending. Named as an opponent the Monk fights. |

**Saturation is the axis.** Both figures sit in the same hue family — 24–34,
which is bronze's family — and differ only in volume:

    Samurai  sat 63–79   louder than the brand
    bronze   sat 59      the brand itself
    Monk     sat  5–45   quieter than the brand

The student is over-saturated; he is trying too hard. The master has worn it
below the brand's own level. **Mastery is turning it down** — the same argument
the agency makes about advertising.

Whether the Samurai is an earlier form of the Monk or a separate figure on a
parallel path is **Spencer's call.** The briefs rhyme (hiding from the sun vs. no
longer hiding, learning to dance vs. dance as movement, blade vs. empty hands) but
that is an observation, not a decision.

## Rules for every Warrior figure

These are expected to hold across the whole cast, not just the Monk. Revisit when
the second figure lands.

1. **The figure is sharp. The motion is around him.** Never motion-blurred. The
   movement lives in ink ribbons, dissolving particles and streaming cloth. This
   is what lets a figure read as moving while standing still.
2. **He dissolves at the edges.** Hems, sleeves, the away side — breaking into
   drifting particles and mist. Never fully contained by his own outline.
3. **The face is at rest.** Eyes down or closed, no aggression, no strain, no
   shout. The violence is in the body. This is the warrior-in-a-garden idea
   compressed into one figure, and it is the rule most likely to be broken by a
   generator asked for "action."
4. **Layered cloth, many weaves.** Never a single garment. Distinct layers at
   distinct values and textures — the same layering logic as the tech diorama and
   the fold language.
5. **Ink ribbons carry the brand colour.** The cloth stays desaturated; petrol
   teal and bronze/rust enter through the brushwork. That is the integration
   point, and the only place saturation belongs on a figure.
6. **Placement decides the mode, not the figure.** Feather to the destination
   ground: `feather.py --day` for paper, plain for sumi. Verify with
   `check-plate.py [--day]`.
7. **A figure's SATURATION states where it is.** Every figure sits in bronze's
   hue family; how loudly they wear it is the characterisation. A new figure's
   saturation should be a deliberate answer to "how far along is this one."
8. **Where a figure is solid, it is a photograph.** Total material fidelity —
   real weave, real fraying, real skin. Any stylisation is confined to what is
   dissolving. If everything is stylised, nothing reads as lost.
9. **`--pb-kindle` #2AD4C8 belongs to blades only.** The one colour in the system
   that means potential rather than material. Never on a figure, never in type,
   never anywhere but behind a weapon.

## Adding a figure

Same protocol as the main lexicon: read the references, name the mechanics, write
borrow / don't-borrow, generate brand-native plates in **both** modes, verify with
the checker, and record what failed.
