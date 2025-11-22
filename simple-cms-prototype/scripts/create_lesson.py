#!/usr/bin/env python3
"""Create a new lesson from Templates/lesson-template.md

Generates a slug id from the title, copies the template, inserts YAML frontmatter,
and optionally opens the file in VS Code or runs the consistency checker.
"""
import argparse
import datetime
import os
import re
import subprocess
import sys

TEMPLATE = os.path.join("Templates", "lesson-template.md")
DEFAULT_CONTENT_ROOT = "Content"
CHECKER = os.path.join("scripts", "check_status_consistency.py")


def slugify(title: str) -> str:
    s = title.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    return s or "untitled"


def write_frontmatter(path, meta, force=False):
    if os.path.exists(path) and not force:
        raise FileExistsError(path)
    lines = ["---"]
    for k, v in meta.items():
        if isinstance(v, list):
            items = ", ".join(f'"{item}"' for item in v if item)
            lines.append(f"{k}: [{items}]")
        elif v is None:
            lines.append(f"{k}: null")
        else:
            # Quote values to be safe
            lines.append(f'{k}: "{v}"')
    lines.append("---")
    lines.append("")  # blank line after frontmatter
    # Read template body (skip template frontmatter if present)
    body = ""
    if os.path.exists(TEMPLATE):
        with open(TEMPLATE, "r", encoding="utf-8") as f:
            content = f.read()
        # remove existing frontmatter if template has it
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                body = parts[2].lstrip("\n")
            else:
                body = content
        else:
            body = content
    else:
        body = f"# {meta.get('title', '')}\n\n"  # fallback
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        f.write(body)


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def run_command(cmd, check=True):
    try:
        return subprocess.run(cmd, check=check)
    except Exception as e:
        print(f"Command failed: {cmd} -> {e}", file=sys.stderr)
        return None


def main():
    p = argparse.ArgumentParser(description="Create lesson from template with frontmatter")
    p.add_argument("title", help="Lesson title")
    p.add_argument("--course", default="Microsoft-Security", help="Course folder name")
    p.add_argument("--module", default="Module-01", help="Module folder name")
    p.add_argument("--status", default="Draft", help="Initial status (Draft|Review|QA|Approval|Published)")
    p.add_argument("--authors", default="", help="Comma-separated authors (e.g. Alice,Bob)")
    p.add_argument("--id", help="Optional id/slug override")
    p.add_argument("--open", action="store_true", help="Open the created file in VS Code")
    p.add_argument("--run-check", action="store_true", help="Run consistency checker (--fix) after creating")
    p.add_argument("--dry-run", action="store_true", help="Show what would be done without creating files")
    p.add_argument("--force", action="store_true", help="Overwrite existing file if present")
    args = p.parse_args()

    slug = args.id or slugify(args.title)
    filename = f"{slug}.md"
    dest_dir = os.path.join(DEFAULT_CONTENT_ROOT, args.course, args.module)
    dest_path = os.path.join(dest_dir, filename)

    meta = {
        "id": slug,
        "title": args.title,
        "course": args.course,
        "module": args.module,
        "status": args.status,
        "authors": [a.strip() for a in args.authors.split(",")] if args.authors else [],
        "last_updated": datetime.datetime.utcnow().strftime("%Y-%m-%d"),
    }

    if args.dry_run:
        print("DRY RUN:")
        print(f" - Destination directory: {dest_dir}")
        print(f" - Destination file: {dest_path}")
        print(" - Frontmatter:")
        for k, v in meta.items():
            print(f"    {k}: {v}")
        return 0

    ensure_dir(dest_dir)
    try:
        write_frontmatter(dest_path, meta, force=args.force)
    except FileExistsError:
        print(f"Error: destination file exists: {dest_path}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Error writing file: {e}", file=sys.stderr)
        return 3

    print(f"Created: {dest_path}")

    if args.open:
        # try to open in VS Code (requires 'code' on PATH)
        run_command(["code", dest_path])

    if args.run_check:
        if os.path.exists(CHECKER):
            run_command([sys.executable, CHECKER, "--fix"])
        else:
            print(f"Checker not found at {CHECKER}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
