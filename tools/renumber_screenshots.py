#!/usr/bin/env python3
import re
import shutil
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
MD = ROOT / 'team9_敬钰娟_week2_final.md'
SS = ROOT / 'screenshots'

def extract_placeholders(md_text):
    # match occurrences of screenshots/filename.png anywhere (more tolerant)
    pattern = re.compile(r'screenshots/(screenshot_\d{2,3}\.png)')
    seen = []
    for m in pattern.finditer(md_text):
        name = m.group(1)
        if name not in seen:
            seen.append(name)
    return seen

def main():
    if not MD.exists():
        print('Markdown not found:', MD)
        return
    if not SS.exists():
        print('Screenshots dir not found:', SS)
        return

    text = MD.read_text(encoding='utf-8')
    placeholders = extract_placeholders(text)
    if not placeholders:
        print('No screenshot placeholders found in markdown.')
        return

    print(f'Found {len(placeholders)} unique placeholders in markdown.')

    pngs = sorted([p for p in SS.iterdir() if p.is_file() and p.suffix.lower()=='.png'])
    print(f'Found {len(pngs)} png files in screenshots/.')

    # backup existing images
    bakdir = SS / f'backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    bakdir.mkdir(exist_ok=True)
    for p in pngs:
        shutil.copy2(p, bakdir/p.name)
    print('Backed up existing pngs to', bakdir.name)

    # prepare mapping: target placeholders ordered as they appear
    targets = placeholders

    # If fewer pngs than targets, we'll reuse last png for remaining
    if len(pngs) == 0:
        print('No png files to rename; aborting.')
        return

    operations = []
    for i, tgt in enumerate(targets):
        if i < len(pngs):
            src = pngs[i]
        else:
            src = pngs[-1]
        operations.append((src, SS / tgt))

    # To avoid name collisions, move files to temp names first
    temp_names = []
    for idx, (src, dst) in enumerate(operations):
        temp = SS / f'.tmp_ren_{idx:03d}.png'
        shutil.copy2(src, temp)
        temp_names.append((temp, dst))

    # remove original pngs (we have backup)
    for p in pngs:
        try:
            p.unlink()
        except Exception:
            pass

    # move temps to final targets
    for temp, dst in temp_names:
        if dst.exists():
            dst.unlink()
        temp.replace(dst)
        print(f'Created {dst.name}')

    print('Renumbering complete.')

if __name__ == '__main__':
    main()
