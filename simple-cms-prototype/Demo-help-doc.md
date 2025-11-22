# Demo Help — Quick steps to demo Simple-CMS-Prototype

Goal: show SMEs and authors how to create and validate a lesson using VS Code, templates, frontmatter, and the repository tooling.

Prerequisites

- Clone the repository and open the folder in VS Code.
- Have Python available on your PATH. On Windows, use PowerShell.
- (Optional) Install `pyyaml` for richer frontmatter parsing:

```powershell
python -m pip install pyyaml
```

Demo steps (2–6 minutes)

1. Open the repository in VS Code

- File → Open Folder → select the repository root. VS Code will recommend extensions defined in `.vscode/extensions.json`. Accept recommended extensions (YAML, Markdown helpers, markdownlint, Live Share).

2. Create a new lesson from the template

Use the `Templates/lesson-template.md` as a starting point. Example PowerShell commands (run in VS Code Terminal):

```powershell
# create module folder (example)
mkdir -Force Content\Microsoft-Security\Module-01
# copy template and give a unique id filename
Copy-Item Templates\lesson-template.md Content\Microsoft-Security\Module-01\ms-security-001.md
code Content\Microsoft-Security\Module-01\ms-security-001.md
```

3. Edit the frontmatter and content

- At the top of the file, update YAML frontmatter fields: `id`, `title`, `course`, `module`, `status` (Draft | Review | Approved | Published), and `authors`.
- Save the file.

Example frontmatter (already in the template):

```yaml
---
id: "ms-security-001"
title: "Intro to Microsoft Security"
course: "Microsoft-Security"
module: "Module-01"
status: "Draft"
authors: ["Alice"]
last_updated: "2025-11-22"
---
```

4. Validate metadata with the consistency checker

- Run the checker in the integrated terminal to ensure frontmatter is consistent with `content_status.json`. Use `--fix` to update the JSON from frontmatter if needed.

```powershell
python .\scripts\check_status_consistency.py --fix
```

- Optional: Regenerate the entire `content_status.json` from frontmatter (useful after bulk edits or migration):

```powershell
python .\scripts\convert_frontmatter_to_json.py
```

5. Start a Live Share session (pair-editing)

- Click the Live Share icon in the VS Code status bar (or run the Live Share extension). Invite an SME by copy/paste of the session link. Both participants can edit the same markdown in real time.

6. Commit your changes and open a PR

```powershell
git add Content\Microsoft-Security\Module-01\ms-security-001.md content_status.json
git commit -m "Add ms-security-001 (Draft)"
git push --set-upstream origin draft/your-branch
```

Troubleshooting

- If the checker prints parsing warnings and you installed `pyyaml`, ensure `python` on PATH is the same interpreter used to install packages.
- If the Live Share extension requires sign-in, follow the extension prompts.

Short demo script (speaker notes)

- 0:00 — Open folder in VS Code, accept recommended extensions.
- 0:20 — Copy the lesson template to a course/module, open file.
- 0:45 — Edit frontmatter `id/title/status` and save.
- 1:10 — Run `check_status_consistency.py --fix` to show automatic alignment.
- 1:40 — Start Live Share and invite an SME; demonstrate collaborative edits.
- 2:30 — Commit and open PR; show the `content_status.json` generated from frontmatter.

That's it — this doc gives authors a tight path to try the workflow and for SMEs to see the live collaboration and metadata validation in action.
