#!/usr/bin/env bash
# Every material study, from the same geometry. Deterministic — rerun any time
# the mark changes and the whole set follows.
set -euo pipefail
cd "$(dirname "$0")/.."
M=brand/marks A=brand/assets O=brand/struck
s(){ python3 brand/strike.py "$@" >/dev/null; }

s foil     $M/06-enso-crane-cut.svg /tmp/s.png --plate $A/mat-paper-dark.png  --px 1600 --inset 0.58
s aperture $M/06-enso-crane-cut.svg /tmp/a.png --plate $A/world-aperture.png  --px 1600 --inset 0.74 --face 0.62
s inlay    $M/06-enso-crane-cut.svg /tmp/i.png --plate $A/world-aperture.png  --px 1600 --inset 0.72 --day
s coin     $M/06-enso-crane-cut.svg /tmp/c.png --plate $A/mat-marble.png      --px 1600 --inset 0.50 --rim
s coin     $M/01-cut-enso.svg       /tmp/d.png --plate $A/mat-marble.png      --px 1600 --inset 0.46 --rim
s deboss   $M/06-enso-crane-cut.svg /tmp/e.png --plate $A/mat-paper-cream.png --px 1600 --inset 0.60 --bevel 0.006
s emboss   $M/06-enso-crane-cut.svg /tmp/f.png --plate $A/mat-paper-cream.png --px 1600 --inset 0.60 --bevel 0.006
s papercut $M/06-enso-crane-cut.svg /tmp/g.png --plate x --px 1600 --inset 0.62 --sun 0.60
s papercut $M/06-enso-crane-cut.svg /tmp/h.png --plate x --px 1600 --inset 0.62 --day
# the lockup is 3.8:1, so it is struck square at a fine bevel and cropped after
s foil $M/lockup-06-enso-crane-cut.svg /tmp/l.png --plate $A/mat-paper-dark.png \
       --px 2600 --inset 0.94 --bevel 0.0011

python3 - <<'PY'
from PIL import Image
pairs = [("/tmp/s.png","foil-kraft"),("/tmp/a.png","aperture-night"),
         ("/tmp/i.png","inlay-day"),("/tmp/c.png","coin-bronze"),
         ("/tmp/d.png","coin-small"),("/tmp/e.png","deboss-cream"),
         ("/tmp/f.png","emboss-cream"),("/tmp/g.png","papercut-night"),
         ("/tmp/h.png","papercut-day")]
for src, name in pairs:
    Image.open(src).convert("RGB").save(f"brand/struck/{name}.jpg", quality=90, optimize=True)
im = Image.open("/tmp/l.png"); w, h = im.size
im.crop((0, int(h*.34), w, int(h*.66))).resize((1200, 384), Image.LANCZOS) \
  .convert("RGB").save("brand/struck/lockup-foil.jpg", quality=92, optimize=True)
PY
python3 brand/check-plate.py brand/struck/papercut-night.jpg
python3 brand/check-plate.py --day brand/struck/papercut-day.jpg
