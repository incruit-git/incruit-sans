# Incruit Sans

이력서·서류 특화 한글 폰트. **Pretendard의 구조**와 **Min Sans의 따뜻함**을 결합했습니다.

## 특징

- **이력서 최적화**: 10–18pt에서 깔끔하고 읽기 쉬운 설계
- **다국어 지원**: 한글, 영문, 숫자 모두 일관된 높이와 가독성
- **가변 폰트(Variable Font)**: 100–900 범위의 모든 굵기 지원
- **웹 최적화**: WOFF2 포맷으로 빠른 로딩
- **무료**: OFL 1.1 라이선스 (상업용 무료)

## 설치

### 웹 사용

```html
<link rel="stylesheet" href="path/to/incruit-sans/fonts/webfonts/style.css">

<style>
  body {
    font-family: "Incruit Sans", -apple-system, BlinkMacSystemFont, sans-serif;
  }
</style>
```

### 데스크톱 / 문서

1. `fonts/otf/` 또는 `fonts/ttf/` 폴더에서 폰트 파일 다운로드
2. 운영체제에 설치:
   - **Windows**: 폰트 파일 더블클릭 → "설치"
   - **macOS**: 폰트 파일 더블클릭 → Font Book에서 "설치"
   - **Word/한글**: 시스템 설치 후 자동으로 사용 가능

## 굵기 (Weights)

| 값 | 이름 | 용도 |
|----|------|------|
| 350 | Thin | 보충 텍스트 |
| 400 | Regular | 본문 (기본) |
| 500 | Medium | 강조, 회사명 |
| 600 | SemiBold | 섹션 제목 |
| 700 | Bold | 이름, 제목 |
| 800 | ExtraBold | 배너 |

## 이력서 권장 설정

```css
:root {
  --is-resume-name:       700;   /* 18pt 성명 */
  --is-resume-section:    600;   /* 13pt 섹션 */
  --is-resume-company:    500;   /* 12pt 회사명 */
  --is-resume-body:       400;   /* 11pt 본문 */
  --is-resume-caption:    350;   /* 10pt 보충 */
}
```

## 문서

- **[디자인 브리프](docs/design-brief.md)** — 설계 철학, 메트릭, 기술 사양
- **[굵기 프리셋](docs/weight-presets.md)** — 굵기별 사용 가이드
- **[Claude와의 협업](docs/claude-contributions.md)** — Claude가 할 수 있는 일들
- **[CLAUDE.md](CLAUDE.md)** — 프로젝트 규칙 및 개발 가이드

## 예시

이력서 미리보기는 `tests/specimen.html`을 브라우저에서 열어 확인하세요.

```bash
# 로컬 테스트 (Python HTTP 서버)
python -m http.server 8000
# 브라우저: http://localhost:8000/tests/specimen.html
```

## 빌드

폰트를 소스에서 빌드하려면:

```bash
# 환경 설정
python3 -m venv venv
source venv/bin/activate
pip install -r build/requirements.txt

# 빌드 실행
python build/build.py
# 또는 직접
fontmake sources/IncruitSans-Regular.glyphs -o otf -d
fontmake sources/IncruitSans-Regular.glyphs -o ttf -d
```

## 호환성

- **브라우저**: Chrome 62+, Firefox 62+, Safari 11+, Edge 79+
- **앱**: Word (Win/Mac), 한글(HWP), PowerPoint, Adobe Acrobat
- **모바일**: iOS 11+, Android 5.0+

## 라이선스

[SIL Open Font License 1.1](LICENSE)

- ✓ 상업용 무료 사용 가능
- ✓ 웹, 앱, 문서에서 임베딩 가능
- ✗ 폰트 자체는 판매 불가
- 자세한 조건은 [LICENSE](LICENSE) 파일 참고

## 기여

버그 리포트, 기능 제안, 개선 사항은 이슈 또는 PR로 제시해주세요.

## 참고

- [Pretendard](https://github.com/orioncactus/pretendard) — 구조와 다국어 가독성 영감
- [Min Sans](https://github.com/fonts/noto-sans-kr) — 따뜻한 곡선 영감

## 버전

- **v1.0** (2026-04-25) — 초기 릴리스

---

**Made with ❤️ for recruiters and job seekers.**
