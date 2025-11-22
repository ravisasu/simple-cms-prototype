# Simple-CMS Demo Cheat Sheet

One-page checklist and copyable commands to run the Guided Hands-On demo.

Quick checklist
- Open the repository root in VS Code and accept recommended extensions.
- Scaffold a lesson with `create_lesson.py` or copy the template into `Content`.
- Edit YAML frontmatter: `id`, `title`, `course`, `module`, `status`, `authors`.
- Run the consistency checker to sync `content_status.json`.
- Commit, push a branch, and open a PR to run CI checks.

Commands (PowerShell) — guided demo (copy-paste):

```powershell
# 1) create module folder (if needed)
mkdir -Force Content\Microsoft-Security\Module-01

# 2) scaffold a lesson (creates file and optionally runs the checker)
python .\scripts\create_lesson.py "Intro to Microsoft Security" --course Microsoft-Security --module Module-01 --run-check

# 3) (or) copy template manually
Copy-Item Templates\lesson-template.md Content\Microsoft-Security\Module-01\ms-security-001.md
code Content\Microsoft-Security\Module-01\ms-security-001.md

# 4) after editing, validate and auto-fix JSON
python .\scripts\check_status_consistency.py --fix

# 5) commit & push
git add Content\Microsoft-Security\Module-01\*.md content_status.json
git commit -m "Add ms-security-001 (Draft)"
git push --set-upstream origin demo/your-branch
```

Speaker notes (short)
- 0:00 — Open folder; accept recommended extensions.
- 0:20 — Scaffold or copy the template and open file.
- 0:45 — Edit frontmatter and save.
- 1:10 — Run `check_status_consistency.py --fix` to show automatic sync.
- 1:40 — Start Live Share to collaborate and iterate live.
- 2:30 — Commit and open PR; show CI checks running.

If you want a printable one-page PDF, print this markdown from VS Code or convert with `pandoc`.
