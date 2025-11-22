#!/usr/bin/env python
"""Generate or update `content_status.json` from markdown frontmatter.

This script walks the `Content/` directory, extracts YAML frontmatter from
each markdown file, and writes a JSON index at the repo root. It is safe to
run multiple times; use it when migrating to frontmatter-first metadata.
"""
import os
import json
import re
from datetime import datetime

try:
    import yaml
except Exception:
    yaml = None


def extract_frontmatter(text):
    m = re.match(r"^---\s*\n(.*?\n)---\s*\n", text, re.S)
    if not m:
        return {}
    fm = m.group(1)
    if yaml:
        try:
            return yaml.safe_load(fm) or {}
        except Exception:
            pass
    data = {}
    for line in fm.splitlines():
        if ':' in line:
            k, v = line.split(':', 1)
            data[k.strip()] = v.strip().strip('"').strip("'")
    return data


def find_content_root():
    for c in ("Content", "content"):
        if os.path.isdir(c):
            return c
    os.makedirs("Content", exist_ok=True)
    return "Content"


def scan_markdown(root):
    out = []
    for dirpath, dirs, files in os.walk(root):
        for f in files:
            if f.lower().endswith('.md'):
                out.append(os.path.join(dirpath, f))
    return out


def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            return fh.read()
    except Exception:
        return ''


def main():
    root = find_content_root()
    md_files = scan_markdown(root)
    index = []
    today = str(datetime.now().date())
    for p in sorted(md_files):
        text = read_file(p)
        fm = extract_frontmatter(text)
        filename = os.path.splitext(os.path.basename(p))[0]
        aid = fm.get('id') or filename
        title = fm.get('title') or filename
        status = fm.get('status') or fm.get('current_status') or 'Draft'
        entry = {
            'id': aid,
            'title': title,
            'current_status': status,
            'course': fm.get('course'),
            'module': fm.get('module'),
            'authors': fm.get('authors') or fm.get('author') or [],
            'path': os.path.relpath(p).replace('\\', '/'),
            'last_updated': fm.get('last_updated') or today,
        }
        index.append(entry)
    out = {'articles': index}
    with open('content_status.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=4, ensure_ascii=False)
    print(f'Wrote {len(index)} entries to content_status.json')


if __name__ == '__main__':
    main()
