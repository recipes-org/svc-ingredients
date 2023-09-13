import httpx
import pytest

from recipes.domain import Recipe


@pytest.mark.asyncio
async def test_create_recipe() -> None:
    data = Recipe.model_validate(
        {
            "name": "Rustica",
            "requirements": [
                {"ingredient": "spinach", "measurement": "grams", "quantity": 500}
            ],
        }
    )
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "http://localhost:8008/recipes/", json=data.model_dump()
        )

    assert resp.status_code == 201
