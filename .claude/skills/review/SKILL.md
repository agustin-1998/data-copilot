---
name: review
description: Review a branch or files like a senior engineer, especially the owner's core code (LangGraph graph, SQL validation, semantic layer, main FastAPI endpoint, evals), for correctness, security, naming, trade-offs and whether the owner can explain it. Use when the owner says "review", "revisá", "/review", or asks for feedback on a branch or a file.
---

# Review like a senior engineer

Scope: the current branch against `main` (`git diff main...HEAD`), or the files the owner names.

## Check, in this order

1. **Correctness.** Bugs, edge cases, wrong results (empty results, NULLs, time zones, rounding, duplicated rows from joins).
2. **Safety rules from `CLAUDE.md`.** SELECT only, allow-listed tables, LIMIT, read-only role, personal data never reaches the model, approval cannot be bypassed, no secrets in code or logs.
3. **Failure handling.** Timeouts, retries, fallback model, errors shown to the user in a useful way.
4. **Tests.** Is there a test that would catch each bug above? Name the missing test.
5. **Naming.** Names that hide what something does or mix two meanings.
6. **Trade-offs.** A choice in the code that has a cost the owner may not have seen, or that contradicts an ADR.
7. **Explainability.** Anything the owner may not be able to explain in an interview (a new library, a clever trick). Ask about it.

## Output

- Speak Spanish. Paths, code and identifiers stay as they are.
- One line per finding, most severe first: `path:line: severity: problem. fix.`
- Severity is `blocker`, `should-fix` or `nit`. Include nits only when there are few findings.
- About ten findings at most. No praise list. If nothing is wrong, say so in one line.

## Do not

- Do not fix core code. Point to the problem. If the owner is stuck, give hints one level at a time: the idea, then pseudocode, then a fragment. Never the full solution unless the owner says "mostrame".
- Do not review style the linter will catch.
