"""Settings read from environment variables and from the repository's .env file."""

from functools import lru_cache
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

# backend/src/data_copilot/config.py -> repository root
REPO_ROOT = Path(__file__).resolve().parents[3]

OWNER_ROLE = "copilot_owner"
READER_ROLE = "copilot_reader"


class Settings(BaseSettings):
    """Environment variables win over values in .env."""

    model_config = SettingsConfigDict(env_file=REPO_ROOT / ".env", extra="ignore")

    database_host: str = "localhost"
    database_port: int = 5432
    database_name: str = "copilot"
    copilot_owner_password: SecretStr
    copilot_reader_password: SecretStr

    def owner_url(self) -> URL:
        """Connection for migrations and the seed. The agent never uses it."""
        return self._url(OWNER_ROLE, self.copilot_owner_password)

    def reader_url(self) -> URL:
        """Read-only connection: the only one the agent uses."""
        return self._url(READER_ROLE, self.copilot_reader_password)

    def _url(self, role: str, password: SecretStr) -> URL:
        return URL.create(
            "postgresql+psycopg",
            username=role,
            password=password.get_secret_value(),
            host=self.database_host,
            port=self.database_port,
            database=self.database_name,
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
