"""이력서 판별성 패스 — l 꼬리(tail) + 0 중앙점(dot, 옵트인).

의장 결정 2026-07-05: l-tail 채택 / 0-dot 현행 크기 유지 / I 무변경.
의장 결정 2026-07-19 (C안): 기본 0은 민짜(0-dot 제거 — 대형 볼드 숫자에서
  counter의 43~66%를 점이 차지해 도형-배경 반전), dotted 0은 GSUB `zero`
  feature 대체 글리프에 주입해 옵트인 제공. 이력서 등 판별성이 필요한 화면만
  CSS `font-variant-numeric: slashed-zero` (= feature "zero") 한 줄로 켠다.

원리 (하드코딩 없음 — 해당 웨이트 자신의 글리프에서 좌표 유도):
- l: 같은 폰트 t 글리프의 foot 곡선(세그 0~4·16)을 인덱스로 추출,
  stem 좌측 정렬 dx 이동 후 l 의 bare bar 에 이식. t stem 폭 == l stem 폭
  (전 웨이트 실측 일치) 이라 무보정 접합.
  어드밴스 = tail 끝 + 0.4×기존 RSB (Regular 프로토타입 검증값 820 재현).
- 0: Pretendard에서 상속된 GSUB `zero` feature 매핑(기본0→대체, tnum0→대체)의
  각 대체 글리프를 「기준 글리프 윤곽 복제 + counter 중심 다이아몬드 dot」로
  덮어쓴다(새 글리프·GSUB 변경 없음 — 대체 글리프의 Pretendard 슬래시 윤곽이
  Min Sans 숫자와 어긋나던 문제도 함께 해소). dot r = 70×(stem폭/182),
  counter 대비 0.33 클램프로 Black 충돌 방지. 어드밴스 = 기준 글리프와 동일
  (feature on/off 시 숫자 폭 불변).

멱등: l 세그 수(5=bare bar)로 기적용 감지 시 skip / 0 은 순수함수 덮어쓰기라
재실행 무해. 구버전(v0.3~0.4) 바이너리에 재실행 시 기본 0의 legacy dot
(3윤곽)을 자동 제거해 민짜로 되돌린다.
"""
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen

# t 글리프 기대 위상 (18세그 — 전 9웨이트 실측 동일)
_T_OPS = (['moveTo', 'curveTo', 'lineTo', 'curveTo', 'curveTo']
          + ['lineTo'] * 11 + ['curveTo', 'closePath'])

DOT_R_REGULAR = 70      # Regular 프로토타입 검증값 (2048 UPM)
STEM_REGULAR = 182      # Regular stem 폭 기준
RSB_FACTOR = 0.4        # 820 = 752 + 0.4*170 (Regular 검증값 역산)
DOT_CLAMP = 0.33        # dot 반경 ≤ 0.33 × min(counter 폭, 높이)


def _record(charstrings, gname):
    pen = RecordingPen()
    charstrings[gname].draw(pen)
    return pen.value


def _bounds(charstrings, gname):
    pen = BoundsPen(None)
    charstrings[gname].draw(pen)
    return pen.bounds


def _contours(segs):
    """RecordingPen 세그를 moveTo 단위 윤곽 리스트로 분할."""
    out, cur = [], []
    for op, pts in segs:
        if op == 'moveTo' and cur:
            out.append(cur)
            cur = []
        cur.append((op, pts))
    if cur:
        out.append(cur)
    return out


def _contour_bbox(contour):
    xs, ys = [], []
    for _, pts in contour:
        for x, y in pts:
            xs.append(x)
            ys.append(y)
    return min(xs), min(ys), max(xs), max(ys)


def _signed_area(contour):
    pts = [p for _, seg in contour for p in seg]
    area = 0.0
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        area += x1 * y2 - x2 * y1
    return area / 2.0


def _new_charstring(pen_draw, width, old_cs):
    pen = T2CharStringPen(width, None)
    pen_draw(pen)
    cs = pen.getCharString(private=old_cs.private, globalSubrs=old_cs.globalSubrs)
    return cs


