"""OTF 9종 → 보간 호환 TTF 9종 → Variable Font 재빌드.

배경 (2026-07-05 실측): 기존 VF는 웨이트별 OTF→TTF 독립 변환으로 곡선 분할점이
어긋나 varLib이 곡선 글리프의 변형을 drop — 14,716 글리프 중 1,950개만 gvar 보유.
결과: wght=900에서 직선 글리프만 Black, 곡선 라틴 25자·한글 대부분 Regular 고정.

해법: Cu2QuMultiPen으로 9웨이트를 '동시에' 변환해 분할점을 통일 → 전 글리프
보간 호환 → varLib 재빌드 시 전 글리프 gvar 확보. + named instances 9종(fontbakery
B2) + STAT AxisValue.

실행:
  venv/bin/python3 build/build_ttf_vf.py ttf   # 9 OTF → build/ttf-pre-hint/*.ttf
  venv/bin/python3 build/build_ttf_vf.py vf    # ttf-pre-hint 9종 → build/IncruitSans-VF.ttf
"""
import sys
from pathlib import Path

from fontTools import varLib
from fontTools.designspaceLib import (AxisDescriptor, DesignSpaceDocument,
                                      InstanceDescriptor, SourceDescriptor)
from fontTools.otlLib.builder import buildStatTable
from fontTools.pens.cu2quPen import Cu2QuMultiPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont, newTable

ROOT = Path(__file__).parent.parent
BUILD = ROOT / 'build'
PRE_HINT = BUILD / 'ttf-pre-hint'

WEIGHTS = [('Thin', 100), ('ExtraLight', 200), ('Light', 300), ('Regular', 400),
           ('Medium', 500), ('SemiBold', 600), ('Bold', 700), ('ExtraBold', 800),
           ('Black', 900)]
MAX_ERR = 2.048  # UPM 2048 / 1000 (cu2qu 권장)


def _sig(rec):
    """세그 구조 시그니처 — (op, 좌표 수) 시퀀스. 마스터 간 동일해야 보간 호환."""
    return tuple((op, len(pts)) for op, pts in rec.value)


def build_ttfs():
    PRE_HINT.mkdir(exist_ok=True)
    fonts = [TTFont(str(BUILD / f'IncruitSans-{w}.otf')) for w, _ in WEIGHTS]
    order = fonts[0].getGlyphOrder()
    for f in fonts[1:]:
        assert f.getGlyphOrder() == order, 'glyph order mismatch across weights'
    glyphsets = [f.getGlyphSet() for f in fonts]

    n = len(fonts)
    tt_glyphs = [dict() for _ in range(n)]
    incompatible = []

    for gi, gname in enumerate(order):
        recs = []
        for gs in glyphsets:
            r = RecordingPen()
            gs[gname].draw(r)
            recs.append(r)
        sigs = {_sig(r) for r in recs}

        pens = [TTGlyphPen(None) for _ in range(n)]
        if len(sigs) == 1:
            # 9웨이트 병렬 변환 — 분할점 통일 (보간 호환)
            mpen = Cu2QuMultiPen(pens, MAX_ERR, reverse_direction=True)
            segs = [r.value for r in recs]
            for j in range(len(segs[0])):
                op = segs[0][j][0]
                if op in ('closePath', 'endPath'):
                    getattr(mpen, op)()
                else:
                    getattr(mpen, op)([segs[i][j][1] for i in range(n)])
        else:
            # 구조 불일치 — 개별 변환 (gvar 제외됨, 리포트)
            incompatible.append(gname)
            from fontTools.pens.cu2quPen import Cu2QuPen
            for r, pen in zip(recs, pens):
                p = Cu2QuPen(pen, MAX_ERR, reverse_direction=True)
                r.replay(p)
        for i in range(n):
            tt_glyphs[i][gname] = pens[i].glyph()
        if (gi + 1) % 2000 == 0:
            print(f'  … {gi + 1}/{len(order)} glyphs')

    print(f'  incompatible glyphs: {len(incompatible)}'
          + (f' → {incompatible[:20]}' if incompatible else ''))

    for (wname, _), font, glyphs in zip(WEIGHTS, fonts, tt_glyphs):
        glyf = newTable('glyf')
        glyf.glyphOrder = order
        glyf.glyphs = glyphs
        font['glyf'] = glyf
        font['loca'] = newTable('loca')
        del font['CFF ']
        if 'VORG' in font:
            del font['VORG']

        maxp = newTable('maxp')
        maxp.tableVersion = 0x00010000
        maxp.numGlyphs = len(order)
        for k in ('maxZones', 'maxTwilightPoints', 'maxStorage', 'maxFunctionDefs',
                  'maxInstructionDefs', 'maxStackElements', 'maxSizeOfInstructions',
                  'maxComponentElements', 'maxComponentDepth'):
            setattr(maxp, k, 1 if k == 'maxZones' else 0)
        font['maxp'] = maxp

        post = font['post']
        post.formatType = 2.0
        post.extraNames = []
        post.mapping = {}
        post.glyphOrder = order

        # TTF는 hmtx lsb == glyf xMin 이어야 함
        for gname in order:
            g = glyphs[gname]
            g.recalcBounds(glyf)
            adv, _ = font['hmtx'][gname]
            font['hmtx'][gname] = (adv, getattr(g, 'xMin', 0))

        # sfnt 서명 OTTO → TrueType (미변경 시 FreeType이 CFF 없다고 거부 — 2026-07-05 실측)
        font.sfntVersion = '\x00\x01\x00\x00'

        out = PRE_HINT / f'IncruitSans-{wname}.ttf'
        font.save(str(out))
        print(f'  ✓ {out.name}')
        font.close()


