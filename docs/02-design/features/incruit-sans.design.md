# Incruit Sans Design Document

> **Summary**: Variable Font (wght 100–900) 빌드 파이프라인, 마스터 구성, 글리프 정제 워크플로우, 인크루트 에디터 통합 아키텍처
>
> **Project**: Incruit Sans
> **Version**: 0.1.0
> **Author**: Claude Code (PDCA Design Phase)
> **Date**: 2026-04-25
> **Status**: Draft
> **Planning Doc**: [incruit-sans.plan.md](../../01-plan/features/incruit-sans.plan.md)
> **PRD**: [incruit-sans.prd.md](../../00-pm/incruit-sans.prd.md)

---

## Context Anchor

> Copied from Plan document. Ensures strategic context survives Design→Do handoff.

| Key | Value |
|-----|-------|
| **WHY** | 한국어 이력서에 최적화된 무료 폰트 부재 → 구직자 페인 + 인크루트 브랜드 차별화 기회 |
| **WHO** | (1) 인크루트 이력서 에디터 사용자 (Beachhead) → (2) 한국 디자이너/개발자 → (3) 일반 구직자 |
| **RISK** | 디자이너 의존성(글리프 정제), 라이선스 호환성(Pretendard/Min Sans 영향), Pretendard 대비 차별화 모호 |
| **SUCCESS** | M+12: 인크루트 자체 서비스 100% 적용, GitHub Star 500+, 외부 채용 플랫폼 1곳 채택, NPS Δ +5pt |
| **SCOPE** | Variable Font (wght 100–900), KS X 1001 한글 2,350자, Latin/숫자/기호, OTF/TTF/WOFF2, OFL 1.1 |

---

## 1. Overview

### 1.1 Design Goals

1. **빌드 자동화**: Glyphs 소스 → 8개 인스턴스 + Variable Font를 단일 명령(`python3 build/build.py`)으로 생성.
2. **인터폴레이션 품질**: Regular + Bold 두 마스터에서 Medium/SemiBold가 시각적으로 자연스럽게 보간.
3. **이력서 가독성**: 10–18pt에서 한글 자모(ㅎ/ㅁ/ㅇ) 가독성 보장, Tabular Figures 자릿수 정렬.
4. **Min Sans 곡선**: 모서리 라운딩 20–40 UPM, ㄴ/ㄹ/ㅂ 끝부분 부드러움.
5. **호환성 보장**: WOFF2 (웹), OTF (macOS), TTF (Windows/HWP), 모든 브라우저 + Word + HWP.
6. **OFL 1.1 준수**: 라이선스 헤더 + 메타데이터 + Pretendard 인용 attribution.

### 1.2 Design Principles

- **Pretendard 호환 메트릭**: 마이그레이션 비용 0을 위해 ascender/descender/x-height 동일.
- **Min Sans 영감의 모서리**: 차별화 포인트는 곡선 처리에 집중 (이름/전체 톤은 Pretendard 계열 유지).
- **Variable First**: 8 인스턴스는 VF에서 추출. 별도 마스터 추가는 시각 검증 실패 시에만.
- **CSS 토큰 우선**: 직접 `font-weight: 700` 대신 `var(--is-weight-bold)` 사용. 향후 굵기 매핑 변경 자유도 확보.
- **Single Source of Truth**: `sources/IncruitSans-Regular.glyphs`가 유일한 진실. 빌드 산출물은 git 미포함.

---

## 2. Architecture Options

### 2.0 Architecture Comparison

폰트 마스터 구성 + 빌드 파이프라인 구조에 대한 3가지 아키텍처 옵션:

| Criteria | Option A: Minimal | Option B: Clean | Option C: Pragmatic |
|----------|:-:|:-:|:-:|
| **Approach** | 2 마스터 (Regular+Bold), 단순 보간 | 5 마스터 (Thin/Light/Regular/Bold/Black), 정밀 제어 | 2 마스터 + Light hint 보조, 검증 후 확장 |
| **Masters** | 2 (Regular 400, Bold 700) | 5 (Thin 100, Light 300, Regular 400, Bold 700, Black 900) | 2 (Regular 400, Bold 700) → v1.5에서 Light 추가 |
| **Glyph Edit Effort** | 2× 글리프 정제 (2,505 × 2 = 5,010) | 5× 글리프 정제 (12,525) | 2× 글리프 정제 + 점진 확장 |
| **Interpolation Quality** | 보통 (극단 굵기에서 어색 가능) | 매우 좋음 (모든 굵기 정밀 제어) | 좋음 (검증 후 마스터 추가) |
| **Designer Time** | 3개월 (외주 1명) | 8개월 (외주 2명) | 3개월 (v1.0) + 2개월 (v1.5) |
| **Risk** | Medium (Thin/Black 품질 저하 가능) | Low (모든 굵기 검증) | Low (점진 확장으로 리스크 분산) |
| **Cost** | 낮음 | 높음 | 중간 |
| **Recommendation** | MVP, 빠른 출시 | 품질 최우선, 장기 | **Default — 검증 후 확장** |

**Selected**: **Option C: Pragmatic** — **Rationale**:
- v1.0은 Regular + Bold 2 마스터로 빠르게 출시 (3개월 디자이너 일정 확보)
- 잘쓸랩 시범 적용 후 시각 검증 → Thin/Black 품질 저하 발견 시 v1.5에서 Light 마스터 추가
- 디자이너 리소스 리스크(R1) 분산 + 비용 효율
- Pretendard도 초기엔 2 마스터 → 점진 확장 경로를 검증함

