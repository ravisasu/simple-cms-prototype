import os
import json
import sys

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

missing = []

if isinstance(data, list):
    for i, entry in enumerate(data):
        path = entry.get('path') if isinstance(entry, dict) else None
        title = entry.get('title') if isinstance(entry, dict) else None
        if path:
            full = os.path.join(ROOT, path)
            if not os.path.exists(full):
                missing.append({'index': i, 'path': path, 'title': title})

elif isinstance(data, dict):
    for key, entry in data.items():
        path = entry.get('path') if isinstance(entry, dict) else None
        title = entry.get('title') if isinstance(entry, dict) else None
        if path:
            full = os.path.join(ROOT, path)
            if not os.path.exists(full):
                missing.append({'key': key, 'path': path, 'title': title})

else:
    print('Unexpected JSON structure in content_status.json (not list or dict).')
    sys.exit(2)

if not missing:
    print('No missing files found in content_status.json (all paths exist).')
    sys.exit(0)

print('Found', len(missing), 'entries pointing to missing files:')
for m in missing:
    if 'index' in m:
        print(f" - [index {m['index']}] path: {m['path']}  title: {m.get('title')}")
    else:
        print(f" - [key {m['key']}] path: {m['path']}  title: {m.get('title')}")

# Exit code 0 to signal success
sys.exit(0)