def add_l_tail(font, verbose=True):
    cmap = font.getBestCmap()
    cs_table = font['CFF '].cff[0].CharStrings
    g_l, g_t = cmap[ord('l')], cmap[ord('t')]

    l_segs = _record(cs_table, g_l)
    if len(l_segs) != 5:  # bare bar(사각형) 아님 → 기적용
        if verbose:
            print('  l: already tailed — skip')
        return False

    t_segs = _record(cs_table, g_t)
    ops = [op for op, _ in t_segs]
    assert ops == _T_OPS, f'unexpected t topology: {ops}'

    l_xmin, _, l_xmax, l_top = _bounds(cs_table, g_l)
    t_stem_left = t_segs[15][1][0][0]    # 세그15 끝점 x = t stem 좌측
    t_stem_right = t_segs[4][1][-1][0]   # 세그4 끝점 x = t stem 우측
    assert abs((t_stem_right - t_stem_left) - (l_xmax - l_xmin)) <= 2, \
        f'stem width mismatch t={t_stem_right - t_stem_left} l={l_xmax - l_xmin}'

    dx = l_xmin - t_stem_left
    sh = lambda p: (p[0] + dx, p[1])
    y_junction = t_segs[4][1][-1][1]     # 내측 foot이 stem 과 만나는 y
    y_foot = t_segs[15][1][0][1]         # 외측 foot 시작 y

    old_adv, _ = font['hmtx'][g_l]
    tail_tip = t_segs[1][1][-1][0] + dx
    new_adv = int(round(tail_tip + RSB_FACTOR * (old_adv - l_xmax)))

    def draw(pen):
        pen.moveTo(sh(t_segs[0][1][0]))
        pen.curveTo(*[sh(p) for p in t_segs[1][1]])
        pen.lineTo(sh(t_segs[2][1][0]))
        pen.curveTo(*[sh(p) for p in t_segs[3][1]])
        c1, c2, _ = t_segs[4][1]
        pen.curveTo(sh(c1), sh(c2), (l_xmax, y_junction))
        pen.lineTo((l_xmax, l_top))
        pen.lineTo((l_xmin, l_top))
        pen.lineTo((l_xmin, y_foot))
        pen.curveTo(*[sh(p) for p in t_segs[16][1]])
        pen.closePath()

    cs_table[g_l] = _new_charstring(draw, new_adv, cs_table[g_l])
    font['hmtx'].metrics[g_l] = (new_adv, int(l_xmin))
    if verbose:
        print(f'  l: tail grafted (dx={dx}, tip={tail_tip:.0f}, adv {old_adv}->{new_adv})')
    return True


def zero_feature_pairs(font):
    """GSUB `zero` feature 의 SingleSubst 매핑 [(기준, 대체), ...] 수집."""
    gsub = font['GSUB'].table
    pairs = []
    seen_lookups = set()
    for fr in gsub.FeatureList.FeatureRecord:
        if fr.FeatureTag != 'zero':
            continue
        for li in fr.Feature.LookupListIndex:
            if li in seen_lookups:
                continue
            seen_lookups.add(li)
            lk = gsub.LookupList.Lookup[li]
            if lk.LookupType != 1:
                continue
            for st in lk.SubTable:
                pairs.extend(sorted(st.mapping.items()))
    return pairs


def _strip_legacy_dot(conts):
    """구버전 기본 0 (외곽+counter+dot 3윤곽)에서 legacy dot 제거."""
    bb = [_contour_bbox(c) for c in conts]
    areas = [(b[2] - b[0]) * (b[3] - b[1]) for b in bb]
    drop = areas.index(min(areas))
    return [c for i, c in enumerate(conts) if i != drop]


