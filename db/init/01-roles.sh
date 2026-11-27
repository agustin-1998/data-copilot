#!/usr/bin/env bash
# Creates the two application roles. PostgreSQL runs this script only once,
# when the data volume is empty. Roles belong to the whole server, so they are
# created here and not in a migration. Table grants live in the migrations.
set -euo pipefail

psql -v ON_ERROR_STOP=1 \
  --username "$POSTGRES_USER" \
  --dbname "$POSTGRES_DB" \
  -v dbname="$POSTGRES_DB" \
  -v owner_password="$COPILOT_OWNER_PASSWORD" \
  -v reader_password="$COPILOT_READER_PASSWORD" <<'SQL'
-- By default every role (PUBLIC) may connect and create temporary tables.
-- Take that away; each role gets only what it needs below.
REVOKE ALL ON DATABASE :"dbname" FROM PUBLIC;

-- Owner: runs migrations and the seed, and owns every table.
CREATE ROLE copilot_owner LOGIN PASSWORD :'owner_password';
ALTER DATABASE :"dbname" OWNER TO copilot_owner;

-- Reader: the only role the agent uses. It can connect and see the schema.
-- It can read a table only after a migration grants SELECT on that table.
CREATE ROLE copilot_reader LOGIN PASSWORD :'reader_password';
GRANT CONNECT ON DATABASE :"dbname" TO copilot_reader;
GRANT USAGE ON SCHEMA public TO copilot_reader;
SQL
