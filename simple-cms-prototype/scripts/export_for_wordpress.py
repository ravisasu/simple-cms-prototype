#!/usr/bin/env python3
"""
export_for_wordpress.py

Converts a markdown file into:
 - a self-contained HTML file with images embedded as data URIs
 - a minimal WordPress WXR XML file with the post content (images embedded in the HTML)

Usage: python scripts/export_for_wordpress.py path/to/article.md

The resulting files will be saved next to the source markdown.
"""
import sys
import os
from pathlib import Path
import base64
import re
from markdown import markdown
import datetime
import xml.sax.saxutils as sax


def md_to_html_with_embedded_images(md_path: Path) -> str:
    """Return HTML with any local image src replaced by data URIs."""
    root = md_path.parent
    md_text = md_path.read_text(encoding='utf-8')
    # Convert markdown -> HTML
    html = markdown(md_text, extensions=['extra', 'tables', 'toc'])

    # Find all image src attributes in the generated HTML
    def replace_src(match):
        src = match.group(1)
        # skip external URLs
        if re.match(r'^https?://', src, flags=re.I):
            return f'src="{src}"'
        # handle absolute file or relative
        src_path = Path(src)
        if not src_path.is_absolute():
            candidate = (root / src_path).resolve()
        else:
            candidate = src_path
        if not candidate.exists():
            print(f'Warning: image not found, leaving SRC unchanged: {candidate}')
            return f'src="{src}"'
        # read and encode
        data = candidate.read_bytes()
        ext = candidate.suffix.lower().lstrip('.')
        mime = 'image/png' if ext == 'png' else 'image/jpeg' if ext in ('jpg','jpeg') else f'image/{ext}'
        b64 = base64.b64encode(data).decode('ascii')
        return f'src="data:{mime};base64,{b64}"'

    html = re.sub(r'src\s*=\s*"([^"]+)"', replace_src, html, flags=re.I)
    return html


def write_self_contained_html(md_path: Path, html: str) -> Path:
    out_path = md_path.with_suffix('.html')
    title = md_path.stem
    html_page = f"<!doctype html>\n<html>\n<head>\n<meta charset=\"utf-8\">\n<title>{sax.escape(title)}</title>\n<style>body {{ font-family: Arial, Helvetica, sans-serif; max-width: 900px; margin: 1.5rem auto; padding: 0 1rem; line-height: 1.45; }}</style>\n</head>\n<body>\n{html}\n</body>\n</html>"
    out_path.write_text(html_page, encoding='utf-8')
    return out_path


def write_wxr(md_path: Path, html: str, author: str = 'importer') -> Path:
    # Basic WXR skeleton
    now = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')
    title = md_path.stem
    wxr = []
    wxr.append('<?xml version="1.0" encoding="UTF-8" ?>')
    wxr.append('<rss version="2.0" xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:wfw="http://wellformedweb.org/CommentAPI/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:wp="http://wordpress.org/export/1.2/">')
    wxr.append('<channel>')
    wxr.append(f'<title>{sax.escape(title)}</title>')
    wxr.append(f'<link>http://example.local/{sax.escape(title)}</link>')
    wxr.append(f'<pubDate>{now}</pubDate>')
    wxr.append('<language>en-US</language>')

    item = []
    item.append('<item>')
    item.append(f'<title>{sax.escape(title)}</title>')
    item.append(f'<link>http://example.local/{sax.escape(title)}</link>')
    item.append(f'<pubDate>{now}</pubDate>')
    item.append(f'<dc:creator>{sax.escape(author)}</dc:creator>')
    # content:encoded contains full HTML content - wrap in CDATA
    item.append('<content:encoded><![CDATA[')
    item.append(html)
    item.append(']]></content:encoded>')
    item.append('<wp:post_date>' + datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S') + '</wp:post_date>')
    item.append('<wp:post_type>post</wp:post_type>')
    item.append('</item>')

    wxr.extend(item)
    wxr.append('</channel>')
    wxr.append('</rss>')

    out_path = md_path.with_suffix('.wp-export.xml')
    out_path.write_text('\n'.join(wxr), encoding='utf-8')
    return out_path


def main():
    if len(sys.argv) != 2:
        print('Usage: python scripts/export_for_wordpress.py Content/articles/<...>.md')
        sys.exit(1)
    md = Path(sys.argv[1])
    if not md.exists():
        print('Markdown file not found:', md)
        sys.exit(1)

    html = md_to_html_with_embedded_images(md)
    html_file = write_self_contained_html(md, html)
    wxr_file = write_wxr(md, html)

    print('WROTE HTML:', html_file)
    print('WROTE WXR:', wxr_file)

if __name__ == '__main__':
    main()