def add_zero_dot(font, verbose=True):
    """기본 0 민짜 유지, GSUB `zero` feature 대체 글리프에 dot 주입 (옵트인)."""
    cmap = font.getBestCmap()
    cs_table = font['CFF '].cff[0].CharStrings
    g_0, g_I = cmap[ord('0')], cmap[ord('I')]  # stem은 무변경 글리프 I에서 측정 (l은 tail로 오염)

    pairs = zero_feature_pairs(font)
    assert pairs, "GSUB 'zero' feature 부재 — Pretendard 상속 GSUB 확인 필요"

    # stem 폭 비례 dot 반경 (전 글리프 공통 — 웨이트당 1회 산출)
    i_xmin, _, i_xmax, _ = _bounds(cs_table, g_I)
    stem_w = i_xmax - i_xmin
    r_base = DOT_R_REGULAR * stem_w / STEM_REGULAR

    changed = False
    for base_g, alt_g in pairs:
        segs = _record(cs_table, base_g)
        conts = _contours(segs)
        if len(conts) == 3:  # 구버전(v0.3~0.4) 기본 0: legacy dot 제거 후 진행
            conts = _strip_legacy_dot(conts)
            adv, lsb = font['hmtx'][base_g]

            def draw_clean(pen, conts=conts):
                for cont in conts:
                    for op, pts in cont:
                        getattr(pen, op)(*pts) if op != 'closePath' else pen.closePath()

            cs_table[base_g] = _new_charstring(draw_clean, adv, cs_table[base_g])
            if verbose:
                print(f'  0: legacy dot stripped from base {base_g}')
        elif len(conts) != 2:
            if verbose:
                print(f'  0: base {base_g} contours={len(conts)} — skip pair')
            continue

        # 외곽/counter 판별 (bbox 면적)
        bb = [_contour_bbox(c) for c in conts]
        areas = [(b[2] - b[0]) * (b[3] - b[1]) for b in bb]
        outer_i = 0 if areas[0] >= areas[1] else 1
        inner_bb = bb[1 - outer_i]
        in_w, in_h = inner_bb[2] - inner_bb[0], inner_bb[3] - inner_bb[1]
        cx = (inner_bb[0] + inner_bb[2]) / 2.0
        cy = (inner_bb[1] + inner_bb[3]) / 2.0

        r = int(round(min(r_base, DOT_CLAMP * min(in_w, in_h))))

        # dot 방향 = 외곽 윤곽과 동일 (CFF non-zero winding)
        outer_ccw = _signed_area(conts[outer_i]) > 0
        if outer_ccw:
            diamond = [(cx, cy + r), (cx - r, cy), (cx, cy - r), (cx + r, cy)]
        else:
            diamond = [(cx, cy + r), (cx + r, cy), (cx, cy - r), (cx - r, cy)]

        adv, lsb = font['hmtx'][base_g]  # 기준 글리프와 동일 폭 (숫자 정렬 유지)

        def draw(pen, conts=conts, diamond=diamond):
            for cont in conts:  # 기준 윤곽 복제
                for op, pts in cont:
                    getattr(pen, op)(*pts) if op != 'closePath' else pen.closePath()
            pen.moveTo(diamond[0])
            for p in diamond[1:]:
                pen.lineTo(p)
            pen.closePath()

        cs_table[alt_g] = _new_charstring(draw, adv, cs_table[alt_g])
        font['hmtx'].metrics[alt_g] = (adv, lsb)
        changed = True
        if verbose:
            print(f'  0: dotted alt {base_g}->{alt_g} (center=({cx:.0f},{cy:.0f}), '
                  f'r={r}, counter={in_w:.0f}x{in_h:.0f}, adv={adv})')
    return changed


def distinguish(font, verbose=True):
    a = add_l_tail(font, verbose=verbose)
    b = add_zero_dot(font, verbose=verbose)
    return a or b


if __name__ == '__main__':
    import sys
    from fontTools.ttLib import TTFont
    src, dst = sys.argv[1], sys.argv[2]
    f = TTFont(src)
    distinguish(f)
    f.save(dst)
    print(f'saved: {dst}')
