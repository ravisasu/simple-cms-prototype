import os
import json
import shutil
import sys
from datetime import datetime

article_arg = sys.argv[1]
stage = sys.argv[2]  # Draft, Review, QA, Approved, Published

json_file = "content_status.json"
article_id = os.path.splitext(article_arg)[0]
article_md = f"{article_id}.md"

# Load JSON
with open(json_file, "r") as f:
    data = json.load(f)

found = False

for article in data.get("articles", []):
    if article.get("id") == article_id or article.get("id") == article_arg:
        found = True
        article["current_status"] = stage
        article["last_updated"] = str(datetime.now().date())

        # Publish Stage -> Move File
        if stage == "Published":
            # Try common folder name variations (case-insensitive on Windows)
            src_dirs = [
                os.path.join("Content", "articles"),
                os.path.join("content", "articles"),
                os.path.join("Content", "Articles"),
                os.path.join("content", "Articles"),
            ]

            dest_dirs = [
                os.path.join("Content", "Published"),
                os.path.join("content", "published"),
                os.path.join("Content", "published"),
                os.path.join("content", "Published"),
            ]

            src_path = None
            for d in src_dirs:
                candidate = os.path.join(d, article_md)
                if os.path.exists(candidate):
                    src_path = candidate
                    break

            if not src_path:
                print(f"Source file not found for '{article_md}' in expected article folders")
                break

            # Ensure destination dir exists (choose first existing or create first candidate)
            dest_dir = None
            for d in dest_dirs:
                if os.path.isdir(d):
                    dest_dir = d
                    break

            if not dest_dir:
                dest_dir = dest_dirs[0]
                os.makedirs(dest_dir, exist_ok=True)

            dest_path = os.path.join(dest_dir, article_md)

            try:
                shutil.move(src_path, dest_path)
                print(f"Article moved to published folder: {dest_path}")
            except Exception as e:
                print(f"Failed to move file: {e}")

        break

if not found:
    print("Article ID not found in content_status.json")
    sys.exit(1)

# Save JSON
with open(json_file, "w") as f:
    json.dump(data, f, indent=4)

print(f"STATUS UPDATED: {article_id} -> {stage}")
