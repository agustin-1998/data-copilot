---
name: issue
description: Draft a small GitHub issue for the next task (goal, acceptance criteria, out of scope), labelled core or delegated, and create it once the owner approves. Use when a new task starts, or when the owner says "issue", "abrí un issue" or "/issue".
---

# Draft and create an issue

One issue is one small task that fits in one pull request, ideally a day of work or less. If the task is bigger, split it and propose the pieces.

## Steps

1. Read `CLAUDE.md`, `docs/progress.md` and the related ADRs.
2. Draft the issue in chat, in English:

   ```markdown
   Title: <short, imperative>

   ## Goal
   One or two sentences: what this task achieves and why.

   ## Acceptance criteria
   - [ ] Testable criterion.
   - [ ] Testable criterion.

   ## Out of scope
   - What this task does not do.

   ## Notes
   Related ADRs. For delegated work: the owner's directive (what, architecture, pattern and why).
   ```

3. Choose the label:
   - `core`: the LangGraph graph, SQL validation, the semantic layer, the main FastAPI endpoint, the evals. The owner writes it.
   - `delegated`: everything else (scaffolding, Docker, UI, tests, CI, deployment, docs).
4. For `delegated` work without a directive, ask the owner for it before going on.
5. Show the draft and wait. Create nothing until the owner approves it.
6. Once approved:
   - Make sure the labels exist: `gh label create core --color B60205 --description "Written by the owner" 2>/dev/null || true` and the same for `delegated` (`--color 0E8A16 --description "Written by Claude or the owner's agents"`).
   - Create it: `gh issue create --title "..." --body "..." --label core` (or `delegated`).
7. Report the issue number and the branch name to use: `feature/<issue-number>-<short-description>`. Create the branch when the work starts.
