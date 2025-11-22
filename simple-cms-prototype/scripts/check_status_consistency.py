#!/usr/bin/env python
"""Consistency checker that prefers frontmatter as canonical source.

This script validates markdown files under `Content/` (or `content/`) for YAML
frontmatter that includes required fields (id, title, status). It compares the
data to `content_status.json` and reports mismatches. With ``--fix`` it will
update `content_status.json` to match frontmatter. With ``--from-frontmatter``
it regenerates the JSON entirely from file frontmatter.

Usage:
  python scripts/check_status_consistency.py [--fix] [--from-frontmatter] [--json content_status.json]

Exit codes:
  0 - no inconsistencies (or fixed with --fix)
  1 - inconsistencies found (and not fixed)
"""
import json
import os
import argparse
import re
from datetime import datetime

try:
    import yaml
except Exception:
    yaml = None


def find_content_dirs():
    candidates = [
        os.path.join("Content"),
        os.path.join("content"),
    ]
    for d in candidates:
        if os.path.isdir(d):
            return d
    # default to Content and create if needed
    os.makedirs(candidates[0], exist_ok=True)
    return candidates[0]


def load_json(path):
    if not os.path.exists(path):
        return {"articles": []}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def extract_frontmatter(text):
    """Return a dict parsed from YAML frontmatter or empty dict.

    Supports files starting with '---' and ending frontmatter with '---'.
    """
    fm_match = re.match(r"^---\s*\n(.*?\n)---\s*\n", text, re.S)
    if not fm_match:
        return {}
    fm_text = fm_match.group(1)
    if yaml:
        try:
            return yaml.safe_load(fm_text) or {}
        except Exception:
            pass
    # Fallback simple parser: key: value lines
    data = {}
    for line in fm_text.splitlines():
        if ':' in line:
            key, val = line.split(':', 1)
            key = key.strip()
            val = val.strip()
            # simple list support: authors: [a, b]
            if val.startswith('[') and val.endswith(']'):
                items = [i.strip().strip('"\'') for i in val[1:-1].split(',') if i.strip()]
                data[key] = items
            else:
                data[key] = val.strip('"').strip('\'')
    return data


def scan_markdown_files(content_root):
    md_files = []
    for root, dirs, files in os.walk(content_root):
        for name in files:
            if name.lower().endswith('.md'):
                md_files.append(os.path.join(root, name))
    return sorted(md_files)


def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return ''


def build_index_from_frontmatter(md_paths):
    index = {}
    for p in md_paths:
        text = read_file(p)
        fm = extract_frontmatter(text)
        # fallback id/title
        filename = os.path.splitext(os.path.basename(p))[0]
        aid = fm.get('id') or filename
        title = fm.get('title') or fm.get('Title') or filename
        status = fm.get('status') or fm.get('current_status') or 'Draft'
        # Normalize common status synonyms to canonical values
        def normalize_status(s):
            if not s:
                return 'Draft'
            s_norm = str(s).strip()
            mapping = {
                'qa': 'Review',
                'quality assurance': 'Review',
                'approval': 'Approved',
                'approved': 'Approved',
                'review': 'Review',
                'draft': 'Draft',
                'published': 'Published'
            }
            low = s_norm.lower()
            return mapping.get(low, s_norm)

        status = normalize_status(status)
        course = fm.get('course')
        module = fm.get('module')
        authors = fm.get('authors') or fm.get('author') or []
        last_updated = fm.get('last_updated') or fm.get('last_updated') or None
        index[aid] = {
            'id': aid,
            'title': title,
            'current_status': status,
            'course': course,
            'module': module,
            'authors': authors,
            'path': os.path.relpath(p).replace('\\', '/'),
            'last_updated': last_updated,
        }
    return index


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--json', default='content_status.json')
    parser.add_argument('--fix', action='store_true', help='Update JSON entries to match frontmatter')
    parser.add_argument('--from-frontmatter', action='store_true', help='Regenerate JSON entirely from frontmatter')
    parser.add_argument('--strict', action='store_true', help='Treat missing required frontmatter fields as errors')
    args = parser.parse_args()

    content_root = find_content_dirs()
    md_paths = scan_markdown_files(content_root)

    fm_index = build_index_from_frontmatter(md_paths)

    data = load_json(args.json)
    json_entries = {e.get('id'): e for e in data.get('articles', [])}

    problems = False

    # Detect files missing frontmatter id/title when strict
    for aid, info in fm_index.items():
        if args.strict:
            if not info.get('id') or not info.get('title'):
                print(f"Missing required frontmatter for {info.get('path')}: id/title")
                problems = True

    # If regenerate requested, overwrite JSON with frontmatter-derived index
    if args.from_frontmatter:
        out = {'articles': list(fm_index.values())}
        save_json(args.json, out)
        print(f"Regenerated {args.json} from frontmatter ({len(fm_index)} entries)")
        return 0

    # Compare each frontmatter entry to JSON
    mismatches = []
    for aid, fm in fm_index.items():
        je = json_entries.get(aid)
        if not je:
            mismatches.append((aid, 'missing_in_json', fm))
            continue
        # compare key fields
        for key in ('title', 'current_status', 'course', 'module'):
            jf = je.get(key)
            ff = fm.get('current_status') if key == 'current_status' else fm.get(key)
            # frontmatter keys mapping
            if key == 'title':
                ff = fm.get('title')
            if jf != ff and (ff is not None and jf is not None):
                mismatches.append((aid, f'field_mismatch:{key}', {'json': jf, 'frontmatter': ff}))

    # Orphan JSON entries where file missing
    files_ids = set(fm_index.keys())
    orphan_json = [i for i in json_entries.keys() if i not in files_ids]

    if not mismatches and not orphan_json and not problems:
        print('All good: frontmatter and JSON are consistent')
        return 0

    if mismatches:
        print('Mismatches detected:')
        for m in mismatches:
            aid = m[0]
            typ = m[1]
            if typ == 'missing_in_json':
                print(f" - {aid}: missing in JSON (file: {fm_index[aid]['path']})")
            elif typ.startswith('field_mismatch:'):
                field = typ.split(':', 1)[1]
                details = m[2]
                print(f" - {aid}: field '{field}' differs (json='{details['json']}' frontmatter='{details['frontmatter']}')")

    if orphan_json:
        print('JSON entries without files:')
        for oid in orphan_json:
            print(f" - {oid}")

    if args.fix:
        # Update JSON entries from frontmatter where available, and append missing entries
        print('Applying fixes to JSON from frontmatter...')
        today = str(datetime.now().date())
        # update existing
        for aid, fm in fm_index.items():
            existing = json_entries.get(aid)
            entry = fm.copy()
            if not entry.get('last_updated'):
                entry['last_updated'] = today
            # normalize keys: ensure current_status exists
            if 'current_status' not in entry and 'status' in fm:
                entry['current_status'] = fm.get('status')
            json_entries[aid] = entry
        # remove orphan entries
        for oid in orphan_json:
            json_entries.pop(oid, None)
        out = {'articles': list(json_entries.values())}
        save_json(args.json, out)
        print(f'Wrote {len(out["articles"])} entries to {args.json}')
        return 0

    # If we reach here, inconsistencies remain and were not fixed
    return 1


if __name__ == '__main__':
    exit(main())
