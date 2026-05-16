# Claude가 폰트 제작에서 할 수 있는 모든 것

## 개요

Claude는 폰트 제작의 **기획, 자동화, 테스트, 문서화** 영역에서 광범위하게 지원할 수 있습니다.  
이 문서는 실제 가능한 작업 범위를 명확히 합니다.

---

## ✅ Claude가 직접 할 수 있는 것

### 1. 설계 & 기획

#### 1-1. 디자인 문서
- ✓ 디자인 브리프 작성 (목표, 메트릭, 곡선 디테일)
- ✓ 타이포그래피 사양서 작성 (x-height, ascender, descender 등)
- ✓ 굵기 프리셋 설계 (Weight 범위, 용도별 가이드)
- ✓ 문자 세트 정의 (필수/선택 글리프)
- ✓ 색상/디자인 토큰 시스템 설계

#### 1-2. 아키텍처 설계
- ✓ Variable Font 축 설계 (wght, wdth 등)
- ✓ Interpolation 전략 수립 (마스터 개수, 중간값 생성)
- ✓ OpenType feature 계획 (Tabular Figures, Ligatures 등)
- ✓ 빌드 파이프라인 설계

**예시**:
```
Claude 작성 요청:
"Variable Font 축을 350–800으로 설정하되, 
Thin(350), Regular(400), Bold(700) 3개 마스터로 
interpolation하는 방식이 좋겠는지 검증해줘"

Claude 응답:
- Interpolation 비율 계산
- 중간값(Medium 500, SemiBold 600) 예측
- 대안 제시 (2 vs 3 마스터 비교)
```

### 2. 스크립팅 & 자동화 (Python)

#### 2-1. Glyphs 스크립트 (Python API)

Glyphs는 Python으로 자동화 가능합니다. Claude가 작성할 수 있는 작업:

```python
# 예: 글리프별 메트릭 일괄 수정
from glyphsApp import Glyphs

doc = Glyphs.currentDocument
font = doc.font

# 모든 글리프의 좌우 여백 조정
for glyph in font.glyphs:
    if glyph.unicode:
        glyph.leftMetricsKey = "n"  # 기준값 설정
        glyph.rightMetricsKey = "n"
```

**Claude가 할 수 있는 Glyphs 자동화**:
- ✓ 메트릭 일괄 설정 (좌우 여백, 커닝)
- ✓ 글리프 정보 추출 (이름, UPM, advance width)
- ✓ 마스터 간 메트릭 동기화
- ✓ 커닝 테이블 생성/수정 (기본 규칙)
- ✓ 글리프 그룹 설정 자동화

#### 2-2. FontForge 스크립트 (Python)

FontForge도 Python API로 자동화 가능:

```python
import fontforge

font = fontforge.open("font.sfd")
for glyph in font.glyphs():
    if glyph.width < 500:
        glyph.width = 550  # 최소 폭 설정

font.save("font-modified.sfd")
font.generate("font.otf")
```

**Claude가 할 수 있는 FontForge 자동화**:
- ✓ UFO/SFD 파일 조작
- ✓ 글리프 너비/메트릭 조정
- ✓ OpenType features 추가
- ✓ 폰트 변수 수정 (UPM, ascender 등)

#### 2-3. fonttools 스크립트 (Python)

fonttools는 TTF/OTF 파이썬 라이브러리:

```python
from fontTools.ttLib import TTFont
from fontTools.pens.t2CharStringPen import T2CharStringPen

font = TTFont("font.otf")

# 메트릭 추출
hhea = font["hhea"]
print(f"Ascender: {hhea.ascender}, Descender: {hhea.descender}")

# OpenType feature 검증
if "GSUB" in font:
    print("GSUB table found (substitutions available)")

font.close()
```

**Claude가 할 수 있는 fonttools 자동화**:
- ✓ 메트릭 추출 & 검증 (ascender, descender, x-height)
- ✓ OpenType features 쿼리 및 수정
- ✓ 글리프 정보 추출 (이름, widths, 경로)
- ✓ 커닝/라이게처 테이블 확인
- ✓ 힌팅 정보 추가 (기본)
- ✓ 메타데이터 수정 (copyright, designer 정보)

