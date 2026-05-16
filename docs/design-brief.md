# 디자인 브리프 (Design Brief)

## Incruit Sans: 이력서·서류 특화 폰트

**버전**: 1.0 (Draft)  
**작성일**: 2026-04-25  
**대상**: 폰트 디자이너, 엔지니어  

---

## 1. 프로젝트 개요

### 목표
Pretendard의 **정돈된 구조·다양한 굵기·우수한 다국어 가독성**과  
Min Sans의 **부드럽고 따뜻한 곡선·안정감 있는 넓은 폭**을 결합하여,  
**HR/채용 입장에서 "프로페셔널하면서도 친근한" 이력서 폰트**를 제작.

### 사용 맥락
- 인크루트 이력서/자소서/경력기술서 웹 에디터
- 다운로드 PDF (Adobe, Office, 브라우저 인쇄)
- 모바일 웹 & 앱 표시
- Word, 한글(HWP), PowerPoint 임베딩

### 핵심 요구사항
- 한글, 영문(대소문자), 숫자, 기호 모두 일관된 톤
- 작은 크기(10–11pt)에서도 깨끗하고 읽기 쉬움
- ATS(지원자 추적 시스템) 호환성
- Pretendard와 유사한 메트릭(호환성 있게)

---

## 2. 설계 철학

### Pretendard에서 가져올 것
✓ **글자 폭 (Character Width)**  
- 글자 폭은 Pretendard를 베이스로 → 이력서는 한 페이지에 정보가 많아야 하므로

✓ **메트릭 (Metrics)**  
- Ascender, Descender, x-height, cap-height 비율
- 한/영 혼용 시 높이 맞춤

✓ **굵기 다양성**  
- Regular, Medium, SemiBold, Bold 등 최소 4단계 이상
- 정보 계층 표현이 풍부

✓ **숫자/기호 정밀성**  
- Tabular Figures (고정폭 숫자)
- Lining Figures (통일된 높이)
- 콜론(:), 하이픈(-), 물결(~), 슬래시(/)의 명확성

### Min Sans에서 가져올 것
✓ **곡선 미학**  
- 직선/곡선 비율을 Pretendard 수준으로 유지하되,
- 획 끝과 모서리를 Min Sans처럼 **미세 라운딩** (부드러움 강조)

✓ **글자 느낌**  
- Pretendard보다 약간 더 **따뜻하고 접근 가능한 톤**
- Min Sans의 넓은 폭은 선택적 (글자 폭은 기본적으로 Pretendard 유지)

✓ **작은 크기 최적화**  
- 내부 공간(counter)이 너무 닫히지 않도록
- ㅇ, ㅎ, 0, 6, 8 같은 폐곡선에서 충분한 호흡감

---

## 3. 기술 사양

### 3-1. 글리프 커버리지 (Glyph Set)

**필수 문자 세트**
- 한글 (KS X 1001 기준)
  - 2,350개 음절
  - 자모(초성, 중성, 종성) 포함
  
- 라틴 (A–Z, a–z, 0–9)
- 추가 기호: ! @ # $ % ^ & * ( ) - _ + = [ ] { } / \ | ; : ' " < > , . ? ~

**선택적 (확장)**
- 그리스 문자, 키릴 문자 (향후)
- 공학 기호, 통화 기호 (향후)

### 3-2. 글리프 정보 (Metrics)

**기본 메트릭 (Pretendard 기준)**

| 항목 | 단위 | 값 |
|------|------|-----|
| **UPM (Units Per Em)** | — | 1000 |
| **Ascender** | UPM | 800 |
| **Descender** | UPM | -200 |
| **Cap Height** | UPM | 750 |
| **X-Height** | UPM | 500 |
| **Default Advance Width** | UPM | ~550 (한글 정사각형 기준) |

**한영 혼용 조정**
- 한글 크기 = 영문 대문자 크기 (같은 높이)
- x-height를 한글 중간글자 높이와 맞춤 → 본문 혼용 시 조화로움

### 3-3. 굵기 축 (Weight Axis)

**Variable Font 설정**

