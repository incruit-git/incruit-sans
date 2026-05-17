"""Fix j descender left overhang.

IncruitSans j has LSB=-132 (90 UPM more negative than Pretendard -42).
Causes overlap with 25 preceding glyphs (most severe: tj/fj/vj/yj ≥1px @ 24pt).

Fix: shift j contour right by +90 UPM. New LSB = -42 (matches Pretendard).
Advance unchanged. Visual: less aggressive leftward descender curl.

Idempotent: skips if LSB already >= -50.
"""
import sys
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Offset

J_TARGET_LSB = -42  # Pretendard original


def shift_glyf(font, gname, dx):
    glyf = font["glyf"]
    glyph = glyf[gname]
    if glyph.numberOfContours == 0:
        return
    if hasattr(glyph, "coordinates"):
        for i in range(len(glyph.coordinates)):
            x, y = glyph.coordinates[i]
            glyph.coordinates[i] = (x + dx, y)
        glyph.recalcBounds(glyf)


def shift_cff(font, gname, dx):
    cff = font["CFF "].cff
    top = cff.topDictIndex[0]
    cs_dict = top.CharStrings
    cs = cs_dict[gname]
    adv = font["hmtx"][gname][0]
    gs = font.getGlyphSet()
    pen = T2CharStringPen(adv, gs)
    transform = TransformPen(pen, Offset(dx, 0))
    gs[gname].draw(transform)
    cs_dict[gname] = pen.getCharString(private=cs.private, globalSubrs=cs.globalSubrs)


def fix_j(font, verbose=True):
    cmap = font.getBestCmap()
    j_gname = cmap.get(ord('j'))
    if not j_gname:
        if verbose: print("  no j glyph")
        return 0
    adv, lsb = font["hmtx"][j_gname]
    if lsb >= -50:
        if verbose: print(f"  j LSB={lsb} (already safe, skip)")
        return 0
    shift = J_TARGET_LSB - lsb  # positive
    new_lsb = lsb + shift
    if verbose:
        print(f"  j: lsb {lsb} → {new_lsb} (shift +{shift})")
    is_cff = "CFF " in font
    if is_cff:
        shift_cff(font, j_gname, shift)
    else:
        shift_glyf(font, j_gname, shift)
    font["hmtx"][j_gname] = (adv, new_lsb)
    return shift


def patch_path(path: Path):
    print(f">>> {path}")
    font = TTFont(str(path))
    s = fix_j(font, verbose=True)
    if s != 0:
        font.save(str(path))
        print("  saved.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    for arg in sys.argv[1:]:
        patch_path(Path(arg))
