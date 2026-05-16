#!/usr/bin/env python3
"""
Bold 마스터 자동 생성 스크립트

Regular 마스터의 모든 글리프를 Bold 마스터로 복사합니다.
디자이너가 Glyphs 3에서 각 글리프의 획 두께를 조정합니다.

사용법:
    python build/setup_bold_master.py
"""

import json
import os
import shutil
from pathlib import Path
from copy import deepcopy


def setup_bold_master():
    """Regular 마스터 기반으로 Bold 마스터 생성"""

    glyphs_path = "sources/IncruitSans-Regular.glyphs"

    # 파일 존재 확인
    if not os.path.exists(glyphs_path):
        print(f"❌ 오류: {glyphs_path}를 찾을 수 없습니다.")
        print("   먼저 'python build/generate_glyphs_template.py'를 실행하세요.")
        return False

    print(f"📂 로드 중: {glyphs_path}")

    # 백업 생성
    backup_path = f"{glyphs_path}.backup"
    if not os.path.exists(backup_path):
        shutil.copy(glyphs_path, backup_path)
        print(f"💾 백업 생성: {backup_path}")

    # JSON 파일 로드
    try:
        with open(glyphs_path, 'r', encoding='utf-8') as f:
            font_data = json.load(f)
    except Exception as e:
        print(f"❌ 파일 로드 오류: {e}")
        return False

    # 1. Regular 마스터 찾기
    masters = font_data.get('fontMaster', [])
    regular_master = None
    regular_master_idx = None

    for idx, master in enumerate(masters):
        if master.get('customName') == 'Regular':
            regular_master = master
            regular_master_idx = idx
            break

    if not regular_master:
        print("❌ Regular 마스터를 찾을 수 없습니다.")
        return False

    print(f"✅ Regular 마스터 찾음: {regular_master.get('customName')}")

    # 2. Bold 마스터 이미 존재하는지 확인
    bold_master_exists = any(m.get('customName') == 'Bold' for m in masters)

    if bold_master_exists:
        print("⚠️  Bold 마스터가 이미 존재합니다.")
        response = input("덮어쓸까요? (y/n): ")
        if response.lower() != 'y':
            print("취소됨.")
            return False
        # Bold 마스터 제거
        font_data['fontMaster'] = [m for m in masters if m.get('customName') != 'Bold']
        print("✓ 기존 Bold 마스터 제거됨")
        masters = font_data['fontMaster']

    # 3. Bold 마스터 생성
    bold_master = deepcopy(regular_master)
    bold_master['customName'] = 'Bold'
    bold_master['id'] = f"bold-master-{len(masters)}"

    masters.append(bold_master)
    font_data['fontMaster'] = masters

    print(f"✅ Bold 마스터 생성: {bold_master['customName']}")

    # 4. 모든 글리프를 Bold 마스터에 복사
    glyphs = font_data.get('glyphs', [])
    glyph_count = 0
    bold_master_id = bold_master['id']
    regular_master_id = regular_master['id']

    for glyph in glyphs:
        # Regular 마스터에서 해당 글리프 찾기
        layers = glyph.get('layers', [])
        regular_layer = None

        for layer in layers:
            if layer.get('layerId') == regular_master_id:
                regular_layer = layer
                break

        if not regular_layer:
            continue

        # Bold 마스터용 레이어 생성 (Regular의 깊은 복사)
        bold_layer = deepcopy(regular_layer)
        bold_layer['layerId'] = bold_master_id

        # Glyph에 Bold 레이어 추가
        glyph['layers'].append(bold_layer)
        glyph_count += 1

    print(f"✅ {glyph_count}개 글리프를 Bold 마스터로 복사")

    # 5. 파일 저장
    try:
        with open(glyphs_path, 'w', encoding='utf-8') as f:
            json.dump(font_data, f, indent=2)
        print(f"💾 저장 완료: {glyphs_path}")
    except Exception as e:
        print(f"❌ 저장 오류: {e}")
        return False

    # 6. 완료 메시지
    print("\n" + "="*60)
    print("✅ Bold 마스터 설정 완료!")
    print("="*60)
    print("""
다음 단계:

1. Glyphs 3에서 파일 열기:
   open sources/IncruitSans-Regular.glyphs

2. Bold 마스터의 각 글리프 수정:
   - 획 두께를 80 UPM → 140 UPM으로 조정
   - 곡선 반지름을 적절히 확대 (정원성 유지)
   - docs/glyph-specifications.md 참조

3. 완료 후 빌드:
   python build/build.py
""")
    return True


if __name__ == "__main__":
    success = setup_bold_master()
    exit(0 if success else 1)
