"""
Incruit Sans v0.2 — 9 weights 일괄 빌드
Pretendard 한글 + Min Sans 라틴 (각 9 weights)
"""
import copy
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter, Options
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform
from fontTools.pens.t2CharStringPen import T2CharStringPen

ROOT = Path(__file__).parent
SOURCE = ROOT / 'source'
BUILD = ROOT / 'build'
BUILD.mkdir(exist_ok=True)

WEIGHTS = [
    ('Thin', 100),
    ('ExtraLight', 200),
    ('Light', 300),
    ('Regular', 400),
    ('Medium', 500),
    ('SemiBold', 600),
    ('Bold', 700),
    ('ExtraBold', 800),
    ('Black', 900),
]


def scale_font_inplace(font, factor):
    upm = font['head'].unitsPerEm
    new_upm = int(upm * factor)
    font['head'].unitsPerEm = new_upm
    for k in ['xMin', 'yMin', 'xMax', 'yMax']:
        setattr(font['head'], k, int(getattr(font['head'], k) * factor))
    for k in ['ascent', 'descent', 'lineGap', 'advanceWidthMax', 'minLeftSideBearing',
              'minRightSideBearing', 'xMaxExtent', 'caretOffset']:
        setattr(font['hhea'], k, int(getattr(font['hhea'], k) * factor))
    os2 = font['OS/2']
    for k in ['xAvgCharWidth', 'ySubscriptXSize', 'ySubscriptYSize', 'ySubscriptXOffset',
              'ySubscriptYOffset', 'ySuperscriptXSize', 'ySuperscriptYSize',
              'ySuperscriptXOffset', 'ySuperscriptYOffset', 'yStrikeoutSize',
              'yStrikeoutPosition', 'sTypoAscender', 'sTypoDescender', 'sTypoLineGap',
              'usWinAscent', 'usWinDescent', 'sxHeight', 'sCapHeight']:
        if hasattr(os2, k):
            setattr(os2, k, int(getattr(os2, k) * factor))
    for glyph_name in font['hmtx'].metrics:
        adv, lsb = font['hmtx'].metrics[glyph_name]
        font['hmtx'].metrics[glyph_name] = (int(adv * factor), int(lsb * factor))
    if hasattr(font['post'], 'underlinePosition'):
        font['post'].underlinePosition = int(font['post'].underlinePosition * factor)
        font['post'].underlineThickness = int(font['post'].underlineThickness * factor)
    if 'CFF ' in font:
        cff = font['CFF '].cff
        for fontname in cff.keys():
            top_dict = cff[fontname]
            char_strings = top_dict.CharStrings
            for glyph_name in char_strings.keys():
                cs = char_strings[glyph_name]
                pen = T2CharStringPen(int(cs.width * factor) if hasattr(cs, 'width') and cs.width else None, None)
                t_pen = TransformPen(pen, Transform(factor, 0, 0, factor, 0, 0))
                cs.draw(t_pen)
                new_cs = pen.getCharString(private=cs.private)
                char_strings[glyph_name] = new_cs
            if hasattr(top_dict, 'FontBBox'):
                top_dict.FontBBox = [int(v * factor) for v in top_dict.FontBBox]


def build_one(weight_name, weight_value):
    pretendard_path = SOURCE / f'Pretendard-{weight_name}.otf'
    minsans_path = SOURCE / f'MinSans-{weight_name}.otf'
    if not pretendard_path.exists() or not minsans_path.exists():
        print(f"  SKIP {weight_name}: source missing")
        return False

    base = TTFont(str(pretendard_path))
    min_sans = TTFont(str(minsans_path))

    opts = Options()
    opts.layout_features = ['*']
    opts.name_IDs = ['*']
    opts.notdef_outline = True
    opts.recalc_bounds = True
    opts.drop_tables = ['DSIG']
    subsetter = Subsetter(options=opts)
    subsetter.populate(unicodes=list(range(0x0020, 0x0080)) + list(range(0x00A0, 0x0250)))
    subsetter.subset(min_sans)

    scale = 2048 / min_sans['head'].unitsPerEm
    scale_font_inplace(min_sans, scale)

    base_cmap = base.getBestCmap()
    ms_cmap = min_sans.getBestCmap()
    base_cff = base['CFF '].cff
    ms_cff = min_sans['CFF '].cff
    base_top = base_cff[base_cff.keys()[0]]
    ms_top = ms_cff[ms_cff.keys()[0]]
    base_cs = base_top.CharStrings
    ms_cs = ms_top.CharStrings

    replaced = 0
    for uni in list(range(0x0020, 0x0080)) + list(range(0x00A0, 0x0250)):
        if uni not in base_cmap or uni not in ms_cmap:
            continue
        base_glyph = base_cmap[uni]
        ms_glyph = ms_cmap[uni]
        if ms_glyph not in ms_cs:
            continue
        new_cs = copy.deepcopy(ms_cs[ms_glyph])
        new_cs.private = base_cs[base_glyph].private
        new_cs.globalSubrs = base_cs[base_glyph].globalSubrs
        base_cs[base_glyph] = new_cs
        if ms_glyph in min_sans['hmtx'].metrics:
            ms_adv, ms_lsb = min_sans['hmtx'].metrics[ms_glyph]
            base['hmtx'].metrics[base_glyph] = (ms_adv, ms_lsb)
        replaced += 1

    new_family = "Incruit Sans"
    new_style = weight_name
    new_full = f"Incruit Sans {weight_name}"
    new_psname = f"IncruitSans-{weight_name}"
    new_version = f"Version 0.2; weight={weight_value}; Built 2026-04-25"

    name_table = base['name']
    base['OS/2'].usWeightClass = weight_value

    for record in name_table.names:
        if record.nameID == 1:
            record.string = new_family.encode(record.getEncoding())
        elif record.nameID == 2:
            record.string = new_style.encode(record.getEncoding())
        elif record.nameID == 3:
            record.string = f"Incruit Sans;{weight_name};Version 0.2".encode(record.getEncoding())
        elif record.nameID == 4:
            record.string = new_full.encode(record.getEncoding())
        elif record.nameID == 5:
            record.string = new_version.encode(record.getEncoding())
        elif record.nameID == 6:
            record.string = new_psname.encode(record.getEncoding())
        elif record.nameID == 13:
            record.string = ("Incruit Sans is a derivative of Pretendard (orioncactus) and Min Sans "
                            "(Jinseong Kim), both licensed under SIL Open Font License 1.1. "
                            "Use, modify, and redistribute freely under the same terms.").encode(record.getEncoding())
        elif record.nameID == 16:
            record.string = new_family.encode(record.getEncoding())
        elif record.nameID == 17:
            record.string = new_style.encode(record.getEncoding())

    base_cff.fontNames = [new_psname]
    base_top.FontName = new_psname
    if hasattr(base_top, 'FullName'):
        base_top.FullName = new_full
    if hasattr(base_top, 'FamilyName'):
        base_top.FamilyName = new_family
    if hasattr(base_top, 'Weight'):
        base_top.Weight = weight_name

    output_path = BUILD / f'{new_psname}.otf'
    base.save(str(output_path))
    print(f"  ✓ {new_psname}.otf  (replaced {replaced} latin)")
    return True


print("Building 9 weights of Incruit Sans...")
for name, value in WEIGHTS:
    build_one(name, value)

print(f"\nDone. Output in: {BUILD}")
