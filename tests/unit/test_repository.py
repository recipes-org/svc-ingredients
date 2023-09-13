import pytest

from recipes.config import Config
from recipes.repository import (
    Repository,
    SQLAlchemyRepository,
    create_repository,
)


@pytest.mark.parametrize("repo", (SQLAlchemyRepository,))
def test_repository_not_initialised(repo: type[Repository]) -> None:
    with pytest.raises(RuntimeError):
        repo()


@pytest.mark.asyncio
@pytest.mark.parametrize("repo", (SQLAlchemyRepository,))
async def test_repository_initialise(repo: type[Repository]) -> None:
    repo.session_factory = None
    await repo.initialise(Config())
    repo.session_factory = None


def test_create_non_existent_uow() -> None:
    with pytest.raises(ValueError):
        create_repository("Nigel Thornberry")
