# Incruit Sans — Product Requirements Document (PRD)

**작성일**: 2026-04-25
**버전**: 1.0 (PM Agent Team 분석 결과)
**작성**: PM Agent Team (Discovery / Strategy / Research / PRD)
**스폰서**: 이광석 (인크루트 의장, CHO)
**프로덕트 코드명**: Incruit Sans

---

## Executive Summary

| 관점 | 내용 |
|------|------|
| **Problem** | 구직자가 이력서를 작성할 때 폰트 선택과 가독성에 시간을 낭비하고, 채용 담당자는 폰트 차이로 인해 동일한 후보자를 다르게 평가한다. 한국어 이력서에 최적화된 무료 폰트가 사실상 없다. |
| **Solution** | Pretendard의 정돈된 구조 + Min Sans의 부드러운 곡선을 결합한 이력서 특화 한글 폰트 (Variable Font, OFL 1.1). 인크루트 자체 에디터에 기본 적용 후 디자인 커뮤니티에 공개. |
| **Function/UX Effect** | 인크루트 이력서 에디터가 "폰트 선택 불필요 + 가독성 보장 + Tabular Figures로 숫자 정렬 완벽"한 결과물을 즉시 제공. Word/HWP/PDF 어디로 export해도 동일한 톤 유지. |
| **Core Value** | "인크루트 = 이력서 작성의 표준" 브랜드 강화. Pretendard 같은 OSS 자산이 되어 한국 디자인 커뮤니티에 기여하면서 SEO/PR/리크루팅 효과 동반. |

---

## Context Anchor

| 항목 | 내용 |
|------|------|
| **WHY** | 한국어 이력서에 최적화된 무료 폰트 부재 → 구직자 페인 + 인크루트 브랜드 차별화 기회 |
| **WHO** | (1) 인크루트 이력서 에디터 사용자 (Beachhead) → (2) 한국 디자이너/개발자 → (3) 일반 구직자 |
| **RISK** | 디자이너 의존성(글리프 정제), 라이선스 호환성(Pretendard/Min Sans 영향), 채택 부진(Pretendard 대비 차별화 약함) |
| **SUCCESS** | M+12: 인크루트 자체 서비스 100% 적용, GitHub Star 500+, 외부 채용 플랫폼 1곳 이상 채택 |
| **SCOPE** | Variable Font (wght 100–900), KS X 1001 한글 2,350자, Latin/숫자/기호, OTF/TTF/WOFF2, OFL 1.1 |

---

## 1. Discovery Analysis (pm-discovery)

### 1.1 5-Step Discovery Chain

#### Step 1: Brainstorm — 이력서 폰트 영역의 페인포인트

| ID | 페인포인트 | 발생 빈도 |
|----|-----------|----------|
| P1 | "어떤 폰트를 써야 프로페셔널해 보일까?" 결정 마비 | 매우 높음 |
| P2 | 한글-영문-숫자 혼용 시 베이스라인 어긋남 | 높음 |
| P3 | 연봉/날짜/KPI 숫자가 정렬되지 않음 (proportional figures) | 매우 높음 |
| P4 | 다운로드 PDF가 환경마다 다르게 보임 | 중간 |
| P5 | Word/HWP의 기본 폰트(맑은 고딕, 함초롬바탕)는 채용 맥락에 어색 | 높음 |
| P6 | 무료 폰트는 굵기 단계가 부족 (정보 계층 표현 한계) | 높음 |
| P7 | Pretendard는 좋지만 "기술/스타트업" 톤이 강함 | 중간 |
| P8 | 채용 담당자가 폰트 차이로 후보자를 무의식적으로 다르게 평가 | 높음 |
| P9 | ATS(Applicant Tracking System) 폰트 호환성 불안 | 중간 |
| P10 | 작은 크기(10–11pt)에서 한글 자모가 뭉개짐 | 높음 |

#### Step 2: Assumptions — 검증 필요 가정

