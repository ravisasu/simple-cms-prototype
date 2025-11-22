# Demo Slides — Simple-CMS-Prototype (one-slide cheat)

- Purpose: Quick presenter bullets for a 3–5 minute demo to authors/SMEs.
- Slide title: "Simple CMS Prototype — Authoring + Live Review"

Bullets for presenter:

1. Open repo in VS Code — accept recommended extensions (YAML, markdownlint, Live Share).
2. Create a lesson from `Templates/lesson-template.md` under `Content/<Course>/Module-01` and edit frontmatter (id/title/status).
3. Run the VS Code Task: "Check content consistency (fix)" to sync frontmatter into `content_status.json`.
4. Start Live Share, invite an SME, and edit the lesson together.
5. Commit, push, and open a PR for review — CI will run the consistency checks.

Speaker notes (10–20s each):
- Show template copy and frontmatter edit (20s).
- Run task to validate; point out `content_status.json` updated (20s).
- Start Live Share and demonstrate simultaneous edit (30–60s).
- Commit & PR, close with next steps and where to find contributor docs (20s).
