import re
from pathlib import Path

md_path = Path('c:/Users/16224/Desktop/week2/team9_曾学阳_week2_final.md')
shots_dir = Path('c:/Users/16224/Desktop/week2/screenshots')

if not md_path.exists():
    print('Markdown not found:', md_path)
    raise SystemExit(1)

png_files = sorted([p.name for p in shots_dir.iterdir() if p.is_file() and p.suffix.lower()=='.png'])
if not png_files:
    print('No PNG files found in', shots_dir)
    raise SystemExit(1)

text = md_path.read_text(encoding='utf-8')
pattern = re.compile(r'!\[[^\]]*\]\((screenshots?/[^)]+)\)')
matches = list(pattern.finditer(text))
print('Found', len(matches), 'image links;', len(png_files), 'png files available')

out = text
for idx, m in enumerate(matches):
    if idx < len(png_files):
        new = f'screenshots/{png_files[idx]}'
    else:
        new = f'screenshots/{png_files[-1]}'
    start, end = m.span(1)
    out = out[:start] + new + out[end:]

md_path.write_text(out, encoding='utf-8')
print('Updated markdown to reference available PNG files (reused last for extras)')