| ID | 가정 | Impact (1-5) | Risk (1-5) | Score |
|----|------|:------------:|:----------:|:-----:|
| A1 | 사용자는 이력서 폰트 선택에 실제로 스트레스를 받는다 | 5 | 4 | 20 |
| A2 | "인크루트 자체 폰트"라는 사실이 채용 담당자에게 신뢰감을 준다 | 4 | 5 | 20 |
| A3 | Pretendard 대비 "부드러운 곡선"이 의미 있는 차별점이다 | 5 | 5 | 25 |
| A4 | OFL 공개 시 디자인 커뮤니티에서 Pretendard 수준 채택을 얻을 수 있다 | 5 | 5 | 25 |
| A5 | 이력서 에디터의 폰트 변경만으로 사용자 만족도가 측정 가능하게 오른다 | 4 | 4 | 16 |
| A6 | 디자이너가 글리프 정제 작업을 합리적 기간(3–6개월) 내 완료한다 | 5 | 4 | 20 |
| A7 | 잡코리아/사람인이 따라 만들기보다는 그냥 Pretendard를 쓴다 | 3 | 3 | 9 |

#### Step 3: Prioritize — 가장 위험하고 영향 큰 가정

**Top 3 가정 (즉시 검증 필요)**:
- **A3** (차별화 정당성): "부드러운 곡선"이 정말 차별점이 되는지 — A/B 테스트로 검증
- **A4** (커뮤니티 채택): OFL 공개 후 6개월 내 GitHub Star 200+ 도달 여부로 검증
- **A6** (실행 가능성): 디자이너 리소스 확보 (현 시점 외주 vs 인하우스 결정 미정)

#### Step 4: Experiments — 실험 설계

| 가정 | 실험 | 성공 기준 | 일정 |
|------|------|----------|------|
| A3 | 5명 채용 담당자 + 5명 구직자에게 동일 이력서 (Pretendard vs Incruit Sans Draft) blind test | 7/10 이상이 Incruit Sans를 "더 따뜻함/친근함" 응답 | 2026-Q3 |
| A1 | 인크루트 이력서 에디터 사용자 200명 설문: "폰트 선택에 시간을 쓴 적이 있는가" | 60%+ Yes | 2026-Q2 |
| A4 | Pre-launch: incruit-sans GitHub repo 공개 + 디자인 커뮤니티(폰트, 디스콰이엇) 사전 공지 | Pre-launch waitlist 100명 | 2026-Q3 |
| A6 | 디자이너 후보 3명과 NDA 후 Glyphs 파일 검토 + 일정 견적 | 3개월 내 104글리프 → 2,350자 확장 가능 견적 확보 | 2026-Q2 |

#### Step 5: Opportunity Solution Tree (OST)

```
[Outcome] 인크루트 = 이력서 작성의 표준
│
├── [Opportunity 1] 구직자가 폰트 결정에 시간을 낭비함 (P1, P10)
│   ├── Solution 1.1: 에디터 기본 폰트 = Incruit Sans (선택 불필요)
│   ├── Solution 1.2: "Resume-Ready" 굵기 프리셋 (--is-weight-body 350 등)
│   └── Solution 1.3: 작은 크기(10pt) 자동 hint 적용 → 깨짐 방지
│
├── [Opportunity 2] 채용 담당자가 정보를 빠르게 스캔하지 못함 (P3, P8)
│   ├── Solution 2.1: Tabular Figures (연봉/날짜 자동 정렬)
│   ├── Solution 2.2: SemiBold/Bold 명확한 위계 (이름 ≠ 회사명 ≠ 본문)
│   └── Solution 2.3: ATS 호환성 보증 마크 ("ATS-Friendly" 배지)
│
├── [Opportunity 3] 인크루트 브랜드가 Pretendard에 의존 (P7)
│   ├── Solution 3.1: 자체 폰트로 incruit.com 메인 적용
│   ├── Solution 3.2: 디자인 시스템 토큰화 (--is-weight-* CSS 변수)
│   └── Solution 3.3: 커뮤니티 공개로 "주는 회사" 포지셔닝
│
└── [Opportunity 4] 환경 간 일관성 부족 (P2, P4, P5)
    ├── Solution 4.1: Variable Font (모든 굵기 단일 파일)
    ├── Solution 4.2: WOFF2/OTF/TTF 동시 빌드 → 웹/Word/HWP 모두 커버
    └── Solution 4.3: PDF embed 가이드 + Word 매크로 템플릿 제공
```

