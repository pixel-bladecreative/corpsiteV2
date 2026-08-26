# struck

Output of `brand/strike.py`. Every image here is the flat mark geometry from
`brand/marks/` pressed into a material — nothing was drawn by hand or by an
image model.

Regenerate all of it with `make-struck.sh`. Material plates live in
`brand/assets/mat-*.png` and are generated empty, with nothing on them; the
geometry is struck into them in code. Never ask an image model to draw the
logo — it returns logo-*pictures*, not marks.

See `.claude/skills/pixel-blade-lexicon/terms/struck.md` for why.
