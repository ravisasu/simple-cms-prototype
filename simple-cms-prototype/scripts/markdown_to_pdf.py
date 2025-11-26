import os
import sys
from markdown import markdown
from xhtml2pdf import pisa

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Default files to convert if no arguments provided
DEFAULT_FILES = [
    (os.path.join(ROOT, 'Author-QuickStart.md'), os.path.join(ROOT, 'Author-QuickStart.pdf')),
    (os.path.join(ROOT, 'Demo-cheatsheet.md'), os.path.join(ROOT, 'Demo-cheatsheet.pdf')),
]

CSS = '''
body { font-family: DejaVu Sans, Arial, sans-serif; margin: 1in; font-size: 12pt; }
h1 { font-size: 20pt; margin-top: 0.1in; }
h2 { font-size: 16pt; }
pre, code { font-family: monospace; background:#f7f7f7; padding:4px; }
img { max-width: 100%; }
'''


def md_to_pdf(md_path, pdf_path):
    if not os.path.exists(md_path):
        print(f"SKIP: source not found: {md_path}")
        return False
    with open(md_path, 'r', encoding='utf-8') as f:
        md = f.read()
    html_body = markdown(md, extensions=['extra', 'tables', 'toc'])
    # Ensure image references that are relative to the markdown file directory
    # resolve correctly when converting to PDF. Replace src="media/..." with
    # an absolute file:// path so pisa can load them regardless of cwd.
    md_dir = os.path.dirname(md_path)
    if md_dir:
        # normalize path for file URLs on Windows
        file_prefix = 'file:///' + md_dir.replace('\\', '/') + '/'
        html_body = html_body.replace('src="media/', f'src="{file_prefix}media/')

        # Convert local image file references to data URIs so xhtml2pdf can embed them
        import re, base64

        def _embed_file(match):
            src = match.group(1)
            # strip file:// if present
            path = src
            if path.startswith('file:///'):
                # convert file:///C:/... to C:/...
                path = path[8:] if path.startswith('file:///') and path[7] == '/' else path[8:]
                # normalize leading slash if any
                if path.startswith('/') and ':' in path[:3]:
                    path = path[1:]
            path = path.replace('/', os.sep)
            if not os.path.exists(path):
                return match.group(0)  # leave unchanged
            ext = os.path.splitext(path)[1].lower().lstrip('.')
            try:
                with open(path, 'rb') as f:
                    data = f.read()
                b64 = base64.b64encode(data).decode('ascii')
                mime = 'image/png' if ext == 'png' else ('image/jpeg' if ext in ('jpg','jpeg') else f'image/{ext}')
                return f'src="data:{mime};base64,{b64}"'
            except Exception:
                return match.group(0)

        html_body = re.sub(r'src="(file:///[^"]+\.(?:png|jpg|jpeg|gif))"', _embed_file, html_body, flags=re.IGNORECASE)
    html = f"""<!doctype html>
<html>
<head>
<meta charset=\"utf-8\">
<style>{CSS}</style>
</head>
<body>
{html_body}
</body>
</html>
"""
    # ensure output directory exists
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    with open(pdf_path, 'wb') as out:
        pisa_status = pisa.CreatePDF(html, dest=out)
    return not pisa_status.err


if __name__ == '__main__':
    # Parse command line arguments
    if len(sys.argv) > 1:
        # Convert files specified on command line
        files_to_convert = []
        for arg in sys.argv[1:]:
            if arg.startswith('--'):
                continue  # Skip flags for now

            # Handle relative or absolute paths
            if os.path.isabs(arg):
                md_path = arg
            else:
                md_path = os.path.join(ROOT, arg)

            # Generate PDF path
            if md_path.endswith('.md'):
                pdf_path = md_path[:-3] + '.pdf'
            else:
                pdf_path = md_path + '.pdf'

            files_to_convert.append((md_path, pdf_path))
    else:
        # No arguments: use default files
        files_to_convert = DEFAULT_FILES

    ok_any = False
    for md, pdf in files_to_convert:
        print(f"Converting: {os.path.basename(md)} -> {os.path.basename(pdf)}")
        ok = md_to_pdf(md, pdf)
        if ok:
            print(f"WROTE: {pdf}")
            ok_any = True
        else:
            print(f"FAILED: {md} -> {pdf}")
    if not ok_any:
        print("No PDFs were produced. Check source files and dependencies.")
        sys.exit(2)
    print("Done.")