**Top Priority**: Opportunity 1 + 2 → 인크루트 에디터 즉시 적용 가능, 측정 가능한 사용자 가치.

---

## 2. Strategy (pm-strategy)

### 2.1 JTBD 6-Part Value Proposition

| Part | 내용 |
|------|------|
| **For** | 한국에서 이력서/자기소개서를 작성하는 구직자와, 그 이력서를 평가하는 채용 담당자 |
| **Who** | 폰트 선택에 시간을 쓰지 않으면서도 프로페셔널하고 가독성 높은 결과물을 원하는 사람 |
| **The Incruit Sans is** | 이력서 특화로 설계된 무료 한글 가변 폰트 |
| **That** | Pretendard 수준의 가독성 + 따뜻한 곡선 + Tabular Figures + 8단계 굵기를 한 패키지로 제공한다 |
| **Unlike** | Pretendard(범용), Noto Sans KR(서버 한정), Spoqa Han Sans(굵기 부족), 시스템 폰트(맑은 고딕/함초롬바탕) |
| **Our product** | 이력서 특화 메트릭(10–18pt 최적화) + ATS 호환 + OFL 무료 + 인크루트 에디터 통합으로 검증된 실전 폰트 |

### 2.2 Lean Canvas

| Block | Content |
|-------|---------|
| **1. Problem** | (a) 한국어 이력서에 최적화된 무료 폰트 부재 (b) 환경 간 폰트 호환성 깨짐 (c) Pretendard는 "기술" 톤 강함 |
| **2. Customer Segments** | (Beachhead) 인크루트 이력서 에디터 월간 활성 사용자 / (Early Adopter) 한국 디자이너·개발자 / (Mass) 일반 구직자, 채용 담당자 |
| **3. Unique Value Proposition** | "이력서를 위해 처음부터 설계된 한글 폰트 — 무료, 가변, 인크루트 검증" |
| **4. Solution** | Variable Font (wght 100–900), 6 weight presets, Tabular Figures, OTF/TTF/WOFF2, OFL 1.1 |
| **5. Channels** | (1) 인크루트 에디터 자체 적용 (2) GitHub OSS 공개 (3) 디자인 커뮤니티 (디스콰이엇, 폰트, Brunch) (4) 인크루트 블로그/SEO |
| **6. Revenue Streams** | 직접 수익 없음. 간접: (a) 인크루트 이력서 에디터 차별화 → 유료 전환 (b) 브랜드 가치 → 영업/리크루팅 (c) SEO 트래픽 |
| **7. Cost Structure** | 디자이너 외주 또는 인하우스 (3–6개월), 빌드/CI/CD 운영, GitHub 호스팅, 타입 호스팅(jslab.incruit.com) |
| **8. Key Metrics** | (a) 에디터 적용률 100% (b) GitHub Star 6개월 내 500+ (c) 외부 채용 플랫폼 채택 1곳+ (d) 사용자 만족도 NPS +10pt |
| **9. Unfair Advantage** | 한국 No.1 채용 플랫폼의 실데이터로 검증된 폰트 + 의장 직접 챔피언 + Pretendard 호환 메트릭 |

### 2.3 SWOT Analysis

| | Helpful | Harmful |
|---|---|---|
| **Internal** | **Strengths**: 의장 스폰서십, 인크루트 자체 채널, Pretendard/Min Sans 영감 명확, OFL 라이선스 | **Weaknesses**: 폰트 디자인 인하우스 역량 부족, 글리프 정제 시간 소요, 차별화 포인트 모호("부드러움"의 정량화 어려움) |
| **External** | **Opportunities**: Pretendard 외 한국 OSS 폰트 부재, AI 이력서 시대에 브랜드 자산 중요성 ↑, OFL 공개 시 PR 효과 | **Threats**: Pretendard가 사실상 표준화 진행 중, 잡코리아/사람인의 빠른 모방, 디자이너 리소스 시장 부족 |

