# Incruit Sans — 폰트 품질 검증 리포트

> **일자**: 2026-07-05
> **도구**: fontbakery 1.1.0 `check-universal` + fontTools 4.62.1 (직접 점검)
> **대상**: 현재 빌드 산출물 — `build/IncruitSans-*.otf` 9 static + `build/IncruitSans-VF.ttf`
> **결과 요약(합산 10폰트)**: ✅ PASS 559 · 🔥 FAIL 51 · ⚠️ WARN 74 · 💥 ERROR 1 (FAIL/WARN은 폰트별 반복 → 아래 고유 이슈로 dedupe)
> **원본**: `/tmp/fb-report.md` (ghmarkdown 전문)

---

## 결론

**기능적으로는 견고하나, 표준 준수·메타데이터 결함으로 v0.2.2 릴리스 준비 안 됨.** 기존 Tier 1 감사(2026-05-18)의 초록 체크는 메트릭 정밀도 한정이었고, 표준 준수(name/version/VF/CFF) 축은 미검증이었음. 이번 검증에서 그 축의 실결함이 드러남.

### ✅ 견고한 것 (직접 확인)
- **글리프 커버리지 완전**: 라틴 A–z 58/58 · **한글 완성형 11,172/11,172** · 숫자 10/10 (총 14,716 글리프)
- **수직 메트릭 9웨이트 전부 정합**: hhea 1950/−494/0 · typo 1949/−494 · win 1949/494 (불일치 0, `USE_TYPO_METRICS` set)
- **usWeightClass 정확**: Thin100 … Black900 · unitsPerEm 2048 · family "Incruit Sans"
- **VF wght 축 범위 정상**: 100–400–900

---

## 🔴 릴리스 블로커 (v0.2.2 태그 전 수정 필요 · 대부분 기계적)

| # | fontbakery code | 내용 | 범위 | 수정 |
|---|---|---|---|---|
| B1 | `mismatch` (opentype/font_version) | **head 버전 `1.30899` ↔ name 버전 문자열 `Version 0.2` 불일치** | 10폰트 | 기계적 — head.fontRevision을 name과 정합 |
| B2 | `no-regular-instance`·`no-bold-instance`·`missing-avar` | **VF에 named instance 0개** (Regular·Bold 없음) + avar 없음 + STAT AxisValue 부재 → 앱 굵기 메뉴 안 뜸, **ERROR(name_family_max_length AttributeError)까지 유발** | VF | 스크립트 — fvar 9 instance(Thin~Black)+STAT+avar 추가 |
| B3 | `mac-names` | **Mac 플랫폼 name 레코드(ID 256+) 다수** 잔존 (병합 원본 MinSans/Pretendard 잔재) | 10폰트(≈52개씩) | 기계적 — platform=1 name 레코드 제거 |

## 🟡 품질 갭 (릴리스 판단 항목 · 일부 디자이너/툴링)

| # | code | 내용 | 성격 |
|---|---|---|---|
| Q1 | `zero-width-bases` | base 글리프 6종 advance width 0 | 조사 필요(렌더 영향) |
| Q2 | `cff-string-not-in-ascii-range` | CFF TopDict 문자열 비-ASCII(한글 메타) | OTF 9종 — CFF 문자열 재생성 |
| Q3 | `missing-case-counterparts` | 대소문자 스왑 짝 없는 글리프 | 조사 |
| Q4 | `missing-chws-feature`·`missing-vchw-feature` | **CJK контекст 자간(chws/vchw) 미탑재** — 한글 구두점 간격 개선 기능 | `chws_tool` 실행(툴링) |
| Q5 | `unreachable-glyphs`·`decomposed-outline`·`mark-chars` | cmap 미도달 글리프 / 분해된 아웃라인(컴포넌트 미사용) / GDEF mark class 누락 | 정리·소스 재빌드 |

## ⚪ 경미·예상됨 (WARN, 수용 가능)

