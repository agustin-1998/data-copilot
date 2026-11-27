# Interview notes

One line per decision or piece of work, ready to say in an interview: "In my project, I…".

- In my project, I designed one core with two entry points: a local MCP server where the connected agent's own model writes the SQL, and a web app where a LangGraph agent calls a free-tier API, so every safety rule lives in one place. ([ADR 0001](adr/0001-llm-strategy-two-entry-points.md))
- In my project, I kept the core and both entry points in one Python package and drew the boundary with folders instead of separate packages, because it was the cheapest setup for a three-week project; I would move to a uv workspace if the MCP server had to ship on its own. ([ADR 0002](adr/0002-repository-layout.md))
- In my project, I used a real e-commerce dataset (Olist, about 100k orders) and added synthetic names, emails and phones to it, so I could prove the model never sees personal data; the seed pins the dataset with a SHA-256 checksum and Faker with a fixed seed, so every machine gets the same database. ([ADR 0003](adr/0003-sample-dataset-olist.md))
- In my project, I used Alembic with hand-written SQL migrations instead of an ORM, so the schema changes stay explicit and every migration runs inside a PostgreSQL transaction. ([ADR 0004](adr/0004-database-migrations-alembic.md))
