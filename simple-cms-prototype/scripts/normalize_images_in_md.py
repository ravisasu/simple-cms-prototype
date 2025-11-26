import re
from pathlib import Path

md_path = Path('Content') / 'articles' / 'Visual Studio Helper' / 'help-viewer-ultimate.md'

if not md_path.exists():
    raise SystemExit(f"Markdown file not found: {md_path}")

text = md_path.read_text(encoding='utf-8')

# Replace <img src="media/file" style="..." /> or <img src="media/file" /> with standard markdown ![](media/file)
pattern = re.compile(r'<img\s+src="(media/[^"]+)"(?:\s+style="[^"]*")?\s*/?>', flags=re.IGNORECASE)
new_text = pattern.sub(r'![](\1) ', text)

# Normalize blockquote + image: remove extra space after > if present
new_text = new_text.replace('>  ![]', '> ![]')

if new_text == text:
    print('No changes required')
else:
    md_path.write_text(new_text, encoding='utf-8')
    print(f'Updated: {md_path}')
