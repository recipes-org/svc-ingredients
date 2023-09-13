from typing import Any, AsyncGenerator, Generator

from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
import pytest
import pytest_asyncio

from recipes import domain
from recipes.app import create_app
from recipes.config import Config
from recipes.repository import (
    Repository,
    SQLAlchemyRepository,
)
from recipes.services import Services
from recipes.uow import SessionUnitOfWork, UnitOfWork


@pytest.fixture
def recipe() -> domain.Recipe:
    return domain.Recipe(name="Rustica", requirements=[])


@pytest.fixture
def recipe_with_requirements(recipe: domain.Recipe) -> domain.Recipe:
    recipe.requirements = [
        domain.Requirement(ingredient="spinach", measurement="grams", quantity=500.0),
        domain.Requirement(
            ingredient="short-crust pastry", measurement="grams", quantity=500.0
        ),
    ]
    return recipe


@pytest.fixture
def in_memory_db_config() -> Generator[Config, Any, Any]:
    yield Config(
        recipes_repository_name="SQLAlchemyRepository",
        database_url="sqlite+aiosqlite://",
        recipes_sql_alchemy_database_create=True,
    )
    SQLAlchemyRepository.session_factory = None
    SessionUnitOfWork.repository_cls = None
    Services.unit_of_work_cls = None


@pytest.fixture
def unit_of_work_cannot_commit() -> type[UnitOfWork]:
    class SessionUnitOfWorkCannotCommit(SessionUnitOfWork):
        async def commit(self) -> None:
            raise ValueError(":(")

    return SessionUnitOfWorkCannotCommit


@pytest.fixture
def repository_cannot_list() -> type[Repository]:
    class SQLAlchemyRepositoryCannotList(SQLAlchemyRepository):
        async def list(self) -> list[domain.RecipeInDB]:
            raise ValueError(":(")

    return SQLAlchemyRepositoryCannotList


@pytest.fixture
def repository_cannot_get() -> type[Repository]:
    class SQLAlchemyRepositoryCannotGet(SQLAlchemyRepository):
        async def get(self, recipe_id: str) -> domain.RecipeInDB:
            raise ValueError(":(")

    return SQLAlchemyRepositoryCannotGet


@pytest.fixture
def in_memory_db_app(in_memory_db_config: Config) -> FastAPI:
    return create_app(cfg=in_memory_db_config)


@pytest.fixture
def in_memory_db_app_cannot_commit(
    in_memory_db_config: Config,
    unit_of_work_cannot_commit: type[UnitOfWork],
) -> FastAPI:
    return create_app(
        cfg=in_memory_db_config,
        unit_of_work_cls=unit_of_work_cannot_commit,
    )


@pytest.fixture
def in_memory_db_app_cannot_list(
    in_memory_db_config: Config,
    repository_cannot_list: type[Repository],
) -> FastAPI:
    return create_app(
        cfg=in_memory_db_config,
        repository_cls=repository_cannot_list,
    )


@pytest.fixture
def in_memory_db_app_cannot_get(
    in_memory_db_config: Config,
    repository_cannot_get: type[Repository],
) -> FastAPI:
    return create_app(
        cfg=in_memory_db_config,
        repository_cls=repository_cannot_get,
    )


@pytest_asyncio.fixture
async def in_memory_db_app_client(
    in_memory_db_app: FastAPI,
) -> AsyncGenerator[AsyncClient, Any]:
    app = in_memory_db_app
    url = "http://test"
    async with AsyncClient(app=app, base_url=url) as client, LifespanManager(app):
        yield client


@pytest_asyncio.fixture
async def in_memory_db_app_cannot_commit_client(
    in_memory_db_app_cannot_commit: FastAPI,
) -> AsyncGenerator[AsyncClient, Any]:
    app = in_memory_db_app_cannot_commit
    url = "http://test"
    async with AsyncClient(app=app, base_url=url) as client, LifespanManager(app):
        yield client


@pytest_asyncio.fixture
async def in_memory_db_app_cannot_list_client(
    in_memory_db_app_cannot_list: FastAPI,
) -> AsyncGenerator[AsyncClient, Any]:
    app = in_memory_db_app_cannot_list
    url = "http://test"
    async with AsyncClient(app=app, base_url=url) as client, LifespanManager(app):
        yield client


@pytest_asyncio.fixture
async def in_memory_db_app_cannot_get_client(
    in_memory_db_app_cannot_get: FastAPI,
) -> AsyncGenerator[AsyncClient, Any]:
    app = in_memory_db_app_cannot_get
    url = "http://test"
    async with AsyncClient(app=app, base_url=url) as client, LifespanManager(app):
        yield client
