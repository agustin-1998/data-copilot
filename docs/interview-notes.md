# Interview notes

One line per decision or piece of work, ready to say in an interview: "In my project, I…".

- In my project, I designed one core with two entry points: a local MCP server where the connected agent's own model writes the SQL, and a web app where a LangGraph agent calls a free-tier API, so every safety rule lives in one place. ([ADR 0001](adr/0001-llm-strategy-two-entry-points.md))
- In my project, I kept the core and both entry points in one Python package and drew the boundary with folders instead of separate packages, because it was the cheapest setup for a three-week project; I would move to a uv workspace if the MCP server had to ship on its own. ([ADR 0002](adr/0002-repository-layout.md))
- In my project, I used Alembic with hand-written SQL migrations instead of an ORM, so the schema changes stay explicit and every migration runs inside a PostgreSQL transaction. ([ADR 0004](adr/0004-database-migrations-alembic.md))
