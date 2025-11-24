import os
import json
import shutil
import sys
from datetime import datetime

"""
workflow_transition.py

Usage:
  python scripts/workflow_transition.py <article_id_or_filename> <stage>

Accepted stages: Draft, Review, Approved, Published (case-insensitive)

Behavior:
- Updates `content_status.json` for the article's `current_status` and `last_updated`.
- If the incoming stage indicates approval (e.g. `Approved`), the script will
  record the approval and then move the file into the `Published` folder and
  set `current_status` to `Published` so metadata remains consistent.
"""

article_arg = sys.argv[1]
stage_raw = sys.argv[2]

# Optional approver: support `--by <approver>` to record who approved the article
approver = None
if '--by' in sys.argv:
    try:
        idx = sys.argv.index('--by')
        if len(sys.argv) > idx + 1:
            approver = sys.argv[idx + 1]
    except Exception:
        approver = None

json_file = "content_status.json"
article_id = os.path.splitext(article_arg)[0]
article_md = f"{article_id}.md"

def normalize_stage(s):
    if not s:
        return 'Draft'
    s2 = str(s).strip().lower()
    if s2 in ('qa', 'quality assurance'):
        return 'Review'
    if s2 in ('approval', 'approved'):
        return 'Approved'
    if s2 in ('review',):
        return 'Review'
    if s2 in ('published', 'publish'):
        return 'Published'
    if s2 in ('draft',):
        return 'Draft'
    # default: capitalize first letter
    return s.strip().capitalize()

stage = normalize_stage(stage_raw)

# Load JSON
if not os.path.exists(json_file):
    print(f"JSON file not found: {json_file}")
    sys.exit(1)

with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

found = False

def find_source_path(article_md):
    # search content tree for the article file
    for base in ("Content", "content"):
        for root, dirs, files in os.walk(base):
            if article_md in files:
                return os.path.join(root, article_md)
    # last attempt: check typical articles folder
    candidates = [os.path.join("Content", "articles", article_md), os.path.join("content", "articles", article_md)]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None

def ensure_published_dir():
    # prefer Content/Published, but accept variations
    candidates = [os.path.join("Content", "Published"), os.path.join("content", "published"), os.path.join("Content", "published"), os.path.join("content", "Published")]
    for d in candidates:
        if os.path.isdir(d):
            return d
    os.makedirs(candidates[0], exist_ok=True)
    return candidates[0]

for article in data.get("articles", []):
    # Match by ID, filename (with or without .md), or path basename
    article_path = article.get("path", "")
    article_filename = os.path.basename(article_path) if article_path else ""

    if (article.get("id") == article_id or
        article.get("id") == article_arg or
        article_filename == article_md or
        article_filename == article_arg):
        found = True
        # If stage is Approved we treat it as approval trigger: record approval, then publish
        if stage == 'Approved':
            # record previous status for auditing
            prev = article.get('current_status')
            article['previous_status'] = prev
            # set last_updated now
            article['last_updated'] = str(datetime.now().date())

            # record approval audit fields
            if approver:
                article['approved_by'] = approver
            article['approved_at'] = datetime.now().isoformat()

            # find source file and move to published folder
            src_path = find_source_path(article_md)
            if not src_path:
                print(f"Source file not found for '{article_md}' in content tree")
                break
            dest_dir = ensure_published_dir()
            dest_path = os.path.join(dest_dir, article_md)
            try:
                shutil.move(src_path, dest_path)
                print(f"Article moved to published folder: {dest_path}")
                # update JSON path to point to the new location
                article['path'] = dest_path.replace('\\', '/')
            except Exception as e:
                print(f"Failed to move file: {e}")
                break

            # update metadata to Published so JSON matches file location
            article['current_status'] = 'Published'
            article['last_updated'] = str(datetime.now().date())

            # Also update frontmatter/status in the moved markdown, if possible
            try:
                with open(dest_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        fm_text = parts[1]
                        body = parts[2]
                        # update or insert status: line
                        new_lines = []
                        updated = False
                        for line in fm_text.splitlines():
                            if line.strip().startswith('status:') or line.strip().startswith('current_status:'):
                                new_lines.append("status: \"Published\"")
                                updated = True
                            else:
                                new_lines.append(line)
                        if not updated:
                            new_lines.append('status: "Published"')
                        # append approval audit fields into frontmatter if present
                        if article.get('approved_by'):
                            new_lines.append(f'approved_by: "{article.get("approved_by")}"')
                        if article.get('approved_at'):
                            new_lines.append(f'approved_at: "{article.get("approved_at")}"')
                        new_fm = '\n'.join(new_lines)
                        new_content = '---\n' + new_fm + '\n---' + body
                        with open(dest_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
            except Exception:
                pass

        else:
            # Normal status update (Draft/Review/Published)
            article['current_status'] = stage
            article['last_updated'] = str(datetime.now().date())

            # If stage is Published explicitly, perform move as well
            if stage == 'Published':
                src_path = find_source_path(article_md)
                if not src_path:
                    print(f"Source file not found for '{article_md}' in content tree")
                    break
                dest_dir = ensure_published_dir()
                dest_path = os.path.join(dest_dir, article_md)
                try:
                    shutil.move(src_path, dest_path)
                    print(f"Article moved to published folder: {dest_path}")
                    article['path'] = dest_path.replace('\\', '/')
                except Exception as e:
                    print(f"Failed to move file: {e}")
                    break

        break

if not found:
    print("Article ID not found in content_status.json")
    sys.exit(1)

# Save JSON
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)

print(f"STATUS UPDATED: {article_id} -> {stage}")
