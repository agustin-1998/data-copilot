# CLAUDE.md

Instructions for Claude Code in this repository.

## Project

Data Copilot is a text-to-SQL agent over a sample e-commerce PostgreSQL database. The user asks a question in plain language ("How much did we sell in October by region?") and gets back the number, the SQL that produced it and a chart.

Target: a working, published demo in the second week of December 2026.

Core ideas:

- **Semantic layer.** A dictionary of tables and business metrics (what a "sale" is, what an "active customer" is). The agent builds SQL from it, not blindly from the raw schema.
- **Safety.** SELECT only, allow-listed tables only, always with a LIMIT, executed by a read-only PostgreSQL role. Expensive queries pause for human approval.
- **Evals.** About 50 questions with known answers. Correctness compares result sets, not SQL text, so we can say "it is right X% of the time".

## Stack (decided)

- Two entry points over one core ([ADR 0001](docs/adr/0001-llm-strategy-two-entry-points.md)):
  - Local: an MCP server. Whoever clones the repository connects their own agent (Claude Code, Codex, Gemini CLI), and that agent's model writes the SQL.
  - Online: the web app, with an agent that calls a free-tier model API.
- Frontend: Next.js, React and TypeScript. Streaming chat, results table, chart and a panel with the SQL.
- API and agent: FastAPI (Python).
- Agent flow (web app): LangGraph. Generate SQL, validate it, ask for approval, execute, answer.
- Tracing and evals: LangSmith.
- Database: PostgreSQL with sample e-commerce data.

Everything else is not decided yet. Open decisions are listed in `docs/adr/README.md`. Do not assume an answer: ask the owner.

## Who writes what

The owner (the human in this session) decides the architecture and writes the core.

Core, written by the owner and reviewed by Claude:

- The LangGraph graph (state, nodes, edges).
- SQL validation.
- The semantic layer.
- The FastAPI endpoint for the agent.
- The evals (questions, expected results, scoring).

Claude does not write core code, even when asked in passing. In core files Claude explains, reviews and describes the fix in words or in a snippet of five lines or fewer. The owner applies it.

Claude in this session:

- Teaches each topic before it is used (`/teach`).
- Reviews the owner's code (`/review`).
- Writes specs (`/spec`) and docs: ADRs after the owner decides (`/adr`), README, runbooks.

The owner's hu-flow agents do the scaffolding, UI, tests, CI and deployment, working from specs in `docs/specs/`.

**Hard rule: if the owner cannot explain it in a job interview, it does not get merged.** When a diff brings in something new (a library, a pattern, a trick), flag it and check that the owner can explain it.

## Language

- Everything in the repository is in English: code, identifiers, comments, docs, ADRs, specs, commit messages, branch names, PR titles and descriptions, issues.
- Conversation with the owner is in Spanish (Rioplatense).

## Git workflow

- No direct commits to `main`. Every change goes on a branch and through a pull request.
- Branch names: `<type>/<short-kebab-description>`, for example `feat/sql-validator`. Types: `feat`, `fix`, `chore`, `docs`, `test`, `ci`, `refactor`.
- Commit messages follow Conventional Commits: `feat: add read-only role`, `fix(api): handle empty result`. Imperative mood, lowercase, no final period.
- Claude commits, pushes and opens pull requests only when the owner says so. Claude never merges a pull request, never force-pushes and never rewrites `main`.

## Security

- Secrets live only in `.env`, which git ignores. `.env.example` lists the variable names with empty values. Never print, log or commit a key. Claude does not read `.env`.
- The agent connects with a read-only database role. Never give the agent's connection write rights, not even temporarily.
- Columns with personal data (names, emails, phone numbers, addresses and similar) never reach the model: not in the schema context, not in sample rows, not in results passed back to the LLM. The semantic layer marks them.
- Generated SQL is untrusted input. Validate it before it runs. Validation and human approval are never bypassed, not for tests and not for demos.

## Architecture Decision Records

- One page per decision: `docs/adr/NNNN-kebab-title.md`, copied from `docs/adr/0000-template.md`.
- Every ADR states its trade-off: what we give up.
- The owner decides. Claude may lay out options and recommend one, and drafts the ADR only after the decision.
- Use `/adr`.

## Roadmap

- **Step 0 (now):** repository and Claude Code setup.
- **Week 1 (Nov 30 to Dec 4):** database with sample data, semantic layer, LangGraph agent and the 50 eval questions.
- **Week 2 (Dec 7 to Dec 11):** FastAPI, Next.js frontend, human approval and a published demo.
- **Week 3:** MCP server, feature flag to turn the agent off, rollback, metrics dashboard (p95 latency, errors, tokens, cost per question, % of rejected SQL), API versioned under `/v1`, a real expand-and-contract migration, README with real numbers, demo video and LinkedIn post.

Also part of the core in weeks 1 and 2: ADRs, personal data hidden from the model, a cache for repeated questions, and timeout + retry + fallback model on LLM calls.

## Commands

To be filled in when the project is scaffolded: install, run, test, lint and evals.

## Skills

- `/teach <topic>`: teach a topic before it is used.
- `/adr <decision>`: lay out options or record a decision.
- `/review`: review the owner's code.
- `/spec <feature>`: write a spec for the hu-flow agents.