#### 2-4. fontmake 파이프라인

fontmake는 Google의 표준 폰트 빌드 도구:

```bash
# fontmake로 OTF 빌드
fontmake sources/IncruitSans-Regular.glyphs -o otf -d

# Variable Font 빌드
fontmake sources/IncruitSans-Variable.glyphs -o variable

# Instances 생성 (고정폭)
fontmake sources/IncruitSans-Variable.glyphs -o otf
```

**Claude가 할 수 있는 fontmake 자동화**:
- ✓ `fontmake` 빌드 명령 작성
- ✓ 빌드 스크립트 작성 (build.sh, Makefile)
- ✓ 결과물 자동 검증 (생성된 폰트 확인)
- ✓ 빌드 로그 해석 및 문제 진단

#### 2-5. 커스텀 Python 유틸리티

Claude가 만들 수 있는 커스텀 도구들:

```python
# 예: 메트릭 비교 스크립트
from fontTools.ttLib import TTFont

def compare_metrics(font1_path, font2_path):
    """두 폰트의 메트릭 비교"""
    f1 = TTFont(font1_path)
    f2 = TTFont(font2_path)
    
    for name in f1.getGlyphOrder():
        w1 = f1["hmtx"][name][0]
        w2 = f2["hmtx"][name][0]
        if w1 != w2:
            print(f"{name}: {w1} vs {w2} (diff: {w2-w1})")

compare_metrics("regular.otf", "medium.otf")
```

**Claude가 만들 수 있는 유틸리티**:
- ✓ 메트릭 비교 도구 (Regular vs Bold 검증)
- ✓ 글리프 커버리지 검증 (필수 문자 확인)
- ✓ 커닝 쌍 분석 도구
- ✓ 렌더링 크기별 최적화 제안 도구
- ✓ SVG/출력 가능한 테스트 보고서 생성

### 3. 테스트 & 검증

#### 3-1. HTML/CSS 스펙시멘 페이지

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    @font-face {
      font-family: "Incruit Sans";
      src: url("../fonts/IncruitSans-Variable.woff2") format("woff2");
      font-weight: 100 900;
    }
    
    body {
      font-family: "Incruit Sans", sans-serif;
    }
    
    .weight-sample {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
    }
    
    .sample {
      font-size: 24px;
      padding: 10px;
      border: 1px solid #ccc;
    }
  </style>
</head>
<body>
  <h1>Incruit Sans Specimen</h1>
  
  <div class="weight-sample">
    <div class="sample" style="font-weight: 350;">Thin (350)</div>
    <div class="sample" style="font-weight: 400;">Regular (400)</div>
    <div class="sample" style="font-weight: 500;">Medium (500)</div>
    <div class="sample" style="font-weight: 600;">SemiBold (600)</div>
    <div class="sample" style="font-weight: 700;">Bold (700)</div>
    <div class="sample" style="font-weight: 800;">ExtraBold (800)</div>
  </div>
</body>
</html>
```

**Claude가 만들 수 있는 테스트 페이지**:
- ✓ 굵기별 스펙시멘 (모든 weight 시각화)
- ✓ 크기별 렌더링 테스트 (10pt–24pt)
- ✓ 한·영·숫자 혼용 테스트
- ✓ 이력서 레이아웃 테스트 (실제 이력서 보기)
- ✓ Tabular Figures 데모 (숫자 정렬 확인)
- ✓ 브라우저 호환성 테스트 페이지
- ✓ 모바일 반응형 테스트

#### 3-2. 자동 테스트 스크립트

```python
# 예: 기본 검증 스크립트
def validate_font(otf_path):
    """폰트 기본 검증"""
    from fontTools.ttLib import TTFont
    
    font = TTFont(otf_path)
    issues = []
    
    # 메트릭 검증
    hhea = font["hhea"]
    if hhea.ascender < 700:
        issues.append("Ascender가 너무 낮음 (< 700)")
    
    # 글리프 커버리지 확인
    required_chars = set("가나다라마바사아자차카타파하")
    available = set(chr(c) for c in font.getBestCmap().values())
    if not required_chars.issubset(available):
        issues.append(f"누락된 문자: {required_chars - available}")
    
    return issues

