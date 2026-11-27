"""Alembic environment: migrations always run as the owner role."""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

from data_copilot.config import get_settings

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Migrations are written by hand in SQL (ADR 0004), so there is no ORM
# metadata and no autogenerate.
target_metadata = None


def run_migrations_offline() -> None:
    """Print the SQL instead of running it (`alembic upgrade head --sql`)."""
    context.configure(
        url=get_settings().owner_url().render_as_string(hide_password=False),
        target_metadata=target_metadata,
        literal_binds=True,
        transaction_per_migration=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run the migrations against the database, one transaction per migration."""
    engine = create_engine(get_settings().owner_url(), poolclass=pool.NullPool)
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            transaction_per_migration=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
