# Module 2 — Latin 글리프 정제 우선순위 명세

> **Module**: 2 (Latin Refinement)
> **Target Version**: v0.3
> **Glyph Count**: 165자 (Latin 95 + Numbers 20 + Symbols 50)
> **Owner**: 폰트 디자이너 (외주 또는 인하우스)
> **Reference**: [Design §3.3 Glyph Coverage Plan](features/incruit-sans.design.md), [glyph-specifications.md](../glyph-specifications.md)

---

## 우선순위 분류 원칙

| 우선순위 | 정의 | 빌드 차단 |
|----------|------|:---------:|
| **P0** | 이력서 텍스트의 95%+ 차지하는 핵심 글리프 — 정제 누락 시 v0.3 출시 불가 | ✅ |
| **P1** | 일반 텍스트에서 자주 사용 — 정제 누락 시 차질이 있으나 v0.3 출시 가능 | ❌ |
| **P2** | 특수 컨텍스트에서만 사용 — v0.5 또는 그 이후로 미룰 수 있음 | ❌ |

---

## 1. Latin Alphabet (95자)

### 1.1 Uppercase A–Z (26자) — **P0 전체**

이력서 본문, 이름, 회사명에 필수.

| 그룹 | 글리프 | 우선 정제 영역 |
|------|--------|--------------|
| 직선형 | `E F H I L T` | 두께 일관성, baseline 정렬 |
| 사선형 | `A K M N V W X Y Z` | 사선 두께(Min Sans 부드러움), 교차점 광학보정 |
| 곡선형 | `B C D G J O P Q R S U` | 곡선 반지름(20–40 UPM), 모서리 라운딩 |

**시각 검증 우선 글리프**: `O` (정원성), `S` (곡선 균형), `M`/`W` (사선 교차점), `Q` (꼬리 처리)

### 1.2 Lowercase a–z (26자) — **P0 전체**

이력서 본문 다수 차지.

| 그룹 | 글리프 | 우선 정제 영역 |
|------|--------|--------------|
| x-height | `a c e i m n o r s u v w x z` | x-height(500 UPM) 정확성 |
| Ascender | `b d f h k l t` | ascender 도달 높이 일관성 |
| Descender | `g j p q y` | descender(-200 UPM) 정확성 |

**시각 검증 우선 글리프**: `a`/`g` (이중층 vs 단층 결정), `o` (정원성), `e` (눈 카운터 비율), `s` (곡선 균형)

### 1.3 합계: 52자 (P0)

---

## 2. Numbers (20자: 0-9 × 2 variants)

### 2.1 Default Figures (Proportional + Lining) — **P0 (10자)**

`0 1 2 3 4 5 6 7 8 9` (proportional width, full-height)

- 사용처: 본문 내 인라인 숫자 ("3년 경력", "2024년")
- **시각 검증 우선**: `0`(O와 구별), `1`(serif 없는 단순 형태), `6`/`9`(곡선 대칭성)

### 2.2 Tabular Figures (.tnum variant) — **P0 (10자)**

`zero.tnum one.tnum ... nine.tnum` (모두 동일 advance width)

- **CRITICAL**: 이력서 컨텍스트의 핵심 가치
- 사용처: 연봉 (`50,000,000원`), 날짜 (`2024.03 - 현재`), KPI (`95.5%`), GPA (`3.85/4.5`)
- **메트릭 요구**: 모든 .tnum 글리프가 정확히 동일한 advance width (예: 600 UPM 고정)
- OpenType feature: `tnum` Default ON (Design §4.3)

### 2.3 합계: 20자 (P0)

---

## 3. Symbols & Punctuation (50자)

### 3.1 Punctuation (P0 — 18자) — 이력서 필수

| 카테고리 | 글리프 | 우선순위 |
|---------|--------|:--------:|
| 마침표/쉼표 | `. , : ;` | P0 |
| 따옴표 | `' " ` ´ ' ' " "` | P0 |
| 괄호 | `( ) [ ] { }` | P0 |
| 하이픈/대시 | `- – —` (hyphen, en-dash, em-dash) | P0 |

> **메트릭 주의**: en-dash(–)는 Tabular figure width와 정렬되어야 함 (`2024–2026` 표기).

### 3.2 Common Symbols (P0 — 17자)

| 카테고리 | 글리프 | 우선순위 |
|---------|--------|:--------:|
| 의문/감탄 | `! ?` | P0 |
| 슬래시 | `/ \` | P0 |
| 단위 | `% & @ #` | P0 |
| 통화 | `$ ₩ ¥ €` (₩는 한국 이력서 필수) | P0 |
| 산술 | `+ - = * <` `>` | P0 |

### 3.3 Extended Symbols (P1 — 10자)

| 카테고리 | 글리프 | 우선순위 |
|---------|--------|:--------:|
| 추가 통화 | `£ ¢` | P1 |
| 수학 | `± × ÷ ≤ ≥ ≠ ≈` | P1 |
| 각주 | `† ‡` | P1 |

