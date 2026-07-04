"""Incruit Sans VF v2 — Pretendard Variable 기반 재건.

배경 (2026-07-05 실측):
- 기존 VF: 정적 OTF 9종을 웨이트별 독립 변환 → 곡선 분할점 불일치로
  14,716 글리프 중 1,950개만 gvar → wght=900에서 한글·곡선 라틴 Regular 고정.
- 정적 9종은 웨이트 간 윤곽 구조 자체가 달라(비호환 8,473 · 전곡선 정규화로도
  8,254 잔존) 보간 불가 — 정적→VF 경로는 근본적으로 막힘.

해법:
1. 한글·기호: PretendardVariable.ttf(공식, 보간 설계 원본, gvar 14,742개) 그대로,
   축만 45–930 → 100–900 제한 (instancer L3).
2. 라틴(0x20-0x7F, 0xA0-0x24F): build/ttf-pre-hint 9종(Cu2QuMultiPen 보간 호환,
   l-tail·0-dot·tabular retune·j fix 포함)을 서브셋 → varLib으로 라틴 VF 빌드 →
   glyf 기본 윤곽 + gvar 튜플 + hmtx를 Pretendard VF에 글리프 단위 이식.
   양쪽 모두 axis 100/400/900·avar 없음 → 정규화 공간 동일, 튜플 직이식 가능.
3. fvar named instances 9종 + STAT AxisValue + 네이밍/버전/Mac name 제거
   (fontbakery B1·B2·B3).

실행: venv/bin/python3 build/build_vf_v2.py
"""
import sys
from pathlib import Path

from fontTools import varLib
from fontTools.designspaceLib import (AxisDescriptor, DesignSpaceDocument,
                                      SourceDescriptor)
from fontTools.otlLib.builder import buildStatTable
from fontTools.pens.cu2quPen import Cu2QuMultiPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.subset import Options, Subsetter
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

sys.path.insert(0, str(Path(__file__).parent))
from compat_fix import compatibilize, draw_multi

ROOT = Path(__file__).parent.parent
BUILD = ROOT / 'build'
PRE_HINT = BUILD / 'ttf-pre-hint'
SOURCES = ROOT / 'source'   # PretendardVariable.ttf (공식 v1.3.x, OFL) 포함

WEIGHTS = [('Thin', 100), ('ExtraLight', 200), ('Light', 300), ('Regular', 400),
           ('Medium', 500), ('SemiBold', 600), ('Bold', 700), ('ExtraBold', 800),
           ('Black', 900)]
LATIN_UNICODES = list(range(0x0020, 0x0080)) + list(range(0x00A0, 0x0250))


def _tt_sig(glyph, glyf):
    """TTF 글리프 구조 시그니처 — 마스터 간 다르면 varLib 스킵 대상."""
    if glyph.numberOfContours <= 0:
        return ('n', glyph.numberOfContours)
    return (tuple(glyph.endPtsOfContours), len(glyph.coordinates))


def fix_incompatible(subset_fonts):
    """서브셋 TTF 9종에서 구조 불일치 글리프를 OTF 원본에서 호환화해 재주입."""
    otfs = [TTFont(str(BUILD / f'IncruitSans-{w}.otf')) for w, _ in WEIGHTS]
    ogsets = [f.getGlyphSet() for f in otfs]
    ocmaps = [f.getBestCmap() for f in otfs]
    scmap = subset_fonts[3].getBestCmap()

    fixed, unfixable = [], []
    for uni in LATIN_UNICODES:
        gname = scmap.get(uni)
        if not gname:
            continue
        sigs = {_tt_sig(f['glyf'][gname], f['glyf']) for f in subset_fonts}
        if len(sigs) == 1:
            continue
        recs = []
        for gs, cm in zip(ogsets, ocmaps):
            r = RecordingPen()
            gs[cm[uni]].draw(r)
            recs.append(r.value)
        aligned = compatibilize(recs)
        if aligned is None:
            unfixable.append(chr(uni))
            continue
        pens = [TTGlyphPen(None) for _ in WEIGHTS]
        mpen = Cu2QuMultiPen(pens, 2.048, reverse_direction=True)
        draw_multi(aligned, mpen)
        for f, pen in zip(subset_fonts, pens):
            g = pen.glyph()
            f['glyf'][gname] = g
            g.recalcBounds(f['glyf'])
            adv, _ = f['hmtx'][gname]
            f['hmtx'][gname] = (adv, getattr(g, 'xMin', 0))
        fixed.append(chr(uni))
    print(f'  호환화: {len(fixed)}자 성공, 불가 {len(unfixable)}자 '
          f'{"".join(unfixable) if unfixable else ""}')


