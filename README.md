# Incruit Sans

**이력서 전문 폰트 — Pretendard 한글 × Min Sans 라틴**

- Version: **v0.5.1** (폰트 바이너리 = v0.51 — [CHANGELOG](CHANGELOG.md))
- Last built: 2026-07-05
- Glyphs: 한글 11,172자 (Pretendard) + 라틴 383자 (Min Sans, 2× 스케일) — 총 14,716 (VF 14,757)
- UPM: 2048 통일
- Weights: **9 — Thin 100 / ExtraLight 200 / Light 300 / Regular 400 / Medium 500 / SemiBold 600 / Bold 700 / ExtraBold 800 / Black 900**
- Variable Font: `IncruitSans-VF.ttf` · `wght` 100–900 · **전 글리프 보간** (gvar 14,738/14,757) · named instances 9종 + STAT
- Hinting: ttfautohint (build/ttf/, build/web/hinted/)
- License: SIL Open Font License 1.1 (원본 둘 다 OFL → 합성도 OFL 상속)
- 브랜드 가이드: [BI-GUIDE.md](BI-GUIDE.md)

## 왜 "이력서 전문"인가

이력서는 9–11pt에서 이름·이메일·전화번호·연도를 정확히 읽는 문서다. Incruit Sans는 이 시나리오에 맞춰 판별성을 조정했다:

| 기능 | 내용 |
|---|---|
| **`l` 꼬리** | 소문자 l에 자족 `t`의 foot 곡선을 이식 — `I`(민바)·`l`(꼬리)·`1`(플래그) 완전 구분. "Illinois", "@gmail" 오독 방지 |
| **`0` 중앙점 (옵트인)** | 기본 0은 민짜(대시보드 대형 숫자 미관), 이력서 등 `O` 구분이 필요한 곳만 CSS `font-variant-numeric: slashed-zero`로 다이아몬드 dot 활성 |
| **등폭 숫자 정렬** | tabular 숫자 중심선 스프레드 0 UPM — 표·연봉·기간 세로 정렬 (9웨이트+VF 전 구간) |
| **한·영 수직 정합** | 수직 메트릭 9웨이트+VF 완전 동일 (hhea/typo/win) |
| **chws 문맥 자간** | 전각 구두점 연쇄 시 반각화(。、！？（） 등) — 렌더러 기본 적용 (v0.4) |
| **한·영 경계 커닝** | 한글↔라틴/숫자 class kern +45/+75 — 혼용 문장 경계 가독성 (v0.4) |

시각 확인: `specimen/specimen-resume.html`

## 합성 의도

- **한글**: 채용 플랫폼은 가독성이 핵심. Pretendard(Source Han Sans 기반)가 검증되어 있어 그대로 채용
- **라틴**: 인크루트 브랜드 톤(친근/사람중심)에 Min Sans(Nunito 계열)의 둥근 라틴이 더 적합하다고 판단

## 파일 구조

```
incruit-sans/
├── README.md / CHANGELOG.md / AUTHORS.md / BI-GUIDE.md
├── glyphs-customization-guide.md        # Glyphs 3 커스터마이징 가이드
├── merge_script.py                      # (역사) 단일 weight 합성 스크립트
├── build_all_weights.py                 # [1] 9 weights OTF 일괄 빌드
├── source/
│   ├── Pretendard-{9 weights}.otf       # 원본 (orioncactus, OFL)
│   ├── PretendardVariable.ttf           # 원본 VF (한글 보간 기반, OFL)
│   └── MinSans-{9 weights}.otf          # 원본 (Jinseong Kim, OFL)
├── build/
│   ├── IncruitSans-{9 weights}.otf      # ★ 디자인툴/인쇄용 (CFF)
│   ├── IncruitSans-VF.ttf               # ★ Variable Font (wght 100-900)
│   ├── distinguish_pass.py              # 판별성 패스 (l-tail + dotted-0 옵트인) — [1]에 통합
│   ├── retune_tabular_digits.py         # tabular 재정렬 — [1]에 통합
│   ├── fix_j_overhang.py                # j 돌출 수정 — [1]에 통합
│   ├── build_ttf_vf.py                  # [2] OTF→보간호환 TTF (ttf-pre-hint/, gitignore)
│   ├── build_vf_v2.py                   # [3] VF 재건 (Pretendard Variable 기반)
│   ├── compat_fix.py                    # 마스터 비호환 글리프 자동 호환화
│   ├── build_web_fonts.py               # [4] woff/woff2 + hinted 일괄
│   ├── ttf/                             # Hinted TTF (ttfautohint)
│   ├── web/                             # ★ 웹 배포 woff2/woff + hinted/
│   └── OFL.txt
├── docs/                                # 감사·검증 리포트
├── design-tokens/                       # Figma Tokens / Style Dictionary 호환
└── specimen/                            # 시각 검수 페이지 (아래 참조)
```

## 빌드 재현 (전체 파이프라인)

```bash
source venv/bin/activate   # fontTools + ttfautohint(brew) 필요
python3 build_all_weights.py          # [1] OTF 9종 (retune·j fix·판별성·B1·B3 포함)
python3 build/build_ttf_vf.py ttf     # [2] 보간 호환 TTF 9종 (Cu2QuMultiPen 병렬 변환)
python3 build/build_vf_v2.py          # [3] VF (Pretendard Variable + 라틴 gvar 이식)
for w in Thin ExtraLight Light Regular Medium SemiBold Bold ExtraBold Black; do
  ttfautohint --no-info --default-script=latn \
    build/ttf-pre-hint/IncruitSans-$w.ttf build/ttf/IncruitSans-$w.ttf
done                                  # [4] hinted TTF
python3 build/build_web_fonts.py      # [5] woff/woff2 + web/hinted
```

