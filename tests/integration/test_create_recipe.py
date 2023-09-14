import httpx
import pytest

from ingredients.domain import Ingredient


@pytest.mark.asyncio
async def test_create_recipe() -> None:
    data = Ingredient.model_validate(
        {
            "name": "Spinach"
        }
    )
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "http://localhost:8008/ingredient/", json=data.model_dump()
        )

    assert resp.status_code == 201
