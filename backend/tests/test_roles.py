"""copilot_reader is the agent's only connection: it reads granted tables and nothing else."""

from collections.abc import Iterator

import psycopg
import pytest
from psycopg.errors import InsufficientPrivilege

PROBE_TABLE = "probe_permissions"


@pytest.fixture
def probe_table(owner: psycopg.Connection) -> Iterator[str]:
    """A table owned by copilot_owner, with no grant to the reader."""
    owner.execute(f"DROP TABLE IF EXISTS {PROBE_TABLE}")  # leftover from a killed run
    owner.execute(f"CREATE TABLE {PROBE_TABLE} (id int)")
    yield PROBE_TABLE
    owner.execute(f"DROP TABLE IF EXISTS {PROBE_TABLE}")


def test_reader_connects_as_itself(reader: psycopg.Connection) -> None:
    assert reader.execute("SELECT current_user").fetchone() == ("copilot_reader",)


@pytest.mark.parametrize(
    "statement",
    [
        "CREATE TABLE reader_table (id int)",
        "CREATE TEMP TABLE reader_temp (id int)",
    ],
)
def test_reader_cannot_create_tables(reader: psycopg.Connection, statement: str) -> None:
    with pytest.raises(InsufficientPrivilege):
        reader.execute(statement)


@pytest.mark.parametrize(
    "statement",
    [
        "SELECT * FROM {table}",
        "INSERT INTO {table} VALUES (1)",
        "UPDATE {table} SET id = 2",
        "DELETE FROM {table}",
    ],
)
def test_reader_cannot_touch_a_table_without_a_grant(
    reader: psycopg.Connection, probe_table: str, statement: str
) -> None:
    with pytest.raises(InsufficientPrivilege):
        reader.execute(statement.format(table=probe_table))


def test_a_grant_allows_select_but_never_writes(
    owner: psycopg.Connection, reader: psycopg.Connection, probe_table: str
) -> None:
    owner.execute(f"GRANT SELECT ON {probe_table} TO copilot_reader")

    assert reader.execute(f"SELECT count(*) FROM {probe_table}").fetchone() == (0,)
    with pytest.raises(InsufficientPrivilege):
        reader.execute(f"INSERT INTO {probe_table} VALUES (1)")
