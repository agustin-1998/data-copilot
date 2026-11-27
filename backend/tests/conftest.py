"""Shared fixtures: one database connection per role, closed after each test."""

from collections.abc import Iterator

import psycopg
import pytest
from pydantic import SecretStr

from data_copilot.config import OWNER_ROLE, READER_ROLE, get_settings


def _connect(role: str, password: SecretStr) -> psycopg.Connection:
    settings = get_settings()
    return psycopg.connect(
        host=settings.database_host,
        port=settings.database_port,
        dbname=settings.database_name,
        user=role,
        password=password.get_secret_value(),
        autocommit=True,
    )


@pytest.fixture
def owner() -> Iterator[psycopg.Connection]:
    with _connect(OWNER_ROLE, get_settings().copilot_owner_password) as conn:
        yield conn


@pytest.fixture
def reader() -> Iterator[psycopg.Connection]:
    with _connect(READER_ROLE, get_settings().copilot_reader_password) as conn:
        yield conn