### 3.4 Decorative / Optional (P2 — 5자)

`§ ¶ © ® ™` (저작권 표기 등)

### 3.5 합계: 50자 (P0: 35자 / P1: 10자 / P2: 5자)

---

## 4. 정제 작업 순서 권고

| Sprint | 글리프 세트 | 누적 | 디자이너 일정 | 검증 단계 |
|--------|------------|:----:|:------------:|----------|
| **S1** (Week 1) | Lowercase a-z | 26 | 5일 | specimen.html lowercase 섹션 |
| **S2** (Week 2) | Uppercase A-Z | 52 | 5일 | specimen.html uppercase + 이름 테스트 |
| **S3** (Week 3) | Numbers + .tnum | 72 | 4일 | tnum 자릿수 정렬 검증 |
| **S4** (Week 4) | P0 Punctuation + Symbols | 107 | 5일 | resume-test.html 풀 렌더링 |
| **S5** (선택) | P1/P2 Symbols | 122–127 | 3일 | Optional, v0.4로 미룰 수 있음 |

**총 일정**: 4주 (P0만) ~ 5주 (P0+P1) — 외주 디자이너 1명 풀타임 기준.

---

## 5. 메트릭 가이드라인 (Design 인용)

> 자세한 내용은 [`docs/glyph-specifications.md`](../glyph-specifications.md) 참조.

| 항목 | 값 (UPM) | 비고 |
|------|----------|------|
| **UPM** | 1000 | 표준 |
| **Ascender** | 800 | Pretendard 호환 |
| **Descender** | -200 | Pretendard 호환 |
| **x-height** | 500 | Pretendard 호환 |
| **Cap-height** | 750 | Pretendard 호환 |
| **Stroke (Regular)** | 80 | Pretendard 기준 |
| **Stroke (Bold)** | 140 | Bold 마스터 |
| **Corner Radius** | 20–40 | **Min Sans 영감 — 차별화 핵심** |
| **Tabular advance** | 600 (10진수 모두 동일) | tnum feature |

---

## 6. 시각 검증 체크리스트 (디자이너용)

각 글리프 정제 후 다음을 확인하세요.

### 6.1 단일 글리프
- [ ] Regular(80 UPM) / Bold(140 UPM) 두께가 정확히 1.75배 비율
- [ ] 모서리 라운딩이 다른 글리프와 일관됨 (20–40 UPM)
- [ ] 베이스라인 / x-height / cap-height 정렬 정확
- [ ] 광학 보정 (예: O가 정원이 아닌 살짝 확장된 타원)

### 6.2 자간 (Kerning)
- [ ] AV, AT, LV, To, Ya 등 표준 kerning pair 시각 검증
- [ ] 한글 + Latin 혼용 시 자간 일관성 (`React 개발자`)

### 6.3 Tabular Figures
- [ ] `123,456,789` 자릿수 정렬 픽셀 단위 확인
- [ ] `2024.03 - 2026.04` 날짜 정렬 확인
- [ ] `95.5% / 3.85` 소수점 정렬 확인

### 6.4 컨텍스트 테스트
- [ ] specimen.html에서 6 weights × 5 sizes 매트릭스 시각 확인
- [ ] resume-test.html에서 실제 이력서 레이아웃 렌더링
- [ ] 10pt에서 모든 글리프 가독 가능

---

## 7. 산출물 (Module 2 완료 시)

| Item | Path | Owner |
|------|------|-------|
| Refined `.glyphs` source | `sources/IncruitSans-Regular.glyphs` | 디자이너 |
| Build artifacts | `fonts/{otf,ttf,webfonts}/` | CI 자동 |
| specimen.html 시각 검증 | `tests/specimen.html` 스크린샷 | Claude (gap-detector) |
| Module 2 Analysis | `docs/03-analysis/incruit-sans-module-2.md` | Claude |

---

## 8. Open Questions for Designer

디자이너 협업 시 다음 결정이 필요합니다:

1. **a/g 형태**: Single-story (간결, Roboto/Inter 류) vs Double-story (전통적, Pretendard 류)?
   - 이력서 컨텍스트에서는 Double-story 권장 (가독성 ↑)
2. **Tabular advance width**: 600 UPM 고정으로 충분한가? (다른 폰트는 530–650 범위)
3. **Hyphen vs Minus**: 시각적으로 같게 vs 다르게 디자인?
4. **₩ (원 기호)**: 한국 이력서에서 자주 사용 — Pretendard보다 더 강조된 형태로?
5. **점(.)/쉼표(,) 두께**: x-height의 1/4 (가벼움) vs 1/3 (안정적)?

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 0.1 | 2026-04-26 | Initial Module 2 priority spec | Claude Code (PDCA Do — Module 2) |
