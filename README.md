# Incruit Sans v0.2

**Pretendard 한글 + Min Sans 라틴 합성 폰트**

- Built: 2026-04-25
- Glyphs: 한글 11,172자 (Pretendard) + 라틴 383자 (Min Sans, 2× 스케일)
- UPM: 2048 통일
- Weights: **9 weights — Thin 100 / ExtraLight 200 / Light 300 / Regular 400 / Medium 500 / SemiBold 600 / Bold 700 / ExtraBold 800 / Black 900**
- Variable Font: `IncruitSans-VF.ttf` · `wght` axis 100–900
- Hinting: ttfautohint 적용 (build/ttf/, build/web/hinted/)
- License: SIL Open Font License 1.1 (둘 다 OFL → 합성도 OFL 자동 상속)
- 브랜드 가이드: [BI-GUIDE.md](BI-GUIDE.md)

## 합성 의도

- **한글**: 채용 플랫폼은 가독성이 핵심. Pretendard(Source Han Sans 기반)가 검증되어 있어 그대로 채용
- **라틴**: 인크루트 브랜드 톤(친근/사람중심)에 Min Sans(Nunito 계열)의 둥근 라틴이 더 적합하다고 판단

## 파일 구조

```
incruit-sans/
├── README.md                            # 이 파일
├── CHANGELOG.md                         # 버전별 변경사항
├── BI-GUIDE.md                          # 인크루트 브랜드 시스템 v0.1
├── glyphs-customization-guide.md        # Glyphs 3 커스터마이징 가이드
├── AUTHORS.md
├── merge_script.py                      # 단일 weight 합성 스크립트
├── build_all_weights.py                 # 9 weights 일괄 빌드 스크립트
├── source/
│   ├── Pretendard-{9 weights}.otf       # 원본 (orioncactus, OFL)
│   └── MinSans-{9 weights}.otf          # 원본 (Jinseong Kim, OFL)
├── build/
│   ├── IncruitSans-{9 weights}.otf      # ★ 디자인툴/인쇄용 (CFF)
│   ├── IncruitSans-VF.ttf               # ★ Variable Font (wght 100-900)
│   ├── ttf/
│   │   └── IncruitSans-{9 weights}.ttf  # Hinted TTF (ttfautohint)
│   ├── web/
│   │   ├── IncruitSans-{9 weights}.woff2   # ★ 웹 배포용 (unhinted)
│   │   ├── IncruitSans-{9 weights}.woff
│   │   ├── IncruitSans-VF.woff2            # Variable Font WOFF2
│   │   └── hinted/
│   │       └── IncruitSans-{9 weights}.woff2   # 웹 작은 사이즈용 (hinted)
│   └── OFL.txt                          # 라이선스
├── design-tokens/                       # Figma Tokens / Style Dictionary 호환
└── specimen/
    ├── specimen.html                    # Regular weight 검수
    ├── specimen-weights.html            # 9 weights 검수 + OTF/Hinted 비교
    └── specimen-resume.html             # 이력서 시나리오 검수 (좌우 비교 + 진단)
```

## 사용법

### macOS에 설치

```bash
# 9 weights 모두 설치
open build/IncruitSans-*.otf
# Font Book 열림 → 모두 설치
```

### CSS — 9 weights

```css
/* 디자인툴/인쇄용 (CFF) */
@font-face { font-family: 'Incruit Sans'; src: url('IncruitSans-Thin.otf') format('opentype'); font-weight: 100; }
@font-face { font-family: 'Incruit Sans'; src: url('IncruitSans-Regular.otf') format('opentype'); font-weight: 400; }
@font-face { font-family: 'Incruit Sans'; src: url('IncruitSans-Bold.otf') format('opentype'); font-weight: 700; }
/* ... 나머지 6 weights 동일 패턴 */

body { font-family: 'Incruit Sans', system-ui, sans-serif; }
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

### CSS — Variable Font (단일 파일 9 weights)

```css
@font-face {
  font-family: 'Incruit Sans VF';
  src: url('build/web/IncruitSans-VF.woff2') format('woff2-variations');
  font-weight: 100 900;
  font-display: swap;
}

.ui-thin   { font-family: 'Incruit Sans VF'; font-weight: 100; }
.ui-bold   { font-family: 'Incruit Sans VF'; font-weight: 700; }
```

### 이력서·표 정렬을 위한 등폭 숫자

```css
.tabular { font-feature-settings: 'tnum' on, 'lnum' on; font-variant-numeric: tabular-nums; }
```

`tnum` 적용 여부는 `specimen/specimen-resume.html` 의 진단 1 영역에서 시각 확인 가능.

### 시각 검수

```bash
open specimen/specimen.html             # Regular 단일 weight
open specimen/specimen-weights.html     # 9 weights + 작은 사이즈 hinting 비교
open specimen/specimen-resume.html      # 이력서 시나리오 검수 (OTF vs Hinted, tabular figures, 한·영 베이스라인)
```

## v0.2 개선 사항

| 항목 | v0.1 | v0.2 |
|---|---|---|
| Weight 수 | Regular 1개 | **9개** (Thin~Black) |
| Variable Font | ❌ | ✅ `IncruitSans-VF.ttf` (wght 100-900) |
| Hinting | ❌ | ✅ ttfautohint (build/ttf/, build/web/hinted/) |
| 웹 배포 포맷 | ❌ | ✅ WOFF2 / WOFF (build/web/) |
| 브랜드 가이드 | ❌ | ✅ [BI-GUIDE.md](BI-GUIDE.md) |
| Design Tokens | ❌ | ✅ design-tokens/ (Figma Tokens 호환) |
| Specimen | 단일 페이지 | 3개 (single weight / 9 weights / 이력서) |

## 다음 단계 후보

| 작업 | 효과 | 시간 |
|---|---|---|
| 인크루트 핵심 글자 커스텀 | "인크루트", "채용" 등 BI 강화 | 1주 (Glyphs 3) |
| GPOS 라틴-한글 커닝 페어 | 한·영 혼용 시 시각 어긋남 보정 | 2일 |
| 자모 분리 디자인 (Track 2) | 진정한 자체 폰트 | 1~3개월 (디자이너 협업) |
| CDN 배포 | incruit 서비스 통합 사용 | jsDelivr 또는 자체 CDN, 1일 |
| OpenType feature 확장 | tnum 검증·ss01 고유 글리프 | 3일 |

## 라이선스 의무

OFL 1.1에 따라:
1. ✅ 이름을 "Pretendard", "Min Sans"가 아닌 "Incruit Sans"로 변경 (Reserved Font Name 회피)
2. ✅ OFL.txt 동봉 (build/OFL.txt)
3. ✅ name table에 origin 표기 (nameID 13 license description)
4. 외부 배포 시 source(또는 build_all_weights.py + 원본 폰트) 함께 배포해야 함
5. ❌ 폰트 파일 자체를 판매 금지 (서비스 일부로 사용은 OK)
6. ✅ 상업적 사용 자유 (인크루트 BI, www, 모바일, 인쇄물 모두 가능)

## 출처

- [Pretendard](https://github.com/orioncactus/pretendard) by 길형진 (orioncactus)
- [Min Sans](https://github.com/poposnail61/min-sans) by 김진성 (Jinseong Kim)
