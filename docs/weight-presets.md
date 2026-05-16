# 굵기 프리셋 (Weight Presets)

Incruit Sans의 권장 굵기 레벨과 사용 사례.

---

## 전체 프리셋 테이블

| 값 | 이름 | 영문명 | 용도 | 일반적 크기 |
|----|------|--------|------|-----------|
| **350** | 극세 | Thin/Light | 보충 텍스트, 주석, 뒷받침 설명 | 9pt |
| **400** | 정규 | Regular | 기본 단락, 본문, UI 일반 텍스트 | 11pt |
| **500** | 중간 | Medium | 강조 단어, 회사명, 직책, 라벨 | 12pt |
| **600** | 준굵음 | SemiBold | 섹션 타이틀 ("경력사항", "학력", "자격증") | 13pt |
| **700** | 굵음 | Bold | 이름(성명), 문서 제목, 주요 헤딩 | 16–18pt |
| **800** | 특굵음 | ExtraBold | 배너, 광고성 헤딩 (이력서 외 용도) | 20pt+ |

---

## 이력서 에디터 권장 설정

### 기본 구성 (3단계)
일반 사용자를 위한 단순한 구성:

| 항목 | 굵기 | 크기 |
|------|------|------|
| 이름(성명) | **700 Bold** | 18pt |
| 섹션 타이틀 | **600 SemiBold** | 13pt |
| 회사명 / 직책 | **500 Medium** | 12pt |
| 본문 | **400 Regular** | 11pt |
| 부가 설명 | **350 Thin** | 10pt |

### 고급 구성 (전체 6단계)
파워 유저를 위한 전체 옵션:
- Thin (350)
- Regular (400)
- Medium (500)
- SemiBold (600)
- Bold (700)
- ExtraBold (800)

---

## 사용 시나리오별 권장

### 시나리오 1: 표준 이력서 (1페이지)
```
이름: 700 Bold 18pt
휴대폰 / 이메일: 400 Regular 11pt
─────────────
섹션 타이틀: 600 SemiBold 13pt
  회사명: 500 Medium 12pt
  직책: 400 Regular 11pt
  주요 업무: 400 Regular 11pt (한 줄 당 한 가지)
  성과: 400 Regular 11pt (bullet 포함)
─────────────
학력: 600 SemiBold 13pt
  대학명: 500 Medium 12pt
  학위: 400 Regular 11pt
  졸업일: 350 Thin 10pt
```

### 시나리오 2: 상세 이력서 (다중 페이지)
- 본문 대부분: **400 Regular 11pt**
- 강조가 필요한 부분만: **500 Medium**
- 섹션 분리: **600 SemiBold** (공백으로 충분함, 글자 크기는 유지)

### 시나리오 3: 자소서 (자유 형식)
- 기본: **400 Regular 11pt** (또는 12pt)
- 항목 구분: **600 SemiBold 13pt**
- 강조 단어: **500 Medium**

### 시나리오 4: 경력기술서 (프로젝트 기반)
- 프로젝트명: **700 Bold 14pt**
- 역할/기술: **600 SemiBold 12pt**
- 상세 설명: **400 Regular 11pt**
- 기술 스택 태그: **500 Medium 10pt**

---

## CSS 변수 (tokens/weight.css)

```css
:root {
  /* 기본 굵기 레벨 */
  --is-weight-thin:       350;
  --is-weight-regular:    400;
  --is-weight-medium:     500;
  --is-weight-semibold:   600;
  --is-weight-bold:       700;
  --is-weight-extrabold:  800;

  /* 이력서 에디터 권장 프리셋 */
  --is-resume-name:       700;      /* 성명 */
  --is-resume-section:    600;      /* 섹션 제목 */
  --is-resume-company:    500;      /* 회사명 */
  --is-resume-body:       400;      /* 본문 */
  --is-resume-caption:    350;      /* 보충 설명 */

  /* 추가: 자소서 프리셋 (옵션) */
  --is-coverletter-title: 600;
  --is-coverletter-body:  400;
}
```

### HTML 사용 예시

```html
<style>
  .resume-name {
    font-weight: var(--is-resume-name);
    font-size: 18px;
  }
  .resume-section {
    font-weight: var(--is-resume-section);
    font-size: 13px;
  }
  .resume-company {
    font-weight: var(--is-resume-company);
    font-size: 12px;
  }
  .resume-body {
    font-weight: var(--is-resume-body);
    font-size: 11px;
  }
</style>

<h1 class="resume-name">김준호</h1>
<h2 class="resume-section">경력사항</h2>
<p class="resume-company">Google</p>
<p class="resume-body">검색 엔진 개선 프로젝트 담당...</p>
```

---

## 설계 철학

### Pretendard와의 호환성
- 굵기 범위: Pretendard의 Thin(100)~Black(900) 중 중앙값 사용
- 이력서: 정보 계층이 명확해야 하므로 6단계 제공

### Min Sans와의 균형
- 너무 부드럽지만 너무 옅지 않게
- 작은 크기(10–11pt)에서도 읽기 편하도록 weight 350을 정규가 아닌 선택적으로 제공

### 웹 호환성
- 표준 CSS font-weight 값과 정렬
  - 350 → 실제 wght 축 값 (Variable Font)
  - 400 → 표준 Regular (모든 브라우저)
  - 500 → 표준 Medium
  - 700 → 표준 Bold

---

## 다국어 텍스트 혼용 고려사항

### 한·영 혼합
- 한글 굵기와 영문 대문자 높이가 맞아야 함
- Pretendard처럼 x-height와 한글 높이 조정 완료

### 숫자
- **Tabular Figures**: 연봉, KPI, 날짜 범위는 반드시 Tabular Figures 사용
  - 예: "2020–2023" (정렬이 깔끔함)
- **Proportional Figures**: 자유 텍스트에서 숫자가 섞일 때

---

## 버전 히스토리

| 버전 | 일자 | 변경사항 |
|------|------|---------|
| 1.0 | 2026-04-25 | 초기 프리셋 정의 (350–800, 6단계) |

---

자세한 디자인 사항은 `design-brief.md` 참고.