**SO 전략**: 의장 스폰서십 + 자체 채널을 활용해 Pretendard 부재 영역(이력서 특화)에 빠르게 깃발 꽂기.
**WT 전략**: 디자이너 역량은 외주 + 단계적 확장(104글리프 → 2,350자)으로 리스크 분산. Pretendard 호환 메트릭으로 마이그레이션 비용 ↓.

### 2.4 Strategic Positioning

```
                       프로페셔널 (정돈)
                              ↑
              Noto Sans KR    │    Pretendard
                              │
         감정적 ←─────────────┼─────────────→ 기술적
                              │       ★ Incruit Sans
              Spoqa Han Sans  │       (이력서 특화)
                              │
                    캐주얼 (자유)
```

Pretendard와 가장 가까운 셀에 자리잡되, "이력서/HR" 컨텍스트로 컨텍스트 차별화.

---

## 3. Market Research (pm-research)

### 3.1 Personas (3종)

#### Persona 1: 신입 구직자 "김취준" (Beachhead의 핵심)
- **인구통계**: 25세, 4년제 졸업 예정, 서울 거주, 인크루트/잡코리아/원티드 동시 사용
- **JTBD**: "내 이력서가 다른 지원자들과 비교해 프로페셔널하게 보이게 하고 싶다"
- **현재 행동**: Word 기본 폰트 → 맑은 고딕으로 작성 → PDF 변환 시 줄바꿈 깨짐 발견 → 검색 → 시간 낭비
- **페인**: 폰트 선택 마비, 한/영 혼용 어색함, 작은 크기에서 흐릿함
- **이득**: 인크루트 에디터에서 자동 적용된 폰트로 "고민 없이 잘 보이는" 이력서
- **채택 트리거**: 인크루트 에디터 사용 시 자연 노출

#### Persona 2: 채용 담당자 "박인사" (HR Manager)
- **인구통계**: 35세, 중견기업 인사팀 5년차, 하루 50–100건 이력서 검토
- **JTBD**: "최소 시간에 후보자의 핵심 정보를 정확히 스캔하고 싶다"
- **현재 행동**: PDF 받기 → 폰트가 깨지면 인쇄 → 정보 위계 파악 어려움 → 시간 낭비
- **페인**: 폰트 차이로 동일 후보를 다르게 평가하는 무의식 편향, 숫자 정렬 안 됨
- **이득**: Tabular Figures로 연봉/기간 한눈에 정렬, 일관된 위계로 빠른 스캔
- **채택 트리거**: 인크루트로 받은 이력서가 "읽기 좋다"는 경험 누적

#### Persona 3: 디자인 커뮤니티 "이디자" (UX Designer / Frontend Dev)
- **인구통계**: 30세, 스타트업/에이전시, Pretendard 사용자, 디스콰이엇 활동
- **JTBD**: "포트폴리오/제품에 쓸 수 있는 차별화된 한글 폰트를 찾고 싶다"
- **현재 행동**: Pretendard 사용 → 비슷한 톤이 너무 많음 → 새 폰트 탐색
- **페인**: Pretendard 외 선택지 부족, 따뜻한 톤의 OFL 폰트 부재
- **이득**: 이력서/HR뿐만 아니라 일반 UI에도 사용 가능한 OFL 가변 폰트
- **채택 트리거**: GitHub Trending, 디자인 뉴스레터 노출

### 3.2 Competitive Analysis (5종)

| 경쟁자 | 강점 | 약점 | Incruit Sans 대비 |
|--------|------|------|-------------------|
| **Pretendard** | 사실상 표준, 9 weights, OFL, 다국어 우수 | 범용 톤, 이력서 특화 X, "기술" 이미지 | **이력서 컨텍스트 + 부드러움**으로 차별 |
| **Noto Sans KR** | Google 보증, 가장 광범위한 글리프 | 무거움(파일 크기), 굵기 제한, 가변 미지원 | **Variable + 가벼운 WOFF2** |
| **Spoqa Han Sans Neo** | 한국 기업 폰트, 무료, Spoqa 브랜드 | 굵기 4종 불과, 업데이트 정체 | **8 weights + Tabular Figures** |
| **본명조/나눔명조** | 정통 명조체, 익숙함 | 본문용 sans-serif 영역 미커버, 화면 가독성 ↓ | **화면 최적화 sans-serif** |
| **G마켓 산스 / 배민도현체** | 브랜드 폰트 OSS 사례, 인지도 | 디스플레이용, 본문 부적합 | **본문/이력서 본격 지원** |

