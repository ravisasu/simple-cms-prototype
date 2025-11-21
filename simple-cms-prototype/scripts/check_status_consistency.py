#!/usr/bin/env python
"""Check content_status.json vs files in Content/articles and optionally fix missing entries.

Usage:
  python scripts/check_status_consistency.py [--fix] [--json content_status.json]

Exit codes:
  0 - no inconsistencies (or fixed with --fix)
  1 - inconsistencies found (and not fixed)
"""
import json
import os
import argparse
from datetime import datetime


def find_articles_dir():
    candidates = [
        os.path.join("Content", "articles"),
        os.path.join("content", "articles"),
    ]
    for d in candidates:
        if os.path.isdir(d):
            return d
    # default to first and create if needed
    os.makedirs(candidates[0], exist_ok=True)
    return candidates[0]


def load_json(path):
    if not os.path.exists(path):
        return {"articles": []}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def scan_files(articles_dir):
    md_files = []
    for name in os.listdir(articles_dir):
        if name.lower().endswith(".md"):
            md_files.append(name)
    return sorted(md_files)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", default="content_status.json")
    parser.add_argument("--fix", action="store_true", help="Append missing entries to JSON using filename/title")
    args = parser.parse_args()

    articles_dir = find_articles_dir()
    md_files = scan_files(articles_dir)

    data = load_json(args.json)
    entries = data.get("articles", [])
    ids_in_json = {e.get("id") for e in entries}

    files_ids = {os.path.splitext(f)[0] for f in md_files}

    missing_in_json = sorted(files_ids - ids_in_json)
    orphan_in_json = sorted([e.get("id") for e in entries if e.get("id") not in files_ids])

    if not missing_in_json and not orphan_in_json:
        print("All good: every article file has a JSON entry and no orphan entries found.")
        return 0

    if missing_in_json:
        print("Files missing from JSON:")
        for mid in missing_in_json:
            print(f" - {mid}.md")

    if orphan_in_json:
        print("JSON entries without files:")
        for oid in orphan_in_json:
            print(f" - {oid}")

    if args.fix and missing_in_json:
        print("Fixing: appending missing entries to JSON with default Draft status")
        today = str(datetime.now().date())
        for mid in missing_in_json:
            # attempt to extract title from first line of file or use id
            file_path = os.path.join(articles_dir, mid + ".md")
            title = mid
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            # use first non-empty line as title if it's not just a markdown header marker
                            title = line.lstrip('# ').strip()
                            break
            except Exception:
                pass
            entries.append({
                "id": mid,
                "title": title,
                "current_status": "Draft",
                "last_updated": today,
            })
        data["articles"] = entries
        save_json(args.json, data)
        print(f"Appended {len(missing_in_json)} entries to {args.json}")
        # After fix, still check orphan entries separately
        if not orphan_in_json:
            return 0

    # If we reach here and inconsistencies remain, return non-zero so hooks fail
    return 1


if __name__ == "__main__":
    exit(main())
