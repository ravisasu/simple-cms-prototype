import os
import json
import sys
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
STATUS = os.path.join(ROOT, 'content_status.json')

if not os.path.exists(STATUS):
    print('content_status.json not found at', STATUS)
    sys.exit(2)

with open(STATUS, 'r', encoding='utf-8') as f:
    try:
        data = json.load(f)
    except Exception as e:
        print('Failed to parse content_status.json:', e)
        sys.exit(2)

bak = STATUS + '.bak.' + datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
with open(bak, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print('Backup written to', bak)

removed = []

if isinstance(data, list):
    kept = []
    for i, entry in enumerate(data):
        path = entry.get('path') if isinstance(entry, dict) else None
        if path:
            full = os.path.join(ROOT, path)
            if not os.path.exists(full):
                removed.append({'index': i, 'path': path, 'title': entry.get('title')})
                continue
        kept.append(entry)
    new_data = kept

elif isinstance(data, dict):
    new_obj = {}
    for key, entry in data.items():
        path = entry.get('path') if isinstance(entry, dict) else None
        if path:
            full = os.path.join(ROOT, path)
            if not os.path.exists(full):
                removed.append({'key': key, 'path': path, 'title': entry.get('title')})
                continue
        new_obj[key] = entry
    new_data = new_obj

else:
    print('Unexpected JSON structure in content_status.json (not list or dict).')
    sys.exit(2)

if not removed:
    print('No entries to remove; content_status.json unchanged.')
    sys.exit(0)

print('Removing', len(removed), 'entries:')
for r in removed:
    if 'index' in r:
        print(f" - [index {r['index']}] {r['path']}  title: {r.get('title')}")
    else:
        print(f" - [key {r['key']}] {r['path']}  title: {r.get('title')}")

with open(STATUS, 'w', encoding='utf-8') as f:
    json.dump(new_data, f, indent=2, ensure_ascii=False)
print('WROTE cleaned content_status.json')
sys.exit(0)