**경쟁 포지션**: Pretendard와 직접 경쟁하기보다 "이력서/HR" 카테고리에서 No.1 선점.

### 3.3 Market Sizing (TAM / SAM / SOM)

#### Method A: Top-Down
- **TAM**: 한국 경제활동인구 ~28M × 연 1회 이력서 작성 가정 = 28M 잠재 사용자/년
- **SAM**: 온라인 채용 플랫폼 활성 사용자 ~10M (인크루트/잡코리아/사람인 합산) × 폰트 선택권이 있는 경우 70% = **7M**
- **SOM (3년)**: 인크루트 MAU 점유 + 외부 채택 = SAM의 15% = **1.05M**

#### Method B: Bottom-Up
- 인크루트 이력서 에디터 MAU (가정): ~500K
- × 자동 노출 100% = **500K** (Beachhead)
- + 외부 채용 플랫폼 1곳 채택 시 추가 200K
- + GitHub OSS 다운로드/CDN 50K/월
- = 3년 누적 **~1M reach**

**검증 포인트**: 인크루트 이력서 에디터 정확한 MAU 데이터 필요 → 데이터팀 확인 필요.

### 3.4 Customer Journey Map (Persona 1: 김취준)

| Phase | Awareness | Consideration | Use | Share |
|-------|-----------|--------------|-----|-------|
| **Action** | 인크루트 가입, 이력서 에디터 진입 | 자동 적용된 Incruit Sans 인지 | 작성 → PDF 다운로드 | 친구에게 인크루트 추천 |
| **Thought** | "이력서 어떻게 쓰지" | "어? 폰트가 좀 다르네, 보기 좋다" | "PDF가 깨끗하게 나옴" | "이건 인크루트 폰트래" |
| **Pain** | 폰트 선택 막막 | (없음 — 자동 적용) | 환경 간 차이 (Word 열 때) | (없음) |
| **Opportunity** | 첫 진입 시 "인크루트 이력서 폰트로 자동 적용" 안내 | "왜 이 폰트가 좋은지" 짧은 설명 카드 | Word/HWP 다운로드 동선에서 "Incruit Sans 시스템 설치" 유도 | "이 폰트로 만든 이력서" 공유 템플릿 |

---

## 4. Beachhead Segment & Go-To-Market (pm-prd)

### 4.1 ICP (Ideal Customer Profile)

**1차 ICP**: 인크루트 이력서 에디터 월간 활성 사용자 중, 신입~3년차 구직자
- 이유: 가장 적극적으로 이력서를 작성/수정 (높은 노출 빈도)
- 의사결정자 = 사용자 본인 (B2C)
- 채택 비용 = 0 (자동 적용)

**2차 ICP**: 한국 디자인 커뮤니티 (디스콰이엇 활동 디자이너/개발자)
- 이유: 폰트 채택 결정권자 + 입소문 영향력
- 채택 비용 = OFL 라이선스 무료 + 1줄 CSS

### 4.2 Beachhead Selection (4-Criteria Scoring)

| Criteria | 인크루트 에디터 사용자 | 외부 채용 플랫폼 | 디자인 커뮤니티 | 일반 기업 브랜드 |
|----------|:--------------------:|:--------------:|:-------------:|:--------------:|
| **Reachable** (자체 채널) | 5 | 2 | 4 | 2 |
| **Compelling Reason** (해결 가치) | 5 | 3 | 3 | 2 |
| **Whole Product** (즉시 사용 가능) | 5 | 4 | 5 | 4 |
| **Strategic Importance** (확장성) | 5 | 4 | 4 | 3 |
| **Total** | **20** | 13 | 16 | 11 |

**Beachhead 결정**: 인크루트 이력서 에디터 사용자 → 입증 후 디자인 커뮤니티 → 외부 플랫폼 확장.

