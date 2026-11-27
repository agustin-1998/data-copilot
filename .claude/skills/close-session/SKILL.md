---
name: close-session
description: Close a work session. Update docs/progress.md (done, pending, blockers) and ask the owner one or two interview-style questions in English about the day's work; at the end of the week, also draft the LinkedIn post. Use when the owner says "cerramos", "terminamos por hoy", "cerrar sesión" or "/close-session".
---

# Close the session

## Steps

1. **Gather what happened today:** the conversation, `git log` since the last entry in `docs/progress.md`, and open pull requests and issues (`gh pr list`, `gh issue list`).
2. **Update `docs/progress.md`**, in English:
   - Rewrite "Current state" in three lines or fewer: where we are and what comes next.
   - Add a dated entry at the top of the log with **Done**, **Pending** and **Blockers**. Short bullets, with links to issues, pull requests and ADRs.
3. **Commit it** on the branch of the current task, together with that work, once the owner says so. If there is no task branch, ask the owner where it goes.
4. **Interview practice.** Ask one or two interview-style questions in English about today's work, one at a time. Follow the rules in `CLAUDE.local.md`: design questions are answered with CARE (Clarify, Architecture, Risks, How I know it works), and feedback stays short.
5. **End of the week** (the last session of the week, or when the owner says so): draft a short LinkedIn post about the week. Keep it concrete: what was built, one decision and its trade-off, and one real number if there is one. No hype. The owner reviews and publishes it; Claude never posts.
