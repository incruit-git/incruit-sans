"""마스터 간 비호환 글리프 자동 호환화 — 형태 보존 변환만 사용.

varLib은 9 마스터의 윤곽 구조(윤곽 수·세그 수·시작점)가 다르면 해당 글리프를
스킵한다(gvar 없음 → 전 웨이트 Regular 고정). MinSans 정적판은 일부 글리프
(6·9·Q·R·S·e·&·accented 등 152자)를 웨이트별로 다르게 그려 이 문제가 발생.

호환화 4단계 (모두 마스터의 최종 형태를 바꾸지 않음 — 대응만 정렬):
1. 전곡선 승격: line → 등가 cubic (제어점 1/3·2/3). 닫는 암시선도 명시화.
2. 윤곽 대응: Regular 기준, (winding, 정규화 중심) 최근접 그리디 매칭.
3. 시작점 회전: 정규화 좌표에서 Regular 시작점과 최근접 지점으로 순환 이동.
4. 세그 수 균등화: 부족한 마스터의 최장 세그를 t=0.5 분할(De Casteljau, 형태 동일).

한계: 세그 분할 대응이 완벽하지 않으면 마스터 '사이' 보간(중간 웨이트)의
모델 정밀도만 저하 — 9 named instance 지점 자체는 항상 마스터와 픽셀 동일.
윤곽 수가 다른 글리프(¼½ȺȾ)는 호환화 불가 → 정적 유지, 호출부에 리포트.
"""


def _parse(rec_value):
    """RecordingPen.value(cubic) → [contour], contour = (start, [seg]),
    seg = ('l', p) | ('c', c1, c2, p). 닫는 암시선 명시화."""
    contours, start, segs = [], None, []
    for op, pts in rec_value:
        if op == 'moveTo':
            start = pts[0]
            segs = []
        elif op == 'lineTo':
            segs.append(('l', pts[0]))
        elif op == 'curveTo':
            segs.append(('c', pts[0], pts[1], pts[2]))
        elif op == 'qCurveTo':
            raise ValueError('quadratic input not supported')
        elif op in ('closePath', 'endPath'):
            if segs and segs[-1][-1] != start:
                segs.append(('l', start))
            if segs:
                contours.append((start, segs))
            start, segs = None, []
    return contours


def _all_cubic(contour):
    start, segs = contour
    out = []
    prev = start
    for seg in segs:
        if seg[0] == 'l':
            p = seg[1]
            c1 = (prev[0] + (p[0] - prev[0]) / 3.0, prev[1] + (p[1] - prev[1]) / 3.0)
            c2 = (prev[0] + 2 * (p[0] - prev[0]) / 3.0, prev[1] + 2 * (p[1] - prev[1]) / 3.0)
            out.append((c1, c2, p))
            prev = p
        else:
            out.append((seg[1], seg[2], seg[3]))
            prev = seg[3]
    return start, out  # segs: [(c1,c2,p)]


def _bbox(contours):
    xs = [p[0] for s, segs in contours for p in [s] + [q for seg in segs for q in seg]]
    ys = [p[1] for s, segs in contours for p in [s] + [q for seg in segs for q in seg]]
    return min(xs), min(ys), max(xs) or 1, max(ys) or 1


def _norm(pt, bb):
    x0, y0, x1, y1 = bb
    w, h = max(x1 - x0, 1), max(y1 - y0, 1)
    return (pt[0] - x0) / w, (pt[1] - y0) / h


def _centroid(contour):
    start, segs = contour
    pts = [start] + [seg[2] for seg in segs]
    return sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)


def _winding(contour):
    start, segs = contour
    pts = [start] + [seg[2] for seg in segs]
    area = 0.0
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        area += x1 * y2 - x2 * y1
    return 1 if area > 0 else -1


def _match_contours(ref_conts, conts, ref_bb, bb):
    """conts를 ref 순서에 맞게 재배열 (winding 동일 + 정규화 중심 최근접)."""
    used = set()
    order = []
    for rc in ref_conts:
        rw, rcen = _winding(rc), _norm(_centroid(rc), ref_bb)
        best, best_d = None, None
        for i, c in enumerate(conts):
            if i in used:
                continue
            d = ((_norm(_centroid(c), bb)[0] - rcen[0]) ** 2
                 + (_norm(_centroid(c), bb)[1] - rcen[1]) ** 2)
            if _winding(c) != rw:
                d += 4.0  # winding 불일치 페널티
            if best_d is None or d < best_d:
                best, best_d = i, d
        used.add(best)
        order.append(conts[best])
    return order


