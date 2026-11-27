---
name: spec
description: Write an implementation spec in docs/specs/ for work delegated to the owner's hu-flow agents (scaffolding, UI, tests, CI, deployment). Use when the owner says "write a spec", "/spec", or when non-core work needs to be handed off.
---

# Write a spec

Specs are for non-core work only. If the request touches the core (graph, SQL validation, semantic layer, agent endpoint, evals), stop and say that the owner writes it.

## Steps

1. Read `CLAUDE.md`, the related ADRs in `docs/adr/` and any existing specs in `docs/specs/`.
2. List the open questions and ask the owner before writing. Do not fill gaps with assumptions.
3. Write `docs/specs/NNNN-kebab-title.md` with these sections:
   - **Status:** Draft, Ready or Done.
   - **Context:** why this is needed. Link the ADRs.
   - **Scope:** what is in and what is out.
   - **Requirements:** numbered and testable.
   - **Interfaces:** API contracts, component props, environment variables, file locations.
   - **Acceptance criteria:** a checklist the agent and the owner can verify.
   - **Tests:** which tests to write (pytest, Vitest, Playwright) and what each one proves.
   - **Open questions:** whatever is still unresolved.
4. The spec stays `Draft` until the owner approves it. Only `Ready` specs go to the agents.

Specs are written in English.
