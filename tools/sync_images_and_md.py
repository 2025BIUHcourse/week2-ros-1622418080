#!/usr/bin/env python3
import re
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MD = ROOT / 'team9_曾学阳_week2_final.md'
SS_DIR = ROOT / 'screenshots'

def list_image_links(md_text):
    # match markdown image links referencing screenshot or screenshots folders
    pattern = re.compile(r"!\[[^\]]*\]\((?:screenshot|screenshots)/([^\)]+)\)")
    return pattern.findall(md_text)

def replace_image_links(md_text, new_names):
    # replace each image link in order with the next new_name
    def repl(match):
        repl.idx += 1
        idx = min(repl.idx - 1, len(new_names)-1)
        return f"![{match.group(1)}](screenshots/{new_names[idx]})"
    repl.idx = 0
    pattern = re.compile(r"!\[([^\]]*)\]\((?:screenshot|screenshots)/([^\)]+)\)")
    return pattern.sub(repl, md_text)

def main():
    if not MD.exists():
        print('Markdown file not found:', MD)
        return
    if not SS_DIR.exists():
        print('Screenshots directory not found:', SS_DIR)
        return

    # Read markdown and find occurrences
    text = MD.read_text(encoding='utf-8')
    links = list_image_links(text)
    print(f'Found {len(links)} image links in markdown.')

    # Find png files in screenshots dir
    pngs = sorted([p for p in SS_DIR.iterdir() if p.is_file() and p.suffix.lower() == '.png'])
    print(f'Found {len(pngs)} png files in screenshots/.')
    if len(pngs) == 0:
        print('No PNGs to rename; aborting.')
        return

    # Back up markdown
    bak = MD.with_suffix('.md.bak')
    if not bak.exists():
        shutil.copy2(MD, bak)
        print('Backed up markdown to', bak.name)

    # Rename pngs to sequential names
    new_names = []
    for i, src in enumerate(pngs, start=1):
        new_name = f'screenshot_{i:02d}.png'
        dst = SS_DIR / new_name
        if src.resolve() == dst.resolve():
            # already correct name
            new_names.append(new_name)
            continue
        # avoid overwrite: if dst exists, pick next available index
        if dst.exists():
            # find next unused index
            j = i
            while True:
                j += 1
                candidate = SS_DIR / f'screenshot_{j:02d}.png'
                if not candidate.exists():
                    dst = candidate
                    break
        shutil.move(str(src), str(dst))
        new_names.append(dst.name)
        print(f'Renamed {src.name} -> {dst.name}')

    # If there are fewer pngs than image links, we'll reuse the last png for remaining links
    if len(new_names) == 0:
        print('No renamed files produced; aborting.')
        return

    # Now replace links in markdown in order of appearance
    new_text = replace_image_links(text, new_names)
    MD.write_text(new_text, encoding='utf-8')
    print('Updated markdown with new image filenames (in-order mapping).')
    print('If the mapping is not correct, restore the markdown from', bak.name)

if __name__ == '__main__':
    main()
