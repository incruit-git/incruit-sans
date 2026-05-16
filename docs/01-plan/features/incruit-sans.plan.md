# Incruit Sans Planning Document

> **Summary**: Pretendard 구조 + Min Sans 곡선 기반의 이력서 특화 한글 가변 폰트 v1.0 설계 및 출시 계획
>
> **Project**: Incruit Sans
> **Version**: 0.1.0 (Draft)
> **Author**: 이광석 (CHO) + Claude Code
> **Date**: 2026-04-25
> **Status**: Draft
> **PRD Reference**: [docs/00-pm/incruit-sans.prd.md](../../00-pm/incruit-sans.prd.md)

---

## Executive Summary

| Perspective | Content |
|-------------|---------|
| **Problem** | 한국어 이력서에 최적화된 무료 폰트 부재로, 구직자는 폰트 선택에 시간을 낭비하고 채용 담당자는 폰트 차이로 무의식 편향이 발생한다. |
| **Solution** | Pretendard의 정돈된 구조 + Min Sans의 부드러운 곡선을 결합한 Variable Font를 OFL 1.1로 제작. 인크루트 에디터에 자동 적용 후 디자인 커뮤니티 공개. |
| **Function/UX Effect** | 이력서 에디터 자동 적용 + Tabular Figures + 8 weights로 "선택 불필요 + 가독성 보장 + 환경 간 일관성" 결과물 즉시 제공. |
| **Core Value** | "인크루트 = 이력서 작성의 표준" 브랜드 강화 + 한국 디자인 커뮤니티 기여 + SEO/PR/리크루팅 간접 효과. |

---

## Context Anchor

> Auto-generated from PRD. Propagated to Design/Do documents for context continuity.

| Key | Value |
|-----|-------|
| **WHY** | 한국어 이력서에 최적화된 무료 폰트 부재 → 구직자 페인 + 인크루트 브랜드 차별화 기회 |
| **WHO** | (1) 인크루트 이력서 에디터 사용자 (Beachhead) → (2) 한국 디자이너/개발자 → (3) 일반 구직자 |
| **RISK** | 디자이너 의존성(글리프 정제), 라이선스 호환성(Pretendard/Min Sans 영향), Pretendard 대비 차별화 모호 |
| **SUCCESS** | M+12: 인크루트 자체 서비스 100% 적용, GitHub Star 500+, 외부 채용 플랫폼 1곳 채택, NPS Δ +5pt |
| **SCOPE** | Variable Font (wght 100–900), KS X 1001 한글 2,350자, Latin/숫자/기호, OTF/TTF/WOFF2, OFL 1.1 |

---

## 1. Overview

### 1.1 Purpose

이력서 작성·평가 컨텍스트에 특화된 무료 한글 가변 폰트를 자체 제작하여, **인크루트 이력서 생태계 전체의 시각 자산을 통일**하고 **한국 디자인 커뮤니티에 기여**한다.

### 1.2 Background

- **시장 공백**: Pretendard가 사실상 표준이지만 "기술/스타트업" 톤이 강해 이력서/HR 맥락에 한정적. Noto Sans KR은 가변 미지원, Spoqa Han Sans는 굵기 부족.
- **인크루트 자체 수요**: 이력서 에디터, 잘쓸랩(jslab.incruit.com), incruit.com 메인이 모두 외부 폰트(Pretendard/시스템 폰트) 의존.
- **브랜드 기회**: G마켓 산스/배민도현체처럼 "기업 OSS 폰트"가 PR/리크루팅 자산으로 검증됨. 의장(CHO) 직접 챔피언.
- **기술적 가능성**: Variable Font + WOFF2 + OFL 1.1 생태계가 성숙. fontmake/glyphsLib로 표준 빌드 가능.

### 1.3 Related Documents

