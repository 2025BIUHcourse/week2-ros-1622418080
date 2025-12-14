import re
from pathlib import Path

md = Path('c:/Users/16224/Desktop/week2/team9_曾学阳_week2_final.md')
shots_dir = Path('c:/Users/16224/Desktop/week2/screenshots')

if not md.exists():
    print('Markdown file not found:', md)
    raise SystemExit(1)

text = md.read_text(encoding='utf-8')

pattern = re.compile(r'!\[[^\]]*\]\((screenshots?/[^)]+)\)')
matches = list(pattern.finditer(text))
print('Found', len(matches), 'image links to screenshots/ in markdown')

counter = 1
repl_text = text
for m in matches:
    new_name = f'screenshots/screenshot_{counter:02}.png'
    # replace only this specific occurrence
    start, end = m.span(1)
    repl_text = repl_text[:start] + new_name + repl_text[end:]
    counter += 1

md.write_text(repl_text, encoding='utf-8')
print('Rewrote', md, 'with', counter-1, 'screenshots referenced')