> **참고**: Option A를 검증하다 품질 이슈가 발견되면 Option C로 자연스럽게 확장. Option B는 Phase 2(M+12 이후)에 검토.

---

### 2.1 Component Diagram

```
┌──────────────────────┐
│  Glyphs 3 (Designer) │
│  .glyphs JSON 편집   │
└──────────┬───────────┘
           │ commit
           ▼
┌──────────────────────────────────────────┐
│  sources/IncruitSans-Regular.glyphs      │
│  (Single Source of Truth, JSON)          │
│   - fontMaster: [Regular, Bold]          │
│   - glyphs: [104→2,505]                  │
│   - instances: [Thin..Black, 8개]        │
└──────────┬───────────────────────────────┘
           │ python3 build/build.py
           ▼
┌──────────────────────────────────────────┐
│  build/ Pipeline (fontmake + fontTools)  │
│  ┌────────────┐  ┌────────────┐          │
│  │ validate_  │→ │ fontmake   │          │
│  │ glyphs.py  │  │  -o otf -d │          │
│  └────────────┘  └─────┬──────┘          │
│                        │                  │
│                  ┌─────┴──────┐          │
│                  │ fontmake   │          │
│                  │  -o ttf -d │          │
│                  └─────┬──────┘          │
│                        │                  │
│                  ┌─────┴──────────┐      │
│                  │ ttfautohint    │      │
│                  └─────┬──────────┘      │
│                        │                  │
│                  ┌─────┴──────────┐      │
│                  │ woff2_compress │      │
│                  └─────┬──────────┘      │
└────────────────────────┼─────────────────┘
                         ▼
┌──────────────────────────────────────────┐
│  fonts/ (gitignore — CI 아티팩트만)      │
│   ├── otf/   IncruitSans-{Style}.otf ×8  │
│   ├── ttf/   IncruitSans-{Style}.ttf ×8  │
│   ├── webfonts/ *.woff2 ×8               │
│   └── IncruitSans-VF.ttf (Variable Font) │
└──────────┬───────────────────────────────┘
           │ GitHub Release (CI)
           ▼
┌──────────────────────────────────────────┐
│  Distribution                             │
│  ┌─────────────┐ ┌─────────────┐         │
│  │ GitHub      │ │ npm registry│         │
│  │ Releases    │ │ incruit-sans│         │
│  └─────────────┘ └─────────────┘         │
│  ┌─────────────┐ ┌─────────────┐         │
│  │ jslab CDN   │ │ jsdelivr    │         │
│  │ (자체)      │ │ (mirror)    │         │
│  └─────────────┘ └─────────────┘         │
└──────────┬───────────────────────────────┘
           │ @import / <link>
           ▼
┌──────────────────────────────────────────┐
│  Consumers                                │
│  ┌──────────────┐ ┌─────────────────┐    │
│  │ 인크루트     │ │ 잘쓸랩          │    │
│  │ 이력서 에디터 │ │ jslab.incruit  │    │
│  └──────────────┘ └─────────────────┘    │
│  ┌──────────────┐ ┌─────────────────┐    │
│  │ incruit.com  │ │ 외부 OSS 사용자 │    │
│  └──────────────┘ └─────────────────┘    │
└──────────────────────────────────────────┘
```

### 2.2 Data Flow

```
[Designer]                [Build Pipeline]              [Web Consumer]
    │                            │                            │
    │ Glyphs 3 편집              │                            │
    ├──→ .glyphs (JSON) ────────→│                            │
    │                            │ validate                   │
    │                            ├──→ ✓ 마스터/글리프 검증    │
    │                            │                            │
    │                            │ fontmake -o otf            │
    │                            ├──→ OTF (8개)               │
    │                            │                            │
    │                            │ fontmake -o ttf            │
    │                            ├──→ TTF (8개)               │
    │                            │                            │
    │                            │ fontmake -o variable       │
    │                            ├──→ VF (1개)                │
    │                            │                            │
    │                            │ ttfautohint                │
    │                            ├──→ TTF (hinted)            │
    │                            │                            │
    │                            │ woff2_compress             │
    │                            ├──→ WOFF2 (8개)             │
    │                            │                            │
    │                            │ GitHub Release              │
    │                            ├───────────────────────────→│
    │                                                          │
    │                                       <link rel="font">  │
    │                                       @font-face         │
    │                                       var(--is-weight-*) │
    │                                                          ▼
    │                                               [Browser Render]
```

### 2.3 Dependencies

| Component | Depends On | Purpose |
|-----------|-----------|---------|
| `build/build.py` | fontmake, fontTools, ttfautohint | 빌드 오케스트레이션 |
| `build/validate_glyphs.py` | json (stdlib) | 마스터/글리프 무결성 검증 |
| `build/setup_bold_master.py` | json, copy (stdlib) | Bold 마스터 자동 생성 |
| fontmake | fontTools, glyphsLib, ufo2ft | Glyphs → OTF/TTF 변환 |
| GitHub Actions | python:3.11, fontmake | CI/CD 자동 빌드 |
| 인크루트 에디터 | `tokens/weight.css`, WOFF2 | 폰트 적용 + 토큰 사용 |

