# Content Authoring & Publishing Workflow

This document finalizes the frontmatter-first workflow for the repository and documents the end-to-end steps from creating a topic to publishing it.

Principles
- Frontmatter-first: YAML frontmatter in each markdown file is the single source of truth for metadata (`title`, `slug`, `course`, `module`, `status`, etc.).
- Single edit tree: Authors edit files under `Content/<Course>/...`; only `Content/Published/` is used to hold published artifacts.
- CI & index driven: `content_status.json` is derived from frontmatter and CI enforces correctness.

Status values
- Draft, Review, Approved, Published
- Only `Approved` triggers an automatic move to `Content/Published/` via `scripts/workflow_transition.py`.

Commands (common)
- Scaffold a lesson (create file and frontmatter):

```powershell
python scripts/create_lesson.py "Customer Onboarding" --course "Microsoft-Dynamics" --module "Module-02" --open
```

- Rebuild/sync index from frontmatter:

```powershell
python scripts/check_status_consistency.py --fix --from-frontmatter
```

- Run a status transition (preferred entrypoint):

```powershell
# Record approver and publish when Approved
python scripts/workflow_transition.py customer-onboarding Approved --by "alice@example.com"
```

- Synchronize a single file's status to/from the index:

```powershell
python scripts/sync_status.py Content/Microsoft-Dynamics/Module-02/customer-onboarding.md
```

Review & PR process
1. Create a feature branch for your edits.
2. Run `check_status_consistency.py` locally before pushing.
3. Open a PR and request reviewers.
4. Address feedback and update the file (frontmatter remains canonical).
5. Once reviewers approve, run `workflow_transition.py <slug> Approved --by "approver"` to publish.

Audit fields
- On approval the script records `approved_by` and `approved_at` in `content_status.json`; when the file is moved these fields are also appended to the markdown frontmatter.

Deprecated behavior
- Folder-based staging (Draft/Review/Approval) and multiple stage mover scripts have been removed; the single canonical entrypoint is `scripts/workflow_transition.py`.

Troubleshooting
- If a file does not move on approval, check script output and `content_status.json` for updated `path` and `current_status`.
- Use `git log` / `git revert` to roll back accidental moves.

Contact / support
- For authoring questions, ask the docs team or open an issue in this repo.
