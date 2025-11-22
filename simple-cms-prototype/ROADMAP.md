# Simple-CMS-Prototype — Roadmap & Implementation Plan

This roadmap describes the recommended GitHub + VS Code system to support multiple authors collaborating on three courses:
- Microsoft Security
- Azure AI Foundations
- Microsoft Dynamics

Goals
- Provide a robust authoring workflow for multiple authors.
- Enforce content metadata consistency and prevent accidental drift.
- Support review & approval stages with clear branching and PR checks.
- Make onboarding simple with VS Code settings, templates and documentation.

High-level design

- Repository structure (recommended)
  - `Content/`
    - `Microsoft-Security/`
      - `Course/` (course-level content)
      - `Module-01/`, `Module-02/`, ...
    - `Azure-AI-Foundations/`
    - `Microsoft-Dynamics/`
  - `Templates/` — markdown templates and course-level skeletons
  - `scripts/` — authoring and sync scripts (add, move, sync, convert)
  - `content_status.json` — optional global registry (interim solution)
  - `.github/` — workflows and PR templates
  - `docs/` — contributor docs, style guide, and the roadmap

Metadata approach
- Recommended: YAML frontmatter in each markdown file as the single source-of-truth for metadata (title, id, status, authors, course, module, last_updated). Benefits:
  - Easier to manage when editing files in VS Code.
  - Aligns with static-site and publishing tools.
- Keep `content_status.json` as a derived index while migrating. Provide scripts to generate/update it from frontmatter.

Essential scripts and automation
- `scripts/add_article.py` — create new markdown with frontmatter and optional initial metadata; optionally register in `content_status.json`.
- `scripts/sync_status.py` — synchronize status between frontmatter and `content_status.json`; allow atomic updates.
- `scripts/move_to_stage.py` — move an article within the repo to a stage folder (Draft, Review, Approval, Published) and update metadata.
- `scripts/publish_article.py` — final mover that ensures published content lives in `Content/<Course>/Published/` (or separate `Published/` area) and optionally tags release metadata.
- `scripts/check_status_consistency.py` — CI-friendly checker that verifies every markdown file has valid frontmatter and `content_status.json` consistency (returns non-zero on error).
- `scripts/convert_frontmatter_to_json.py` — migration tool to generate `content_status.json` from existing frontmatter.

Repository policies & checks
- Pre-commit hook: run `check_status_consistency.py` locally to block commits with mismatches.
- GitHub Actions: run checker on pull requests and run a minimal lint (markdown/frontmatter validation) and link-checker.
- Branching model: main + feature branches
  - `main` — production-ready content for publishing
  - `draft/<author>/<topic>` — in-progress work
  - `review/<pr-number>` — used by reviewers if needed
- PR requirements: at least one reviewer, passing CI checks, and a short description of content changes

VS Code setup for multi-author collaboration
- Workspace settings (store in `.vscode/`): recommended extensions and editor settings (trim trailing whitespace, YAML frontmatter support, Markdown linting).
- Live Share: instructions for real-time collaboration; include `COLLABORATION.md` linking to Live Share setup.
- Recommended extensions:
  - `yzhang.markdown-all-in-one`
  - `DavidAnson.vscode-markdownlint`
  - `redhat.vscode-yaml`
  - `ms-vsliveshare.vsliveshare` (optional for pair editing)

Onboarding & contributor docs
- `CONTRIBUTING.md`: step-by-step: fork/branch/PR, content conventions, frontmatter examples, status lifecycle, how to run scripts locally.
- `TEMPLATES/` include a `course-template.md` and `lesson-template.md` with required frontmatter fields.

Course-specific organization and workflow
- Create three top-level directories under `Content/` named after courses (use URL-friendly names, e.g., `Microsoft-Security`).
- Each course gets modules/lessons as subfolders. Each new lesson should have frontmatter including:
  - `id`: unique slug (e.g. `ms-security-001`)
  - `title`
  - `course`
  - `module`
  - `status`: Draft | Review | Approval | Published
  - `authors`: list
  - `last_updated`

Migration plan (short)
1. Add frontmatter to existing files (scripted or manual): `scripts/add-frontmatter.py` can add missing but minimal frontmatter.
2. Run `scripts/convert_frontmatter_to_json.py` to populate `content_status.json` from files.
3. Switch CI hooks to validate frontmatter and make frontmatter canonical.

Implementation milestones (concrete)
- Milestone 1 (Day 0-1): Repository organisation
  - Create course directories under `Content/`
  - Add `Templates/` for lessons and courses
  - Add `CONTRIBUTING.md` and `ROADMAP.md`
- Milestone 2 (Day 1-2): Core scripting
  - Implement `add_article.py`, `sync_status.py`, `move_to_stage.py`, `check_status_consistency.py`, and `convert_frontmatter_to_json.py`.
  - Add pre-commit hook installer (`install_precommit_hook.ps1` already exists). Ensure it validates frontmatter.
- Milestone 3 (Day 2-4): CI and PR automation
  - Add GitHub Actions to run consistency checks and markdown lint on PRs.
  - Add PR template and CODEOWNERS for the three course leads.
- Milestone 4 (Day 4-7): Onboarding and docs
  - Add `CONTRIBUTING.md`, `COLLABORATION.md`, `README.md` updates, and sample articles for each course.
  - Run a lightweight sample authoring session (Live Share recommended).

Acceptance criteria
- Every markdown file contains required frontmatter.
- `check_status_consistency.py` returns 0 when metadata/file system are consistent.
- PRs fail CI if metadata is missing or malformed.
- Authors can create a new lesson via `scripts/add_article.py` and open it in VS Code with a single command.

Immediate next steps I will implement for you now
1. Add this `ROADMAP.md` (done).
2. Remove the deprecated `scripts/update_status.py` (done).
3. Update `README.md` to remove references to the deleted script (done).

Optional follow-ups I can implement next (pick any):
- Commit & push these changes to the remote (I can do that if you approve).
- Create `CONTRIBUTING.md`, `TEMPLATES/lesson-template.md`, and a `codeowners` file for the three course leads.
- Implement the frontmatter-first migration scripts and update CI to validate frontmatter.
- Add PR templates and a GitHub Actions workflow that validates frontmatter and runs `check_status_consistency.py`.

If you want me to continue, tell me which of the optional follow-ups to start with; I can implement them and commit/push the changes.

---
Generated on 2025-11-22
