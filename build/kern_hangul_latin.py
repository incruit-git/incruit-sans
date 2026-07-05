"""한글↔라틴 스크립트 경계 class kern (Tier1 감사 Gap 해소, 2026-07-05).

실측(Regular, 2048 UPM): 시각 간격 = RSB(앞)+LSB(뒤) 중앙값 기준
  한→한 146 · 라→라 209 · 한→라 192 · 라→한 163
→ 라→한이 한→한 수준으로 끼어 스크립트 경계가 답답. 목표: 경계 간격을
  라→라(209)보다 약간 넓게 — A/B/C 시안(0 / +45·+75 / +90·+120) 렌더 판정으로
  **mid(한→라 +45, 라→한 +75)** 채택 (strong은 대형 사이즈에서 과다).

구현: PairPos format 2 (class 기반) 룩업 1개 — 한글 완성형 11,172 ↔ 라틴/숫자
(U+0020–U+024F 중 Letter·digit). 기존 'kern' feature 전 레코드에 등록.
값은 앞 글리프 XAdvance 가산. 전 웨이트 단일 값(감사 권고), VF에도 동일 적용.
"""
import unicodedata

import fontTools.ttLib.tables.otTables as ot
from fontTools.otlLib.builder import buildPairPosClassesSubtable, buildValue

V_HANGUL_TO_LATIN = 45
V_LATIN_TO_HANGUL = 75


def _classes(font):
    cmap = font.getBestCmap()
    hang = tuple(sorted({cmap[u] for u in range(0xAC00, 0xD7A4) if u in cmap}))
    lat = set()
    for u, g in cmap.items():
        if u > 0x24F:
            continue
        ch = chr(u)
        if unicodedata.category(ch)[0] == 'L' or ch.isdigit():
            lat.add(g)
    return hang, tuple(sorted(lat))


def add_script_kern(font, v_hl=V_HANGUL_TO_LATIN, v_lh=V_LATIN_TO_HANGUL,
                    verbose=True):
    """GPOS kern feature에 한↔라 class pair 룩업 추가. 멱등(마커 검사)."""
    gpos = font['GPOS'].table
    # 멱등: 마지막 룩업이 이미 우리 것(type2 + 한글 규모 class)이면 skip
    for lk in gpos.LookupList.Lookup:
        if getattr(lk, '_isans_script_kern', False):
            if verbose:
                print('  script-kern: already present — skip')
            return False

    hang, lat = _classes(font)
    pairs = {
        (hang, lat): (buildValue({'XAdvance': v_hl}), None),
        (lat, hang): (buildValue({'XAdvance': v_lh}), None),
    }
    st = buildPairPosClassesSubtable(pairs, font.getReverseGlyphMap())
    lookup = ot.Lookup()
    lookup.LookupType, lookup.LookupFlag = 2, 0
    lookup.SubTable, lookup.SubTableCount = [st], 1
    lookup._isans_script_kern = True
    gpos.LookupList.Lookup.append(lookup)
    gpos.LookupList.LookupCount += 1
    idx = gpos.LookupList.LookupCount - 1
    n = 0
    for fr in gpos.FeatureList.FeatureRecord:
        if fr.FeatureTag == 'kern':
            fr.Feature.LookupListIndex.append(idx)
            fr.Feature.LookupCount += 1
            n += 1
    if verbose:
        print(f'  script-kern: 한→라 +{v_hl} · 라→한 +{v_lh}, '
              f'{len(hang)}×{len(lat)} classes, kern feature {n}곳 등록')
    return True