### 4.3 GTM Strategy (3-Phase)

#### Phase 1 — Internal Validation (M0–M6)
- 인크루트 잘쓸랩(jslab.incruit.com) 시범 적용
- 인크루트 이력서 에디터 100% 적용 (사내 dogfooding 포함)
- 사용자 만족도 측정 (NPS, 폰트 변경 유도 클릭률)
- **Metric**: 에디터 적용률 100%, NPS Δ +5pt

#### Phase 2 — Open Source Launch (M6–M12)
- GitHub `incruit/incruit-sans` 공개 (OFL 1.1)
- 디자인 커뮤니티 사전 공지 (디스콰이엇, 폰트, Brunch, Velog)
- ProductHunt / GeekNews 런칭
- 인크루트 블로그 시리즈 ("폰트 만든 이야기")
- **Metric**: GitHub Star 500+, npm/CDN 다운로드 10K+/월

#### Phase 3 — Ecosystem Expansion (M12–M24)
- 외부 채용 플랫폼 1곳 이상 채택 유도 (PR + 직접 영업)
- 워드/HWP 템플릿 패키지 배포
- AI 이력서 생성 도구와 통합 (KakaoBrain, Naver CLOVA 등)
- **Metric**: 외부 플랫폼 1+, 누적 reach 1M+

### 4.4 Battlecards (vs Pretendard)

| Q&A | 답변 |
|-----|------|
| "왜 Pretendard 안 쓰고?" | Pretendard는 범용. Incruit Sans는 이력서 특화 메트릭 + Tabular Figures 기본 활성 + 따뜻한 곡선. Pretendard와 호환 메트릭이라 마이그레이션 0 비용. |
| "Pretendard 만든 사람도 있는데?" | 우리는 "이력서 컨텍스트"에 집중. Pretendard 위에 서지, 대체하지 않음. (Pretendard도 Inter 위에 섰던 것처럼) |
| "왜 무료로 풀어?" | 인크루트 = 이력서 표준 브랜딩 + 디자인 커뮤니티 기여 + SEO/PR 효과. 직접 수익보다 간접 가치. |

### 4.5 Growth Loops

```
[제품 사용] → [PDF 다운로드 시 미세 워터마크 "Made with Incruit Sans"]
     ↓                                              ↓
[채용 담당자 노출] → [폰트 인지] → [GitHub 검색] → [디자이너 채택]
     ↓                                              ↓
[다른 이력서/UI에 적용] → [SNS 공유] → [신규 사용자 유입]
```

---

## 5. Product Requirements (8-Section PRD)

### 5.1 Goals & Non-Goals

**Goals**:
1. 인크루트 이력서 에디터에 100% 적용 (M+6)
2. OFL 1.1로 GitHub 공개 (M+6)
3. 8단계 굵기 + Tabular Figures + 2,350자 한글 지원 (M+9)
4. 외부 채용 플랫폼 1곳 채택 (M+18)

**Non-Goals**:
- 디스플레이 폰트(헤드라인 전용) 시장 진입 X
- Italic 스타일 X (Latin Italic 유사 디자인은 향후)
- 손글씨/명조 영역 X
- 직접 수익화 (구독/유료 라이선스) X

### 5.2 User Stories

```
US-1: 구직자로서, 이력서 에디터 진입 시 자동으로 적용된 프로페셔널한 폰트로
      별도 선택 없이 작성을 시작할 수 있어야 한다.

US-2: 구직자로서, 작성한 이력서를 PDF로 다운로드했을 때 화면에서 본 모습과
      동일하게 보여야 한다 (폰트 임베딩).

US-3: 채용 담당자로서, 받은 이력서의 연봉/날짜/KPI 숫자가 자릿수에 맞춰
      정렬되어 한눈에 비교할 수 있어야 한다 (Tabular Figures).

US-4: 채용 담당자로서, 후보자의 이름/회사명/본문이 명확한 위계로 구분되어
      3초 안에 핵심 정보를 스캔할 수 있어야 한다.

US-5: 디자이너로서, GitHub에서 다운로드 후 1줄 CSS로 내 프로젝트에
      적용할 수 있어야 한다.

US-6: 사용자로서, Word/HWP에 폰트를 설치한 뒤 인크루트에서 만든 이력서를
      열어도 동일한 모습으로 표시되어야 한다.

US-7: 사용자로서, 10pt 같은 작은 크기에서도 한글 자모(ㅎ, ㅁ, ㅇ)가
      뭉개지지 않아야 한다.
```

