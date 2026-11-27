"""Shared fixtures: one database connection per role, closed after each test."""

from collections.abc import Iterator

import psycopg
import pytest

from data_copilot.config import OWNER_ROLE, READER_ROLE, get_settings


@pytest.fixture
def owner() -> Iterator[psycopg.Connection]:
    with psycopg.connect(**get_settings().connect_kwargs(OWNER_ROLE), autocommit=True) as conn:
        yield conn


@pytest.fixture
def reader() -> Iterator[psycopg.Connection]:
    with psycopg.connect(**get_settings().connect_kwargs(READER_ROLE), autocommit=True) as conn:
        yield conn
