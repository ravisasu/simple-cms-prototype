import sys
import os
import json
from datetime import datetime

def update_json(json_path, article_id, new_status):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    found = False
    for article in data.get("articles", []):
        if article.get("id") == article_id:
            article["current_status"] = new_status
            article["last_updated"] = str(datetime.now().date())
            found = True
            break
    if not found:
        print(f"Article ID '{article_id}' not found in {json_path}")
        return False
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Updated {article_id} status in {json_path} → {new_status}")
    return True

def update_md_header(articles_dir, article_id, new_status):
    filename = f"{article_id}.md"
    file_path = os.path.join(articles_dir, filename)
    if not os.path.exists(file_path):
        print(f"Markdown file not found: {file_path}")
        return False
    lines = []
    status_updated = False
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().lower().startswith("# status"):
                lines.append(f"# Status: {new_status}\n")
                status_updated = True
            else:
                lines.append(line)
    if not status_updated:
        # Insert status after first header or at top
        inserted = False
        for i, line in enumerate(lines):
            if line.strip().startswith("#"):
                lines.insert(i+1, f"# Status: {new_status}\n")
                inserted = True
                break
        if not inserted:
            lines.insert(0, f"# Status: {new_status}\n")
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"Updated status in {file_path} → {new_status}")
    return True

def find_articles_dir():
    for d in [os.path.join("Content", "articles"), os.path.join("content", "articles")]:
        if os.path.isdir(d):
            return d
    return os.path.join("Content", "articles")

def main():
    if len(sys.argv) != 3:
        print("Usage: python scripts/sync_status.py <article_id> <new_status>")
        sys.exit(1)
    article_id = sys.argv[1]
    new_status = sys.argv[2]
    json_path = "content_status.json"
    articles_dir = find_articles_dir()
    ok_json = update_json(json_path, article_id, new_status)
    ok_md = update_md_header(articles_dir, article_id, new_status)
    if ok_json and ok_md:
        print(f"Status for '{article_id}' updated to '{new_status}' in both JSON and markdown file.")
    else:
        print("One or both updates failed. Check file paths and article ID.")

if __name__ == "__main__":
    main()