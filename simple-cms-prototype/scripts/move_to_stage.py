import os
import sys
import shutil
import json
from datetime import datetime

"""
Move an article file to a stage folder (e.g. Approval) and update content_status.json.

Usage:
  python scripts/move_to_stage.py <article_id> <StageName>

Example:
  python scripts/move_to_stage.py sample-article-004 Approval

Behavior:
 - Searches under `Content/articles` (and `content/articles`) for the file `<article_id>.md`.
 - Moves it to one of these destination locations (first existing chosen, else created):
     - `Content/<StageName>/`
     - `content/<StageName>/`
     - `Content/articles/<StageName>/`
     - `content/articles/<StageName>/`
 - Updates `content_status.json` entry for the article (sets `current_status` and `last_updated`).
"""


def find_source(article_md):
    candidates = [
        os.path.join("Content", "articles"),
        os.path.join("content", "articles"),
    ]
    for base in candidates:
        for root, dirs, files in os.walk(base):
            if article_md in files:
                return os.path.join(root, article_md)
    # final attempt: check the file at base paths directly
    for base in candidates:
        candidate = os.path.join(base, article_md)
        if os.path.exists(candidate):
            return candidate
    return None


def choose_destination_dir(stage):
    candidates = [
        os.path.join("Content", stage),
        os.path.join("content", stage),
        os.path.join("Content", "articles", stage),
        os.path.join("content", "articles", stage),
    ]
    for d in candidates:
        if os.path.isdir(d):
            return d
    # create first candidate if none exist
    os.makedirs(candidates[0], exist_ok=True)
    return candidates[0]


def update_json(article_id, stage, json_path="content_status.json"):
    if not os.path.exists(json_path):
        print(f"JSON file not found: {json_path}")
        return False
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    found = False
    for article in data.get("articles", []):
        if article.get("id") == article_id:
            article["current_status"] = stage
            article["last_updated"] = str(datetime.now().date())
            found = True
            break
    if not found:
        print(f"Article ID '{article_id}' not found in {json_path}")
        return False
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    return True


def main():
    if len(sys.argv) != 3:
        print("Usage: python scripts/move_to_stage.py <article_id> <StageName>")
        sys.exit(1)
    article_id = sys.argv[1]
    stage = sys.argv[2]
    article_md = f"{article_id}.md"

    src = find_source(article_md)
    if not src:
        print(f"Source file not found for '{article_md}'.")
        sys.exit(1)

    dest_dir = choose_destination_dir(stage)
    dest_path = os.path.join(dest_dir, article_md)

    try:
        shutil.move(src, dest_path)
        print(f"Moved {article_md} -> {dest_path}")
    except Exception as e:
        print(f"Failed to move file: {e}")
        sys.exit(1)

    # Update JSON status (best-effort)
    if update_json(article_id, stage):
        print(f"Updated content_status.json: {article_id} -> {stage}")
    else:
        print("Warning: JSON not updated (entry may be missing).")


if __name__ == "__main__":
    main()