---

## 3. Data Model

### 3.1 Glyphs File Schema (JSON)

`sources/IncruitSans-Regular.glyphs`는 Glyphs 3 JSON 포맷:

```typescript
interface GlyphsFile {
  ".appVersion": string;          // Glyphs 앱 버전
  "familyName": string;            // "Incruit Sans"
  "unitsPerEm": number;            // 1000 (UPM)
  "versionMajor": number;          // 0
  "versionMinor": number;          // 1
  "date": string;                  // ISO timestamp

  fontMaster: FontMaster[];        // [Regular, Bold]
  glyphs: Glyph[];                 // 한글 + Latin + 숫자 + 기호
  instances: Instance[];           // 8개 (Thin..Black)
  classes: GlyphClass[];           // OpenType class
  features: OTFeature[];           // tnum, kern, liga
  featurePrefixes: FeaturePrefix[];

  customParameters: CustomParam[];
  kerningLTR: Record<string, number>;
  kerningRTL: Record<string, number>;
  userdata: Record<string, unknown>;
}

interface FontMaster {
  customName: "Regular" | "Bold";
  id: string;                      // "master-regular" | "bold-master-N"
  ascender: 800;
  descender: -200;
  capHeight: 750;
  xHeight: 500;
  customParameters: CustomParam[]; // typoAscender, winAscender, etc.
}

interface Glyph {
  glyphname: string;               // "A", "uni3131" (한글 ㄱ), "zero.tnum"
  unicode?: string;                // "0041" (Latin), "AC00" (한글 가)
  layers: GlyphLayer[];            // 마스터당 1 레이어
  category?: string;               // "Letter", "Number", "Symbol"
  subCategory?: string;            // "Hangul", "Latin", "Decimal Digit"
  export?: boolean;                // 빌드 시 포함 여부
}

interface GlyphLayer {
  layerId: string;                 // 마스터 ID 매칭
  width: number;                   // advance width (UPM)
  shapes: Shape[];                 // path/component
  anchors?: Anchor[];
  guides?: Guide[];
  hints?: Hint[];                  // TrueType hinting
}

interface Instance {
  name: string;                    // "Thin", "Light", "Regular", ...
  type: "instance";
  axesValues: [number];            // [100], [400], [700], [900]
  customParameters: CustomParam[];
  weightValue: number;             // wght 축 값
  isBold?: boolean;
  isItalic?: boolean;
}
```

### 3.2 Master ↔ Instance 관계

```
fontMaster (소스)              instances (산출물)
┌──────────────┐               ┌──────────────┐
│ Regular (400)│──┐            │ Thin     100 │ extrapolated
└──────────────┘  │            │ ExtraLight 200│ extrapolated
                  │ interpolate│ Light     300 │ extrapolated
                  ├───────────→│ Regular   400 │ exact (master)
┌──────────────┐  │            │ Medium    500 │ interpolated
│ Bold     (700)│─┘            │ SemiBold  600 │ interpolated
└──────────────┘               │ Bold      700 │ exact (master)
                               │ ExtraBold 800 │ extrapolated
                               │ Black     900 │ extrapolated
                               └──────────────┘
```

> **주의**: Thin(100) / Black(900)은 extrapolation으로 생성됨. 시각 검증 후 품질 저하 시 v1.5에서 Light/ExtraBold 마스터 추가 (Option C).

### 3.3 Glyph Coverage Plan

| Phase | Set | Count | Source | Status |
|-------|-----|:-----:|--------|:------:|
| **Template** | 한글 14자 + Latin 52자 + 숫자 10자 + 기호 28자 | 104 | `generate_glyphs_template.py` | ✅ |
| **Phase A** (v0.5) | Latin 95자 + 숫자 20자 (tnum 포함) + 기호 50자 + 한글 고빈도 500자 | 665 | 디자이너 정제 | ⏳ |
| **Phase B** (v1.0) | Phase A + KS X 1001 한글 2,350자 (전체) | 2,505 | 디자이너 정제 | ⏳ |
| **Phase C** (v1.5) | Phase B + 그리스 24자 + 키릴 33자 + 통화 기호 10자 | 2,572 | 디자이너 정제 | 📅 |

**한글 고빈도 500자 기준**: 국립국어원 빈도 조사 상위 500자 (이력서 텍스트 95%+ 커버).

---

## 4. CSS / OpenType Specification

### 4.1 CSS Variables (디자인 토큰)

```css
/* tokens/weight.css */
:root {
  /* 굵기 6단계 프리셋 */
  --is-weight-body:       350;  /* 이력서 본문 */
  --is-weight-regular:    400;  /* 기본 텍스트 */
  --is-weight-medium:     500;  /* 강조, 회사명 */
  --is-weight-semibold:   600;  /* 섹션 타이틀 */
  --is-weight-bold:       700;  /* 이름, 제목 */
  --is-weight-extrabold:  800;  /* 배너 헤딩 */

  /* 이력서 컨텍스트 권장 프리셋 */
  --is-resume-name:       700;  /* 이름 */
  --is-resume-section:    600;  /* "경력사항", "학력" */
  --is-resume-company:    500;  /* 회사명, 직책 */
  --is-resume-body:       400;  /* 본문 */
  --is-resume-caption:    350;  /* 캡션, 메타 */
}
```