errors = validate_font("incruit-sans.otf")
for err in errors:
    print(f"⚠️  {err}")
```

**Claude가 만들 수 있는 검증 도구**:
- ✓ 메트릭 검증 (X-height, ascender 범위 확인)
- ✓ 글리프 커버리지 확인 (필수 문자 포함 여부)
- ✓ OpenType features 검증
- ✓ 복제 글리프 감지
- ✓ 이름 테이블 검증

### 4. CI/CD 파이프라인

#### 4-1. GitHub Actions 워크플로우

```yaml
name: Build Fonts

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -r build/requirements.txt
      
      - name: Build fonts
        run: |
          python build/build.py
      
      - name: Run validation
        run: |
          python build/validate.py
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: fonts
          path: fonts/
```

**Claude가 만들 수 있는 CI/CD**:
- ✓ GitHub Actions 워크플로우 (자동 빌드)
- ✓ 빌드 검증 단계 추가
- ✓ 릴리스 자동화 (v1.0 태그 → fonts/ 업로드)
- ✓ 웹사이트 자동 배포 (specimen 페이지)

### 5. 문서화

#### 5-1. 프로젝트 문서
- ✓ README.md (설치, 사용, 라이선스)
- ✓ CONTRIBUTING.md (기여 방식)
- ✓ 변경 로그 (CHANGELOG.md)
- ✓ API 문서 (Python 스크립트용)

#### 5-2. 사용자 가이드
- ✓ CSS 변수 가이드 (tokens/weight.css 설명)
- ✓ 이력서 에디터 적용 방법
- ✓ Word/한글 임베딩 방법
- ✓ 문제 해결 가이드 (Troubleshooting)

#### 5-3. 디자이너 가이드
- ✓ Glyphs 3 설정 가이드
- ✓ 메트릭 수정 방법
- ✓ 마스터 추가/삭제 가이드
- ✓ Feature 작성 안내 (OpenType)

---

## ❌ Claude가 직접 할 수 없는 것

### 1. 글리프 드로잉

**불가능한 이유**: 시각적 판단이 필요함

```
❌ "ㄴ의 곡선 각도를 30도에서 25도로 줄여줘"
   → Claude는 Glyphs UI에서 직접 드로잉할 수 없음
   
✓ Claude가 할 수 있는 것:
   - 드로잉 방법 설명 (가이드)
   - 현재 글리프와 다른 글리프 비교 (메타데이터)
   - 드로잉 후 메트릭 자동 조정 (Python 스크립트)
```

**필요한 도구**: Glyphs / FontLab / Inkscape (사람이 사용)

### 2. 실제 폰트 파일 생성

**불가능한 이유**: 소스 글리프 파일이 없음

```
❌ "Incruit Sans를 만들어줄 수 없을까?"
   → Glyphs 소스 없이는 .ttf/.otf 불가능
   
✓ Claude가 할 수 있는 것:
   - Pretendard/Min Sans를 기반으로 수정하는 방법 제시
   - 빌드 파이프라인 준비 (소스가 있으면 빌드 자동화)
```

### 3. 커닝 (Kerning) 시각적 조정

**불가능한 이유**: 눈으로 직접 봐야 함

```
❌ "VA 커닝 쌍 조정해줘"
   → Claude는 두 글리프가 얼마나 멀리 보이는지 판단 불가
   
✓ Claude가 할 수 있는 것:
   - 커닝 테이블 추출 (현재 값 분석)
   - 기본 커닝 규칙 제시 ("A는 V와 -50 추천")
   - 커닝 쌍 자동 생성 (기본 규칙 기반)
   - 최종 수동 검증용 시각화 페이지 생성
```

### 4. 화면 렌더링 미리보기

**불가능한 이유**: Claude는 폰트를 실제로 렌더링할 수 없음

```
❌ "10pt에서 어떻게 보여? 스크린샷 줄래?"
   → Claude는 브라우저를 조작할 수 없음
   
✓ Claude가 할 수 있는 것:
   - HTML 테스트 페이지 생성 (사용자가 브라우저에서 열기)
   - 렌더링 권장사항 제시 (메트릭 기반)
