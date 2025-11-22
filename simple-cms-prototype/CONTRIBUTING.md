# Contributing to Simple-CMS-Prototype

This project uses YAML frontmatter in each markdown file as the canonical source
of metadata (id, title, status, authors, course, module, last_updated). The
repository includes scripts to help create, validate, and migrate metadata.


Quick start (authoring a new lesson)

1. Create a branch from `main`:

```powershell
git checkout -b draft/<your-name>/<short-topic>
```

1. Use the lesson template in `Templates/lesson-template.md` to create a new
   markdown file under the appropriate course folder, for example:

```powershell
mkdir -p Content\Microsoft-Security\Module-01
copy Templates\lesson-template.md Content\Microsoft-Security\Module-01\ms-security-001.md
# then open in VS Code
code Content\Microsoft-Security\Module-01\ms-security-001.md
```

1. Fill in frontmatter fields at the top of the file. Required fields:

- `id` (unique slug)
- `title`
- `course` (e.g. `Microsoft-Security`)
- `status` (Draft | Review | Approval | Published)

1. Run the consistency checker locally before committing:

```powershell
python .\scripts\check_status_consistency.py --fix
```

1. Add, commit, push, and open a pull request for review:

```powershell
git add Content\Microsoft-Security\Module-01\ms-security-001.md content_status.json
git commit -m "Add ms-security-001 (Draft)"
git push --set-upstream origin draft/your-branch
```

PR checklist for authors

- Ensure frontmatter contains required fields.
- Run `python .\scripts\check_status_consistency.py --fix` locally.
- Add a short description of what changed and which module/course the change affects.
- Request a reviewer and wait for CI checks to pass.

If you need to regenerate `content_status.json` from files (migration step):

```powershell
python .\scripts\convert_frontmatter_to_json.py
```

If you have questions, contact the course lead or open an issue.