### 4.2 @font-face Declaration

```css
/* Variable Font (단일 파일) */
@font-face {
  font-family: 'Incruit Sans';
  src: url('IncruitSans-VF.woff2') format('woff2-variations'),
       url('IncruitSans-VF.woff2') format('woff2');
  font-weight: 100 900;
  font-style: normal;
  font-display: swap;
}

/* 정적 인스턴스 (개별 파일, IE11 등 fallback) */
@font-face {
  font-family: 'Incruit Sans';
  src: url('IncruitSans-Regular.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}
/* ... Bold, Medium, SemiBold ... */
```

### 4.3 OpenType Features

| Feature | Tag | 활성화 | 설명 |
|---------|-----|:------:|------|
| Tabular Figures | `tnum` | **Default ON** (이력서 컨텍스트) | 숫자 자릿수 정렬 |
| Kerning | `kern` | Default ON | 자동 자간 |
| Standard Ligatures | `liga` | Default ON | fi, fl 등 |
| Lining Figures | `lnum` | Optional | 라이닝 숫자 (대문자 높이) |
| Old-style Figures | `onum` | Optional | 올드스타일 숫자 |
| Stylistic Set 01 | `ss01` | Won't (v1) | 향후 곡선 변형 |

```css
/* 이력서 본문에서 tnum 활성 */
body {
  font-family: 'Incruit Sans', sans-serif;
  font-weight: var(--is-resume-body);
  font-feature-settings: "tnum" 1, "kern" 1, "liga" 1;
}
```

### 4.4 Polyfill / Fallback Chain

```css
font-family:
  'Incruit Sans',           /* 메인 */
  'Pretendard',             /* 1차 fallback (호환 메트릭) */
  '-apple-system',          /* iOS/macOS */
  'BlinkMacSystemFont',     /* Chrome on macOS */
  'Segoe UI',               /* Windows */
  'Malgun Gothic',          /* Windows 한글 */
  'Apple SD Gothic Neo',    /* macOS 한글 */
  sans-serif;
```

---

## 5. UI/UX Design (Specimen + Resume Test)

### 5.1 specimen.html — 굵기/크기 매트릭스

```
┌────────────────────────────────────────────────┐
│  Incruit Sans                                  │
│  Variable Font Specimen                        │
├────────────────────────────────────────────────┤
│  Body 350  | 다람쥐 헌 쳇바퀴에 타고파         │
│  Regular   | 다람쥐 헌 쳇바퀴에 타고파         │
│  Medium    | 다람쥐 헌 쳇바퀴에 타고파         │
│  SemiBold  | 다람쥐 헌 쳇바퀴에 타고파         │
│  Bold      | 다람쥐 헌 쳇바퀴에 타고파         │
│  ExtraBold | 다람쥐 헌 쳇바퀴에 타고파         │
├────────────────────────────────────────────────┤
│  Size Test (Regular)                            │
│  10pt: 채용공고 — 시니어 프론트엔드 개발자     │
│  12pt: 채용공고 — 시니어 프론트엔드 개발자     │
│  14pt: 채용공고 — 시니어 프론트엔드 개발자     │
│  18pt: 채용공고                                 │
│  24pt: 채용공고                                 │
├────────────────────────────────────────────────┤
│  Latin / Numbers / Symbols                      │
│  ABCDEFGHIJKLMNOPQRSTUVWXYZ                     │
│  abcdefghijklmnopqrstuvwxyz                     │
│  0123456789  !@#$%^&*()                         │
├────────────────────────────────────────────────┤
│  Tabular Figures Test                           │
│  연봉 12,000,000원                              │
│  연봉  9,500,000원                              │
│  연봉    800,000원   ← 자릿수 정렬 확인         │
└────────────────────────────────────────────────┘
```

### 5.2 resume-test.html — 실제 이력서 레이아웃

```
┌────────────────────────────────────────────────┐
│  김취준                            [700, 28pt] │
│  Frontend Developer                [400, 14pt] │
├────────────────────────────────────────────────┤
│                                                 │
│  경력사항                          [600, 16pt] │
│  ──────────                                     │
│                                                 │
│  인크루트 (2024.03 - 현재)         [500, 14pt] │
│  Frontend Engineer                  [400, 13pt] │
│  • React/Next.js 기반 이력서 에디터 개발       │
│  • TypeScript 도입 및 코드베이스 마이그레이션  │
│                                                 │
│  연봉: 50,000,000원                 [tnum 활성] │
│  KPI: 95.5% 달성                                │
│                                                 │
├────────────────────────────────────────────────┤
│  학력                              [600, 16pt] │
│  ────                                           │
│  서울대학교 컴퓨터공학부 (2020-2024)            │
│  GPA: 3.85/4.5                      [tnum 활성] │
└────────────────────────────────────────────────┘
```

### 5.3 Page UI Checklist

#### specimen.html
- [ ] Heading: "Incruit Sans Specimen" (font-weight: 800, size: 32pt)
- [ ] Section: 6개 굵기 프리셋 라벨 + 샘플 텍스트 (다람쥐 헌 쳇바퀴)
- [ ] Section: 5개 크기(10/12/14/18/24pt) 동일 텍스트 비교
- [ ] Section: Latin 대문자/소문자/숫자/기호 4줄
- [ ] Section: Tabular Figures 테스트 — 자릿수 다른 3개 숫자 수직 정렬
- [ ] Section: 한글 자모 가독성 — "흙, 햇, 흥, 곱, 빛" 10pt 표시
- [ ] Toggle: Variable axis slider (wght 100→900 실시간 조정)
- [ ] Console: 0 errors

