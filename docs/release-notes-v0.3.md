# Release Notes — Incruit Sans v0.3

> GitHub Release 본문 (v0.3 확정 — 의장 승인 2026-07-05).


---

## Incruit Sans v0.3 — 이력서 전문 폰트로의 첫 도약

### ✨ 새 기능 — 이력서 판별성

이력서는 9–11pt에서 이름·이메일·전화번호·연도를 정확히 읽는 문서입니다.

- **소문자 `l`에 꼬리**: 자족 `t`의 foot 곡선을 이식해 `I`(민바)·`l`(꼬리)·`1`(플래그)이 완전히 구분됩니다. "Illinois", "@gmail.com" 오독 방지. 9웨이트 각각 해당 웨이트의 `t`에서 좌표를 유도해 전 굵기에서 자연스럽습니다.
- **숫자 `0`에 중앙점**: `O`와의 구분 (전화번호·사번·계좌).

### 🔧 Variable Font 전면 재건

기존 VF는 14,716 글리프 중 1,950개만 굵기 변형 데이터(gvar)를 갖고 있어 **wght=900에서 한글·곡선 라틴이 Regular로 남는 결함**이 있었습니다.

- 한글·기호: 공식 **Pretendard Variable** 기반으로 재건 (축 100–900 제한)
- 라틴: 보간 호환 변환(Cu2QuMultiPen) + 비호환 148자 자동 호환화(호길이+기하 DP 정렬)
- 결과: **gvar 14,738/14,757** — 한글 포함 전 구간(100–900) 연속 보간, `font-weight: 620` 같은 중간값도 안전
- named instances 9종 + STAT 추가 — 앱 굵기 메뉴 정상 표시
- QA: 148자+대조군 × 17웨이트 잉크 곡선 전수 스캔 + 픽셀 검증

### 🩹 표준·호환성 수정

- head 버전 ↔ name 버전 문자열 정합 (fontbakery `font_version`)
- Mac 플랫폼 name 레코드 제거 (병합 원본 잔재 ≈52개/폰트)
- TTF sfnt 서명 `OTTO`→TrueType 교정 — **FreeType 계열 환경에서 로드 거부되던 원인**
- VF smart dropout control (prep) 추가
- fontbakery: FAIL 51 + ERROR 1 → **FAIL 4** (전부 상류 유래 또는 문서화된 항목)

### 📦 산출물

| 용도 | 경로 |
|---|---|
| 디자인툴/인쇄 (CFF) | `build/IncruitSans-{weight}.otf` ×9 |
| Variable Font | `build/IncruitSans-VF.ttf` |
| Windows/소자 최적화 | `build/ttf/IncruitSans-{weight}.ttf` ×9 (ttfautohint) |
| 웹 | `build/web/*.woff2·woff` + `build/web/hinted/*.woff2` |

### ⚠️ 업그레이드 주의

- 구 VF를 CDN에 올린 경우 **캐시 무효화 필수** (한글 Bold 결함 파일 잔존 방지)
- `l`·`0` 자형이 변경되므로 렌더링 스냅샷 테스트가 있다면 기준 이미지 갱신 필요

### 알려진 제한

- VF에서 ¼ ½ Ⱥ Ⱦ 4자는 정적 (마스터 간 윤곽 수 상이)
- chws/vchw(한글 구두점 문맥 자간) 미탑재 — 다음 버전 후보
- VF nested/transformed components 경고 — Pretendard Variable 상류 유래, 기능 문제 없음

### 라이선스

SIL Open Font License 1.1. 원본: [Pretendard](https://github.com/orioncactus/pretendard)(길형진), [Min Sans](https://github.com/poposnail61/min-sans)(김진성).
