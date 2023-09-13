import pytest

from recipes.uow import create_unit_of_work, SessionUnitOfWork


@pytest.mark.asyncio
async def test_uow_not_initialised() -> None:
    with pytest.raises(RuntimeError):
        async with SessionUnitOfWork():
            pass


def test_create_non_existant_uow() -> None:
    with pytest.raises(ValueError):
        create_unit_of_work("NigelThornberry")