#### resume-test.html
- [ ] Header: 이름 (font-weight: 700, 28pt)
- [ ] Header: 직책 (font-weight: 400, 14pt)
- [ ] Section title: "경력사항" (font-weight: 600, 16pt)
- [ ] Company name: (font-weight: 500, 14pt)
- [ ] Body: bullet list (font-weight: 400, 13pt)
- [ ] Number: 연봉/KPI 숫자가 tnum으로 자릿수 정렬됨
- [ ] Layout: A4 비율(210×297mm) 컨테이너
- [ ] Print: `@media print` 적용 시 폰트 임베딩 확인

---

## 6. Error Handling

### 6.1 Build Pipeline Errors

| Error | Cause | Handling |
|-------|-------|----------|
| `❌ sources/IncruitSans-Regular.glyphs not found` | 소스 파일 부재 | 사용자에게 `generate_glyphs_template.py` 실행 안내 |
| `❌ Regular 마스터를 찾을 수 없습니다` | fontMaster 키 누락 또는 customName 불일치 | validate_glyphs.py로 사전 검증 + 구조 확인 메시지 |
| `❌ Bold 마스터가 이미 존재합니다` | 중복 실행 | 사용자 확인(y/n) 후 덮어쓰기 |
| `fontmake: glyph X has no contours in master Y` | 글리프가 한 마스터에만 존재 | validate_glyphs.py에서 사전 감지 → 빌드 중단 |
| `fontmake: interpolation failed` | 마스터 간 노드 수 불일치 | Glyphs 3에서 글리프 호환성 검사 (`Filter > Compatibility`) |
| `woff2_compress: file too large` | TTF 파일 4MB 초과 | 글리프 축소 또는 hinting 최적화 |
| `ttfautohint: error processing` | TrueType 노드 오류 | Glyphs 3에서 TTF export 모드 검증 |

### 6.2 Runtime / CSS Errors

| Error | Cause | Handling |
|-------|-------|----------|
| FOUT (Flash of Unstyled Text) | 폰트 로딩 지연 | `font-display: swap` + WOFF2 preload |
| FOIT (Flash of Invisible Text) | font-display 부적절 | `font-display: swap` 강제 |
| 한글 깨짐 (□ 표시) | 글리프 미포함 또는 CSS 누락 | Fallback chain (Pretendard → 시스템 폰트) |
| Tabular Figures 미적용 | font-feature-settings 누락 | CSS reset에 `"tnum" 1` 강제 |
| Variable axis 무시됨 | 브라우저 미지원 | `@supports (font-variation-settings: normal)` 분기 |

### 6.3 Validation Output Format

```bash
$ python3 build/validate_glyphs.py

📂 검증 중: sources/IncruitSans-Regular.glyphs

✅ 마스터 구성: Regular + Bold
✅ 글리프 통계: 2505 (Regular: 2505/2505, Bold: 2505/2505)
✅ Unicode 매핑: 모든 한글 KS X 1001 포함
⚠️  경고: 'uni3131' (ㄱ)이 Bold 마스터에서 노드 수 불일치 (Regular: 12, Bold: 14)
❌ 오류: 'A' 글리프가 Bold 마스터에 없음
```

---

## 7. Security / Legal Considerations

### 7.1 OFL 1.1 Compliance Checklist

- [ ] LICENSE 파일에 OFL 1.1 전문 포함 ✅ (이미 존재)
- [ ] 모든 폰트 메타데이터(`name table`)에 OFL 1.1 명시
- [ ] Reserved Font Name: "Incruit Sans" — Modified Version은 사용 불가
- [ ] Copyright: "Copyright 2026 Incruit Corp. (fonts@incruit.com)"
- [ ] OFL 인용: README + 폰트 자체 메타데이터 동봉
- [ ] Pretendard / Min Sans 영감 attribution (README 명시)
- [ ] Modified Version 가이드라인 (README 명시)

### 7.2 Trademark / Naming

- [ ] **KIPRIS 검색**: "Incruit Sans" 한국 상표 등록 여부 — 법무 진행 (R3)
- [ ] **USPTO 검색**: 미국 상표 충돌 검토
- [ ] **GitHub/npm 검색**: "incruit-sans" 패키지명 가용성 확인
- [ ] **글로벌 폰트 DB 검색**: Google Fonts, Adobe Fonts, MyFonts 등에 동명 폰트 없음 확인

### 7.3 Source Code License

- 빌드 스크립트 (`build/*.py`): MIT 또는 OFL 동일 적용 검토
- HTML 테스트 페이지 (`tests/*.html`): MIT
- 디자인 토큰 (`tokens/*.css`): OFL 1.1 (폰트 일부)
- 문서 (`docs/*.md`): CC BY 4.0 권장

### 7.4 Privacy

- 폰트 자체는 추적 코드 미포함
- CDN 서빙 시 CORS 헤더 필요 (`Access-Control-Allow-Origin: *`)
- `font-display: swap`으로 사용자 경험 차단 방지

---

## 8. Test Plan

### 8.1 Test Scope