def build_vf():
    doc = DesignSpaceDocument()
    ax = AxisDescriptor()
    ax.tag, ax.name = 'wght', 'Weight'
    ax.minimum, ax.default, ax.maximum = 100, 400, 900
    doc.addAxis(ax)
    for wname, val in WEIGHTS:
        s = SourceDescriptor()
        s.path = str(PRE_HINT / f'IncruitSans-{wname}.ttf')
        s.location = {'Weight': val}
        doc.addSource(s)
        inst = InstanceDescriptor()
        inst.familyName = 'Incruit Sans'
        inst.styleName = wname
        inst.postScriptFontName = f'IncruitSans-{wname}'
        inst.location = {'Weight': val}
        doc.addInstance(inst)

    vf, _, _ = varLib.build(doc)

    # 네이밍 — 기존 VF 관례 미러
    name = vf['name']
    name.setName('Incruit Sans Variable', 1, 3, 1, 0x409)
    name.setName('Regular', 2, 3, 1, 0x409)
    name.setName('Incruit Sans;Regular;Version 0.2', 3, 3, 1, 0x409)
    name.setName('Incruit Sans Variable', 4, 3, 1, 0x409)
    name.setName('Version 0.2; variable; Built 2026-07-05', 5, 3, 1, 0x409)
    name.setName('IncruitSans-Variable', 6, 3, 1, 0x409)
    name.setName('Incruit Sans', 16, 3, 1, 0x409)
    name.setName('Regular', 17, 3, 1, 0x409)
    name.removeNames(platformID=1)
    vf['head'].fontRevision = 0.2

    # STAT AxisValues (fontbakery B2)
    stat_values = []
    for wname, val in WEIGHTS:
        v = dict(value=val, name=wname)
        if val == 400:
            v['flags'] = 0x2          # ElidableAxisValueName
            v['linkedValue'] = 700    # Regular ↔ Bold 링크
        stat_values.append(v)
    buildStatTable(vf, [dict(tag='wght', name='Weight', ordering=0,
                             values=stat_values)], elidedFallbackName='Regular')

    out = BUILD / 'IncruitSans-VF.ttf'
    vf.save(str(out))

    # 검증 요약
    vf2 = TTFont(str(out), lazy=True)
    n_inst = len(vf2['fvar'].instances)
    gvar_n = sum(1 for g, tv in vf2['gvar'].variations.items() if tv)
    print(f'  ✓ {out.name}  instances={n_inst}  glyphs-with-gvar={gvar_n}')


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if mode in ('ttf', 'all'):
        print('[1/2] OTF → 보간 호환 TTF 9종')
        build_ttfs()
    if mode in ('vf', 'all'):
        print('[2/2] varLib VF 재빌드')
        build_vf()