| Weight | 마스터 | 글리프 소스 | 비고 |
|--------|--------|-----------|------|
| 350 | Thin | Thin master | 보충 텍스트 |
| 400 | Regular | Regular master | 기본값, 높은 사용률 |
| 500 | Medium | Interpolation | 강조 텍스트 |
| 600 | SemiBold | Interpolation | 섹션 제목 |
| 700 | Bold | Bold master | 주요 헤딩 |
| 800 | ExtraBold | Bold 기반 | 배너, 특수 용도 |

**interpolation 전략**
```
Thin (350) → Regular (400) → Bold (700) → ExtraBold (800)
           ↑ 선형 보간 ↑
```

### 3-4. 획 (Stroke) 특성

**획 두께**
- 수평/수직 획 두께: **거의 동일** (1:1 비율 유지)
- Pretendard처럼 스트레스가 낮은(Low-Contrast) 산세리프
- Min Sans의 부드러움은 **끝점의 라운딩**으로 표현

**특징적 글자**

| 글자 | 특성 | 예시 |
|------|------|------|
| ㄴ, ㄹ | 모서리 미세 라운딩 (1–2pt) | Thin에서도 각지지 않음 |
| ㅁ, ㅂ | 내부 공간 충분히 개방 | 10pt에서도 번지지 않음 |
| ㅇ | 내부 counter 최대한 개방 | 다른 자체보다 약간 확대 |
| 영문 "O", "0" | 한글 ㅇ과 높이/폭 통일 | 혼용 시 리듬감 |
| "l" (소문자 L) | "1"과 구분되는 세리프 (선택) | 명확성 우선 |

---

## 4. 곡선 & 디테일 튜닝 (Min Sans 영향)

### 4-1. 라운딩 수준

**접근 방식**
- Pretendard: 대부분 직선/각진 산세리프
- Min Sans: 부드럽고 둥근 곡선
- **Incruit Sans**: Pretendard 85% + Min Sans 15% (느낌으로만)

**구체적 적용**
| 부위 | Pretendard 스타일 | Min Sans 스타일 | Incruit 목표 |
|------|---------|---------|---------|
| **획 끝** | 직선(90도) | 둥글게(45도) | 미세 라운딩(20–30도) |
| **모서리** (ㄴ→ㄹ 연결) | 예각 | 둥근 곡선 | 1pt 라운드 필렛 |
| **내부 카운터** | 정사각형 | 부드러운 타원 | 정사각형 유지, 모서리만 둥글게 |

### 4-2. 감정적 톤

**Pretendard**
- 이미지: 깔끔함, 신뢰감, 현대적
- 톤: 중립적, 전문적

**Min Sans**
- 이미지: 따뜻함, 부드러움, 접근 가능
- 톤: 감성적, 친근함

**Incruit Sans** (목표)
- 이미지: 프로페셔널 + 따뜻함
- 톤: 신뢰감 있으면서도 딱딱하지 않음 (HR 이미지에 부합)

---

## 5. 이력서 특화 튜닝

### 5-1. 작은 크기 최적화 (10–11pt)

**체크리스트**
- ✓ X-height를 충분히 크게 (한글과 영문 읽기 쉬움)
- ✓ Counter (내부 공간)가 너무 좁지 않음 (번지지 않음)
- ✓ 스트로크 두께가 균형 있게 (너무 얇지 않음)
- ✓ 숫자 "0"과 "O" 구분 (하단에 작은 slant 또는 세리프)
- ✓ 소문자 "l"과 숫자 "1" 명확히 구분

### 5-2. 숫자 (Numbers)

**Lining Figures** (기본)
- 모든 숫자가 같은 높이 (대문자 높이)
- 이력서 본문 혼용에 최적

**Tabular Figures** (고정폭, 필수 OpenType Feature)
- 각 숫자가 같은 폭 → 연봉, 기간 정렬이 깔끔
  ```
  2020–2023  ✓ 각 숫자 정렬
  ```

### 5-3. 다국어 혼용

**한·영 혼합**
- 한글과 영문 대문자가 같은 기준선/높이
- x-height (영문 소문자)와 한글 중간글자 어울림
- 공백(spacing)이 한·영 모두 자연스러움

**한·영·숫자 혼합**
```
회사: Google (2020–2023)
직책: Senior Software Engineer
↑ 한글, 영어 대소문자, 숫자, 기호 모두 조화
```

---

## 6. 빌드 및 포맷

### 6-1. 포맷