def _rotate_start(contour, ref_start_n, bb):
    """시작점을 ref 시작점(정규화)과 최근접한 on-curve 점으로 순환 이동."""
    start, segs = contour
    oncurve = [start] + [seg[2] for seg in segs[:-1]]
    dists = [((_norm(p, bb)[0] - ref_start_n[0]) ** 2
              + (_norm(p, bb)[1] - ref_start_n[1]) ** 2) for p in oncurve]
    k = dists.index(min(dists))
    if k == 0:
        return contour
    new_segs = segs[k:] + segs[:k]
    return oncurve[k], new_segs


def _params(contour):
    """각 세그 끝점의 누적 chord-length 파라미터 (0..1 정규화)."""
    start, segs = contour
    prev = start
    acc, out = 0.0, []
    for c1, c2, p in segs:
        acc += ((p[0] - prev[0]) ** 2 + (p[1] - prev[1]) ** 2) ** 0.5 or 1e-6
        out.append(acc)
        prev = p
    total = out[-1] or 1.0
    return [v / total for v in out]


def _split_at(p0, seg, t_locs):
    """cubic 하나를 로컬 파라미터 리스트(오름차순)에서 순차 분할."""
    out = []
    c1, c2, p3 = seg
    prev_t = 0.0
    cur = (p0, c1, c2, p3)
    for t in t_locs:
        tl = (t - prev_t) / (1.0 - prev_t)
        a0, a1, a2, a3 = cur
        lerp = lambda a, b: (a[0] + (b[0] - a[0]) * tl, a[1] + (b[1] - a[1]) * tl)
        q1 = lerp(a0, a1); q2 = lerp(a1, a2); q3 = lerp(a2, a3)
        r1 = lerp(q1, q2); r2 = lerp(q2, q3)
        mid = lerp(r1, r2)
        out.append((q1, r1, mid))
        cur = (mid, r2, q3, a3)
        prev_t = t
    out.append((cur[1], cur[2], cur[3]))
    return out


def _rotations(contour):
    """시작점을 각 on-curve 노드로 옮긴 회전 후보 전부 (형태 동일)."""
    start, segs = contour
    oncurve = [start] + [seg[2] for seg in segs[:-1]]
    out = []
    for k in range(len(segs)):
        out.append((oncurve[k], segs[k:] + segs[:k]))
    return out


def _align_to_profile(contour, ref_params, ref_pts_n, own_bb):
    """세그 끝점을 ref 프로파일에 단조 DP 정렬, 미대응 위치는 분할 삽입.

    비용 = |호길이 파라미터 차| + 정규화 좌표 유클리드 거리(기하 항).
    기하 항이 없으면 점대칭 글자(S 등)에서 뒤집힌 회전이 동비용으로 선택되는
    모호성이 생긴다 (2026-07-05 스윕 QA에서 실측).
    자기 끝점은 전부 유지(형태 보존), ref 잉여 위치에만 분할 추가.
    반환: (비용, 정렬된 contour).
    """
    start, segs = contour
    own = _params(contour)
    own_pts = [_norm(seg[2], own_bb) for seg in segs]
    m, n = len(own), len(ref_params)

    def cost_ji(j, i):
        dx = own_pts[j][0] - ref_pts_n[i][0]
        dy = own_pts[j][1] - ref_pts_n[i][1]
        return abs(own[j] - ref_params[i]) + (dx * dx + dy * dy) ** 0.5

    if m == n:
        return sum(cost_ji(k, k) for k in range(m)), contour
    INF = float('inf')
    # dp[j][i] = own[0..j] 를 ref[0..i] 에 단조 사상한 최소 비용 (마지막 j→i)
    dp = [[INF] * n for _ in range(m)]
    back = [[-1] * n for _ in range(m)]
    for i in range(n - (m - 1)):
        dp[0][i] = cost_ji(0, i)
    for j in range(1, m):
        best, bi = INF, -1
        for i in range(j, n - (m - 1 - j)):
            if dp[j - 1][i - 1] < best:
                best, bi = dp[j - 1][i - 1], i - 1
            dp[j][i] = best + cost_ji(j, i)
            back[j][i] = bi
    # 마지막 own 끝점(=시작점 복귀)은 ref 마지막에 고정돼야 자연스러움
    i = n - 1
    assign = [0] * m
    for j in range(m - 1, -1, -1):
        assign[j] = i
        i = back[j][i] if j > 0 else -1
    # ref 미대응 인덱스 → 해당 own 세그의 로컬 t 위치에 분할
    assigned = set(assign)
    inserts = {}  # own seg index j → [로컬 t]
    for ri in range(n):
        if ri in assigned:
            continue
        t = ref_params[ri]
        # t가 속한 own 세그 j: own[j-1] < t <= own[j]
        j = next(k for k in range(m) if own[k] >= t or k == m - 1)
        lo = own[j - 1] if j > 0 else 0.0
        hi = own[j]
        tl = min(max((t - lo) / max(hi - lo, 1e-9), 0.05), 0.95)
        inserts.setdefault(j, []).append(tl)

    new_segs = []
    prev = start
    for j, seg in enumerate(segs):
        if j in inserts:
            new_segs.extend(_split_at(prev, seg, sorted(inserts[j])))
        else:
            new_segs.append(seg)
        prev = seg[2]
    cost = dp[m - 1][n - 1]
    return cost, (start, new_segs)


