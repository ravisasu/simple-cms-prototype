# Author Quick Checklist

A short printable checklist authors can use when creating, reviewing, and publishing content.

1. Scaffold

- Run: `python scripts/create_lesson.py "<Title>" --course "<Course>" --module "<Module>" --open`
- Confirm file created under `Content/<Course>/<Module>/<slug>.md` with YAML frontmatter.

1. Drafting

- Edit content in the `.md` file; keep frontmatter correct and complete.
- Set `status: "Draft"` while drafting.
- Run local linters and validator if present; install pre-commit hook: `.\scripts\install_precommit_hook.ps1`.

1. Pre-commit checks

- Run: `python scripts/check_status_consistency.py --fix` to normalize statuses and update `content_status.json`.

1. Create PR

- Branch and push changes; open Pull Request for review.
- Ensure CI checks (frontmatter checks, markdownlint) pass.

1. Address Feedback

- Make requested changes and push to the PR branch until reviewers approve.

1. Final Approval & Publish

- After approval, run:
  - `python scripts/workflow_transition.py <slug> Approved --by "your.name@example.com"`
- This records `approved_by`/`approved_at`, updates `content_status.json`, and moves the file to `Content/Published/`.

1. Post-publish

- Verify file in `Content/Published/` and that `content_status.json` shows `current_status: "Published"`.
- Delete your feature branch if desired:
  - `git push origin --delete <branch>`
  - `git branch -D <branch>`

Notes

- Do not rely on folder placement for status — frontmatter is canonical.
- Keep binaries out of `main`; use GitHub Releases for distribution assets.
- For troubleshooting, see `WORKFLOW.md` or run the consistency checks.