**INVEST 체크**: 모두 Independent / Negotiable / Valuable / Estimable / Small / Testable 통과.

### 5.3 Functional Requirements

| ID | 요구사항 | Priority |
|----|---------|----------|
| FR-1 | Variable Font (wght 100–900) 단일 파일 빌드 | Must |
| FR-2 | 6개 굵기 프리셋 (--is-weight-body 350 / regular 400 / medium 500 / semibold 600 / bold 700 / extrabold 800) | Must |
| FR-3 | Tabular Figures 기본 활성 옵션 (font-feature-settings: "tnum") | Must |
| FR-4 | KS X 1001 한글 2,350자 지원 | Must |
| FR-5 | Latin (A–Z, a–z), 숫자 (0–9), 기본 기호 지원 | Must |
| FR-6 | OTF / TTF / WOFF2 동시 빌드 | Must |
| FR-7 | OFL 1.1 라이선스 적용 | Must |
| FR-8 | 인크루트 에디터 통합 (CSS 변수, font-display: swap) | Must |
| FR-9 | ATS 호환성 검증 (Workday, Greenhouse 등 5개 시스템 테스트) | Should |
| FR-10 | 작은 크기(8pt) 자동 hint 적용 | Should |
| FR-11 | 그리스/키릴/통화 기호 확장 | Could |
| FR-12 | Italic 스타일 | Won't (v1) |

### 5.4 Non-Functional Requirements

| 항목 | 요구사항 |
|------|---------|
| **성능** | WOFF2 파일 ≤ 350KB (가변 폰트 단일), 초기 로딩 ≤ 200ms (인크루트 환경) |
| **호환성** | Chrome/Safari/Edge 최신 2버전, iOS Safari, Android Chrome, Word/HWP 최근 5년 버전 |
| **접근성** | WCAG 2.1 AA 가독성 (대비비, 글자 크기) |
| **법적** | OFL 1.1 (Pretendard 호환), 이름 충돌 검색 완료, 상표 등록 검토 |
| **유지보수** | GitHub Actions CI/CD 빌드, semantic versioning, CHANGELOG.md |

### 5.5 Test Scenarios

| US | 테스트 시나리오 | 검증 방법 |
|----|----------------|----------|
| US-1 | 인크루트 에디터 진입 → font-family가 Incruit Sans로 적용되는가 | E2E (Playwright), 5개 브라우저 |
| US-2 | PDF 다운로드 후 Adobe Acrobat에서 임베딩 확인 | 수동 + pdfinfo 자동 |
| US-3 | 1234567 숫자가 모노스페이스로 정렬되는가 | tnum feature 활성 시 글자폭 동일성 검증 |
| US-4 | h1/h2/p 태그의 font-weight 위계 시각 검증 | tests/resume-test.html + Storybook |
| US-5 | npm i incruit-sans 또는 CDN 1줄 적용 | README dogfooding |
| US-6 | Word 2019 + HWP 2020에서 한국어 입력 시 폰트 표시 | 실기기 수동 |
| US-7 | 10pt에서 "흙, 햇, 흥" 글자 가독성 | 디자이너 + 사용자 5명 시각 평가 |

### 5.6 Pre-mortem (Top 3 Risks)

| # | 위험 | 영향 | 완화 |
|---|------|------|------|
| **R1** | 디자이너 리소스 확보 실패 → 글리프 정제 6개월 이상 지연 | 매우 높음 | 외주 후보 3명 사전 선정 + Glyphs 파일 검토 견적 + 의장 직속 우선순위 부여 |
| **R2** | "Pretendard와 차별화 부족" 디자인 커뮤니티 평가 → 채택 부진 | 높음 | 사전 5+5 blind test 검증 + "이력서 특화" 카테고리로 포지셔닝 (직접 비교 회피) + Pretendard와 호환 메트릭으로 마이그레이션 비용 0 강조 |
| **R3** | 라이선스/이름 충돌 (기존 Incruit Sans 폰트 존재 또는 Pretendard 라이선스 위반 의혹) | 매우 높음 | OFL 1.1 준수 검토 + USPTO/KIPRIS 상표 검색 + Pretendard 메인테이너에 사전 인사 |

