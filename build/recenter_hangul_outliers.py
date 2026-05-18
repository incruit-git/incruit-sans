"""Re-center extreme Hangul outliers — consistent across weights.

Strategy:
  1. Identify outlier glyph SET from a reference weight (Regular).
     Criteria: |center - slot_center| > DRIFT_THRESHOLD_UPM
  2. Apply per-weight shift to that SAME glyph set in every font.
     Each weight computes its own shift based on its glyph metrics.

Why shared set: keeps glyph-to-glyph behavior consistent across weights.
Avoids "this glyph centered at Bold but drifts at Thin" inconsistency.

Threshold 100 UPM = ~0.7px @ 14pt — only fixes clearly visible drift.
"""
import sys
import statistics
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Offset

DRIFT_THRESHOLD_UPM = 100
MIN_SHIFT_UPM = 20
HANGUL_START = 0xAC00
HANGUL_END = 0xD7A4
REFERENCE_FONT = "build/IncruitSans-Regular.otf"

# Codepoints flagged as outliers from REFERENCE_FONT. Stored as codepoints
# (not glyph names) so they resolve via each font's own cmap — OTF uses CID
# names (cid09630), TTF uses uni names (uniD0A6). Same codepoint, different naming.


def measure(font, gname):
    adv, lsb = font["hmtx"][gname]
    gs = font.getGlyphSet()
    bp = BoundsPen(gs)
    gs[gname].draw(bp)
    if bp.bounds is None:
        return adv, lsb, 0, 0, 0
    xMin, yMin, xMax, yMax = bp.bounds
    return adv, lsb, xMax - xMin, xMin, xMax


def shift_glyf(font, gname, dx):
    glyph = font["glyf"][gname]
    if glyph.numberOfContours == 0:
        return
    if hasattr(glyph, "coordinates"):
        for i in range(len(glyph.coordinates)):
            x, y = glyph.coordinates[i]
            glyph.coordinates[i] = (x + dx, y)
        glyph.recalcBounds(font["glyf"])


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


def find_reference_outliers():
    """Return list of CODEPOINTS (from reference font) to be patched.

    Returns codepoints — not glyph names — so each target font resolves names
    via its own cmap (OTF uses CID names, TTF uses uni names).
    """
    font = TTFont(REFERENCE_FONT)
    cmap = font.getBestCmap()
    outliers_cp = []
    for cp in range(HANGUL_START, HANGUL_END):
        gname = cmap.get(cp)
        if not gname:
            continue
        adv, lsb, w, _, _ = measure(font, gname)
        if w == 0:
            continue
        center = lsb + w / 2.0
        slot_center = adv / 2.0
        if abs(center - slot_center) > DRIFT_THRESHOLD_UPM:
            outliers_cp.append(cp)
    return outliers_cp


def recenter_in_font(font, target_codepoints, verbose=True):
    """Patch the given codepoints in this font (per-font naming + shift)."""
    cmap = font.getBestCmap()
    is_cff = "CFF " in font
    patched = 0
    sample = 0
    for cp in target_codepoints:
        gname = cmap.get(cp)
        if not gname:
            if verbose: print(f"  skip U+{cp:04X}: not in cmap")
            continue
        adv, lsb, w, _, _ = measure(font, gname)
        if w == 0:
            continue
        center = lsb + w / 2.0
        slot_center = adv / 2.0
        shift = int(round(slot_center - center))
        if abs(shift) < MIN_SHIFT_UPM:
            continue
        new_lsb = lsb + shift
        if new_lsb < 0 or new_lsb > adv:
            if verbose: print(f"  skip {gname}: shift {shift} → invalid lsb={new_lsb}")
            continue
        if is_cff:
            shift_cff(font, gname, shift)
        else:
            shift_glyf(font, gname, shift)
        font["hmtx"][gname] = (adv, new_lsb)
        if verbose and sample < 3:
            print(f"  {chr(cp)} ({gname}): lsb {lsb}→{new_lsb} (shift {shift:+d})")
            sample += 1
        patched += 1
    if verbose:
        print(f"  Patched: {patched} of {len(target_codepoints)} target glyphs")
    return patched


def patch_path(path: Path, target_codepoints):
    print(f">>> {path}")
    font = TTFont(str(path))
    n = recenter_in_font(font, target_codepoints, verbose=True)
    if n > 0:
        font.save(str(path))
        print(f"  saved.")
    else:
        print(f"  no changes.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    print(f"=== Identifying outliers from {REFERENCE_FONT} ===")
    outliers = find_reference_outliers()
    print(f"Found {len(outliers)} outlier codepoints (drift > {DRIFT_THRESHOLD_UPM} UPM from slot center)")
    print(f"Outliers: {[f'U+{cp:04X} ({chr(cp)})' for cp in outliers]}")
    print()
    for arg in sys.argv[1:]:
        patch_path(Path(arg), outliers)