- **PRD**: [docs/00-pm/incruit-sans.prd.md](../../00-pm/incruit-sans.prd.md)
- **Design Brief**: [docs/design-brief.md](../../design-brief.md) — 메트릭, 곡선, 호환성 사양
- **Glyph Specifications**: [docs/glyph-specifications.md](../../glyph-specifications.md) — 글리프별 설계 가이드
- **Weight Presets**: [docs/weight-presets.md](../../weight-presets.md) — 6단계 굵기 + CSS 변수
- **Claude Contributions**: [docs/claude-contributions.md](../../claude-contributions.md) — 자동화 가능 영역
- **External**: [Pretendard](https://github.com/orioncactus/pretendard), [fontmake](https://github.com/googlei18n/fontmake), [SIL OFL 1.1](https://scripts.sil.org/OFL)

---

## 2. Scope

### 2.1 In Scope (v1.0)

- [x] 빌드 파이프라인 (fontmake, GitHub Actions CI/CD)
- [x] 디자인 토큰 (CSS 변수 `--is-weight-*`, `--is-resume-*`)
- [x] 기초 문서 (CLAUDE.md, design-brief, glyph-specifications, weight-presets)
- [x] HTML 스펙시멘 (specimen.html, resume-test.html)
- [x] sources/IncruitSans-Regular.glyphs 템플릿 (104 글리프, Regular + Bold 마스터)
- [ ] **글리프 정제 — Latin (A–Z, a–z, 0–9, 기본 기호 ~100자)**
- [ ] **글리프 정제 — KS X 1001 한글 2,350자**
- [ ] **Variable Font 빌드 (wght 100–900 단일 파일)**
- [ ] **Tabular Figures (`tnum`) OpenType feature**
- [ ] **8개 인스턴스 빌드 (Thin/ExtraLight/Light/Regular/Medium/SemiBold/Bold/ExtraBold/Black)**
- [ ] **OTF / TTF / WOFF2 동시 빌드**
- [ ] **OFL 1.1 라이선스 검증 + 상표 검색**
- [ ] **인크루트 에디터 통합 가이드 (font-display: swap, 토큰 사용법)**
- [ ] **잘쓸랩(jslab.incruit.com) 시범 적용**
- [ ] **GitHub OSS 공개 (incruit/incruit-sans)**

### 2.2 Out of Scope (v1.0)

- Italic 스타일 (Latin Italic 유사 기울기는 향후 v1.5)
- 디스플레이 폰트(헤드라인 전용 변형) — Won't
- 손글씨/명조체 영역 — Won't
- 그리스/키릴/통화 기호 확장 — Could (v1.5)
- ATS 호환성 자동 테스트 자동화 — Should (수동 테스트로 시작)
- AI 이력서 도구 통합 (KakaoBrain/CLOVA) — v2.0
- Word/HWP 템플릿 패키지 — v2.0
- PDF 임베딩 가이드/매크로 — v2.0
- 직접 수익화 (구독, 유료 라이선스) — Won't (영구)

---

## 3. Requirements

### 3.1 Functional Requirements

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-01 | Variable Font (wght 100–900, step 1) 단일 파일 빌드 | High | Pending |
| FR-02 | 6개 굵기 프리셋 CSS 변수 (`--is-weight-body` 350 ~ `--is-weight-extrabold` 800) | High | Done |
| FR-03 | Tabular Figures 기본 활성 옵션 (`font-feature-settings: "tnum"`) | High | Pending |
| FR-04 | KS X 1001 한글 2,350자 지원 | High | Pending (104자만 템플릿) |
| FR-05 | Latin (A–Z, a–z), 숫자 (0–9), 기본 기호 (~100자) 지원 | High | Pending (템플릿만) |
| FR-06 | OTF / TTF / WOFF2 동시 빌드 (`build/build.py`) | High | Done (스크립트) |
| FR-07 | OFL 1.1 라이선스 적용 (LICENSE 파일 + 폰트 메타데이터) | High | Done (LICENSE), Pending (메타데이터) |
| FR-08 | 인크루트 에디터 통합 (CSS 변수, `font-display: swap`) | High | Pending |
| FR-09 | ATS 호환성 검증 (Workday, Greenhouse 등 5개 시스템 수동 테스트) | Medium | Pending |
| FR-10 | 작은 크기(8–10pt) 자동 hint 적용 (TTF autohint) | Medium | Pending |
| FR-11 | 그리스/키릴/통화 기호 확장 | Low | Won't (v1) |
| FR-12 | Italic 스타일 | Low | Won't (v1) |
| FR-13 | 8개 인스턴스 빌드 (Thin/ExtraLight/Light/Regular/Medium/SemiBold/Bold/ExtraBold/Black) | High | Pending |
| FR-14 | GitHub Actions CI/CD 자동 빌드 + 아티팩트 업로드 | Medium | Done (`.github/workflows/build-fonts.yml`) |

### 3.2 Non-Functional Requirements

| Category | Criteria | Measurement Method |
|----------|----------|-------------------|
| **Performance** | WOFF2 VF ≤ 1.2MB (한글 2,350자 기준), 정적 WOFF2 (unhinted) ≤ 850KB, 초기 로딩 ≤ 300ms (**측정 환경: Slow 4G throttle, Lighthouse Performance 모드, 사내망 제외 외부 측정**) | `ls -lh fonts/webfonts/`, Lighthouse CI (`--throttling-method=devtools --throttling.cpuSlowdownMultiplier=4`). **2026-04-25 베이스라인 측정 반영, 2026-04-26 측정 조건 명시화 (Analysis I2)** |
| **Compatibility** | Chrome/Safari/Edge 최신 2버전, iOS Safari, Android Chrome, Word 2019+, HWP 2020+ | BrowserStack + 실기기 수동 |
| **Accessibility** | WCAG 2.1 AA — 10pt 한글 대비비 4.5:1, 글자 크기 조절 가능 | Lighthouse, axe-core |
| **Legal** | OFL 1.1 호환성 (Pretendard 인용 시 LICENSE 동봉), "Incruit Sans" 상표 충돌 없음 | KIPRIS/USPTO 검색, 법무 검토 |
| **Maintenance** | semantic versioning (MAJOR.MINOR.PATCH), CHANGELOG.md 유지, GitHub Actions 빌드 | `git tag`, `CHANGELOG.md`, CI 통과율 |
| **File Size** | OTF ≤ 1.5MB, TTF ≤ 1.5MB (각 인스턴스), VF ≤ 4MB | `ls -lh fonts/{otf,ttf}/` |
| **Glyph Coverage** | 한글 2,350자 + Latin 95자 + 숫자 10자 + 기호 50자 = 약 2,505자 | `python -m fontTools.ttx fonts/ttf/*.ttf` glyf 카운트 |

---

## 4. Success Criteria

### 4.1 Definition of Done (v1.0 Release)

- [ ] **글리프 완성**: 한글 2,350자 + Latin/숫자/기호 모두 Regular + Bold 마스터에서 정제됨
- [ ] **빌드 성공**: `python build/build.py` 실행 → OTF (8개), TTF (8개), WOFF2 (8개), VF (1개) 생성
- [ ] **검증 통과**: `python build/validate_glyphs.py` → 전 마스터 100% 글리프 적용 확인
- [ ] **시각 검증**: `tests/specimen.html` + `tests/resume-test.html` 5개 브라우저에서 렌더링 정상
- [ ] **메트릭 검증**: 10pt 한글 자모 가독성 통과 (디자이너 + 사용자 5명 시각 평가)
- [ ] **잘쓸랩 시범**: jslab.incruit.com 100% 적용, 1주 무이슈
- [ ] **에디터 통합**: 인크루트 이력서 에디터에 폰트 적용 PR 머지
- [ ] **OSS 공개**: `incruit/incruit-sans` GitHub repo 공개, README + LICENSE + CHANGELOG 완비
- [ ] **법무 승인**: 라이선스 + 상표 검토 완료
- [ ] **문서 완료**: 사용 가이드, CSS 변수 가이드, Glyphs 설정 가이드

### 4.2 Quality Criteria

- [ ] WOFF2 VF 파일 ≤ 1.2MB (한글 2,350자 풀셋), v0.5(500자)에서 ≤ 400KB 목표 재측정
- [ ] 빌드 시간 ≤ 5분 (GitHub Actions 기준)
- [ ] specimen.html 콘솔 에러 0
- [ ] OFL 1.1 위반 0 (라이선스 헤더 모든 파일 포함)
- [ ] CI 통과율 100% (PR 머지 조건)

### 4.3 Outcome Metrics (M+12)

- [ ] 인크루트 이력서 에디터 적용률 100%
- [ ] GitHub Star 500+
- [ ] npm/CDN 다운로드 10K+/월
- [ ] 외부 채용 플랫폼 1곳 이상 채택
- [ ] 사용자 만족도 NPS Δ +5pt (적용 전/후 비교)

---

## 5. Risks and Mitigation

| ID | Risk | Impact | Likelihood | Mitigation |
|----|------|--------|------------|------------|
| **R1** | 디자이너 리소스 확보 실패 → 글리프 정제 6개월 이상 지연 | High | High | 외주 후보 3명 사전 선정 + Glyphs 파일 검토 견적 + 의장 직속 우선순위 부여. **Plan 단계 결정 필요**. |
| **R2** | "Pretendard 대비 차별화 부족" 평가 → 디자인 커뮤니티 채택 부진 | High | Medium | 사전 5+5 blind test 검증 + "이력서 특화" 카테고리 포지셔닝 (직접 비교 회피) + 호환 메트릭으로 마이그레이션 비용 0 강조 |
| **R3** | 라이선스/이름 충돌 (기존 "Incruit Sans" 폰트 존재 또는 OFL 위반 의혹) | High | Low-Medium | KIPRIS/USPTO 상표 검색 + Pretendard 메인테이너(orioncactus)에 사전 인사 + 법무 검토. **M0 즉시 진행**. |
| **R4** | Variable Font interpolation 품질 저하 (Regular ↔ Bold 사이 중간 굵기가 어색) | Medium | Medium | Glyphs 3에서 Medium/SemiBold 인스턴스 시각 검증, 필요 시 master 추가 |
| **R5** | KS X 1001 한글 2,350자 정제 시간이 예상(3개월) 초과 | Medium | Medium | 우선순위 단계화: Phase A(고빈도 500자) → Phase B(2,350자), Phase A 완료 후 v0.5 배포 |
| **R6** | 인크루트 이력서 에디터 통합 시 기존 CSS 충돌 (Pretendard 의존 코드) | Medium | High | `--is-*` 토큰 기반으로만 적용 + 점진 적용 (베타 사용자 → 100%) |
| **R7** | ATS 시스템(Workday 등)에서 폰트 미인식 → 텍스트 깨짐 | High | Low | PDF 임베딩 강제 + ATS 5개 수동 테스트 + 폴백 폰트 체인 (`Pretendard, sans-serif`) |
| **R8** | macOS Glyphs 3 라이선스 부재로 디자이너 협업 차단 | Medium | Low | Glyphs 3 라이선스 1카피 사내 확보 또는 외주 디자이너 자체 라이선스 활용 |

---

## 6. Impact Analysis

> **Purpose**: Incruit Sans 도입이 인크루트 기존 서비스에 미치는 영향을 사전 인벤토리.

### 6.1 Changed Resources

| Resource | Type | Change Description |
|----------|------|--------------------|
| 인크루트 이력서 에디터 CSS | Frontend (Web) | `font-family` Pretendard → Incruit Sans, `--is-*` 토큰 추가 |
| 인크루트 이력서 PDF 생성기 | Backend (Server) | 폰트 임베딩 변경, Tabular Figures 활성 |
| 잘쓸랩 (jslab.incruit.com) | Frontend (Web) | 시범 적용 — 본문 폰트 변경 |
| incruit.com 메인 | Frontend (Web) | 향후 적용 (v1.0 이후) |
| Word/HWP 사용자 환경 | Client (Desktop) | OTF 다운로드/설치 안내 추가 |
| GitHub `incruit/incruit-sans` | Public Repo | 신규 공개 OSS |

### 6.2 Current Consumers

| Resource | Operation | Code Path | Impact |
|----------|-----------|-----------|--------|
| 이력서 에디터 폰트 | READ (CSS) | incruit-resume-editor → `body { font-family: Pretendard }` | **Breaking** — 폰트 변경. 토큰 도입 + 점진 적용 필요 |
| 이력서 PDF | EMBED | resume-pdf-generator → font embedding | **Needs verification** — 임베딩 폰트 추가, Acrobat 호환성 확인 |
| 잘쓸랩 본문 | READ (CSS) | jslab.incruit.com → font-family 적용 | **Needs verification** — 시범 적용 후 1주 모니터링 |
| Pretendard 직접 참조 코드 | Various | `@import "pretendard"`, CDN URL 등 | **Needs verification** — 의존성 inventory 필요 |
| ATS 외부 시스템 | UPLOAD | 사용자가 PDF를 외부 ATS에 업로드 | **Needs verification** — 5개 시스템 수동 테스트 |

### 6.3 Verification

- [ ] 인크루트 이력서 에디터에서 Pretendard 직접 참조 코드 grep
- [ ] PDF 생성기 폰트 임베딩 테스트 (Adobe Acrobat 5개 PDF 검증)
- [ ] 잘쓸랩 시범 1주 모니터링 (Sentry/사용자 피드백)
- [ ] ATS 5개 시스템 수동 업로드 테스트 (Workday, Greenhouse, Lever, Taleo, SAP SuccessFactors)
- [ ] Word 2019/HWP 2020 실기기 수동 테스트
- [ ] iOS Safari / Android Chrome 모바일 테스트

---

## 7. Architecture Considerations

### 7.1 Project Type

이 프로젝트는 **폰트 패키지 프로젝트**로, 일반적인 웹 애플리케이션 Level 분류(Starter/Dynamic/Enterprise)에 직접 매핑되지 않는다. 폰트 프로젝트 특화 분류:

| Type | Characteristics | Selected |
|------|-----------------|:--------:|
| **Font Asset (Static)** | 빌드 산출물(OTF/TTF/WOFF2) 배포, 최소 인프라 | ☑ |
| **Font Service (Dynamic)** | 자체 CDN, 동적 서브셋 API | ☐ (v2.0 가능) |
| **Font Platform (Enterprise)** | 폰트 SaaS, 커스터마이징 | ☐ |

### 7.2 Key Architectural Decisions

| Decision | Options | Selected | Rationale |
|----------|---------|----------|-----------|
| **Source Format** | UFO / Glyphs / FontLab | **Glyphs 3 (.glyphs JSON)** | Pretendard/Min Sans 표준, JSON 기반 자동화 용이 |
| **Build Tool** | fontmake / FontLab Studio / 자체 | **fontmake (CLI)** | OSS 표준, GitHub Actions 통합 용이 |
| **Variable Font Axis** | wght / wght+wdth / wght+ital | **wght 단일 (100–900)** | 이력서 컨텍스트는 굵기만 충분, 빌드 단순 |
| **Master Count** | Regular only / Regular+Bold / 다중 | **Regular + Bold (2 마스터)** | 8 인스턴스 interpolation 충분, 디자인 부담 ↓ |
| **OpenType Features** | 최소 / 기본 / 풍부 | **`tnum`, `kern`, `liga` (기본)** | 이력서 핵심: tnum, 그 외 표준 |
| **License** | OFL 1.1 / MIT / Custom | **OFL 1.1** | Pretendard 호환, 폰트 표준 |
| **Distribution** | GitHub Release / npm / CDN | **All 3** | GitHub (소스), npm (개발자), CDN (직접 사용) |
| **CI/CD** | GitHub Actions / CircleCI / 없음 | **GitHub Actions** | OSS 표준, 무료 + 아티팩트 업로드 |
| **Hinting** | autohint / manual / 없음 | **TTF autohint (`ttfautohint`)** | 자동화, 작은 크기 가독성 ↑ |
| **Subsetting** | 전체 / KS X 1001 / 동적 | **KS X 1001 + 확장 분리** | v1.0은 단일 파일, v2.0에서 동적 서브셋 검토 |

### 7.3 Folder Structure

```
incruit-sans/
├── CLAUDE.md
├── README.md
├── LICENSE                          # OFL 1.1
├── CHANGELOG.md                     # ⚠️ 신규 생성 필요
├── package.json                     # ⚠️ npm 배포용 (v0.6+)
│
├── sources/                         # 글리프 소스 (Glyphs 3)
│   ├── IncruitSans-Regular.glyphs   # ✅ 생성됨 (104자, Regular+Bold)
│   └── IncruitSans-Regular.glyphs.backup
│
├── tokens/                          # 디자인 토큰
│   └── weight.css                   # ✅ 생성됨
│
├── docs/                            # 설계 문서
│   ├── 00-pm/                       # PM 분석
│   │   └── incruit-sans.prd.md      # ✅ 생성됨
│   ├── 01-plan/features/            # Plan 문서
│   │   └── incruit-sans.plan.md     # ⚠️ 이 문서
│   ├── 02-design/features/          # Design 문서 (다음 단계)
│   ├── design-brief.md              # ✅ 생성됨
│   ├── glyph-specifications.md      # ✅ 생성됨
│   ├── weight-presets.md            # ✅ 생성됨
│   └── claude-contributions.md      # ✅ 생성됨
│
├── build/                           # 빌드 스크립트
│   ├── build.py                     # ✅ 생성됨
│   ├── setup_bold_master.py         # ✅ 생성됨
│   ├── validate_glyphs.py           # ✅ 생성됨
│   ├── requirements.txt             # ✅ 생성됨
│   └── (참고용 폰트 파일들 — 빌드 산출물이 아님, gitignore 검토)
│
├── fonts/                           # 빌드 산출물 (gitignore)
│   ├── otf/
│   ├── ttf/
│   └── webfonts/
│
├── tests/                           # 검증 페이지
│   ├── specimen.html                # ✅ 생성됨
│   └── resume-test.html             # ✅ 생성됨
│
└── .github/workflows/
    └── build-fonts.yml              # ✅ 생성됨
```

---

## 8. Convention Prerequisites

### 8.1 Existing Project Conventions

- [x] `CLAUDE.md` 폰트 프로젝트 컨벤션 명시 (한국어 주석, 커밋 메시지)
- [x] 빌드 명령어 정의 (`python3 build/build.py`)
- [x] OFL 1.1 라이선스 채택
- [ ] `CHANGELOG.md` 미존재 — **생성 필요**
- [ ] `package.json` 미존재 — **npm 배포 시 생성 필요 (v0.6+)**
- [ ] `.gitignore` 검토 — `fonts/`, `venv/`, `build/*.otf` 등

### 8.2 Conventions to Define

| Category | Current | To Define | Priority |
|----------|---------|-----------|:--------:|
| **글리프 명명** | 미정 | `uniXXXX` (한글), AGLFN (Latin), Pretendard 컨벤션 따름 | High |
| **버전 관리** | 미정 | semver: `MAJOR.MINOR.PATCH`, `0.x` (unstable) → `1.0.0` (안정) | High |
| **Git 브랜치** | 미정 | `main` (배포), `develop` (개발), `feature/*` (글리프 단위) | Medium |
| **커밋 메시지** | CLAUDE.md 정의 | "한국어 + 동사 시작" — 예: "한글 음절 ㄱ 행 정제" | Medium |
| **파일 명명** | 미정 | `IncruitSans-{Style}.{ext}` — Pretendard 컨벤션 | High |
| **OpenType feature 우선순위** | 미정 | `tnum` 기본 활성, `kern/liga` 활성, `ss01` 등 stylistic set은 v2.0 | Medium |

### 8.3 Required Tools & Versions

| Tool | Version | Purpose |
|------|---------|---------|
| Python | ≥ 3.11 | 빌드 스크립트 |
| fontmake | latest | 빌드 (Glyphs → OTF/TTF) |
| fontTools | latest | WOFF2 변환, ttx 검증 |
| Glyphs 3 | 3.x | 글리프 정제 (디자이너 도구) |
| ttfautohint | latest | TTF hinting |
| Node.js | ≥ 20 | (npm 배포 시) |

### 8.4 Pipeline Phases (폰트 프로젝트 특화)

| Phase | Description | Owner | Status |
|-------|-------------|-------|:------:|
| **P1: Source Setup** | sources/IncruitSans-Regular.glyphs 템플릿 + Bold 마스터 | Claude | ✅ |
| **P2: Glyph Refinement** | Latin/숫자/기호 정제 → 한글 2,350자 정제 | 디자이너 | ⏳ |
| **P3: Build** | fontmake로 OTF/TTF/WOFF2/VF 생성 | Claude (자동) | 🟡 (테스트만) |
| **P4: Validation** | validate_glyphs.py + specimen.html 시각 검증 | Claude + 디자이너 | ⏳ |
| **P5: Integration** | 잘쓸랩 → 이력서 에디터 → incruit.com | 인크루트 FE팀 | ⏳ |
| **P6: Public Release** | OFL 공개, GitHub repo, npm 배포, CDN | 마케팅 + Claude | ⏳ |

---

## 9. Open Questions (Plan 진행 전 결정 필요)

> PRD에서 식별된 5개 Open Questions. **이 중 #2, #3은 즉시 결정 필요** (M0 마일스톤 차단).

| # | Question | Owner | Deadline | Status |
|---|----------|-------|----------|:------:|
| 1 | 인크루트 이력서 에디터 정확한 MAU? | 데이터팀 | M+1 (Beachhead 크기 검증) | ⏳ |
| 2 | **디자이너 외주 vs 인하우스 결정?** | 의장 + 인사팀 | **M+0 즉시** (예산/일정 결정) | 🚨 |
| 3 | **"Incruit Sans" 상표 충돌 검색 결과?** | 법무 | **M+0 즉시** (이름 변경 리스크) | 🚨 |
| 4 | Pretendard 메인테이너(orioncactus)와 사전 협의? | 의장 | M+1 (관계 리스크) | ⏳ |
| 5 | AI 이력서 도구 통합 우선순위? (KakaoBrain/CLOVA/자체) | 잘쓸랩 PM | v2.0 결정 | 📅 |

---

## 10. Next Steps

1. [ ] **즉시**: Open Question #2 (디자이너), #3 (상표) 결정 → 의장 회의
2. [ ] Design 문서 작성 (`/pdca design incruit-sans`) — 글리프 정제 우선순위, 빌드 파이프라인 상세, 통합 아키텍처
3. [ ] CHANGELOG.md, package.json (v0.6 시점) 생성
4. [ ] `.gitignore` 정비 (fonts/, venv/, build/*.otf 빌드 참고용 파일)
5. [ ] 디자이너 계약 후 글리프 정제 Phase A (고빈도 500자) 시작
6. [ ] Design 단계에서 3가지 아키텍처 옵션 평가 (Master 2개 vs 3개, Subset 전략 등)

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 0.1 | 2026-04-25 | Initial draft from PRD | Claude Code (PDCA Plan Phase) |
