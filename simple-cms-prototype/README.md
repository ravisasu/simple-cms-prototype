Project scripts overview

This repository contains helper scripts to manage article files and their lifecycle status. Below are one-line descriptions for each script and concrete PowerShell examples you can run from the repository root.

## Scripts (one-line descriptions)

- `scripts/add_article.py`: Create a new markdown article file under `Content/articles` and append its metadata to `content_status.json`.
- `scripts/check_status_consistency.py`: Compare `content_status.json` with files under `Content/articles` and report (or `--fix` append) missing entries.
- `scripts/install_precommit_hook.ps1`: PowerShell helper to install a Git pre-commit hook that runs the consistency checker before commits.
- `scripts/sync_status.py`: Update an article's `current_status` in both `content_status.json` and the article's markdown `# Status:` header.
- `scripts/move_to_stage.py`: Move an article file to a named stage folder (e.g. `Approval`) and update its status in `content_status.json`.
- `scripts/move_to_published.py`: (empty placeholder) Intended place for a standalone mover to publish articles.
- `scripts/publish_article.py`: Simple script to move an article from `content/articles` to `content/published`.
- `scripts/workflow_transition.py`: Update an article's status in JSON and (when set to `Published`) move the file to the published folder; includes folder-name fallbacks.


## Examples (PowerShell)

Note: run these from the repository root (where `content_status.json` and the `scripts/` folder live). Use `python` or `py` depending on your environment.

### Create a new article (dry-run, then create)

```powershell
python .\scripts\add_article.py sample-article-006 "My New Article" --dry-run
python .\scripts\add_article.py sample-article-006 "My New Article"
```

### Update status in both JSON and the markdown header

```powershell
python .\scripts\sync_status.py sample-article-003 QA
```

### Move an article into a stage folder (creates folder if needed)

```powershell
python .\scripts\move_to_stage.py sample-article-004 Approval
```

### Update only the JSON status (no file move)

Prefer `sync_status.py` which updates JSON and the markdown header; it can be used where you only want JSON changed as well.

```powershell
python .\scripts\sync_status.py sample-article-003 Review
```

### Publish an article (workflow transition will move on `Published`)

```powershell
python .\scripts\workflow_transition.py sample-article-003 Published
# Or use the older simple mover (if adapted to your folder layout):
python .\scripts\publish_article.py sample-article-003.md
```

### Check consistency between files and JSON

```powershell
python .\scripts\check_status_consistency.py
# Auto-append missing entries (safe):
python .\scripts\check_status_consistency.py --fix
```

### Install the pre-commit hook (PowerShell)

```powershell
.\scripts\install_precommit_hook.ps1
```

### Git workflow (after changes)

```powershell
git add Content/articles/sample-article-006.md content_status.json
git commit -m "Add sample-article-006 and update status"
git push
```

## Notes

- Scripts assume `Content/articles` (or `content/articles`) as the article source. They include fallbacks for common folder name variants on Windows.
- The pre-commit hook runs `check_status_consistency.py` and will abort commits when mismatches are detected.
- Frontmatter-first: This repository now treats YAML frontmatter in each markdown file as the canonical source-of-truth for metadata. Use `CONTRIBUTING.md` and the files in `Templates/` for onboarding and examples.

If you want, I can commit these changes (README, templates, CONTRIBUTING, migration scripts) and push them to `origin/main` for you.
