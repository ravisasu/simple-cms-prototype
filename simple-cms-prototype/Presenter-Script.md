# Presenter Script — Guided Hands-On Demo

Audience: content authors and SMEs
Duration: 10–15 minutes (guided, interactive)

Overview
- Quickly explain the frontmatter-first policy and why `content_status.json` is derived from each markdown file.
- Show how to scaffold a lesson, edit frontmatter, validate, collaborate with Live Share, and create a PR to run CI.

Timing & script
- 0:00 — Intro (20s)
  - Say: “We treat YAML frontmatter as the canonical metadata for each lesson. Our tools validate and keep `content_status.json` in sync.”

- 0:20 — Scaffold the lesson (40s)
  - Action: Run the scaffold command (or copy template). Use the `auto_demo_runner.ps1` or the `create_lesson.py` helper.
  - Say: “This creates a new markdown file with frontmatter already populated from your inputs.”

- 1:00 — Edit frontmatter (60–90s)
  - Action: Open the file in VS Code, change `title`, `status`, and `authors`. Save.
  - Say: “Make the title descriptive and set initial status to `Draft`.”

- 2:30 — Validate (30s)
  - Action: Run `python .\scripts\check_status_consistency.py --fix`.
  - Say: “The checker compares files with `content_status.json` and will auto-append or correct entries from the file’s frontmatter.”

- 3:00 — Live Share (60–120s, optional)
  - Action: Start Live Share, invite one SME, show editing in real time.
  - Say: “Collaborators can suggest edits and we’ll re-run the checker to keep metadata tidy.”

- 5:00 — Commit & open PR (30–60s)
  - Action: `git add`, commit, push to a demo branch, open a PR in GitHub.
  - Say: “The PR runs CI checks — frontmatter validation, markdownlint and link-checking.”

Troubleshooting lines to read
- If the checker prints parse warnings: “Install `pyyaml` in the Python environment used by the repository. Make sure the `python` on PATH matches where you installed packages.”
- If the PR CI fails with markdownlint: “We put a minimal `.markdownlint.json` in the repo — we can adjust rules if you prefer different style constraints.”

Closing (10s)
- Remind the group where templates and CONTRIBUTING docs live and offer the cheat-sheet for participants: `Demo-cheatsheet.md`.
