# Incruit Brand Identity Guide v0.1

> 인크루트 브랜드 시각 시스템 — 폰트, 색상, 여백, 타이포그래피
> 2026-04-25 · AX Office 작성 · Working Draft

---

## 0. 브랜드 톤

> **사람이 일이고, 일이 사람이다**

- **신뢰** (Trust): 1998년부터 27년간 검증된 채용 플랫폼
- **명료** (Clarity): 정보가 정직하고 빠르게 전달됨
- **사람중심** (Human): 데이터와 알고리즘은 도구, 사람이 주체

이 톤이 모든 시각 결정의 기준.

---

## 1. 타이포그래피

### 1.1 메인 폰트: Incruit Sans

- **출처**: Pretendard 한글 + Min Sans 라틴 합성 (자체 빌드)
- **위치**: `incruit-sans/build/`
- **굵기**: 9 weights (Thin 100 ~ Black 900)
- **포맷**: OTF (디자인툴/인쇄), Hinted TTF (웹/UI)
- **라이선스**: SIL OFL 1.1 — 상업 사용 자유

### 1.2 굵기 사용 가이드

| 굵기 | 값 | 용도 | 예시 |
|---|---|---|---|
| Thin | 100 | 거의 사용 안 함 | 매우 큰 헤드라인 장식용 |
| ExtraLight | 200 | 거의 사용 안 함 | 큰 영어 타이틀의 보조 |
| **Light** | 300 | **부제/긴 본문** | 기사 본문, 50자+ 설명 |
| **Regular** | 400 | **기본 본문** | 본문 14~18px, 중요 단락 |
| **Medium** | 500 | **강조 본문** | 폼 라벨, 메뉴, 카드 제목 |
| **SemiBold** | 600 | **서브 헤드** | h3~h4, 섹션 제목, 버튼 |
| **Bold** | 700 | **헤드** | h1~h2, 키 메시지 |
| ExtraBold | 800 | 광고/포스터 헤드 | 외부 마케팅 자료 |
| Black | 900 | 로고/심볼 | "Incruit" 로고타이프, 거대 헤드 |

> 일반 UI에서는 **Light 300, Regular 400, Medium 500, SemiBold 600, Bold 700** 5개만 사용 권장.

### 1.3 사이즈 시스템 (8pt grid)

| 토큰 | px | 굵기 | 용도 |
|---|---|---|---|
| `text-xs` | 12 | 400/500 | caption, footnote |
| `text-sm` | 14 | 400/500 | 보조 본문, 라벨 |
| `text-base` | 16 | 400 | 기본 본문 |
| `text-lg` | 18 | 400/500 | 강조 본문 |
| `text-xl` | 20 | 600 | 작은 헤드 (h4) |
| `text-2xl` | 24 | 600 | h3 |
| `text-3xl` | 30 | 700 | h2 |
| `text-4xl` | 36 | 700 | h1 |
| `text-5xl` | 48 | 700/800 | 페이지 헤드라인 |
| `text-6xl` | 64 | 800/900 | 랜딩 hero |

### 1.4 line-height & letter-spacing

| 사이즈 범위 | line-height | letter-spacing |
|---|---|---|
| 12~16px (본문) | 1.5 ~ 1.6 | 0 |
| 18~24px (서브헤드) | 1.4 | -0.005em |
| 30~48px (헤드) | 1.2 | -0.02em |
| 64px+ (디스플레이) | 1.05 | -0.03em |

### 1.5 한글-영문 혼용 규칙

- 한자/숫자 모두 폰트 그대로 (Incruit Sans가 한자 9,990자 + 라틴 525자 모두 포함)
- 영문 약어(API, AI, CTO)는 **대문자**로
- 단위는 약어 없이 한글 (×) → "1만 명" (○)
- 따옴표는 한글 따옴표 「」 보다 라틴 "..." 권장 (Incruit Sans에서 더 자연스러움)

---

## 2. 색상 시스템

### 2.1 Primary

```
Incruit Blue
- 50:  #EBF2FF
- 100: #C7DAFF
- 200: #94B5FF
- 300: #608FFF
- 400: #2D6AFF
- 500: #0044FF  ← 기본 Primary (CTA, 링크, 강조)
- 600: #0036CC
- 700: #002999
- 800: #001B66
- 900: #000E33
```

