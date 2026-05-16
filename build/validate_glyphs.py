#!/usr/bin/env python3
"""
Glyphs 파일 검증 스크립트

생성된 IncruitSans-Regular.glyphs 파일의 메트릭, 글리프, 마스터 설정을 검증합니다.

사용법:
    python build/validate_glyphs.py
"""

import os
import sys
import json


def validate_glyphs():
    """Glyphs 파일 검증"""

    glyphs_path = "sources/IncruitSans-Regular.glyphs"

    # 파일 존재 확인
    if not os.path.exists(glyphs_path):
        print(f"❌ 오류: {glyphs_path}를 찾을 수 없습니다.")
        print("   먼저 'python build/generate_glyphs_template.py'를 실행하세요.")
        return False

    print(f"📂 검증 중: {glyphs_path}\n")

    # JSON 파일 로드
    try:
        with open(glyphs_path, 'r', encoding='utf-8') as f:
            font_data = json.load(f)
    except Exception as e:
        print(f"❌ 파일 로드 오류: {e}")
        return False

    # 1. 기본 정보
    print("=" * 60)
    print("📋 폰트 기본 정보")
    print("=" * 60)
    print(f"패밀리명: {font_data.get('.appVersion', 'N/A')}")
    print(f"포스트스크립트명: {font_data.get('fontMaster', [{}])[0].get('customName', 'N/A')}")
    print(f"유니버설 디자인 모듈(UPM): {font_data.get('unitsPerEm', 1000)}")
    print()

    # 2. 마스터 확인
    print("=" * 60)
    print("🎭 마스터 구성")
    print("=" * 60)

    masters = font_data.get('fontMaster', [])
    print(f"마스터 개수: {len(masters)}")

    master_names = []
    for i, master in enumerate(masters):
        name = master.get('customName', 'Unknown')
        master_id = master.get('id', 'N/A')
        print(f"  [{i}] {name} (ID: {master_id[:16]}...)")
        master_names.append(name)

    # Regular와 Bold가 모두 있는지 확인
    has_regular = "Regular" in master_names
    has_bold = "Bold" in master_names

    if has_regular and has_bold:
        print("✅ Regular + Bold 마스터 완벽!")
    elif has_regular:
        print("⚠️  Regular만 있습니다. Bold 마스터를 추가하려면:")
        print("   python build/setup_bold_master.py")
    else:
        print("❌ Regular 마스터가 없습니다!")

    print()

    # 3. 글리프 통계
    print("=" * 60)
    print("📊 글리프 통계")
    print("=" * 60)

    glyphs = font_data.get('glyphs', [])
    total_glyphs = len(glyphs)
    print(f"총 글리프 수: {total_glyphs}")

    # 마스터별 글리프 적용 상태
    for master in masters:
        master_id = master.get('id')
        glyph_count = sum(
            1 for g in glyphs
            if any(layer.get('layerId') == master_id for layer in g.get('layers', []))
        )
        name = master.get('customName', 'Unknown')
        print(f"  • {name}: {glyph_count}/{total_glyphs} 글리프")

    print()

    # 4. 최종 상태
    print("=" * 60)
    print("✅ 검증 완료")
    print("=" * 60)

    if has_regular:
        print("""
다음 단계:

1. Glyphs 3에서 파일 열기:
   open sources/IncruitSans-Regular.glyphs

2. 각 글리프 수정 (docs/glyph-specifications.md 참조):
   - 획 두께, 곡선, 라운딩 조정
   - 10-18pt에서 렌더링 확인

3. Bold 마스터 추가 (아직 안 했으면):
   python build/setup_bold_master.py

4. 빌드:
   python build/build.py
""")
        return True
    else:
        print("\n⚠️  Regular 마스터가 없습니다.")
        return False


if __name__ == "__main__":
    success = validate_glyphs()
    sys.exit(0 if success else 1)
