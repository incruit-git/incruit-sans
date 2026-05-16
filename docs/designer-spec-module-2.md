# Incruit Sans — 디자이너 작업 명세 & 견적 요청서

> **수신**: 외주 폰트 디자이너 후보
> **발신**: 인크루트 ㈜ (fonts@incruit.com)
> **작성일**: 2026-04-26
> **회신 마감**: 2026-05-09 (2주)
> **프로젝트 연락처**: 이광석 (의장, CHO)

---

## 1. 프로젝트 개요

### 1.1 프로젝트명
**Incruit Sans** — 이력서·자기소개서 특화 한글 가변 폰트

### 1.2 컨셉
- **구조**: Pretendard의 정돈된 메트릭 + 다양한 굵기
- **곡선**: Min Sans의 부드러운 모서리 처리 (차별화 포인트)
- **컨텍스트**: 한국어 이력서 작성·평가 환경에 최적화

### 1.3 라이선스
- **SIL Open Font License 1.1 (OFL)** — 디자인 작업물도 OFL 양도
- 디자이너 크레딧은 README와 폰트 메타데이터에 명기

### 1.4 산출물 규모
| Phase | 글리프 수 | 마스터 |
|-------|:--------:|:------:|
| **Module 2 (v0.3)** | 165자 (Latin 95 + 숫자 20 + 기호 50) | Regular + Bold |
| **Module 3 (v0.5)** | + 한글 고빈도 500자 = 665자 | Regular + Bold |
| **Module 4 (v1.0)** | + KS X 1001 한글 잔여 1,850자 = 2,505자 | Regular + Bold |

---

## 2. 기술 사양

### 2.1 작업 도구
- **Glyphs 3** (필수, 디자이너 자체 라이선스 사용 또는 인크루트가 제공 협의)
- 산출물 형식: `.glyphs` (Glyphs 3 텍스트 포맷)

### 2.2 폰트 메트릭

| 항목 | 값 (UPM) | 비고 |
|------|----------|------|
| **UPM** | 1000 | 표준 |
| **Ascender** | 800 | Pretendard 호환 |
| **Descender** | -200 | Pretendard 호환 |
| **x-height** | 500 | Pretendard 호환 |
| **Cap-height** | 750 | Pretendard 호환 |
| **Stroke (Regular 마스터)** | 80 UPM | 기본 두께 |
| **Stroke (Bold 마스터)** | 140 UPM | 1.75배 |
| **Corner Radius** | 20–40 UPM | **Min Sans 영감 — 차별화 핵심** |

> ⚠️ Pretendard 메트릭 호환은 마이그레이션 비용 0을 위한 의도적 설계 결정입니다. 변경 시 사전 협의 요망.

### 2.3 마스터 구성 (확정)

```
Regular (wght 400) — 마스터 1
   ↑↓ Variable interpolation
Bold (wght 700) — 마스터 2
```

8 인스턴스(Thin/ExtraLight/Light/Regular/Medium/SemiBold/Bold/ExtraBold/Black)는 fontmake가 자동 보간 생성. 디자이너는 Regular와 Bold 두 마스터만 정제.

### 2.4 OpenType Features (필수)

| Feature | Tag | 디자이너 역할 |
|---------|-----|--------------|
| **Tabular Figures** | `tnum` | `zero.tnum`–`nine.tnum` 변형 글리프 10개 추가 정제 (모두 동일 advance width) |
| Kerning | `kern` | 표준 kerning pair 정제 (AV, AT, To, Yo, 한+영 혼용 등) |
| Standard Ligatures | `liga` | fi, fl 정제 |

> **CRITICAL**: tnum은 이력서 컨텍스트의 핵심 가치 (연봉/날짜/KPI 자릿수 정렬). Default ON 활성.

---

## 3. Module 2 작업 명세 (이번 견적의 핵심)

### 3.1 정제할 글리프 (165자)

자세한 우선순위는 `docs/02-design/glyph-priority-latin.md` 참조.

