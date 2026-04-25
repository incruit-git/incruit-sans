# Incruit Sans — Glyphs 3 커스텀 가이드

> Pretendard 기반 한글 폰트를 Glyphs 3에서 인크루트 브랜드에 맞게 부분 수정하는 절차
> 2026-04-25

---

## 0. 왜 Glyphs 3인가

- **Pretendard 원본 .glyphspackage 제공**: `git clone orioncactus/pretendard` → `src/Pretendard.glyphspackage` 그대로 열림
- **AI 협업 가능**: 의장이 Glyphs UI에서 디자인, Claude가 일괄 변환/배치 수정 자동화
- **OFL 라이선스 호환**: 수정 → "Incruit Sans"로 export 후 자유롭게 사용

대안: FontForge (무료, UI 거침), Robofont ($499, 더 비쌈), Birdfont (무료, 한글 약함). **Glyphs 3가 한글 폰트 작업 표준.**

---

## 1. 환경 준비 (의장 직접)

### 1.1 Glyphs 3 구매 + 설치
- 가격: €299 (약 44만원, 1회 결제, 평생 사용)
- 다운로드: https://glyphsapp.com/buy
- 14일 trial 가능 — 먼저 trial 후 결정 권장
- macOS Sonoma 14+ 필요 (의장 Mac 사양 충분)

### 1.2 Pretendard 소스 받기
```bash
cd ~/Projects
git clone https://github.com/orioncactus/pretendard
cd pretendard
ls src/  # Pretendard.glyphspackage 확인
```

### 1.3 Glyphs에서 열기
```bash
open src/Pretendard.glyphspackage
```
→ Glyphs 3가 .glyphspackage 디렉토리를 인식해서 11,172자 한글 + 525자 라틴 + 9,990자 한자 + ... 모두 로드

---

## 2. Claude 협업 워크플로

### 2.1 두 가지 방식

**A. UI 작업 → Claude 자동화** (의장 → Claude)
1. 의장이 글리프 1개 디자인 (예: '인' 자의 ㅣ 길이 조정)
2. Glyphs에서 .glyphspackage 저장
3. Claude에게 "이 변경을 다른 글자에도 일관되게 적용해줘"
4. Claude가 glyphsLib으로 .glyphspackage 직접 편집 → 일괄 변환
5. 의장이 Glyphs에서 결과 확인

**B. Claude 분석 → UI 검수** (Claude → 의장)
1. Claude가 자모 구조 분석, 변경 제안 작성
2. Claude가 .glyphspackage에 직접 적용 (스크립트로)
3. 의장이 Glyphs UI에서 시각 검수, 미세 조정
4. 저장 → export

### 2.2 Claude의 한계 명확

| 가능 ✓ | 불가능 ✗ |
|---|---|
| .glyphspackage 텍스트 편집 (좌표, 메타) | 베지어 곡선 시각 디자인 |
| glyphsLib으로 글리프 일괄 변환 | "이 곡선이 더 예쁜가" 판단 |
| 빌드/내보내기 자동화 | UI 클릭, 메뉴 조작 |
| 자모 합성 규칙 적용 | 화면 보고 즉석 미세조정 |
| 패스 좌표 일괄 변환 (스케일/이동) | 디자이너 안목 |

→ **분업 권장**: 의장은 Glyphs UI에서 의도/방향 정함, Claude가 노가다 처리.

---

## 3. 인크루트 커스터마이징 시나리오

### 3.1 Tier 1: 핵심 BI 단어 강화 (1주)

**목표**: 인크루트 자주 쓰는 단어들이 시각적으로 더 인크루트답게

**대상 글자 (약 50자)**:
- 회사명: 인 크 루 트
- 핵심 명사: 채 용 이 력 서 공 고 면 접 회 사 직 무 경 력 연 봉
- 영문: I n c r u i t (대소문자 14자)
- 숫자: 0~9 (10자, 채용공고 번호 표시)

**작업**:
1. 의장 또는 디자이너가 50자에 대해 BI 강화 (예: 더 둥글게, 더 modern하게)
2. Claude가 같은 자모를 가진 다른 글자에도 일관성 적용
   - 예: '인'의 'ㅇ'을 둥글게 변경 → '안', '온', '운' 등 13자에 동일 변환

**결과**: Incruit Sans v0.5

### 3.2 Tier 2: 자모 67자 재디자인 (1개월)

**목표**: 인크루트만의 한글 자모 시스템 (탈네모틀)

**대상**: 초성 19자 + 중성 21자 + 종성 27자 = 67 자모

**작업**:
1. 디자이너가 자모 67자 디자인 (Glyphs)
2. Claude가 11,172자 한글 자동 합성 (자모 조합 규칙)
3. 의장 검수 → 어색한 글자만 수동 보정

**결과**: Incruit Sans v1.0 (진짜 자체 폰트)

### 3.3 Tier 3: 굵기/너비 변형 (3개월)

- 9 weights → Variable Font (단일 파일)
- Condensed/Wide 변형 추가
- 한글-라틴 페어링 미세 조정 (커닝)

**결과**: Incruit Sans v2.0 (production 완성품)

---

## 4. Tier 1 실전 예시

### 4.1 시나리오: '인' 자의 'ㅇ'을 더 둥글게

**의장 작업 (Glyphs UI)**:
1. Glyphs에서 '인' 글리프 더블클릭
2. 'ㅇ' 부분 베지어 곡선 조정 (더 정원에 가깝게)
3. ⌘S 저장

