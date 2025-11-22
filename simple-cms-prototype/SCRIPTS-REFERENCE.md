# Scripts Reference

This file provides a one-sentence explanation, an example command, and a brief usage note for every script in the `scripts/` folder.

---

- `add_article.py`
  - Explanation: Creates a new article file from a template and adds an entry to the content index.
  - Example: `python scripts/add_article.py "My New Article" --module "Module-01" --course "Microsoft-Security"`
  - Usage: Run to scaffold a new markdown article with frontmatter in the correct course/module path.

- `check_status_consistency.py`
  - Explanation: Validates and optionally synchronizes YAML frontmatter `status` fields with `content_status.json`, normalizing synonyms.
  - Example: `python scripts/check_status_consistency.py --fix --from-frontmatter`
  - Usage: Use `--fix` to apply corrections to the JSON index and `--from-frontmatter` to rebuild the index from files.

- `convert_frontmatter_to_json.py`
  - Explanation: Scans content files and converts their YAML frontmatter into a single `content_status.json` index.
  - Example: `python scripts/convert_frontmatter_to_json.py --output content_status.json`
  - Usage: Run when you want to regenerate the status index from the repository's markdown files.

- `create_lesson.py`
  - Explanation: CLI helper to scaffold a lesson (slugify title, write frontmatter, and create folder structure).
  - Example: `python scripts/create_lesson.py "Intro to X" --course "Microsoft-Security" --module "Module-01" --open`
  - Usage: Use to create new lessons; `--open` can launch your editor and `--run-check` triggers consistency checks.

- `install_precommit_hook.ps1`
  - Explanation: PowerShell script that installs a Git pre-commit hook for local linting and validation.
  - Example: `. emplates\scripts\install_precommit_hook.ps1` (run from repo root)
  - Usage: Run once per developer environment to add local pre-commit checks.

- `markdown_to_pdf.py`
  - Explanation: Converts configured Markdown files into PDFs by rendering Markdown → HTML → PDF using `markdown` and `xhtml2pdf`.
  - Example: `python scripts/markdown_to_pdf.py`
  - Usage: Generates `Author-QuickStart.pdf` and `Demo-cheatsheet.pdf`; edit the `FILES` list to convert other docs.

- `move_to_published.py`
  - Explanation: Moves a content file into the `Content/Published/` folder and updates the index metadata.
  - Example: `python scripts/move_to_published.py Content/Microsoft-Security/Module-01/foo.md`
  - Usage: Use for explicit, single-file publish operations that relocate the article to the Published pool.

- `move_to_stage.py`
  - Explanation: Moves a content file to an arbitrary stage folder (e.g., Draft, Review, Published) and updates `content_status.json`.
  - Example: `python scripts/move_to_stage.py Content/X/Module-01/foo.md Published`
  - Usage: Run to manually change an article's folder stage and sync its path/status in the index.

- `publish_article.py`
  - Explanation: High-level wrapper that marks an article as published and triggers configured publish-time updates (e.g., metadata changes).
  - Example: `python scripts/publish_article.py intro-to-microsoft-security`
  - Usage: Use to mark a slug as published; it may call the mover or workflow script under the hood.

- `sync_status.py`
  - Explanation: Synchronizes the `status` field between a single markdown file's frontmatter and the `content_status.json` entry.
  - Example: `python scripts/sync_status.py Content/Microsoft-Security/Module-01/foo.md`
  - Usage: Handy for correcting or pushing a single file's status into the index or updating the file from the index.

- `update_status.py`
  - Explanation: CLI utility to update an article's status in `content_status.json` (and optionally its frontmatter).
  - Example: `python scripts/update_status.py intro-to-microsoft-security Approved --frontmatter`
  - Usage: Use when you need to change the status value programmatically; add `--frontmatter` to write it back into the file.

- `workflow_transition.py`
  - Explanation: Implements workflow rules (normalizes stage names) and triggers publish actions (moves file to Published on Approved and updates JSON/frontmatter).
  - Example: `python scripts/workflow_transition.py intro-to-microsoft-security Approved`
  - Usage: Preferred entrypoint for scripted status transitions that may need to move files and update audit fields.

---

If you want the exact CLI flags and full help text for any specific script, I can append the script's `--help` or print its argument parser output into this document.
