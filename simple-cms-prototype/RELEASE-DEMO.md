# Demo Release — Guided + Quick Demo

This release snapshot packages the demo-ready materials used for the Guided Hands-On and Quick Demo presentations.

Included demo materials
- `Author-QuickStart.md` — one-page copyable commands for authors.
- `Demo-cheatsheet.md` — short checklist and commands for attendees.
- `Presenter-Script.md` — timed speaker notes for the Guided Hands-On session.
- `auto_demo_runner.ps1` — interactive runner that scaffolds a lesson, opens VS Code, waits for edits, runs the checker, commits and pushes a demo branch, and captures a transcript.
- `quick_demo.ps1` — (added) minimal commands to run the Quick Demo flow.

How to run the Quick Demo (2–5 minutes)

1. Open PowerShell in the repository root.
2. Ensure Python is on PATH and `pyyaml` is installed:

```powershell
python -m pip install pyyaml
```

3. Run the quick demo script (it will scaffold a lesson and run the checker):

```powershell
.\quick_demo.ps1
```

Guided Hands-On (recommended)

Follow `Presenter-Script.md` and use `auto_demo_runner.ps1` to run a rehearsal. The `Demo-cheatsheet.md` is ideal as a handout for attendees.

Release tag
- This snapshot is tagged `demo-guided-2025-11-22`.