def build_latin_vf():
    """pre-hint TTF 9종을 라틴 서브셋 + 호환화 후 varLib으로 라틴 VF 빌드."""
    tmp = BUILD / 'tmp-latin'
    tmp.mkdir(exist_ok=True)
    subset_fonts = []
    for wname, _ in WEIGHTS:
        f = TTFont(str(PRE_HINT / f'IncruitSans-{wname}.ttf'))
        opts = Options()
        opts.layout_features = []
        opts.drop_tables += ['GSUB', 'GPOS', 'GDEF']
        opts.notdef_outline = True
        opts.recalc_bounds = True
        ss = Subsetter(options=opts)
        ss.populate(unicodes=LATIN_UNICODES)
        ss.subset(f)
        subset_fonts.append(f)

    fix_incompatible(subset_fonts)
    for (wname, _), f in zip(WEIGHTS, subset_fonts):
        f.save(str(tmp / f'{wname}.ttf'))

    doc = DesignSpaceDocument()
    ax = AxisDescriptor()
    ax.tag, ax.name = 'wght', 'Weight'
    ax.minimum, ax.default, ax.maximum = 100, 400, 900
    doc.addAxis(ax)
    for wname, val in WEIGHTS:
        s = SourceDescriptor()
        s.path = str(tmp / f'{wname}.ttf')
        s.location = {'Weight': val}
        doc.addSource(s)
    latin_vf, _, _ = varLib.build(doc)
    n = sum(1 for g, tv in latin_vf['gvar'].variations.items() if tv)
    print(f'  라틴 VF: {latin_vf["maxp"].numGlyphs} 글리프, gvar {n}개')
    return latin_vf


