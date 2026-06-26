"""
build/web/ 산출물 일괄 생성 — 9 weights OTF + VF TTF → woff + woff2

실행: source venv/bin/activate && python3 build/build_web_fonts.py
"""
from pathlib import Path
from fontTools.ttLib import TTFont

ROOT = Path(__file__).parent.parent
SRC = ROOT / 'build'
DEST = ROOT / 'build' / 'web'
DEST.mkdir(parents=True, exist_ok=True)

WEIGHTS = ['Thin', 'ExtraLight', 'Light', 'Regular', 'Medium',
           'SemiBold', 'Bold', 'ExtraBold', 'Black']

def convert(src_path: Path, dest_dir: Path, base_name: str):
    if not src_path.exists():
        print(f"  SKIP {src_path.name}: not found")
        return 0
    count = 0
    for flavor in ('woff', 'woff2'):
        font = TTFont(str(src_path))
        font.flavor = flavor
        out = dest_dir / f'{base_name}.{flavor}'
        font.save(str(out))
        size_kb = out.stat().st_size // 1024
        print(f"  ✓ {out.name:42s}  {size_kb} KB")
        count += 1
    return count

print(f"Source: {SRC}")
print(f"Output: {DEST}\n")

total = 0
print("[9 weights OTF → woff/woff2]")
for w in WEIGHTS:
    total += convert(SRC / f'IncruitSans-{w}.otf', DEST, f'IncruitSans-{w}')

print("\n[VF TTF → woff/woff2]")
total += convert(SRC / 'IncruitSans-VF.ttf', DEST, 'IncruitSans-VF')

print(f"\nDone. Generated {total} files in {DEST}")
