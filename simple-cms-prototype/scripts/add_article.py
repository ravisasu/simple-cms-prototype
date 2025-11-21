import argparse
import json
import os
from datetime import datetime


TEMPLATE = """# Title: {title}

# Author:
<Your Name>

# Status:
{status}

# Content:
<Write your content here...>

"""


def choose_dir():
    # prefer existing directory variants, else create Content/articles
    candidates = [
        os.path.join("Content", "articles"),
        os.path.join("content", "articles"),
        os.path.join("Content", "Articles"),
        os.path.join("content", "Articles"),
    ]
    for d in candidates:
        if os.path.isdir(d):
            return d
    # otherwise create the first candidate
    os.makedirs(candidates[0], exist_ok=True)
    return candidates[0]


def load_status(json_path):
    if not os.path.exists(json_path):
        return {"articles": []}
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_status(json_path, data):
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def article_exists(data, article_id):
    for a in data.get("articles", []):
        if a.get("id") == article_id:
            return True
    return False


def main():
    parser = argparse.ArgumentParser(description="Create new article file and update content_status.json")
    parser.add_argument("id", help="Article id (e.g. sample-article-003)")
    parser.add_argument("title", help="Article title (wrap in quotes if it has spaces)")
    parser.add_argument("--status", default="Draft", help="Initial status (default: Draft)")
    parser.add_argument("--json", default="content_status.json", help="Path to content_status.json")
    parser.add_argument("--dry-run", action="store_true", help="Show actions without writing files")
    parser.add_argument("--open", action="store_true", help="Open the new file after creating (platform default editor)")
    args = parser.parse_args()

    article_id = args.id
    filename = f"{article_id}.md"
    articles_dir = choose_dir()
    filepath = os.path.join(articles_dir, filename)

    json_path = args.json
    data = load_status(json_path)

    if article_exists(data, article_id):
        print(f"Article id '{article_id}' already exists in {json_path}")
        return

    # Prepare JSON entry
    entry = {
        "id": article_id,
        "title": args.title,
        "current_status": args.status,
        "last_updated": str(datetime.now().date())
    }

    print("Planned actions:")
    print(f"- Create article file: {filepath}")
    print(f"- Add entry to {json_path}: {entry}")

    if args.dry_run:
        print("Dry-run mode: no files were written.")
        return

    # Create article file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(TEMPLATE.format(title=args.title, status=args.status))

    # Update JSON
    data.setdefault("articles", []).append(entry)
    save_status(json_path, data)

    print("Created article and updated status file.")
    print(f"- File: {filepath}")
    print(f"- JSON: {json_path}")

    if args.open:
        try:
            os.startfile(filepath)
        except Exception:
            pass


if __name__ == "__main__":
    main()