**Claude 자동화 (요청 시)**:
```
"방금 '인' 자의 ㅇ 부분 변경한 걸 다음 글자에도 적용해줘:
안 어 여 오 요 우 유 으 이 (ㅇ + 모음 시작 글자)
완 원 윤 ... (ㅇ 받침 없음)
인 안 언 온 ... (ㄴ 받침 있음)
영 양 용 ... (ㅇ 받침)
"
```

Claude가 할 일:
1. .glyphspackage에서 '인' 글리프의 'ㅇ' 컴포넌트 좌표 추출
2. 'ㅇ' 컴포넌트를 사용하는 다른 글자 식별 (Glyphs는 컴포넌트 시스템 사용)
3. 각 글자의 'ㅇ' 컴포넌트 위치 보정 (글자별 크기/위치 다름)
4. .glyphspackage 저장
5. 변경 사항 보고 ("23개 글자에 적용 완료")

의장이 Glyphs에서 다시 열어 일괄 검수.

### 4.2 디자이너 협업 시 추천 프로세스

```
디자이너 (Glyphs UI 디자인)
   ↓ .glyphspackage commit
GitHub 리포지토리
   ↓ pull
의장 + Claude (협업)
   ↓ "이 자모 변경을 ㄴ ㅁ ㄹ 받침 글자에도 적용해줘"
Claude (.glyphspackage 자동 편집)
   ↓ commit
디자이너 (검수, 미세조정)
   ↓ 합의된 버전
Build → OTF/TTF/WOFF2
   ↓
인크루트 서비스 적용
```

---

## 5. Glyphs 3 학습 자료

### 5.1 공식
- [Glyphs Tutorials](https://glyphsapp.com/learn) — 영문, 한글 자모 합성 튜토리얼 별도
- [Creating a Hangeul Font](https://glyphsapp.com/learn/creating-a-hangeul-font) — 11,172자 합성 공식 가이드
- [Components and Substitution](https://glyphsapp.com/learn/components) — 자모 컴포넌트 시스템

### 5.2 한국 자료
- 산돌커뮤니케이션 블로그 (Glyphs 한글 작업법, 정성껏 쓴 글 다수)
- AG타이포그라피 인스타그램 (실무 팁)
- 폰트클럽 (한글 폰트 디자이너 커뮤니티)

### 5.3 주요 단축키
| 단축키 | 동작 |
|---|---|
| ⌘+숫자 | weight master 전환 (Thin~Black) |
| ⌘E | 폰트 export (OTF/TTF) |
| F | 글리프 채우기 미리보기 토글 |
| Space | 텍스트 모드 (실제 사용해보기) |
| ⌥⌘↑/↓ | 글리프 고도 ±10 |

---

## 6. 자주 묻는 질문

### Q. Glyphs 안 사고 무료로 가능?
- **FontForge** (무료) — UI 거칠고 한글 작업 비효율적이지만 가능
- **glyphsLib** (Python) — 의장이 GUI 안 쓰고 Claude로만 .glyphspackage 편집 가능 (완전 코드 기반)
- 디자인 작업이 거의 없고 변환만 한다면 glyphsLib + Claude로 충분

### Q. 디자이너 어디서 구하나?
- 인크루트 사내 디자인팀 (있다면 가장 좋음)
- AG타이포 / 산돌 / 윤디자인 외주 (한글 폰트 디자이너, 시간당 5~15만원)
- 비핸스/노트폴리오 프리랜서 검색

### Q. 작업 후 .glyphspackage는 어디 두나?
```
incruit-sans/
├── source/
│   ├── pretendard-fork/          # git clone (변경하지 말고 reference)
│   └── IncruitSans.glyphspackage # 인크루트 자체 작업 사본
└── build/
    └── *.otf                     # Glyphs export 결과
```
- `IncruitSans.glyphspackage`를 git LFS로 인크루트 사내 저장소에 보관
- 매 커밋마다 export → build/ 갱신

### Q. 의장이 직접 디자인 가능?
- 한글 폰트 디자인은 학습 곡선 가파름 (1자모도 잘 디자인하려면 수개월 훈련)
- 권장: **방향성만 의장이 정하고, 디자이너 또는 Claude가 실행**
- 의장 적합한 역할: BI 콘셉트 결정, 검수, 핵심 단어 시각 톤 결정

---

## 7. 의사결정 체크리스트

Glyphs 3 구매 전 확인:

- [ ] **Tier 1 작업 명확한가?** (어떤 50자, 어떻게 변형할지 BI 가이드 있나)
- [ ] **디자이너 협업 가능한가?** (사내 또는 외주)
- [ ] **시간 투자 가능한가?** (Tier 1만 해도 디자이너 1주, 의장 검수 시간)
- [ ] **인크루트 BI 자체 정리 됐나?** (BI-GUIDE.md 작성/승인 필요)

위 4개 모두 ✓면 구매.

만약 모두 안 되어 있고 "그냥 시도해보고 싶다"면 → **14일 trial 먼저, Tier 1 안 하고 그냥 학습용으로**.

---

## 8. 결론

**Glyphs 3 = 직접 손대고 싶다면 사야 하고, AI 협업으로 충분하다면 안 사도 됨.**

- **사야 함**: 인크루트 자체 폰트를 진지하게 자산화할 의도 + 디자이너 협업 가능 → ★★★★★
- **사지 마**: 단순 합성/변형은 이미 완료, 더 깊은 디자인 변경 의향 없음 → ★

지금 시점(v0.2 합성 완료)에서:
1. **v0.2를 실제 인크루트 화면에 1주 적용해보고**
2. **인크루트 BI 가이드 v1.0 작성하고** (BI-GUIDE.md 보완)
3. **그래도 더 손대고 싶으면 Glyphs 3 구매**

이 순서가 가장 합리적.
