# Incruit Sans v0.1

**Pretendard 한글 + Min Sans 라틴 합성 폰트**

- Built: 2026-04-25
- Glyphs: 한글 11,172자 (Pretendard) + 라틴 383자 (Min Sans, 2× 스케일)
- UPM: 2048 통일
- Style: Regular (400)
- License: SIL Open Font License 1.1 (둘 다 OFL → 합성도 OFL 자동 상속)

## 합성 의도

- **한글**: 채용 플랫폼은 가독성이 핵심. Pretendard(Source Han Sans 기반)가 검증되어 있어 그대로 채용
- **라틴**: 인크루트 브랜드 톤(친근/사람중심)에 Min Sans(Nunito 계열)의 둥근 라틴이 더 적합하다고 판단

## 파일 구조

```
incruit-sans/
├── README.md                            # 이 파일
├── merge_script.py                      # 재현 가능 빌드 스크립트
├── source/
│   ├── Pretendard-Regular.otf           # 원본 (orioncactus, OFL)
│   └── MinSans-Regular.otf              # 원본 (Jinseong Kim, OFL)
├── build/
│   ├── IncruitSans-Regular.otf          # ★ 산출물
│   └── OFL.txt                          # 라이선스
└── specimen/
    └── specimen.html                    # 시각 검수 페이지
```

## 사용법

### macOS에 설치
```bash
open build/IncruitSans-Regular.otf
# Font Book 열림 → "글꼴 설치" 클릭
```

### CSS
```css
@font-face {
  font-family: 'Incruit Sans';
  src: url('IncruitSans-Regular.otf') format('opentype');
  font-weight: 400;
}
body { font-family: 'Incruit Sans', sans-serif; }
```

### 시각 검수
```bash
open specimen/specimen.html
```

## v0.1 한계 (다음 단계)

- **Regular 1weight만**: 9 weights(Thin~Black)로 확장 필요. 둘 다 9 weights 제공하므로 동일 스크립트로 batch 처리 가능
- **메트릭 미세조정 X**: Min Sans 라틴의 베이스라인이 Pretendard와 살짝 다를 수 있음. specimen.html 검수 후 hhea/OS/2 fine-tune 필요
- **커닝 미점검**: GPOS 테이블의 라틴-한글 커닝 페어 검증 필요
- **힌팅 부재**: ttfautohint 적용 후 작은 사이즈 체크 (특히 본문 14px 이하)
- **Variable Font 미지원**: 두 원본 모두 Variable 버전 있으므로 차후 합성 가능

## 다음 작업 후보

| 작업 | 효과 | 도구 | 시간 |
|---|---|---|---|
| 9 weights 일괄 빌드 | Thin~Black 풀세트 | merge_script.py 루프 | 1시간 |
| 인크루트 핵심 글자 커스텀 | "인크루트", "채용" 등 BI 강화 | Glyphs 3 | 1주 |
| ttfautohint 적용 | 작은 사이즈 가독성 | `ttfautohint` CLI | 30분 |
| Variable Font 합성 | 단일 파일 9 weights | merge_script.py 변형 | 4시간 |
| 자모 분리 디자인 (Track 2) | 진정한 자체 폰트 | Glyphs 3 + 디자이너 | 1~3개월 |

## 라이선스 의무

OFL 1.1에 따라:
1. ✅ 이름을 "Pretendard", "Min Sans"가 아닌 "Incruit Sans"로 변경 (Reserved Font Name 회피)
2. ✅ OFL.txt 동봉 (build/OFL.txt)
3. ✅ name table에 origin 표기 (nameID 13 license description)
4. 외부 배포 시 source(또는 merge_script.py + 원본 폰트) 함께 배포해야 함
5. ❌ 폰트 파일 자체를 판매 금지 (서비스 일부로 사용은 OK)
6. ✅ 상업적 사용 자유 (인크루트 BI, www, 모바일, 인쇄물 모두 가능)

## 출처

- [Pretendard](https://github.com/orioncactus/pretendard) by 길형진 (orioncactus)
- [Min Sans](https://github.com/poposnail61/min-sans) by 김진성 (Jinseong Kim)
