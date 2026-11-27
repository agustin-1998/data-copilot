# 0002. Repository layout: one Python package and a separate web app

- **Status:** Accepted
- **Date:** 2026-11-27

> I chose one Python package that holds the core and both entry points, next to a separate Next.js app, because it is the least setup for a three-week project and "two entry points over one core" is just as clear with folders; what I pay is that nothing but code review enforces the boundary between the core and the entry points; if the MCP server has to be installed on its own, or the boundary starts to leak, I move to a uv workspace with one package per piece.

## Context

[ADR 0001](0001-llm-strategy-two-entry-points.md) defines one core and two entry points: FastAPI for the web app and an MCP server for local agents. Both must use the same core without copying it. The project has a Python side and a TypeScript side, the deadline is three weeks away, and every new tool costs learning time.

## Options considered

1. **One Python package plus a separate web app.** Folders for the core and for each entry point, one `pyproject.toml`.
2. **uv workspace.** One package per piece (`packages/core`, `apps/api`, `apps/mcp`) plus the web app. The tooling enforces that the entry points depend only on the core.
3. **One repository per piece.** Rejected: versioning across repositories is pure cost for a three-week project.

## Decision

Option 1:

```
data-copilot/
├── backend/                 Python, managed with uv, one pyproject.toml
│   ├── src/data_copilot/
│   │   ├── core/            semantic layer, SQL validation, read-only execution
│   │   ├── agent/           LangGraph graph
│   │   ├── api/             FastAPI routes under /v1
│   │   └── mcp/             MCP server
│   ├── evals/
│   └── tests/
├── web/                     Next.js, managed with pnpm
├── db/                      schema, roles, seed data
├── docs/
└── docker-compose.yml       PostgreSQL
```

The FastAPI app and the MCP server are two commands of the same package, and both import from `core/`.

## Trade-off

- The boundary between `core/` and the entry points is a folder convention. If `mcp/` imports from `api/`, only code review stops it.
- The MCP server cannot be installed without the rest of the backend.
- Revisit if the MCP server has to be published as its own package, or if imports start crossing the boundary.

## Consequences

- Import rules, checked in every review: `core/` imports nothing from `agent/`, `api/` or `mcp/`. `api/` and `mcp/` never import from each other.
- CI needs one job for the backend and one for the web app.
- The migration tool and where migrations live are a separate decision.
