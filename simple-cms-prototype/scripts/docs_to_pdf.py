import os
import sys
from markdown import markdown
from xhtml2pdf import pisa

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FILES = [
    os.path.join(ROOT, 'Author-QuickStart.md'),
    os.path.join(ROOT, 'AUTHOR-CHECKLIST.md'),
    os.path.join(ROOT, 'WORKFLOW.md'),
]
OUT = os.path.join(ROOT, 'authoring-workflow.pdf')

CSS = '''
body { font-family: DejaVu Sans, Arial, sans-serif; margin: 1in; font-size: 11pt; }
h1 { font-size: 18pt; margin-top: 0.1in; }
h2 { font-size: 14pt; }
pre, code { font-family: monospace; background:#f7f7f7; padding:4px; }
img { max-width: 100%; }
.section-break { page-break-after: always; }
'''


def build_html(parts):
    joined = '\n\n<div class="section-break"></div>\n\n'.join(parts)
    html = f"""<!doctype html>
<html>
<head>
<meta charset=\"utf-8\">
<style>{CSS}</style>
</head>
<body>
{joined}
</body>
</html>
"""
    return html


def md_file_to_html(path):
    with open(path, 'r', encoding='utf-8') as f:
        md = f.read()
    return markdown(md, extensions=['extra', 'tables', 'toc'])


def create_pdf(html, out_path):
    with open(out_path, 'wb') as out:
        pisa_status = pisa.CreatePDF(html, dest=out)
    return not pisa_status.err


if __name__ == '__main__':
    parts = []
    for p in FILES:
        if not os.path.exists(p):
            print(f"Warning: source not found, skipping: {p}")
            continue
        print(f"Including: {os.path.basename(p)}")
        parts.append(md_file_to_html(p))

    if not parts:
        print("No source files were found. Exiting.")
        sys.exit(2)

    html = build_html(parts)
    ok = create_pdf(html, OUT)
    if ok:
        print(f"WROTE: {OUT}")
    else:
        print("PDF generation failed")
        sys.exit(1)
