# Incruit Sans — Changelog

## v0.4.1 — 2026-07-05
- **CDN(jsDelivr) 배포 지원**: `web/incruit-sans.css`·`incruit-sans-hinted.css`·`incruit-sans-vf.css` 추가
  — 태그 핀 URL(`@v0.4.1`)로 즉시 사용, 상대경로 url()이라 CSS와 woff2가 같은 태그로 불변 서빙
- 디자인 토큰 이관: 구 클론(incruitsans) 미커밋분 resume 토큰 20종 + brand/body fontFamily
  → `design-tokens/tokens.json` (토큰 SSOT를 이 repo로 단일화)
- 저장소 위생: sources/ 42MB 중복 제거(전수 byte 비교), 빈 fonts/ 제거, 구 클론 아카이브
- 폰트 바이너리 변경 없음 (v0.4와 동일)

## v0.4 — 2026-07-05
- **한글↔라틴 스크립트 경계 커닝** (class kern): 실측 기반 한→라 +45·라→한 +75 —
  "이력서Plus"·"2026년 AI" 같은 혼용 경계가 숨 쉬도록. 9웨이트+VF, 기존 라틴 kern 보존
- **chws 한글 구두점 문맥 자간 탑재** (chws_tool·halt 포함): 전각 문장부호(。、！？（） 등) 연쇄 시
  선행 부호 반각화(1920→960) — 9웨이트 OTF + VF 전체. Chrome·CoreText 등 렌더러가 기본 적용
- vchw는 세로쓰기 테이블(vmtx) 부재로 대상 아님 (fontbakery WARN 잔존은 예상 동작)
- 빌드 파이프라인에 chws 후처리 편입 (build_all_weights.py·build_vf_v2.py) — 폰트 내부 버전 0.4

## v0.3 — 2026-07-05
- **이력서 판별성**: `l` 꼬리(자족 `t` foot 이식) + `0` 중앙점 — 9웨이트+VF 전체 (Il1·0O 구분, 의장 결정)
- **VF 전면 재건**: Pretendard Variable 기반 + 라틴 gvar 이식 — gvar 보유 1,950 → **14,738/14,757** 글리프
  (구 VF는 wght=900에서 한글·곡선 라틴이 Regular로 고정되는 결함)
- 라틴 비호환 148자 자동 호환화 (전곡선 승격→윤곽 매칭→호길이+기하 DP 정렬→이웃 연쇄, `build/compat_fix.py`)
- 보간 QA: 148자+대조군 × 17웨이트 잉크 곡선 전수 스캔 + 픽셀 육안 검증
- fontbakery 결함 해소: head 버전 정합(B1) · VF named instances 9종+STAT(B2) · Mac name 제거(B3) · smart dropout prep
- TTF sfnt 서명 OTTO→TrueType 교정 (FreeType 로드 거부 원인)
- hinted TTF(ttfautohint)·웹폰트(woff/woff2) 전량 재생성
- 잔존 알려진 항목: case_mapping(Q3) · chws/vchw(Q4) · nested/transformed components(Pretendard 상류 유래) · ¼½ȺȾ 4자 VF 정적

## v0.2 — 2026-04-25
- 9 weights 일괄 빌드 (Thin 100 ~ Black 900)
- ttfautohint 적용한 Hinted TTF 추가 (build/ttf/)
- WOFF2/WOFF 변환 (build/web/, build/web/hinted/)
- Variable Font 빌드 (IncruitSans-VF.ttf, wght axis 100-900)
- BI-GUIDE.md 첨부 (인크루트 브랜드 시스템 v0.1)
- Glyphs 3 커스터마이징 가이드 첨부

## v0.1 — 2026-04-25
- 초기 합성: Pretendard 한글 + Min Sans 라틴 (Regular 1 weight)
- merge_script.py 작성 (재현 가능 빌드)
- specimen.html 시각 검수 페이지