## 사용법

### CDN (jsDelivr) — 웹 서비스 권장

repo에 커밋된 `web/*.css`를 jsDelivr 태그 핀 URL로 바로 사용한다. 태그 핀 URL은 영구 캐시라
배포 후 변하지 않으며, 버전 업그레이드 = `<link>`의 태그만 교체.

```html
<!-- 정적 9웨이트 (일반 본문) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/incruit-git/incruit-sans@v0.5.1/web/incruit-sans.css">

<!-- 소형 UI·Windows 최적화 (ttfautohint) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/incruit-git/incruit-sans@v0.5.1/web/incruit-sans-hinted.css">

<!-- Variable Font 단일 파일 (family: 'Incruit Sans Variable') -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/incruit-git/incruit-sans@v0.5.1/web/incruit-sans-vf.css">
```

```css
body { font-family: 'Incruit Sans', Pretendard, sans-serif; }
```

> ⚠️ **`@main` 사용 금지.** `@main`은 12시간 유동 캐시라 릴리스 간 파일이 섞일 수 있고,
> v0.3 이전의 한글 Bold 결함 VF가 캐시에 남을 수 있다. 반드시 태그를 핀한다.

### macOS에 설치

```bash
open build/IncruitSans-*.otf   # Font Book → 모두 설치
```

### CSS — 웹 배포 (WOFF2 권장)

```css
/* 일반 웹 본문: unhinted WOFF2 */
@font-face {
  font-family: 'Incruit Sans';
  src: url('build/web/IncruitSans-Regular.woff2') format('woff2');
  font-weight: 400;
  font-display: swap;
}

/* 작은 사이즈/UI 컴포넌트: hinted WOFF2 */
@font-face {
  font-family: 'Incruit Sans Hinted';
  src: url('build/web/hinted/IncruitSans-Regular.woff2') format('woff2');
  font-weight: 400;
  font-display: swap;
}
```

### CSS — Variable Font (단일 파일, 100–900 전 구간)

```css
@font-face {
  font-family: 'Incruit Sans VF';
  src: url('build/web/IncruitSans-VF.woff2') format('woff2-variations');
  font-weight: 100 900;
  font-display: swap;
}

.ui-thin { font-family: 'Incruit Sans VF'; font-weight: 100; }
.ui-bold { font-family: 'Incruit Sans VF'; font-weight: 700; }
.ui-mid  { font-family: 'Incruit Sans VF'; font-weight: 620; }  /* 중간값도 안전 */
```

> VF는 한글 포함 **전 글리프가 보간**된다 (2026-07-05 재건). 이전 버전(gvar 1,950개)은
> wght=900에서 한글이 Regular로 남는 결함이 있었다 — CDN 캐시 갱신 필수.

### 이력서·표 정렬을 위한 등폭 숫자

```css
.tabular { font-feature-settings: 'tnum' on, 'lnum' on; font-variant-numeric: tabular-nums; }
```

### 시각 검수

```bash
open specimen/specimen.html             # Regular 단일 weight
open specimen/specimen-weights.html     # 9 weights + 작은 사이즈 hinting 비교
open specimen/specimen-resume.html      # 이력서 시나리오 (tabular, 한·영 베이스라인, Il1/0O)
open specimen/digit-alignment-test.html # tabular 정렬 진단
open specimen/latin-hangul-test.html    # 한·라틴 조화 진단
```

## 버전 요약

| 항목 | v0.1 | v0.2 | v0.3 (2026-07-05) |
|---|---|---|---|
| Weights | 1 | 9 | 9 |
| Variable Font | ❌ | △ (gvar 13%, 한글 Bold 불가) | ✅ **전 글리프 보간 + instances 9종** |
| 판별성 (Il1·0O) | ❌ | ❌ | ✅ l-tail + dotted-0(zero feature 옵트인) |
| 표준 준수 | — | FAIL 51+ERROR 1 | FAIL 4 (상류 유래·문서화) |
| Hinting / WOFF2 | ❌ | ✅ | ✅ (전량 재생성) |

## 다음 단계 후보

| 작업 | 효과 | 규모 |
|---|---|---|
| 인크루트 핵심 글자 커스텀 | "인크루트", "채용" 등 BI 강화 | 1주 (Glyphs 3) |
| 자모 분리 디자인 (Track 2) | 진정한 자체 폰트 | 1–3개월 (디자이너 협업) |

## 라이선스 의무

OFL 1.1에 따라:
1. ✅ 이름을 "Pretendard", "Min Sans"가 아닌 "Incruit Sans"로 변경 (Reserved Font Name 회피)
2. ✅ OFL.txt 동봉 (build/OFL.txt)
3. ✅ name table에 origin 표기 (nameID 13 license description)
4. 외부 배포 시 source(또는 빌드 스크립트 + 원본 폰트) 함께 배포해야 함
5. ❌ 폰트 파일 자체를 판매 금지 (서비스 일부로 사용은 OK)
6. ✅ 상업적 사용 자유 (인크루트 BI, www, 모바일, 인쇄물 모두 가능)

## 출처

- [Pretendard](https://github.com/orioncactus/pretendard) by 길형진 (orioncactus) — 정적 9종 + Variable
- [Min Sans](https://github.com/poposnail61/min-sans) by 김진성 (Jinseong Kim)
