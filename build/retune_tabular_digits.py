"""Tabular digit center re-alignment patch.

Issue: All 10 digits share tabular advance (1222 UPM), but glyph centers drift
by up to 71 UPM, causing visual misalignment in financial/date columns.

Fix: For each digit, shift glyph contours so visual center = advance/2.
Update hmtx LSB to match. Both CFF (OTF) and glyf (TTF) handled.

Usage:
    python3 build/retune_tabular_digits.py <font_path> [<font_path> ...]
"""
import sys
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Offset

DIGITS = "0123456789"


def measure(font, gname):
    adv, lsb = font["hmtx"][gname]
    gs = font.getGlyphSet()
    bp = BoundsPen(gs)
    gs[gname].draw(bp)
    if bp.bounds is None:
        return adv, lsb, 0, 0, 0
    xMin, yMin, xMax, yMax = bp.bounds
    width = xMax - xMin
    return adv, lsb, width, xMin, xMax


def shift_glyf(font, gname, dx):
    """Shift TTF glyph contours by dx along X axis."""
    glyf = font["glyf"]
    glyph = glyf[gname]
    if glyph.numberOfContours == 0:
        return
    if hasattr(glyph, "coordinates"):
        for i in range(len(glyph.coordinates)):
            x, y = glyph.coordinates[i]
            glyph.coordinates[i] = (x + dx, y)
        # Refresh xMin/xMax
        glyph.recalcBounds(glyf)


def shift_cff(font, gname, dx):
    """Shift CFF charstring by dx via TransformPen + re-encode."""
    cff = font["CFF "].cff
    top = cff.topDictIndex[0]
    cs_dict = top.CharStrings
    cs = cs_dict[gname]

    # Get advance from hmtx (T2CharStringPen needs width)
    adv = font["hmtx"][gname][0]
    gs = font.getGlyphSet()

    pen = T2CharStringPen(adv, gs)
    transform = TransformPen(pen, Offset(dx, 0))
    gs[gname].draw(transform)

    new_cs = pen.getCharString(private=cs.private, globalSubrs=cs.globalSubrs)
    cs_dict[gname] = new_cs


def patch_font(path: Path):
    print(f"\n>>> {path}")
    font = TTFont(str(path))
    cmap = font.getBestCmap()
    is_cff = "CFF " in font

    # Gather digit metrics
    rows = []
    for d in DIGITS:
        cp = ord(d)
        gname = cmap.get(cp)
        if not gname:
            print(f"  skip: U+{cp:04X} not in cmap")
            continue
        adv, lsb, w, xMin, xMax = measure(font, gname)
        center = lsb + w / 2
        rows.append((d, gname, adv, lsb, w, xMin, xMax, center))

    if not rows:
        print("  no digits — skip")
        return

    advances = {r[2] for r in rows}
    if len(advances) > 1:
        print(f"  WARN: digits have multiple advances {advances} — not tabular")
    adv = rows[0][2]
    target_center = adv / 2.0

    print(f"  adv={adv}  target_center={target_center:.1f}  format={'CFF' if is_cff else 'glyf'}")
    print(f"  {'d':<4}{'gname':<14}{'lsb_old':>8}{'w':>6}{'cen_old':>10}{'shift':>8}{'lsb_new':>10}")

    for d, gname, adv, lsb, w, xMin, xMax, center in rows:
        shift = target_center - center
        shift_int = int(round(shift))
        new_lsb = int(round(lsb + shift_int))
        print(f"  {d:<4}{gname:<14}{lsb:>8}{w:>6.0f}{center:>10.1f}{shift_int:>8}{new_lsb:>10}")
        if shift_int == 0:
            continue
        if is_cff:
            shift_cff(font, gname, shift_int)
        else:
            shift_glyf(font, gname, shift_int)
        font["hmtx"][gname] = (adv, new_lsb)

    # Save
    font.save(str(path))
    print(f"  saved.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    for arg in sys.argv[1:]:
        patch_font(Path(arg))
