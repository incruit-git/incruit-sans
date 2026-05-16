#!/usr/bin/env python3
"""
Incruit Sans 폰트 빌드 스크립트

Glyphs 소스 파일(.glyphs)을 OTF, TTF, WOFF2 형식으로 컴파일합니다.

사용법:
    python build/build.py [--clean] [--verbose]

옵션:
    --clean     빌드 전에 fonts/ 디렉토리 정리
    --verbose   상세 로그 출력
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def ensure_directory(path):
    """디렉토리 생성"""
    Path(path).mkdir(parents=True, exist_ok=True)


def run_command(cmd, description="", verbose=False):
    """명령어 실행 및 에러 처리"""
    if verbose:
        print(f"  $ {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd, capture_output=not verbose, text=True, check=True
        )
        if not verbose and result.stdout:
            print(f"    {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 실패")
        if e.stderr:
            print(f"   {e.stderr}")
        return False
    except FileNotFoundError:
        print(f"❌ {description}: 명령어를 찾을 수 없습니다 ({cmd[0]})")
        return False


def build_fonts(clean=False, verbose=False):
    """폰트 빌드"""

    glyphs_path = "sources/IncruitSans-Regular.glyphs"

    # 소스 파일 확인
    if not os.path.exists(glyphs_path):
        print(f"❌ 오류: {glyphs_path}를 찾을 수 없습니다.")
        print("   먼저 'python build/generate_glyphs_template.py'를 실행하세요.")
        return False

    print("🔨 Incruit Sans 폰트 빌드 시작\n")

    # 빌드 디렉토리 정리
    if clean:
        for build_dir in ["fonts/otf", "fonts/ttf", "fonts/webfonts"]:
            if os.path.exists(build_dir):
                shutil.rmtree(build_dir)
                print(f"🗑️  {build_dir} 정리됨")

    # 빌드 디렉토리 생성
    ensure_directory("fonts/otf")
    ensure_directory("fonts/ttf")
    ensure_directory("fonts/webfonts")

    # 1. OTF 빌드 (모든 인스턴스)
    print("\n📦 OTF 빌드 중 (모든 인스턴스)...")
    if not run_command(
        ["fontmake", "-g", glyphs_path, "-o", "otf", "-i", "--output-dir", "fonts/otf"],
        "OTF 빌드",
        verbose=verbose,
    ):
        return False
    print("✅ OTF 빌드 완료")

    # 2. TTF 빌드 (모든 인스턴스)
    print("\n📦 TTF 빌드 중 (모든 인스턴스)...")
    if not run_command(
        ["fontmake", "-g", glyphs_path, "-o", "ttf", "-i", "--output-dir", "fonts/ttf"],
        "TTF 빌드",
        verbose=verbose,
    ):
        return False
    print("✅ TTF 빌드 완료")

    # 2.5. Variable Font 빌드 (단일 VF 파일)
    print("\n📦 Variable Font 빌드 중...")
    if not run_command(
        [
            "fontmake", "-g", glyphs_path, "-o", "variable",
            "--output-path", "fonts/IncruitSans-VF.ttf",
        ],
        "Variable Font 빌드",
        verbose=verbose,
    ):
        print("⚠️  Variable Font 빌드 건너뜀 (정적 인스턴스만 생성)")
    else:
        print("✅ Variable Font 빌드 완료")

    # 3. WOFF2 생성
    print("\n🔗 WOFF2 변환 중...")
    ttf_files = list(Path("fonts/ttf").glob("*.ttf"))

    if not ttf_files:
        print("⚠️  TTF 파일을 찾을 수 없습니다.")
        return False

    for ttf_file in ttf_files:
        woff2_path = f"fonts/webfonts/{ttf_file.stem}.woff2"
        if not run_command(
            [
                "python",
                "-m",
                "fontTools.ttLib.woff2_compress",
                str(ttf_file),
                "-o",
                woff2_path,
            ],
            f"WOFF2 변환 ({ttf_file.name})",
            verbose=verbose,
        ):
            return False
        print(f"  ✅ {ttf_file.name} → {Path(woff2_path).name}")

    print("✅ WOFF2 변환 완료")

    # 4. 빌드 결과 요약
    print("\n" + "=" * 60)
    print("✅ 빌드 성공!")
    print("=" * 60)

    print("\n📊 생성된 파일:")

    for fmt, path in [
        ("OTF", "fonts/otf"),
        ("TTF", "fonts/ttf"),
        ("WOFF2", "fonts/webfonts"),
    ]:
        files = list(Path(path).glob("*"))
        if files:
            print(f"  {fmt}:")
            for f in sorted(files):
                size_kb = f.stat().st_size / 1024
                print(f"    • {f.name} ({size_kb:.1f} KB)")

    # 5. 다음 단계
    print("\n" + "=" * 60)
    print("📋 다음 단계")
    print("=" * 60)
    print("""
1. HTML 스펙시멘 확인:
   python -m http.server 8000
   → http://localhost:8000/tests/specimen.html

2. 이력서 렌더링 테스트:
   → http://localhost:8000/tests/resume-test.html

참고: OTF/TTF는 로컬 설치용, WOFF2는 웹용입니다.
""")

    return True


if __name__ == "__main__":
    # 인자 파싱
    clean = "--clean" in sys.argv
    verbose = "--verbose" in sys.argv

    if not build_fonts(clean=clean, verbose=verbose):
        sys.exit(1)

    print("\n✅ 모든 단계 완료!")
    sys.exit(0)
