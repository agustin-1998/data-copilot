# 0004. Database migrations: Alembic with hand-written SQL

- **Status:** Accepted
- **Date:** 2026-11-27

> I chose Alembic with every migration written in plain SQL through `op.execute`, because it is the standard migration tool next to FastAPI, it maps one to one with Laravel migrations, and it keeps the SQL visible; what I pay is an extra dependency (SQLAlchemy) and no autogenerate, so I write every migration by hand; if the project grows an ORM model layer, I turn autogenerate on.

## Context

The database schema has to evolve in versioned, ordered steps that anyone can replay. Week 3 needs a real expand-and-contract migration, so the schema cannot be a single file loaded once. The agent works with raw SQL, so there are no ORM models. PostgreSQL supports transactional DDL: a migration that fails halfway is rolled back entirely, which MySQL does not do.

## Options considered

1. **Alembic, with SQL written by hand inside each migration.** The usual tool in the SQLAlchemy and FastAPI ecosystem.
2. **dbmate.** A language-agnostic binary that runs plain `.sql` files with up and down sections.
3. **A `schema.sql` loaded by the Docker init scripts.** Rejected: no versioning, so no expand-and-contract migration.

## Decision

Alembic, configured in `backend/migrations/`. Each migration writes its SQL explicitly with `op.execute`, in both `upgrade()` and `downgrade()`.

## Trade-off

- SQLAlchemy becomes a dependency even though the app does not use its ORM.
- No autogenerate: without models, Alembic cannot detect schema changes, so every migration is written by hand.
- Revisit if the project adds ORM models: autogenerate would then save time.

## Consequences

- Migrations run as `copilot_owner`, which owns every table.
- The migration that creates a table also grants `SELECT` on it to `copilot_reader` when the table is on the allow-list. Access is granted table by table.
- Each migration runs inside a transaction, so a failed migration leaves the schema unchanged.
- Every migration has a working `downgrade()`, tested by running upgrade, downgrade and upgrade again.