| 포맷 | 용도 | 제공 여부 |
|------|------|---------|
| **.glyphs** | Glyphs 3 소스 | ✓ Primary |
| **.ufo** | Universal Font Format (백업) | ✓ |
| **.otf** | OpenType (PostScript) | ✓ |
| **.ttf** | TrueType (Hinting 적용) | ✓ |
| **.woff2** | Web Font (최적화) | ✓ |

### 6-2. Variable Font

- **축**: wght (100–900, step 1)
- **마스터**: Regular(400), Bold(700)
- **변수 폰트**: 모든 중간값 자동 interpolation
- **브라우저 지원**: Chrome 62+, Firefox 62+, Safari 11+, Edge 79+

### 6-3. 라이선스

**모델**: Pretendard 참고 (OFL 1.1)
- ✓ 상업용 무료 사용 가능
- ✓ 폰트 자체는 판매 불가
- ✓ 수정 후 재배포 시 라이선스 유지 필수
- ✓ 명칭 고지 의무

---

## 7. 호환성 타깃

### 7-1. 브라우저

| 환경 | 지원 레벨 | 비고 |
|------|---------|------|
| Chrome 62+ | ✓ Full | Variable Font 지원 |
| Firefox 62+ | ✓ Full | Variable Font 지원 |
| Safari 11+ (Mac) | ✓ Full | Variable Font 지원 |
| Safari (iOS) | ✓ Full | iOS 11+ |
| Edge 79+ | ✓ Full | Variable Font 지원 |
| IE 11 | ⚠ Fallback | Variable Font 미지원, 고정폭 대체 |

### 7-2. 문서 앱

| 앱 | 포맷 | 호환성 |
|----|------|--------|
| **Word** | TTF/OTF | ✓ 윈도우/맥 모두 |
| **한글** | TTF/OTF | ✓ 임베딩 가능 |
| **PowerPoint** | TTF/OTF | ✓ 슬라이드 삽입 |
| **Adobe Acrobat** | OTF | ✓ PDF 임베딩 |
| **Pages (맥)** | TTF/OTF | ✓ |

### 7-3. 모바일

| 디바이스 | 지원 |
|---------|------|
| **Android 5.0+** | ✓ 브라우저/앱 |
| **iOS 11+** | ✓ 브라우저/앱 |
| **iPad** | ✓ |

---

## 8. 개발 로드맵

### Phase 1: 메인 마스터 제작
- Thin(350), Regular(400), Bold(700) 마스터 글리프 완성
- 메트릭 정의, 커닝 테이블 초안

### Phase 2: Interpolation & 검증
- Variable Font 빌드
- 중간값(Medium, SemiBold) 검증
- 10–18pt 렌더링 테스트

### Phase 3: OpenType Features
- Tabular Figures 구현
- Ligatures (선택적: fi, fl)
- Localized Forms (한글 호환)

### Phase 4: 웹폰트 최적화
- woff2 압축
- Subset generation (한글 부분 로드)
- Performance 테스트

### Phase 5: 최종 검증 & 배포
- 모든 포맷 빌드 (.otf, .ttf, .woff2)
- 테스트 페이지 준비 (specimen, resume-test)
- GitHub 저장소 공개

---

## 9. 참고 자료

- [Pretendard 깃허브](https://github.com/orioncactus/pretendard)
- [Min Sans 프로젝트](https://github.com/fonts/noto-sans-kr)
- [Glyphs 글리프 편집](https://glyphsapp.com)
- [fontmake 빌드 도구](https://github.com/googlei18n/fontmake)
- [Variable Fonts 표준](https://www.w3.org/TR/css-fonts-4/)

---

## 검증 체크리스트

- [ ] Thin(350) 마스터 완성 & 메트릭 검증
- [ ] Regular(400) 마스터 완성 & 메트릭 검증
- [ ] Bold(700) 마스터 완성 & 메트릭 검증
- [ ] Variable Font interpolation 생성
- [ ] Tabular Figures 구현 & 테스트
- [ ] 10pt 렌더링 테스트 (한/영/숫자)
- [ ] 다국어 혼용 테스트
- [ ] Word/한글(HWP) 임베딩 테스트
- [ ] woff2 변환 & 웹 테스트
- [ ] PDF 출력 테스트
- [ ] 모바일 렌더링 테스트
