# CLAUDE.md

이 파일은 Claude Code가 이 폰트 프로젝트에서 반복 작업을 할 때 참조하는 규칙과 컨텍스트를 제공합니다.

## 프로젝트 개요

**Incruit Sans** — 이력서·서류 특화 한글 폰트
- **기초**: Pretendard의 구조·다양한 굵기 + Min Sans의 부드러운 곡선
- **용도**: 인크루트 이력서/자소서/경력기술서 에디터, 웹, PDF
- **타겟 환경**: 브라우저(Chrome/Edge/Safari), Word/한글(HWP), 모바일

---

## 디렉토리 구조

```
incruit-sans/
├── CLAUDE.md                       # 이 파일
├── README.md                       # 프로젝트 소개 및 사용 가이드
├── LICENSE                         # 라이선스 (Pretendard 참고)
├── sources/                        # 글리프 소스 (Glyphs/UFO 파일)
│   └── IncruitSans-Regular.glyphs
├── tokens/                         # 디자인 토큰
│   └── weight.css
├── docs/                           # 설계 문서
│   ├── design-brief.md            # 디자이너용 상세 브리프
│   ├── weight-presets.md          # 굵기 프리셋 테이블
│   └── claude-contributions.md    # Claude 역할 가이드
├── build/                          # 빌드 스크립트
│   ├── build.sh
│   └── requirements.txt
├── fonts/                          # 빌드 결과물
│   ├── otf/                        # OpenType 포맷
│   ├── ttf/                        # TrueType 포맷
│   └── webfonts/                  # woff2 웹 폰트
├── tests/                          # 테스트 및 미리보기
│   ├── specimen.html              # 굵기별 스펙시멘
│   └── resume-test.html           # 이력서 레이아웃 테스트
└── .github/
    └── workflows/
        └── build-fonts.yml        # 자동 빌드 파이프라인
```

---

## 폰트 네이밍 규칙

- **패밀리명**: `Incruit Sans`
- **Weight 축**: 100–900 (Variable Font)
- **스타일**: Regular (Italic 미지원)
- **마스터**:
  - `IncruitSans-Regular` (Regular/400)
  - `IncruitSans-Bold` (Bold/700)
  - 중간 굵기는 interpolation으로 자동 생성

---

## 굵기 프리셋 (CSS 변수)

| CSS 변수 | 값 | 용도 |
|---------|-----|------|
| `--is-weight-body` | 350 | 이력서 본문, 설명 텍스트 |
| `--is-weight-regular` | 400 | 기본 텍스트 |
| `--is-weight-medium` | 500 | 강조, 회사명 |
| `--is-weight-semibold` | 600 | 섹션 타이틀 |
| `--is-weight-bold` | 700 | 이름, 제목 |
| `--is-weight-extrabold` | 800 | 배너 헤딩 |

자세한 내용은 `docs/weight-presets.md` 참고.

---

## 빌드 명령어

### 환경 설정
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r build/requirements.txt
```

### 폰트 빌드 (fontmake 사용)
```bash
# 모든 형식 빌드 (OTF, TTF, woff2)
python build/build.py

# 또는 직접 실행
fontmake sources/IncruitSans-Regular.glyphs -o otf -d
fontmake sources/IncruitSans-Regular.glyphs -o ttf -d
python -m fontTools.ttLib.woff2_compress fonts/ttf/IncruitSans-Regular.ttf
```

---

## 언어 규칙

- **코드 주석**: 한국어
- **커밋 메시지**: 한국어 (동사로 시작)
  - ✅ "폰트 메트릭 조정"
  - ✅ "Tabular Figures 추가"
  - ❌ "update font"
- **파일명**: camelCase 또는 kebab-case (일관성 유지)
- **변수명**: 한글 설명은 주석, 변수 자체는 영어 (font_weight, counter_width 등)

---

## 일반적인 작업 플로우

### 1. 메트릭 수정 (소스는 Glyphs/FontLab에서)
- `sources/IncruitSans-*.glyphs` 편집 (디자이너)
- Claude: Python/fonttools 스크립트 작성하여 일괄 수정 자동화 가능
- 빌드 후 `tests/specimen.html`, `tests/resume-test.html` 확인

### 2. 디자인 문서 업데이트
- `docs/design-brief.md` (메트릭, 곡선, 호환성 변경)
- `docs/weight-presets.md` (굵기 추가/변경 시)
- `tokens/weight.css` (CSS 변수 동기화)

### 3. 테스트
- 브라우저: `tests/specimen.html` 열어서 각 굵기 확인
- 이력서 레이아웃: `tests/resume-test.html` (10–18pt 크기별 테스트)
- 다국어: 한글, 영문 대소문자, 숫자, 기호 모두 확인

---

## Claude가 할 수 있는 작업

자세한 내용은 `docs/claude-contributions.md` 참고.

**직접 가능**:
- 디자인 브리프, 메트릭 정의, 프리셋 설계
- Python 스크립트: fonttools/Glyphs API, 일괄 처리, CI/CD
- HTML/CSS 테스트 페이지
- 문서화

**불가능**:
- 글리프 직접 드로잉 (Glyphs/FontLab 필요)
- 실제 .ttf/.otf 생성 (소스 없음)
- 시각적 커닝 (사람의 눈)

---

## 유용한 레퍼런스

- [Glyphs 글리프 편집](https://glyphsapp.com)
- [fontmake 문서](https://github.com/googlei18n/fontmake)
- [fonttools 문서](https://github.com/fonttools/fonttools)
- [Pretendard 프로젝트](https://github.com/orioncactus/pretendard)
- [Min Sans 프로젝트](https://github.com/fonts/noto-sans-kr)

---

## 성실함 규칙

- **추측 금지**: "아마 될 거예요" 대신 실행 후 결과 제시
- **검증 필수**: 수정 후 반드시 빌드 → 테스트 HTML 확인
- **한 번에 하나**: 여러 파일 수정 후 "됐을 겁니다" 금지
- **끝까지 추적**: 에러 발견 시 원인 파악 후 해결 또는 명확히 보고
