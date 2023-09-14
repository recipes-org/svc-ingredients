from typing import Any

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    debug: bool = False
    database_url: str = "sqlite+aiosqlite://"
    ingredients_router_prefix: str = "/v1"
    ingredients_repository_name: str = "SQLAlchemyRepository"
    ingredients_sql_alchemy_database_create: bool = False
    ingredients_unit_of_work_name: str = "SessionUnitOfWork"

    @field_validator("database_url")
    @classmethod
    def database_url_add_async_driver(cls, v: str) -> str:
        driver, *parts = v.split(":")
        if driver.startswith("postgresql") and not driver.endswith("asyncpg"):
            driver = "postgresql+asyncpg"
        return ":".join([driver] + parts)

    @field_validator("database_url")
    @classmethod
    def database_url_replace_sslmode(cls, v: str) -> str:
        if v.lower().startswith("postgresql") and "?" in v:
            *parts, params = v.split("?")
            params = params.replace("sslmode=", "ssl=")
            v = "?".join(parts + [params])
        return v

    def log_safe_model_dump(self) -> dict[str, Any]:
        return {
            k: v for k, v in self.model_dump().items() if not k.endswith("database_url")
        }
