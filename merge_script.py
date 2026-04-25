"""
Incruit Sans v0.1 — Pretendard 한글 + Min Sans 라틴 합성

Strategy:
1. Pretendard을 base로 (units=2048, 한글 11,172자)
2. Min Sans Latin 글리프(U+0020~U+024F)만 추출 → 2048 UPM으로 스케일
3. Pretendard의 Latin 글리프를 Min Sans Latin으로 교체
4. 이름 변경, OFL 표기

라이선스: 두 폰트 모두 SIL Open Font License → 합성 산출물도 OFL.
"""

from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter, Options
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
import copy

print("Step 1: Pretendard을 base로 로드 (2048 UPM)")
base = TTFont('source/Pretendard-Regular.otf')
print(f"  base: {base['head'].unitsPerEm} UPM, {len(base.getBestCmap())} glyphs")

print("\nStep 2: Min Sans 로드 (1024 UPM) — Latin만 subset")
min_sans = TTFont('source/MinSans-Regular.otf')
print(f"  source: {min_sans['head'].unitsPerEm} UPM, {len(min_sans.getBestCmap())} glyphs")

# Min Sans에서 Latin 영역만 subset
opts = Options()
opts.layout_features = ['*']
opts.name_IDs = ['*']
opts.notdef_outline = True
opts.recalc_bounds = True
opts.drop_tables = ['DSIG']

subsetter = Subsetter(options=opts)
# Latin Basic (U+0020-007F) + Latin-1 Supplement (U+00A0-00FF) + Latin Extended-A (U+0100-017F) + Extended-B (U+0180-024F)
subsetter.populate(unicodes=list(range(0x0020, 0x0080)) + list(range(0x00A0, 0x0250)))
subsetter.subset(min_sans)
print(f"  Latin-only Min Sans: {len(min_sans.getBestCmap())} glyphs")

print("\nStep 3: Min Sans를 2048 UPM으로 스케일 (×2)")
# unitsPerEm 변경 + 모든 좌표 ×2
scale = 2048 / min_sans['head'].unitsPerEm
print(f"  scale factor: {scale}")

# CFF 폰트는 outline이 'CFF '/'CFF2' 테이블에 있음
# Pretendard는 CFF (otf), Min Sans도 CFF
# 두 폰트 모두 OTF/CFF이므로 같은 방식으로 처리

# 간단한 방법: setUnitsPerEm은 직접 지원이 없으므로 모든 메트릭과 outline 수동 스케일
def scale_font_inplace(font, factor):
    upm = font['head'].unitsPerEm
    new_upm = int(upm * factor)
    
    # head 테이블
    font['head'].unitsPerEm = new_upm
    for k in ['xMin','yMin','xMax','yMax']:
        setattr(font['head'], k, int(getattr(font['head'], k) * factor))
    
    # hhea
    for k in ['ascent','descent','lineGap','advanceWidthMax','minLeftSideBearing','minRightSideBearing','xMaxExtent','caretOffset']:
        setattr(font['hhea'], k, int(getattr(font['hhea'], k) * factor))
    
    # OS/2
    os2 = font['OS/2']
    for k in ['xAvgCharWidth','ySubscriptXSize','ySubscriptYSize','ySubscriptXOffset','ySubscriptYOffset',
              'ySuperscriptXSize','ySuperscriptYSize','ySuperscriptXOffset','ySuperscriptYOffset',
              'yStrikeoutSize','yStrikeoutPosition','sTypoAscender','sTypoDescender','sTypoLineGap',
              'usWinAscent','usWinDescent','sxHeight','sCapHeight']:
        if hasattr(os2, k):
            setattr(os2, k, int(getattr(os2, k) * factor))
    
    # hmtx (advance width, lsb)
    for glyph_name in font['hmtx'].metrics:
        adv, lsb = font['hmtx'].metrics[glyph_name]
        font['hmtx'].metrics[glyph_name] = (int(adv * factor), int(lsb * factor))
    
    # post
    if hasattr(font['post'], 'underlinePosition'):
        font['post'].underlinePosition = int(font['post'].underlinePosition * factor)
        font['post'].underlineThickness = int(font['post'].underlineThickness * factor)
    
    # CFF outlines
    if 'CFF ' in font:
        cff = font['CFF '].cff
        for fontname in cff.keys():
            top_dict = cff[fontname]
            char_strings = top_dict.CharStrings
            for glyph_name in char_strings.keys():
                cs = char_strings[glyph_name]
                # T2 CharString 재구성: Pen 통과
                pen = T2CharStringPen(int(cs.width * factor) if hasattr(cs, 'width') and cs.width else None, None)
                t_pen = TransformPen(pen, Transform(factor, 0, 0, factor, 0, 0))
                cs.draw(t_pen)
                new_cs = pen.getCharString(private=cs.private)
                char_strings[glyph_name] = new_cs
            # FontMatrix는 그대로
            if hasattr(top_dict, 'FontBBox'):
                top_dict.FontBBox = [int(v * factor) for v in top_dict.FontBBox]