| 카테고리 | 글리프 | 우선순위 | 마스터 |
|---------|--------|:--------:|:------:|
| Lowercase | a–z (26자) | P0 | Regular + Bold |
| Uppercase | A–Z (26자) | P0 | Regular + Bold |
| Numbers (proportional) | 0–9 (10자) | P0 | Regular + Bold |
| Numbers (tabular `.tnum`) | zero.tnum–nine.tnum (10자) | P0 | Regular + Bold |
| Punctuation | `. , : ; ' " ` ´ ' ' " " ( ) [ ] { } - – —` (18자) | P0 | Regular + Bold |
| Symbols | `! ? / \ % & @ # $ ₩ ¥ € + - = * < >` (17자) | P0 | Regular + Bold |
| Extended Symbols | `£ ¢ ± × ÷ ≤ ≥ ≠ ≈ † ‡` (10자) | P1 | Regular + Bold |
| Decorative | `§ ¶ © ® ™` (5자) | P2 (옵션) | Regular + Bold |

### 3.2 작업 일정 권고

| Sprint | 내용 | 일정 |
|--------|------|------|
| S1 | Lowercase a-z 정제 | Week 1 (5일) |
| S2 | Uppercase A-Z 정제 | Week 2 (5일) |
| S3 | Numbers + tnum variants | Week 3 (4일) |
| S4 | P0 Punctuation + Symbols | Week 4 (5일) |
| S5 (옵션) | P1 Extended Symbols | Week 5 (3일) |

**예상 총 일정**: P0만 4주, P0+P1 5주 (디자이너 1명 풀타임 기준)

### 3.3 시각 검증 산출물

각 Sprint 완료 시:
1. `.glyphs` 파일 commit (Git 또는 Dropbox)
2. specimen 페이지(`tests/specimen.html`) 스크린샷
3. 인쇄 품질 PDF (10pt-18pt 렌더링 확인)
4. 한국어 이력서 샘플(`tests/resume-test.html`) 스크린샷

---

## 4. 디자인 가이드라인

### 4.1 곡선 처리 (Min Sans 영감)
- **모서리 라운딩**: 20–40 UPM (글리프 크기에 비례 조정)
- **획 끝 처리**: ㄴ, ㄹ, ㅁ, ㅂ, ㅅ 등의 외곽 곡선을 부드럽게
- **획 대비**: 수직·수평 두께 거의 동일 (고른 무게감)

### 4.2 광학 보정
- **O / 0 / 정원**: 정원이 아닌 살짝 확장된 타원 (시각적 정원 느낌)
- **둥근 글자 베이스라인**: O, C, G 등은 baseline 아래로 약 5–10 UPM 확장
- **첨예한 끝**: V, A, W의 vertex는 약간 평탄화

### 4.3 한글 자모 (Module 3+에서 본격 작업)
- **counter 개방도**: ㅁ, ㅂ, ㅇ의 내부 공간이 작은 크기에서도 막히지 않게
- **받침 처리**: 받침 글자(ㄾ, ㄻ 등)가 10pt에서도 가독 가능
- **한·영 혼용**: 한글과 Latin의 시각적 무게감 일치

### 4.4 Pretendard 차이점 (의도적)
- ❌ Pretendard보다 더 기술적 / 첨예한 톤 ❌
- ✅ Pretendard보다 더 따뜻하고 친근한 톤 ✅
- ✅ 모서리 라운딩이 가시적으로 더 부드러움
- ✅ 작은 크기(10pt)에서 한글 자모 가독성 더 우수

---

## 5. 견적 요청 항목

다음 항목에 대한 견적을 회신해주세요.

### 5.1 작업 범위 견적

| Phase | 작업 | 견적 (KRW) | 일정 |
|-------|------|-----------|------|
| Module 2 (Latin 165자) | Regular + Bold 정제 | (작성) | (작성) |
| Module 3 (한글 500자) | Regular + Bold 정제 | (작성) | (작성) |
| Module 4 (한글 1,850자) | Regular + Bold 정제 | (작성) | (작성) |
| **Total** | v1.0까지 | (작성) | (작성) |

### 5.2 옵션 작업 견적

| 옵션 | 작업 | 견적 (KRW) | 일정 |
|------|------|-----------|------|
| 추가 마스터 | Light(300) 또는 ExtraBold(800) 마스터 추가 | (작성) | (작성) |
| Italic 스타일 | Latin Italic | (작성) | (작성) |
| 그리스/키릴 | 67자 확장 | (작성) | (작성) |