- `large-font` 1.5MB > 1MB — 한글 11,172자라 정상
- `softhyphen` Soft Hyphen 존재 / `width-outliers` math 글리프 / `ots-sanitize-warn` OTS 경고

---

## 권고

1. **v0.2.2 태그 보류** — B1·B2·B3 수정 전 릴리스 금지. (감사 리포트 §4의 "tag/Release" 미완 항목이 실제로는 블로커였음.)
2. **기계적 3종(B1·B3 + B2 일부)은 스크립트로 즉시 처리 가능** — fontTools로 버전 정합·Mac name 제거·VF named instance/STAT 생성. `build/`에 fix 스크립트 추가 + 빌드 파이프라인 편입 권장.
3. **Q1·Q3·Q4·Q2는 조사/툴링/디자이너 영역** — chws_tool(Q4)은 한글 품질에 실효, 우선 검토 권장.
4. 재빌드 시 위 전부 자연 해소되도록 `build_all_weights.py`에 후처리 편입이 근본책.

---

## 재검증 (2026-07-05 재빌드 후)

같은 날 재빌드로 위 결함 대부분 해소. 핵심 변화:

| 항목 | 이전 | 이후 |
|---|---|---|
| B1 font_version | FAIL ×10 | ✅ 해소 (head.fontRevision=0.2) |
| B2 VF instances/STAT | FAIL + ERROR | ✅ fvar 9 instances + STAT AxisValue |
| B3 mac-names | FAIL ×10 (≈52개씩) | ✅ 전 폰트 platform=1 제거 |
| **VF gvar 커버리지** | **1,950/14,716** (한글·곡선 라틴 Bold 불가) | **14,738/14,757** (Pretendard Variable 기반 재건) |
| smart dropout (VF) | FAIL | ✅ prep 추가 |
| TTF sfnt 서명 | 'OTTO' 오기 → FreeType 로드 거부 | ✅ TrueType 서명 교정 |
| 판별성 (신규) | l=I 동형, 0 무표시 | ✅ l-tail + 0-dot 9웨이트+VF |

**VF 재건 방법**: 정적 OTF 9종은 웨이트 간 윤곽 구조 상이(8,473 글리프)로 보간 불가 →
한글은 공식 Pretendard Variable(축 100–900 제한), 라틴은 자체 보간 호환 TTF 9종에서
varLib으로 gvar 생성 후 글리프 단위 이식. 비호환 라틴 148자는 `build/compat_fix.py`
자동 호환화(형태 보존: 전곡선 승격→윤곽 매칭→호길이+기하 DP→이웃 연쇄 정렬).
QA: 148자+대조군 × 17웨이트 잉크 곡선 스캔 + 중간 웨이트 픽셀 검증 (Ɠ 블롭 등 3차 교정).

**잔존 (v0.2.2 판단 항목)**:
- case_mapping(Q3)·chws/vchw(Q4)·unreachable/decomposed(Q5) — 기존 품질 갭 유지
- VF nested/transformed components — Pretendard Variable 상류 유래 (기능상 문제 없음, 구형 래스터라이저 경고)
- VF ¼ ½ Ⱥ Ⱦ 4자 — 윤곽 수 상이로 정적 유지 (전 웨이트 Regular 형태)
- interpolation_issues WARN — fontbakery 자체 검사; 픽셀 스캔으로는 미검출, 추후 상세 조사

## 변경 이력
- 2026-07-05: fontbakery 1.1.0 + fontTools 표준 검증 최초 수행 (Tier 1 감사 이후 표준 준수 축 첫 점검)
- 2026-07-05: 재빌드 후 재검증 — B1·B2·B3 해소, VF gvar 1,950→14,738, 판별성 반영
- 2026-07-05 (v0.4): chws 탑재 — Q4 해소. `。、` 연쇄 1920→960 실측(hb-shape --features=chws), 대상 전각 구두점 어드밴스 전 웨이트 불변 확인 후 VF에도 정적 적용. vchw는 vmtx 부재로 비대상.