### 5.7 Stakeholder Map

| 이해관계자 | 역할 | 영향력 | 관여도 |
|-----------|------|:------:|:------:|
| 이광석 의장 | Sponsor / Champion | 5 | Decide |
| 인크루트 이력서팀 PM | Beachhead 적용 책임 | 4 | Approve |
| 인크루트 디자인팀 | 글리프 정제, 브랜드 | 5 | Execute |
| 외부 폰트 디자이너 | 글리프 작업 (외주) | 4 | Execute |
| 잘쓸랩 팀 | 시범 적용 | 3 | Execute |
| 인크루트 마케팅/PR | OSS 런칭 | 3 | Inform/Approve |
| 법무 | 라이선스/상표 | 5 | Approve |
| 디자인 커뮤니티 (디스콰이엇 등) | 채택자 | 3 | Inform |
| Pretendard 메인테이너 | 호의적 관계 유지 | 2 | Inform |

### 5.8 Milestones & Success Metrics

| Phase | 일정 | Deliverable | Success Metric |
|-------|------|-------------|----------------|
| **M1** | 2026-Q2 | 글리프 정제 (104자 → 2,350자), 디자이너 계약 | Glyphs 소스 v0.5 |
| **M2** | 2026-Q3 | Variable Font 빌드 + 잘쓸랩 시범 적용 | jslab.incruit.com 100% 적용 |
| **M3** | 2026-Q4 | 인크루트 이력서 에디터 적용 + 사용자 측정 | 에디터 100%, NPS Δ +5pt |
| **M4** | 2027-Q1 | OFL 1.1 GitHub 공개 + 디자인 커뮤니티 런칭 | GitHub Star 500+, 다운로드 10K/월 |
| **M5** | 2027-Q2 | incruit.com 메인 적용 + AI 이력서 도구 통합 | 인크루트 자체 서비스 100% |
| **M6** | 2027-Q3 | 외부 채용 플랫폼 채택 + 워드/HWP 템플릿 | 외부 1곳+, 누적 reach 1M+ |

---

## 6. Open Questions

1. 인크루트 이력서 에디터 정확한 MAU? (데이터팀 확인 필요 — Beachhead 크기 검증)
2. 디자이너 외주 vs 인하우스 결정? (예산/일정에 결정적 영향)
3. "Incruit Sans" 이름 상표 충돌 검색 결과? (법무 진행 필요)
4. Pretendard 메인테이너(orioncactus)와 사전 협의 여부? (관계 리스크)
5. AI 이력서 도구 통합 우선순위? (KakaoBrain / Naver CLOVA / 자체 구축)

---

## 7. Attribution

PM Agent Team analysis frameworks integrated from [pm-skills](https://github.com/phuryn/pm-skills) by Pawel Huryn (MIT License):
- 5-Step Discovery Chain & Opportunity Solution Tree (Teresa Torres)
- JTBD 6-Part Value Proposition (Tony Ulwick)
- Lean Canvas (Ash Maurya)
- Beachhead Segment Selection (Geoffrey Moore — Crossing the Chasm)

Project sources:
- `/Users/starkid/Projects/incruit-sans/CLAUDE.md`
- `/Users/starkid/Projects/incruit-sans/docs/design-brief.md`
- `/Users/starkid/Projects/incruit-sans/docs/weight-presets.md`
- `/Users/starkid/Projects/incruit-sans/README.md`

---

## 다음 단계

```
/pdca plan incruit-sans
```

이 PRD는 Plan 문서에 자동 참조됩니다. Plan 단계에서는 (1) 디자이너 리소스 확보 (2) 글리프 정제 일정 (3) 빌드 파이프라인 검증 (4) 인크루트 에디터 통합 시점을 구체화합니다.