### 5.3 작업 조건
- 작업 형태: 풀타임 / 파트타임 (선택)
- 일주 작업 시간: ____시간
- 협업 도구: GitHub / Dropbox / Slack (선호 표기)
- 결제 방식: 마일스톤 (Phase별) / 월 단위 (선호 표기)
- 시작 가능 시점: ____년 ____월 ____일

### 5.4 포트폴리오 요청
- 이전에 작업한 한글/Latin 폰트 작업물 (3개 이상)
- 가능하면 OFL 또는 OSS 폰트 작업 경험
- Glyphs 3 사용 경험 연수

---

## 6. 평가 기준 (인크루트 내부)

| 기준 | 가중치 |
|------|:------:|
| 한글 폰트 디자인 경험 | 30% |
| Latin/숫자/기호 디자인 품질 | 20% |
| 일정 신뢰성 | 20% |
| 견적 합리성 | 15% |
| 의사소통 및 협업 능력 | 15% |

---

## 7. 협업 환경 안내

### 7.1 인크루트 측 지원
- ✅ Glyphs 소스 템플릿 (`sources/IncruitSans-Regular.glyphs`) — Regular + Bold 마스터 구조 + 104자 더미 글리프 사전 준비
- ✅ 빌드 자동화 스크립트 (`build/build.py`) — 디자이너는 .glyphs만 작업하면 OTF/TTF/WOFF2/VF 자동 생성
- ✅ GitHub Actions CI — push 시 자동 빌드
- ✅ 시각 검증 페이지 (`tests/specimen.html`, `tests/resume-test.html`) — 작업 결과 즉시 브라우저 확인 가능
- ✅ 글리프 사양 문서 (`docs/glyph-specifications.md`) — 메트릭, 곡선 가이드라인
- ✅ 의사결정 빠른 회신 (의장 직속 우선순위)

### 7.2 디자이너 책임
- `.glyphs` 파일 정기 커밋 (최소 주 1회)
- Sprint 완료 시 시각 검증 산출물 제출
- 인크루트 디자인 리뷰(주 1회 30분 미팅) 참여
- 마스터 간 호환성 유지 (interpolation 가능 상태)
- OFL 라이선스 준수 (외부 폰트 트레이싱 금지)

---

## 8. 회신 요청 정보

다음 정보를 회신 메일에 포함해주세요:

1. **포트폴리오 링크** (3개 이상)
2. **§5 견적표** (작성 완료)
3. **이력 / CV** (PDF)
4. **시작 가능 시점**
5. **Q&A** — 본 명세서 관련 질문 (있다면)
6. **참고 작업** — Pretendard 또는 Min Sans 작업 경험이 있다면 명시

회신 메일: `fonts@incruit.com`
회신 마감: **2026-05-09 (KST 23:59)**

---

## 9. 추가 안내

### 9.1 NDA
- 견적 검토 단계: 별도 NDA 없음 (본 명세서가 공개 가능 수준)
- 계약 후: 인크루트 표준 NDA 체결

### 9.2 결제
- 마일스톤 결제 권장: 각 Module 완료 시 30%/30%/40% 분할
- 또는 월 단위 결제 (협의 가능)
- 부가세 별도

### 9.3 IP 권리
- 작업물의 저작권은 OFL 1.1로 공개 (인크루트 + 디자이너 공동 명기)
- "Incruit Sans" 이름은 인크루트 reserved name (디자이너의 향후 modified version은 다른 이름으로 배포)

### 9.4 분쟁 해결
- 한국 상사중재원 중재 (필요 시)

---

## 10. 다음 단계

귀하의 견적 회신 후:

1. **인터뷰** (1주 내) — 30분 화상 미팅
2. **샘플 작업** (선택, 1주) — 글리프 5–10자 샘플 정제 후 평가
3. **계약 체결** — 표준 외주 계약서 + NDA
4. **킥오프 미팅** — 작업 환경 셋업, 첫 Sprint 정의

문의사항은 `fonts@incruit.com` 또는 직접 연락 부탁드립니다.

감사합니다.

— Incruit Corp.