### 2.2 Neutral (Gray)

```
Gray
- 50:  #FAFAFA  ← 페이지 배경
- 100: #F5F5F5  ← 카드 배경
- 200: #E5E5E5  ← 디바이더, 보더
- 300: #D4D4D4
- 400: #A3A3A3  ← 비활성 텍스트
- 500: #737373
- 600: #525252  ← 보조 본문
- 700: #404040  ← 본문
- 800: #262626  ← 강한 본문
- 900: #171717  ← 헤드라인
```

### 2.3 Semantic

| 용도 | 색상 | hex |
|---|---|---|
| 성공 | Green | `#10B981` |
| 경고 | Amber | `#F59E0B` |
| 오류 | Red | `#EF4444` |
| 정보 | Blue 500 | `#0044FF` |

### 2.4 사용 비율 가이드

- **60%** Neutral (배경, 디바이더, 본문)
- **30%** Primary (헤드, 강조, CTA)
- **10%** Semantic (상태 표시만)

> 페이지에서 파란색이 너무 많이 보이면 잘못된 사용. CTA 1~2개에만.

---

## 3. 여백/간격 시스템 (8pt grid)

| 토큰 | px | 사용 |
|---|---|---|
| `space-1` | 4 | 인라인 작은 간격 |
| `space-2` | 8 | 텍스트와 아이콘 사이 |
| `space-3` | 12 | 작은 컴포넌트 내부 |
| `space-4` | 16 | 일반 컴포넌트 내부 |
| `space-5` | 20 | 라벨과 입력 사이 |
| `space-6` | 24 | 카드 패딩, 폼 그룹 |
| `space-8` | 32 | 섹션 내부 분리 |
| `space-10` | 40 | 카드 간 간격 |
| `space-12` | 48 | 섹션 사이 |
| `space-16` | 64 | 페이지 섹션 사이 |
| `space-24` | 96 | 페이지 헤드 마진 |

### 3.1 컨테이너 max-width

- 모바일: 100% (16px 좌우 패딩)
- 태블릿: 768px
- 데스크탑: 1200px (대부분의 콘텐츠)
- 와이드: 1440px (대시보드, 데이터 테이블)

---

## 4. 코드 토큰 (CSS / Tailwind)

### 4.1 CSS Custom Properties

```css
:root {
  /* Typography */
  --font-sans: 'Incruit Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', 'D2Coding', monospace;

  /* Colors */
  --primary: #0044FF;
  --primary-hover: #0036CC;
  --gray-50: #FAFAFA;
  --gray-100: #F5F5F5;
  --gray-900: #171717;
  --success: #10B981;
  --warning: #F59E0B;
  --error: #EF4444;

  /* Spacing — 8pt grid */
  --s-1: 4px; --s-2: 8px; --s-3: 12px; --s-4: 16px;
  --s-6: 24px; --s-8: 32px; --s-12: 48px; --s-16: 64px;

  /* Typography sizes */
  --text-sm: 14px; --text-base: 16px; --text-lg: 18px;
  --text-2xl: 24px; --text-4xl: 36px;
}

body {
  font-family: var(--font-sans);
  font-weight: 400;
  font-size: var(--text-base);
  line-height: 1.6;
  color: var(--gray-900);
  background: var(--gray-50);
}

h1 { font-weight: 700; font-size: var(--text-4xl); letter-spacing: -0.02em; line-height: 1.2; }
h2 { font-weight: 700; font-size: 30px; letter-spacing: -0.015em; line-height: 1.25; }
h3 { font-weight: 600; font-size: var(--text-2xl); letter-spacing: -0.01em; line-height: 1.3; }
```

### 4.2 Tailwind config (`tailwind.config.js`)

