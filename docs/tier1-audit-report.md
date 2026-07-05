# Incruit Sans — Tier 1 Metrics 완성도 감사 리포트

> **버전**: v0.2.2 작업 사이클
> **일자**: 2026-05-18
> **범위**: Tier 1 (메트릭 정밀도) — 단기 자동화 가능 영역
> **참고**: [완전한 폰트 로드맵](#) (5-tier 계획)

---

## 1. Tier 1 범위

| Item | 작업 | 자동화 |
|------|------|:------:|
| 1.1 | Hangul outlier per-weight 보정 | ✅ |
| 1.2 | Kerning pair audit | ✅ |
| 1.3 | Contour validation | ✅ |
| 1.4 | OS/2 metrics 정합 | ✅ |
| 1.5 | HVAR/MVAR cleanup | ⏸ |

---

## 2. 결과 요약

### 2.1 Hangul Outlier 재정렬 (1.1)

**문제**: Pretendard 한글 상속 — 일부 글리프 시각 중심이 슬롯 중심(885 UPM)에서 크게 이탈.

**수정** ([PR #5](https://github.com/incruit-git/incruit-sans/pull/5)):
- 6자 보정: 쮞, 킦, 킭, 킮, 킯, 킼
- Threshold: drift > 100 UPM (~0.7px @ 14pt)
- 11,172 한글 중 0.05% 변경 — Pretendard 디자인 의도 보존

**잔여 (임계값 미달, 디자이너 task)**:
- ㄴ+ㅣ 계열 26자: drift ~22 UPM (0.15px @ 14pt — subpixel)
- ㅆ+ㅐ 계열 88자: drift ~48 UPM (0.33px @ 14pt — subpixel)

### 2.2 Kerning Audit (1.2)

| 항목 | 값 | 판정 |
|------|----|----|
| 총 kern pairs | 402,119 | ✅ 풍부 |
| Latin 표준 problem pairs | 36/38 | ✅ (fi/fl은 ligature 영역) |
| Korean-Latin 혼용 | 0 | ⚠ Gap |
| Tight kerns (< -150) | edge case (quotes) | ✅ 무해 |
| Major Latin asymmetry (>50 UPM) | 17 | ✅ 의도된 디자인 |

**Major asymmetry sample** (의도된 디자인):
- `To` -158 vs `oT` -79 (T 가로 막대 위 o 들어감)
- `Wc` -103 vs `cW` -2 (W 사선 끝 위 c)
- `Yp` -79 vs `pY` -173 (descender 충돌 회피)

**Gap**: Latin↔Hangul mixing kerning 없음. → ✅ **2026-07-05 해소** (`build/kern_hangul_latin.py` class kern +45/+75, v0.4)
- 영향: `React 개발자`, `50,000,000원` 등 혼용 문장에서 자간 미세 어색
- 해결: 디자이너가 class-based kern 추가 (Latin-class ↔ Hangul-class, 단일 값)
- **Tier 2-3 디자이너 작업 영역**

### 2.3 Contour Audit (1.3)

| 결함 | 수 | 판정 |
|------|:--:|----|
| Top overflow (yMax > ascender+50) | 36 | 검토 권장 |
| Bottom overflow | 1 (combining mark) | ✅ 정상 |
| Left overflow (xMin < -100) | 205 | ✅ 의도된 디자인 |
| Tiny glyphs | 0 | ✅ |
| Empty glyphs (non-space) | 18 | 검토 권장 |
| **총 검사** | **13,701** | — |

Major 결함 없음. 26개 검토 권장 글리프는 희귀 문자/대시 류.

### 2.4 OS/2 metrics 정합 (1.4)

| 항목 | 값 |
|------|----|
| hhea.ascent | 1950 |
| OS2.sTypoAscender | 1949 |
| Diff | 1 UPM (0.007px @ 14pt) |
| USE_TYPO_METRICS flag | ✅ set |
| Win.ascent + Win.descent | 1949 + 494 = 2443 |
| OS2 typo sum | 1949 + 494 = 2443 |

- 1 UPM 차이 cosmetic. 14pt에서 가시 불가.
- Cross-platform 라인 높이 일관 ✓.
- Linegap = 0 (모든 weight)
- 수정 불필요.

### 2.5 HVAR/MVAR cleanup (1.5)

- HVAR digits 매핑 (10자 → Item 297, deltas `[-8,-10,-22,6,10,10,18,34]`)
- 그러나 `fontTools instancer`는 glyf 폰트 HVAR를 dropped — gvar phantom만 사용
- 결과: HVAR 데이터 dead data
- **Cleanup skip 결정**: 소스 rebuild 없이 직접 cleanup 위험 (정상 variation entry 손상 가능)
- Tier 2+ 디자이너 도구 (Glyphs 3) 재빌드 시 자연 정리

---

## 3. 검증 스크립트

| 스크립트 | 용도 |
|----------|------|
| `build/retune_tabular_digits.py` | Tabular digit 중심 재정렬 (v0.2.1) |
| `build/fix_j_overhang.py` | j 좌측 돌출 수정 (v0.2.1) |
| `build/recenter_hangul_outliers.py` | Hangul outlier 재정렬 (v0.2.2) |
| `build/distinguish_pass.py` | 이력서 판별성 l-tail + 0-dot (2026-07-05) |
| `build/build_ttf_vf.py` | OTF→보간 호환 TTF 변환 (2026-07-05) |
| `build/build_vf_v2.py` + `compat_fix.py` | VF 재건 + 비호환 글리프 호환화 (2026-07-05) |
| `build_all_weights.py` (통합) | OTF 빌드 시 자동 retune + fix_j + 판별성 + 표준 정합 |

---

## 4. 출시 체크리스트 (2026-07-05 갱신 — 릴리스 범위가 v0.2.2를 초과)

- [x] Tier 1.1 Hangul outlier fix (PR #5)
- [x] Tier 1.2~1.4 audit complete (no code change needed)
- [x] All artifact files updated (47 binary → 2026-07-05 전량 재생성)
- [x] WOFF/WOFF2 repacked (+ web/hinted 재생성)
- [x] CHANGELOG.md 업데이트 (v0.3 섹션)
- [x] Release notes 초안 (`docs/release-notes-v0.3.md`)
- [x] 표준 검증 (fontbakery — `docs/font-quality-verification-2026-07-05.md`)
- [x] 버전 결정: **v0.3** (의장 승인 2026-07-05)
- [x] tag + GitHub Release — **v0.3 발행 완료** (2026-07-05, https://github.com/incruit-git/incruit-sans/releases/tag/v0.3)

---

## 5. 다음 단계 (Tier 2 진입)

### Tier 2 — 디자이너 정제 (4-12주, 외주)
- 2.1 Latin 165자 Min Sans 곡선 적용
- 2.2 한글 고빈도 500자 라운딩
- 2.3 Italic Latin (선택)
- **2.4 외주 견적 발송** (`docs/designer-spec-module-2.md` 준비됨)

### 의장 결정 대기
1. **외주 vs 인하우스** (Q#2)
2. **상표 검색 "Incruit Sans"** (Q#3)
3. **OSS 공개 시점** (GTM Phase 2: M6-M12)
4. **디자인 방향** — Min Sans 곡선 강도

---

## 6. 변경 이력

| 일자 | 변경 | 작성자 |
|------|------|--------|
| 2026-05-18 | Tier 1 감사 리포트 작성 | Claude Code |
| 2026-05-17 | Tier 1.1 (Hangul outlier) PR #5 merged | Claude Code |
| 2026-05-17 | v0.2.1 release (tabular digit + j fix) | Claude Code |
