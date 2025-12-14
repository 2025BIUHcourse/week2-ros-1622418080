import os
import re
import sys
from pathlib import Path

def ensure_pillow():
    try:
        from PIL import Image  # noqa: F401
    except Exception:
        print('Pillow not found, installing...')
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--user', 'Pillow'])


def main():
    ensure_pillow()
    from PIL import Image

    repo_root = Path(__file__).resolve().parents[1]
    screenshots_dir = repo_root / 'screenshots'
    md_file = repo_root / 'team9_曾学阳_week2_final.md'

    if not screenshots_dir.exists():
        print('screenshots/ folder not found at', screenshots_dir)
        return
    files = sorted([p for p in screenshots_dir.iterdir() if p.is_file()])
    print(f'Found {len(files)} files in', screenshots_dir)

    new_paths = []
    i = 1
    for p in files:
        try:
            img = Image.open(p)
        except Exception as e:
            print('Skipping non-image file', p, e)
            continue
        target_name = f'screenshot_{i:02}.png'
        target = screenshots_dir / target_name
        # convert and save as PNG
        rgb = img.convert('RGBA')
        rgb.save(target, 'PNG')
        new_paths.append(target_name)
        print('Saved', target_name)
        # remove original file if different
        try:
            if p.name != target_name:
                p.unlink()
        except Exception as e:
            print('Could not remove', p, e)
        i += 1

    # Update markdown file references to .png and to screenshots/ prefix
    if md_file.exists():
        text = md_file.read_text(encoding='utf-8')
        # replace occurrences like screenshots/screenshot_01.jpg or screenshot/screenshot_14.png etc.
        text2 = re.sub(r"(screenshots?/screenshot_\d{2})\\.[a-zA-Z0-9]+", r"\1.png", text)
        # Also ensure the names use two-digit zero padding (already are)
        md_file.write_text(text2, encoding='utf-8')
        print('Updated markdown links to .png in', md_file)
    else:
        print('Markdown file not found at', md_file)

if __name__ == '__main__':
    main()