```js
module.exports = {
  theme: {
    extend: {
      fontFamily: {
        sans: ['Incruit Sans', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
      },
      colors: {
        primary: {
          50: '#EBF2FF', 100: '#C7DAFF', 500: '#0044FF',
          600: '#0036CC', 900: '#000E33',
        },
        gray: {
          50: '#FAFAFA', 100: '#F5F5F5', 200: '#E5E5E5',
          400: '#A3A3A3', 700: '#404040', 900: '#171717',
        },
      },
      letterSpacing: {
        tight: '-0.02em',
        tighter: '-0.03em',
      },
    },
  },
}
```

### 4.3 Webfont 호스팅

```css
/* /static/fonts/incruit-sans.css */
@font-face {
  font-family: 'Incruit Sans';
  font-weight: 100;
  font-display: swap;
  src: url('/fonts/IncruitSans-Thin.woff2') format('woff2'),
       url('/fonts/IncruitSans-Thin.woff') format('woff');
}
/* ... 9 weights 모두 동일하게 ... */
```

> WOFF2/WOFF 변환은 다음 단계 (`build_woff.py` 추가 예정)

---

## 5. 적용 예시

### 5.1 헤드라인

```html
<h1 style="font-weight:700; font-size:48px; letter-spacing:-0.025em; line-height:1.1;">
  사람이 일이고<br>일이 사람이다
</h1>
```

### 5.2 채용공고 카드

```html
<div class="card">
  <h4 class="title">백엔드 개발자 (시니어)</h4>
  <p class="meta">인크루트 · 서울 강남구 · 정규직</p>
  <p class="info"><strong>연봉</strong> 8,000~12,000만원</p>
</div>

<style>
.card { padding: 24px; background: white; border-radius: 8px; border: 1px solid #E5E5E5; }
.title { font-weight: 600; font-size: 18px; margin: 0 0 8px; color: #171717; }
.meta { font-weight: 400; font-size: 14px; color: #737373; margin: 0; }
.info { font-weight: 400; font-size: 14px; color: #404040; margin-top: 8px; }
.info strong { font-weight: 600; }
</style>
```

### 5.3 CTA 버튼

```html
<button class="btn-primary">로그인</button>
<button class="btn-secondary">회원가입</button>

<style>
.btn-primary {
  font-family: inherit; font-weight: 600; font-size: 14px;
  padding: 10px 24px; background: #0044FF; color: white;
  border: none; border-radius: 6px; cursor: pointer;
}
.btn-secondary {
  font-family: inherit; font-weight: 500; font-size: 14px;
  padding: 10px 24px; background: white; color: #0044FF;
  border: 1px solid #0044FF; border-radius: 6px; cursor: pointer;
}
</style>
```

---

## 6. Don't 리스트

- ❌ Pretendard, Noto Sans KR, Apple SD Gothic Neo 등 다른 한글 폰트와 혼용
- ❌ font-stretch (Condensed, Expanded) 사용 — 9 weights 외 변형 X
- ❌ italic 사용 — Incruit Sans는 italic 글리프 없음
- ❌ 본문 14px 미만 (모바일 작은 폰트는 가독성 저하)
- ❌ Primary Blue 외 임의의 강조색 (purple, teal 등)
- ❌ letter-spacing 양수 (한글에서 어색)
- ❌ line-height 1.0 미만 (글자 겹침)
- ❌ 페이지 전체에 Bold 사용 (위계 무너짐)

---

## 7. 다음 단계

- [ ] WOFF2/WOFF 변환 (웹 배포용 압축)
- [ ] Variable Font 빌드 (단일 파일 9 weights)
- [ ] 인크루트 핵심 글자 50자 커스텀 (Glyphs 3 작업)
- [ ] 다크 모드 색상 토큰 추가
- [ ] 일러스트레이션 가이드라인
- [ ] 로고 클리어 스페이스 정의
- [ ] 인쇄용 CMYK 변환 가이드
- [ ] 디자인 토큰 JSON export (Figma Tokens, Style Dictionary 호환)

---

## 8. 파일 위치

```
incruit-sans/
├── build/                        # 9 weights OTF + Hinted TTF
├── BI-GUIDE.md                   # 이 문서
├── README.md
├── specimen/specimen-weights.html  # 시각 검수 페이지
└── glyphs-customization-guide.md # Glyphs 3 작업 가이드 (별도)
```

> 의문 사항은 AX Office (kslee@incruit.com)로 문의.