```

### 5. 디자인 판단

**불가능한 이유**: 미적 취향은 주관적임

```
❌ "ㄴ의 모서리를 2pt 더 라운딩할까, 아니면 1pt?"
   → Claude는 "더 따뜻해 보일지, 덜 딱딱해 보일지" 판단 불가
   
✓ Claude가 할 수 있는 것:
   - 두 가지 옵션을 시각적으로 설명 (가이드)
   - Pretendard/Min Sans 비교 분석
   - 최종 결정은 디자이너가
```

---

## 실전 워크플로우: Claude와 함께 폰트 제작하기

### 시나리오 1: 메트릭 최적화

```
1. 디자이너: "Glyphs에서 Regular 마스터 완성했어. 
              메트릭 검증해줄 수 있어?"

2. Claude:
   - Regular 글리프 내보내기 (UFO/OTF) → Dropbox/GitHub
   - fonttools로 메트릭 추출
   - "X-height: 500 (Good), Ascender: 750 (OK), 
              ㄴ 내부 공간: 충분"
   - 개선 제안 제시

3. 디자이너: "그럼 Medium(500)은 어떻게 생성할까?"

4. Claude:
   - Interpolation 계산 (Regular 400 + Bold 700 → Medium 500)
   - fontmake로 Variable Font 빌드
   - 렌더링 테스트 HTML 생성
   - "10–18pt에서 모두 깨끗합니다" ✓
```

### 시나리오 2: Tabular Figures 추가

```
1. 디자이너: "숫자 정렬이 필요해. Tabular Figures 어떻게 만들어?"

2. Claude:
   - OpenType feature 파일 (.fea) 작성
   - Glyphs에 복사해서 붙이는 방법 설명
   - 빌드 후 검증 스크립트 제공

3. 디자이너: Glyphs에 feature 추가, Claude가 검증

4. Claude:
   - "tnum feature 확인됨. 
     '2020–2023'이 균등하게 정렬됩니다" ✓
```

### 시나리오 3: Web Font 최적화

```
1. 디자이너: "웹에서 쓸 woff2는 어떻게 준비할까?"

2. Claude:
   - fontmake로 TTF → woff2 변환 스크립트
   - CSS 로드 코드 생성 (@font-face)
   - 성능 최적화 제안 (subset, variable font vs instances)
   - 테스트 페이지 생성

3. 디자이너: "좋아, 실제로 웹에 업로드하고 테스트하자"

4. Claude:
   - 검증 스크립트: "모든 weight 로드 완료" ✓
```

---

## Claude 요청 팁

### 좋은 요청

```
✓ "Regular 마스터가 완성됐어. 
   메트릭 검증해주고, 
   Bold(700)와의 interpolation 계획을 세워줄 수 있어?"

✓ "Tabular Figures OpenType feature를 
   쓸 수 있는 형태로 만들어줄 수 있어?"

✓ "10–11pt에서 이력서 레이아웃이 어떻게 보일지 
   테스트하는 HTML 페이지 만들어줘"
```

### 피해야 할 요청

```
❌ "ㄴ의 획각을 다시 그려줄 수 있어?" 
   → Claude는 Glyphs에서 직접 드로잉 불가

❌ "어떤 곡선이 더 따뜻해 보여?"
   → 미적 판단은 디자이너의 몫

❌ "완성된 폰트 주세요" (소스 없이)
   → 글리프 데이터 없으면 불가능
```

---

## 결론

**Claude의 강점**:
- 설계 & 기획: 개념화, 메트릭 계산
- 자동화: Python 스크립트, 빌드 파이프라인
- 검증: 메트릭 비교, 글리프 커버리지 확인
- 문서화: 가이드, 마크다운, API 문서
- 테스트: HTML 페이지, 자동화된 검증

**사람(디자이너/엔지니어)의 역할**:
- 글리프 드로잉 & 곡선 미적 판단
- 화면 렌더링 및 시각적 검증
- 최종 QA & 릴리스

**최적 협업**: Claude의 자동화 + 디자이너의 창의성 = 빠르고 정확한 폰트 제작 🚀