scale_font_inplace(min_sans, scale)
print(f"  scaled to: {min_sans['head'].unitsPerEm} UPM")

print("\nStep 4: Pretendard에 Min Sans Latin 글리프 교체 삽입")
# 전략: Pretendard에서 Latin Unicode 코드포인트 → 글리프 이름 매핑
# Min Sans에서 같은 Unicode → 글리프 이름
# Pretendard의 해당 글리프를 Min Sans의 outline + advance로 교체

base_cmap = base.getBestCmap()
ms_cmap = min_sans.getBestCmap()

base_cff = base['CFF '].cff
ms_cff = min_sans['CFF '].cff
base_top = base_cff[base_cff.keys()[0]]
ms_top = ms_cff[ms_cff.keys()[0]]
base_cs = base_top.CharStrings
ms_cs = ms_top.CharStrings

replaced = 0
skipped = 0

# Unicode 0x20-0x024F 범위에서 두 폰트가 모두 가진 글자
for uni in list(range(0x0020, 0x0080)) + list(range(0x00A0, 0x0250)):
    if uni not in base_cmap or uni not in ms_cmap:
        continue
    base_glyph = base_cmap[uni]
    ms_glyph = ms_cmap[uni]
    
    if ms_glyph not in ms_cs:
        skipped += 1
        continue
    
    # Min Sans 글리프 → Pretendard로 복사
    # CharString을 깊은 복사 (private dict reference 주의)
    new_cs = copy.deepcopy(ms_cs[ms_glyph])
    # private을 base의 것으로 변경
    new_cs.private = base_cs[base_glyph].private
    new_cs.globalSubrs = base_cs[base_glyph].globalSubrs
    
    base_cs[base_glyph] = new_cs
    
    # advance width도 Min Sans 것으로 교체
    if ms_glyph in min_sans['hmtx'].metrics:
        ms_adv, ms_lsb = min_sans['hmtx'].metrics[ms_glyph]
        base['hmtx'].metrics[base_glyph] = (ms_adv, ms_lsb)
    
    replaced += 1

print(f"  Replaced: {replaced} latin glyphs ; Skipped: {skipped}")

print("\nStep 5: 폰트 메타데이터 변경 → Incruit Sans")
name_table = base['name']
new_family = "Incruit Sans"
new_full = "Incruit Sans Regular"
new_psname = "IncruitSans-Regular"
new_version = "Version 0.1; Built 2026-04-25; Pretendard Korean + Min Sans Latin"

# nameID 1=family, 2=subfamily, 4=full, 6=postscript, 16=preferred family
for record in name_table.names:
    if record.nameID == 1:
        record.string = new_family.encode(record.getEncoding())
    elif record.nameID == 4:
        record.string = new_full.encode(record.getEncoding())
    elif record.nameID == 6:
        record.string = new_psname.encode(record.getEncoding())
    elif record.nameID == 16:
        record.string = new_family.encode(record.getEncoding())
    elif record.nameID == 5:  # version
        record.string = new_version.encode(record.getEncoding())
    elif record.nameID == 13:  # license description
        record.string = ("Incruit Sans is a derivative of Pretendard (orioncactus) and Min Sans (Jinseong Kim), "
                        "both licensed under the SIL Open Font License 1.1. "
                        "This font may be freely used, modified, and redistributed under the same terms.").encode(record.getEncoding())

# CFF 내부의 fontname도 변경
base_cff.fontNames = ['IncruitSans-Regular']
base_top.FontName = 'IncruitSans-Regular'
if hasattr(base_top, 'FullName'):
    base_top.FullName = 'Incruit Sans Regular'
if hasattr(base_top, 'FamilyName'):
    base_top.FamilyName = 'Incruit Sans'

print("\nStep 6: 저장")
base.save('output/IncruitSans-Regular.otf')
print(f"  → output/IncruitSans-Regular.otf")

# 검증
result = TTFont('output/IncruitSans-Regular.otf')
rcmap = result.getBestCmap()
print(f"\n=== Output verification ===")
print(f"  Family: {result['name'].getDebugName(1)}")
print(f"  Full:   {result['name'].getDebugName(4)}")
print(f"  Version:{result['name'].getDebugName(5)}")
print(f"  Hangul: {sum(1 for c in rcmap if 0xAC00 <= c <= 0xD7AF)}")
print(f"  Latin:  {sum(1 for c in rcmap if 0x0020 <= c <= 0x024F)}")
print(f"  UPM:    {result['head'].unitsPerEm}")