def main():
    print('[1/4] Pretendard Variable 축 제한 45-930 → 100-900')
    base = TTFont(str(SOURCES / 'PretendardVariable.ttf'))
    instancer.instantiateVariableFont(base, {'wght': (100, 400, 900)},
                                      inplace=True, updateFontNames=False)
    ax = base['fvar'].axes[0]
    print(f'  축: {ax.axisTag} {ax.minValue}-{ax.defaultValue}-{ax.maxValue}, '
          f'instances={len(base["fvar"].instances)}')

    print('[2/4] 라틴 VF 빌드 (pre-hint 9종 → varLib)')
    latin = build_latin_vf()

    print('[3/4] 라틴 글리프 이식 (glyf + gvar + hmtx)')
    b_cmap = base.getBestCmap()
    l_cmap = latin.getBestCmap()
    b_glyf, l_glyf = base['glyf'], latin['glyf']
    b_gvar, l_gvar = base['gvar'], latin['gvar']
    replaced = skipped = 0
    for uni in LATIN_UNICODES:
        bg, lg = b_cmap.get(uni), l_cmap.get(uni)
        if not bg or not lg:
            continue
        glyph = l_glyf[lg]
        if glyph.isComposite():   # 서브셋 라틴 VF에 컴포지트 잔존 시 이식 불가
            skipped += 1
            continue
        b_glyf[bg] = glyph
        b_gvar.variations[bg] = l_gvar.variations.get(lg, [])
        base['hmtx'][bg] = latin['hmtx'][lg]
        replaced += 1
    print(f'  이식 {replaced} · 스킵(컴포지트) {skipped}')

    print('[4/4] 네이밍·STAT·instances·메트릭 정합')
    name = base['name']
    name.setName('Incruit Sans Variable', 1, 3, 1, 0x409)
    name.setName('Regular', 2, 3, 1, 0x409)
    name.setName('Incruit Sans;Regular;Version 0.2', 3, 3, 1, 0x409)
    name.setName('Incruit Sans Variable', 4, 3, 1, 0x409)
    name.setName('Version 0.2; variable; Built 2026-07-05', 5, 3, 1, 0x409)
    name.setName('IncruitSans-Variable', 6, 3, 1, 0x409)
    name.setName('Incruit Sans', 16, 3, 1, 0x409)
    name.setName('Regular', 17, 3, 1, 0x409)
    # 라이선스 설명 (정적판과 동일)
    name.setName('Incruit Sans is a derivative of Pretendard (orioncactus) and '
                 'Min Sans (Jinseong Kim), both licensed under SIL Open Font '
                 'License 1.1. Use, modify, and redistribute freely under the '
                 'same terms.', 13, 3, 1, 0x409)
    base['head'].fontRevision = 0.2          # fontbakery B1

    # fvar instance 이름을 우리 name 테이블 기준으로 재설정
    fvar = base['fvar']
    inst_by_wght = {int(i.coordinates['wght']): i for i in fvar.instances}
    assert len(inst_by_wght) == 9, f'instances={len(fvar.instances)}'
    for wname, val in WEIGHTS:
        inst = inst_by_wght[val]
        inst.subfamilyNameID = name.addName(wname, platforms=((3, 1, 0x409),))
        inst.postscriptNameID = name.addName(f'IncruitSans-{wname}',
                                             platforms=((3, 1, 0x409),))

    stat_values = []
    for wname, val in WEIGHTS:
        v = dict(value=val, name=wname)
        if val == 400:
            v['flags'] = 0x2
            v['linkedValue'] = 700
        stat_values.append(v)
    buildStatTable(base, [dict(tag='wght', name='Weight', ordering=0,
                               values=stat_values)],
                   elidedFallbackName='Regular')
    # Mac name 제거는 buildStatTable(멀티플랫폼 name 추가) 뒤에 (fontbakery B3)
    name.removeNames(platformID=1)

    # smart dropout control (fontbakery lacks-smart-dropout): 표준 prep
    from fontTools.ttLib import newTable
    prep = newTable('prep')
    prep.program = __import__('fontTools.ttLib.tables.ttProgram',
                              fromlist=['Program']).Program()
    prep.program.fromAssembly(['PUSHW[]', '511', 'SCANCTRL[]',
                               'PUSHB[]', '4', 'SCANTYPE[]'])
    base['prep'] = prep

    # 수직 메트릭·OS/2 — 정적판과 정합 (family 일관성)
    st = TTFont(str(BUILD / 'IncruitSans-Regular.otf'), lazy=True)
    for k in ('ascent', 'descent', 'lineGap'):
        setattr(base['hhea'], k, getattr(st['hhea'], k))
    so, bo = st['OS/2'], base['OS/2']
    for k in ('sTypoAscender', 'sTypoDescender', 'sTypoLineGap',
              'usWinAscent', 'usWinDescent', 'fsSelection', 'usWeightClass'):
        setattr(bo, k, getattr(so, k))

    out = BUILD / 'IncruitSans-VF.ttf'
    base.save(str(out))

    vf = TTFont(str(out), lazy=True)
    gv = vf['gvar'].variations
    print(f'  ✓ {out.name}: instances={len(vf["fvar"].instances)}, '
          f'gvar 보유 글리프={sum(1 for g in gv if gv[g])}/{vf["maxp"].numGlyphs}')


if __name__ == '__main__':
    main()