| Type | Target | Tool | Phase |
|------|--------|------|-------|
| **L1: Build Test** | 빌드 명령 + 산출물 검증 | bash + python | Do |
| **L2: Glyph Validation** | 마스터/글리프 무결성 | validate_glyphs.py + fontTools | Do |
| **L3: Visual Test** | specimen.html / resume-test.html 렌더링 | Playwright + 5개 브라우저 | Do/Check |
| **L4: Compatibility Test** | Word/HWP/PDF/ATS 호환성 | 수동 + 실기기 | Check |
| **L5: Performance Test** | 파일 크기, 로딩 시간 | Lighthouse + ls | Check |

### 8.2 L1: Build Test Scenarios

| # | Command | Expected Output | Verification |
|---|---------|-----------------|-------------|
| 1 | `python3 build/setup_bold_master.py` | Bold 마스터 추가, 104 글리프 복사 | grep "✅ Bold 마스터 생성" |
| 2 | `python3 build/validate_glyphs.py` | 마스터 2개, 글리프 100% | grep "✅ Regular + Bold 마스터 완벽" |
| 3 | `python3 build/build.py` | OTF×8 + TTF×8 + WOFF2×8 + VF×1 | `ls fonts/{otf,ttf,webfonts}/*.{otf,ttf,woff2}` |
| 4 | `python3 build/build.py --clean` | fonts/ 정리 후 재빌드 | `find fonts/ -newer /tmp/before` |
| 5 | GitHub Actions push | CI 통과, 아티팩트 업로드 | gh run list --workflow=build-fonts.yml |

### 8.3 L2: Glyph Validation Scenarios

| # | Test | Expected | Tool |
|---|------|----------|------|
| 1 | 모든 글리프가 양 마스터에 존재 | Regular: 2505/2505, Bold: 2505/2505 | validate_glyphs.py |
| 2 | 마스터 간 노드 수 일치 | 모든 글리프 호환 | fontmake compatibility check |
| 3 | Unicode 매핑 정확성 | KS X 1001 한글 전체 포함 | `python -m fontTools.ttx` |
| 4 | 메트릭 일관성 | ascender/descender/xHeight 동일 | validate_glyphs.py |
| 5 | OpenType feature 적용 | tnum, kern, liga 활성 | `python -m fontTools.ttx` features |

### 8.4 L3: Visual Test Scenarios

| # | Page | Action | Expected | Verification |
|---|------|--------|----------|-------------|
| 1 | specimen.html | 페이지 로드 | 6개 굵기 모두 표시 | Playwright screenshot diff |
| 2 | specimen.html | wght slider 100→900 | 굵기 실시간 변경 | screenshot at 5 stops |
| 3 | specimen.html | Tabular Figures 섹션 | 12,000,000 / 9,500,000 / 800,000 자릿수 정렬 | pixel x-position 비교 |
| 4 | resume-test.html | A4 출력 모드 | print CSS 적용, 한 페이지 fit | `@media print` 활성 |
| 5 | resume-test.html | 10pt 한글 자모 | "흙/햇/흥" 가독 | 디자이너 + 사용자 5명 |

### 8.5 L4: Compatibility Test Scenarios

| # | Environment | Test | Expected |
|---|-------------|------|----------|
| 1 | macOS Safari 17+ | specimen.html 렌더링 | 모든 굵기 + Variable 정상 |
| 2 | Windows Chrome 120+ | specimen.html 렌더링 | 한글 깨짐 0 |
| 3 | iOS Safari 17+ | resume-test.html | 모바일 viewport 정상 |
| 4 | Word 2019 | OTF 설치 → 한글 입력 | 폰트 표시 + 자간 정상 |
| 5 | HWP 2020 | OTF 설치 → 한글 입력 | 폰트 표시 + 줄바꿈 정상 |
| 6 | Adobe Acrobat | PDF 임베딩 검증 | 폰트 임베디드, 누락 0 |
| 7 | ATS: Workday | PDF 업로드 → 텍스트 추출 | 한글 추출 정확 |
| 8 | ATS: Greenhouse | PDF 업로드 → 텍스트 추출 | 한글 추출 정확 |

### 8.6 L5: Performance Test Scenarios

| # | Metric | Target | Tool |
|---|--------|--------|------|
| 1 | WOFF2 VF 파일 크기 | ≤ 350KB | `ls -lh fonts/webfonts/*.woff2` |
| 2 | OTF 단일 인스턴스 크기 | ≤ 1.5MB | `ls -lh fonts/otf/*.otf` |
| 3 | 초기 로딩 시간 (3G) | ≤ 200ms | Lighthouse (Slow 3G throttle) |
| 4 | First Contentful Paint | ≤ 1.5s | Lighthouse |
| 5 | Cumulative Layout Shift | ≤ 0.1 | Lighthouse |

### 8.7 Seed Data Requirements

폰트 프로젝트는 별도 DB seed 불필요. 단, 테스트용 데이터:

| Asset | Purpose | Location |
|-------|---------|----------|
| 샘플 이력서 텍스트 | resume-test.html | `tests/data/sample-resume.json` (생성 예정) |
| 한글 빈도 텍스트 | 가독성 테스트 | `tests/data/korean-frequency.txt` (생성 예정) |
| Tabular 숫자 세트 | tnum 검증 | `tests/data/tnum-test.json` (생성 예정) |

