# Release Notes — Incruit Sans v0.4

## Incruit Sans v0.4 — 한글 조판 정밀화 (chws + 한·영 경계 커닝)

v0.3(판별성 + VF 재건) 위에 한글 조판 품질 두 축을 더했습니다.

### ✨ chws — 한글 구두점 문맥 자간

전각 문장부호(。、！？（） 등)가 연달아 올 때 선행 부호를 반각화(1920→960)해
구두점 사이 벙벙한 공백을 제거합니다. `halt` 동봉.

- 9웨이트 OTF + Variable Font 전체
- Chrome·CoreText 등 주요 렌더러가 **기본 적용** (Noto CJK와 동일한 표준 출하 방식)
- 세로쓰기(vchw)는 vmtx 부재로 비대상

### ✨ 한글↔라틴 스크립트 경계 커닝

"이력서Plus", "2026년 AI혁신" 같은 혼용 문장에서 스크립트 경계가 숨 쉬도록
class 기반 kern을 추가했습니다.

- 실측 기반 설계: 시각 간격 중앙값(한→한 146 · 라→라 209 · 한→라 192 · 라→한 163, 2048 UPM)
  → A/B/C 렌더 판정으로 **한→라 +45 · 라→한 +75** 채택
- 대상: 한글 완성형 11,172자 ↔ 라틴·숫자 (U+0020–U+024F Letter/digit)
- 기존 라틴 커닝(402,119 pairs)·chws·판별성 기능 전부 보존 검증

### 📦 산출물

v0.3과 동일 구성 — OTF 9종 / VF / hinted TTF 9종 / 웹폰트(woff2·woff + hinted).
폰트 내부 버전 0.4.

### ⚠️ 업그레이드 주의

- 혼용 문장 폭이 미세하게 넓어집니다(경계당 +2.2~3.7% em) — 픽셀 스냅샷 테스트 기준 갱신 필요
- v0.2 이하에서 올라오는 경우 v0.3 노트의 주의사항(VF 캐시 무효화, l·0 자형 변경)도 함께 적용

### 라이선스

SIL Open Font License 1.1. 원본: [Pretendard](https://github.com/orioncactus/pretendard)(길형진),
[Min Sans](https://github.com/poposnail61/min-sans)(김진성).
