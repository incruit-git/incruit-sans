# Incruit Sans — Changelog

## v0.5.1 — 2026-07-22
- **tnum+zero 체인 버그 수정** — GSUB에서 `zero`(lookup 13)가 `tnum`(lookup 53)보다 먼저
  적용돼, dotted 0 옵트인 상태에서 tnum을 켜면 0만 proportional 폭(Regular 1222 vs
  tabular 1258)으로 남아 숫자 정렬이 36유닛 어긋나던 문제(Pretendard 상속, harfbuzz 실측).
  tnum lookup에 dotted alt 짝 매핑(cid14525→cid14541)을 주입해 체인 완성 — 9웨이트 전수
  `tnum+zero` 셰이핑 균일 확인. VF 동일 적용. 폰트 내부 버전 0.51 (VF head.fontRevision
  0.5 잔존도 0.51로 정합)
- **VF dotted tabular 0 어드밴스 정합** — 이식된 dotted tabular 0이 정적 마스터의
  어드밴스 모델(Black 1394)을 따라와, Pretendard 모델(1396)을 쓰는 VF의 다른 tabular
  숫자와 최대 2유닛 어긋나던 문제. gvar phantom(pp1) 델타와 hmtx를 짝 글리프(uniE071)에
  정합해 전 웨이트 spread 0 (harfbuzz 실측). 윤곽 델타는 무변경

## v0.5.0 — 2026-07-19
- **기본 `0` 민짜 복귀 (0-dot 제거)** — 의장 결정 C안: 대형 볼드 숫자(대시보드 통계 카드)에서
  중앙점이 counter의 43%(Bold)~66%(Black)를 차지해 도형-배경이 반전되어 보이는 문제.
  판별이 필요한 9–14px 본문에선 점이 1px 안팎이라 실효도 낮았음 (실측)
- **dotted 0 옵트인 제공 (GSUB `zero` feature)**: Pretendard 상속 `zero` feature의 대체
  글리프(정적 cid14525·cid14541 / VF uniE06B·uniE07B)를 「기준 0 윤곽 + 중앙 다이아몬드
  dot」로 교체 — 이력서 등 0/O 구분이 필요한 화면만 CSS 한 줄로 활성:
  `font-variant-numeric: slashed-zero` (폴백 `font-feature-settings: "zero" 1`).
  대체 글리프가 Pretendard 슬래시 윤곽이라 Min Sans 숫자와 어긋나던 문제도 함께 해소.
  어드밴스는 기준 0과 동일(tnum 폭 정렬 유지). web/ CSS 3종에 `.incruit-sans-dotted-zero`
  유틸 클래스 추가
- l-tail 등 나머지 판별성 요소는 무변경. 전 산출물(9웨이트 OTF·pre-hint/hinted TTF·VF·
  woff/woff2) 재빌드, 폰트 내부 버전 0.5
- hinted TTF는 ttfautohint 기본 옵션 + `--no-info`로 재생성 (기존 바이너리에 옵션 기록
  부재 — TTFA 테이블·name 정보 없음 실측)

## v0.4.2 — 2026-07-05
- **CDN(jsDelivr) 배포 지원**: `web/incruit-sans.css`·`incruit-sans-hinted.css`·`incruit-sans-vf.css` 추가
  — 태그 핀 URL(`@v0.4.2`)로 즉시 사용, 상대경로 url()이라 CSS와 woff2가 같은 태그로 불변 서빙
- repo public 전환 (의장 결정 2026-07-05, 전 히스토리 시크릿 스캔 0건)
- v0.4.1 태그 폐기: repo 공개 전 jsDelivr에 요청된 version+path는 404가 영구 캐시되어
  (purge로도 미해소) 새 태그로 재발행 — 내용 차이는 태그 문자열뿐
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