---

## 9. Architecture (Font Project Specific)

### 9.1 Layer Structure (폰트 특화 변형)

| Layer | Responsibility | Location |
|-------|---------------|----------|
| **Source** | 글리프 정의 (디자이너 작업) | `sources/*.glyphs` |
| **Build** | 빌드 자동화, 검증 | `build/*.py` |
| **Asset** | 빌드 산출물 (OTF/TTF/WOFF2) | `fonts/` (gitignore) |
| **Token** | CSS 변수, 디자인 토큰 | `tokens/*.css` |
| **Documentation** | 사양서, 가이드 | `docs/` |
| **Verification** | 시각 테스트, 호환성 검증 | `tests/` |
| **Distribution** | 패키지 메타데이터, README | `package.json`, `README.md`, `.github/` |

### 9.2 Dependency Rules

```
[Source] → [Build] → [Asset] → [Distribution]
              │
              └→ [Verification] (read-only)

[Token] → [Distribution] (CSS는 별도 채널)
[Documentation] (independent, references all)
```

**Rule**: Build는 Source에 read-only. Asset은 빌드 산출물로 절대 직접 수정 금지. 디자이너는 Source만 수정.

### 9.3 File Convention

| Item | Convention |
|------|-----------|
| Glyph source | `sources/IncruitSans-{Style}.glyphs` (단일 파일, 모든 마스터 포함) |
| Build output (OTF) | `fonts/otf/IncruitSans-{Style}.otf` (Style: Thin, Light, ..., Black) |
| Build output (Variable) | `fonts/IncruitSans-VF.{ttf,woff2}` |
| CSS token | `tokens/{purpose}.css` (purpose: weight, color, ...) |
| Build script | `build/{action}.py` (action: build, validate, setup_bold_master, ...) |
| Test page | `tests/{type}.html` (type: specimen, resume-test, ...) |
| Doc | `docs/{kebab-case}.md` |

---

## 10. Naming & Convention Reference

### 10.1 Glyph Naming

| Type | Pattern | Example |
|------|---------|---------|
| Latin | AGLFN | `A`, `a`, `zero`, `period` |
| 한글 자모 | `uni{HEX}` | `uni3131` (ㄱ), `uniAC00` (가) |
| Tabular variant | `{base}.tnum` | `zero.tnum`, `one.tnum` |
| Stylistic alt | `{base}.ss01` | `a.ss01` (v2.0+) |

### 10.2 Style Naming (Pretendard 호환)

| Weight | Style Name | PostScript Name |
|--------|-----------|-----------------|
| 100 | Thin | `IncruitSans-Thin` |
| 200 | ExtraLight | `IncruitSans-ExtraLight` |
| 300 | Light | `IncruitSans-Light` |
| 400 | Regular | `IncruitSans-Regular` |
| 500 | Medium | `IncruitSans-Medium` |
| 600 | SemiBold | `IncruitSans-SemiBold` |
| 700 | Bold | `IncruitSans-Bold` |
| 800 | ExtraBold | `IncruitSans-ExtraBold` |
| 900 | Black | `IncruitSans-Black` |

### 10.3 Version Convention

```
MAJOR.MINOR.PATCH

MAJOR:  파괴적 변경 (메트릭 변경, 글리프 set 변경)
MINOR:  기능 추가 (새 weights, 새 features, 새 글리프)
PATCH:  버그 수정 (글리프 정제, hinting 개선)

v0.1.0 - 초기 템플릿 (현재)
v0.5.0 - Phase A 글리프 정제 (한글 500자) — 잘쓸랩 시범
v1.0.0 - Phase B 완료 (한글 2,350자) — OFL 공개
v1.5.0 - Phase C (그리스/키릴) + Light 마스터 추가 (필요 시)
v2.0.0 - Italic 또는 Display variant
```

### 10.4 Commit Convention

```
{동사} {대상}: {상세}

예시:
- 추가 한글 ㄱ 행 글리프 (가-깋, 50자)
- 수정 Bold 마스터 ㅎ 자모 곡선 반지름
- 개선 specimen.html Variable axis slider 반응성
- 빌드 v0.5.0 — Phase A 글리프 정제 완료
```

---

## 11. Implementation Guide

### 11.1 File Structure (이미 구축됨, 확장 영역만)

```
incruit-sans/
├── sources/
│   ├── IncruitSans-Regular.glyphs       # ✅ 템플릿 (104자)
│   └── IncruitSans-Regular.glyphs.backup # ✅ 백업
│
├── build/                               # ✅ 모든 스크립트 존재
│   ├── build.py                         # ✅
│   ├── validate_glyphs.py               # ✅
│   ├── setup_bold_master.py             # ✅
│   ├── requirements.txt                 # ✅
│   └── (참고용 .otf 파일들 — gitignore 필요)
│
├── tokens/weight.css                    # ✅
│
├── tests/
│   ├── specimen.html                    # ✅ (개선 필요: VF slider, tnum 섹션)
│   ├── resume-test.html                 # ✅ (개선 필요: A4 print mode)
│   └── data/                            # ⏳ 생성 필요
│       ├── sample-resume.json
│       ├── korean-frequency.txt
│       └── tnum-test.json
│
├── docs/
│   ├── 00-pm/incruit-sans.prd.md        # ✅
│   ├── 01-plan/features/incruit-sans.plan.md  # ✅
│   ├── 02-design/features/incruit-sans.design.md  # ✅ (이 문서)
│   └── (기존 문서들)                    # ✅
│
├── .github/workflows/build-fonts.yml    # ✅
├── CHANGELOG.md                         # ⏳ 생성 필요
├── package.json                         # ⏳ v0.6+ 시점
└── .gitignore                           # ⏳ 정비 필요
```

