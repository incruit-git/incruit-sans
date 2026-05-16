# Changelog

이 프로젝트의 모든 주요 변경사항을 이 파일에 기록합니다.

이 형식은 [Keep a Changelog](https://keepachangelog.com/ko/1.1.0/)를 기반으로 하며,
이 프로젝트는 [Semantic Versioning](https://semver.org/lang/ko/)을 따릅니다.

## [Unreleased]

### Added
- `.gitignore` (fonts/, venv/, build 임시 파일, IDE/OS 산출물 등)
- `CHANGELOG.md` (Keep a Changelog 1.1.0 포맷, semver 적용)
- `build/build.py` Variable Font 빌드 단계 추가 (`fontmake -o variable`)
- Module 1: Build Pipeline 검증 — 참고용 폰트 파일로 베이스라인 측정

### Changed
- `build/build.py` fontmake CLI 옵션 수정 — `-d` 제거 (최신 버전 비호환), `-g`/`-i` 명시
- `build/build.py` 빌드 산출물에 Variable Font (`fonts/IncruitSans-VF.ttf`) 추가

### Baseline Measurements (build/ 참고용 폰트 기준 — 한글 2,505자 풀셋)
| Format | File | Size |
|--------|------|:----:|
| Variable Font (TTF) | `IncruitSans-VF.ttf` | 3.86 MB |
| Variable Font (WOFF2) | `IncruitSans-VF.woff2` | 1.11 MB |
| Static OTF (per instance) | `IncruitSans-{Style}.otf` | 1.4–1.5 MB |
| Static WOFF2 (unhinted) | `web/IncruitSans-{Style}.woff2` | 713–818 KB |
| Static WOFF2 (hinted) | `web/hinted/IncruitSans-{Style}.woff2` | 1.3–1.6 MB |

> **참고**: Plan/Design의 NFR "WOFF2 ≤ 350KB"는 한글 2,350자 풀셋에서 비현실적. v0.5(고빈도 500자)에서 재측정 후 Plan NFR 보정 예정.

### Notes
- 현재 `sources/IncruitSans-Regular.glyphs`는 Python으로 생성한 JSON 형식이라 fontmake/glyphsLib과 직접 호환되지 않음
- 디자이너가 Glyphs 3 앱에서 열어 저장하면 정식 텍스트 포맷으로 변환되어 빌드 가능
- 실제 빌드 검증은 디자이너 첫 정제 작업 후(Module 2 시작 시) 수행 예정

## [0.1.0] - 2026-04-25

### Added
- 프로젝트 초기 셋업 (CLAUDE.md, README.md, LICENSE, .github/workflows/)
- 디자인 문서 일체 (`docs/design-brief.md`, `docs/glyph-specifications.md`,
  `docs/weight-presets.md`, `docs/claude-contributions.md`)
- CSS 디자인 토큰 (`tokens/weight.css`) — 6단계 굵기 + 이력서 권장 프리셋
- HTML 스펙시멘 (`tests/specimen.html`, `tests/resume-test.html`)
- Glyphs 3 소스 템플릿 (`sources/IncruitSans-Regular.glyphs`)
  - Regular + Bold 마스터
  - 104 글리프 (Latin 52자, 한글 기본 음절 14자, 숫자 10자, 기호 28자)
  - 8개 인스턴스 정의 (Thin/ExtraLight/Light/Regular/Medium/SemiBold/Bold/ExtraBold/Black)
- 빌드 자동화 스크립트
  - `build/build.py` — fontmake 기반 OTF/TTF/WOFF2 빌드
  - `build/setup_bold_master.py` — Bold 마스터 자동 생성
  - `build/validate_glyphs.py` — 마스터/글리프 무결성 검증
  - `build/requirements.txt` — Python 의존성
- GitHub Actions CI/CD (`.github/workflows/build-fonts.yml`)
- PDCA 프로세스 문서
  - `docs/00-pm/incruit-sans.prd.md` — Product Requirements Document
  - `docs/01-plan/features/incruit-sans.plan.md` — Plan 문서
  - `docs/02-design/features/incruit-sans.design.md` — Design 문서

### Notes
- v0.1.0은 디자이너 정제 전 템플릿 단계입니다
- 글리프는 vendor 폰트(Pretendard + Min Sans 참조)로부터 메트릭 영감을 받음
- OFL 1.1 라이선스 채택, 상표 검색 진행 중

## [Roadmap]

### [0.2.0] - Module 1 완료 (예정)
- Build Pipeline 실제 빌드 검증
- WOFF2 파일 크기 베이스라인 측정
- GitHub Actions CI 통과 확인

### [0.3.0] - Phase A: Latin 정제 (예정)
- Latin 95자 + 숫자 20자 (tnum 포함) + 기호 50자 정제
- specimen.html 시각 검증 통과

### [0.5.0] - Phase A: 한글 고빈도 500자 (예정)
- 국립국어원 빈도 상위 500자 정제 (이력서 텍스트 95% 커버)
- 잘쓸랩(jslab.incruit.com) 시범 적용

### [1.0.0] - Phase B: KS X 1001 한글 2,350자 (예정)
- 한글 KS X 1001 전체 정제 (2,350자)
- 인크루트 이력서 에디터 통합
- ATS 5개 시스템 호환성 검증
- OFL 1.1 GitHub 공개

### [1.5.0] - Phase C: 확장 (예정)
- 그리스/키릴/통화 기호 확장
- Light 마스터 추가 (Thin/Black 품질 검증 후 필요 시)

### [2.0.0] - 미래
- Italic 스타일 검토
- AI 이력서 도구 통합
- Word/HWP 템플릿 패키지

[Unreleased]: https://github.com/incruit/incruit-sans/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/incruit/incruit-sans/releases/tag/v0.1.0