def _best_alignment(contour, ref_params, ref_pts_n, own_bb):
    """전 회전 후보 중 (프로파일+기하) 정렬 비용 최소인 결과 선택."""
    best_cost, best = None, None
    for cand in _rotations(contour):
        cost, aligned = _align_to_profile(cand, ref_params, ref_pts_n, own_bb)
        if best_cost is None or cost < best_cost:
            best_cost, best = cost, aligned
    return best


def compatibilize(recordings, ref_index=3):
    """9 마스터 cubic recording → 대응 정렬된 [contours]×9. 실패 시 None."""
    parsed = [[_all_cubic(c) for c in _parse(r)] for r in recordings]
    ncont = {len(p) for p in parsed}
    if len(ncont) != 1:
        return None  # 윤곽 수 상이 — 호환화 불가

    bbs = [_bbox(p) for p in parsed]
    ref = parsed[ref_index]
    ref_bb = bbs[ref_index]

    # 윤곽 대응 + 시작점 회전
    aligned = []
    for i, (conts, bb) in enumerate(zip(parsed, bbs)):
        if i == ref_index:
            aligned.append(conts)
            continue
        conts = _match_contours(ref, conts, ref_bb, bb)
        conts = [_rotate_start(c, _norm(ref[j][0], ref_bb), bb)
                 for j, c in enumerate(conts)]
        aligned.append(conts)

    # 세그 수 균등화 + 노드 대응 — 최다 세그 마스터(ref)에서 웨이트 순으로
    # "이웃 마스터에 연쇄 정렬". 이웃은 형태가 가장 비슷해 회전 선택이
    # 모호하지 않다. (전원을 ref에 독립 정렬하면 멀리 있는 마스터끼리
    # 다른 회전을 골라 마스터 '사이'에서 델타가 상쇄·블롭 발생 — Ɠ 실측)
    n_conts = len(ref)
    n_masters = len(aligned)
    for j in range(n_conts):
        counts = [len(m[j][1]) for m in aligned]
        ref_i = counts.index(max(counts))
        target = counts[ref_i]
        chain = ([(i, i + 1) for i in range(ref_i - 1, -1, -1)]
                 + [(i, i - 1) for i in range(ref_i + 1, n_masters)])
        for i, nb in chain:
            nb_cont = aligned[nb][j]
            profile = _params(nb_cont)
            nb_pts_n = [_norm(seg[2], bbs[nb]) for seg in nb_cont[1]]
            c = _best_alignment(aligned[i][j], profile, nb_pts_n, bbs[i])
            if c is None or len(c[1]) != target:
                return None  # DP 정렬 실패 — 안전하게 포기
            aligned[i] = aligned[i][:j] + [c] + aligned[i][j + 1:]
    return aligned


def draw_multi(aligned, mpen):
    """대응 정렬된 마스터 윤곽들을 Cu2QuMultiPen에 병렬로 그림."""
    n_conts = len(aligned[0])
    for j in range(n_conts):
        mpen.moveTo([(m[j][0],) for m in aligned])
        n_segs = len(aligned[0][j][1])
        for s in range(n_segs):
            mpen.curveTo([m[j][1][s] for m in aligned])
        mpen.closePath()