### 11.2 Implementation Order (v1.0까지)

#### Module 1: Build Pipeline 검증 + 보완 (v0.2)
1. [x] `.gitignore` 정비 (fonts/, venv/, build/*.otf 빌드 참고용) — ✅ 2026-04-25 완료
2. [x] CHANGELOG.md 생성 (Keep a Changelog 포맷) — ✅ 2026-04-25 완료
3. [ ] `build/build.py` 실제 실행 → Module 2에서 unblock (디자이너 .glyphs 저장 후)
4. [ ] GitHub Actions CI 실행 검증 → Module 2에서 unblock
5. [x] WOFF2 파일 크기 측정 (베이스라인: 1.11MB VF / 713–818KB 정적, **참고용 폰트 한글 2,505자 풀셋 기준**) — ✅ 2026-04-25 완료
   - 초기 목표 "≤ 350KB"는 v0.5 (한글 고빈도 500자) 기준으로 재해석. 풀셋 기준 NFR은 Plan §3.2에서 1.2MB로 보정됨 (Analysis M2 반영)

#### Module 2: Phase A — Latin + 숫자 + 기호 정제 (v0.3)
1. [ ] 디자이너 계약 (Open Q#2 해결 후)
2. [ ] Latin 95자 정제 (Regular + Bold 마스터)
3. [ ] 숫자 0-9 + tnum variant (zero.tnum 등)
4. [ ] 기본 기호 50자 (.,!?@#$ 등)
5. [ ] specimen.html 시각 검증

#### Module 3: Phase A — 한글 고빈도 500자 (v0.5)
1. [ ] 빈도 상위 500자 리스트 작성 (국립국어원 기반)
2. [ ] 자모 단위 모듈화 (ㄱ-ㅎ 14자모 + 모음 21자 + 받침 27자)
3. [ ] 정자체 → 합성 → 시각 보정 워크플로우
4. [ ] 잘쓸랩 시범 적용 → 1주 모니터링
5. [ ] 사용자 피드백 수집 (Sentry, NPS)

#### Module 4: Phase B — KS X 1001 한글 2,350자 (v1.0)
1. [ ] 나머지 1,850자 정제
2. [ ] Variable Font 빌드 검증
3. [ ] ATS 호환성 5개 시스템 테스트
4. [ ] 인크루트 이력서 에디터 통합 PR
5. [ ] OFL 라이선스 + 상표 검증 완료

#### Module 5: OSS 공개 + 배포 (v1.0 launch)
1. [ ] GitHub `incruit/incruit-sans` repo 공개
2. [ ] npm 배포 (`incruit-sans` 패키지)
3. [ ] CDN 미러 설정 (jsdelivr)
4. [ ] 디자인 커뮤니티 공지 (디스콰이엇, 폰트, Velog)
5. [ ] 인크루트 블로그 시리즈

### 11.3 Session Guide

#### Module Map

| Module | Scope Key | Description | Owner | Estimated Duration |
|--------|-----------|-------------|-------|:------------------:|
| 1. Build Pipeline 보완 | `module-1-build` | gitignore, CHANGELOG, 빌드 검증 | Claude | 1 session |
| 2. Latin 정제 | `module-2-latin` | Latin 95자 + 숫자 + 기호 | 디자이너 | 2-3주 |
| 3. 한글 고빈도 500자 | `module-3-hangul-a` | 이력서 텍스트 95% 커버 | 디자이너 | 6-8주 |
| 4. 한글 2,350자 + 검증 | `module-4-hangul-b` | KS X 1001 전체 + ATS 테스트 | 디자이너 + Claude | 12-16주 |
| 5. OSS 공개 | `module-5-launch` | GitHub/npm 배포, 마케팅 | Claude + 마케팅 | 2주 |

#### Recommended Session Plan

| Session | Phase | Scope | Owner | Turns/Duration |
|---------|-------|-------|-------|:--------------:|
| Session 1 | PM + Plan + Design | 전체 | Claude | ✅ 완료 |
| Session 2 | Do | `--scope module-1-build` | Claude | 1 session |
| Session 3 | Do | `--scope module-2-latin` | 디자이너 (Glyphs 3) | 2-3주 |
| Session 4 | Check (Phase A) | Latin 검증 | Claude (gap-detector) | 1 session |
| Session 5 | Do | `--scope module-3-hangul-a` | 디자이너 | 6-8주 |
| Session 6 | Check + Iterate | Phase A 시범 적용 | Claude + qa | 1-2 sessions |
| Session 7-12 | Do + Check | `--scope module-4-hangul-b` | 디자이너 + Claude | 12-16주 |
| Session 13 | Do + Report | `--scope module-5-launch` | Claude + 마케팅 | 1-2 sessions |

> **다음 세션**: `/pdca do incruit-sans --scope module-1-build`

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 0.1 | 2026-04-25 | Initial draft from Plan + PRD | Claude Code (PDCA Design Phase) |
