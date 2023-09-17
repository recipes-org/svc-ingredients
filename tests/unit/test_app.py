import pytest
from httpx import AsyncClient

from ingredients import domain


@pytest.mark.asyncio
async def test_sanity(in_memory_db_app_client: AsyncClient) -> None:
    resp = await in_memory_db_app_client.get("/v1/ingredients/")
    assert resp.status_code == 200, resp
    assert resp.json() == [], resp.json()


@pytest.mark.asyncio
async def test_ingredient_round_trip(
    in_memory_db_app_client: AsyncClient,
    ingredient: domain.Ingredient,
) -> None:
    data = ingredient.model_dump()

    resp = await in_memory_db_app_client.post("/v1/ingredients/", json=data)
    assert resp.status_code == 201, resp.json()

    created_ingredient = domain.IngredientInDB.model_validate(resp.json())
    assert created_ingredient.id
    assert created_ingredient.name == ingredient.name

    resp = await in_memory_db_app_client.get(f"/v1/ingredients/{created_ingredient.id}")
    assert resp.status_code == 200, resp.json()

    got = domain.IngredientInDB.model_validate(resp.json())

    assert got == created_ingredient


@pytest.mark.asyncio
async def test_invalid_ingredient(in_memory_db_app_client: AsyncClient) -> None:
    resp = await in_memory_db_app_client.post("/v1/ingredients/", json={})
    assert resp.status_code == 422, resp


async def test_problem_committing(
    in_memory_db_app_cannot_commit_client: AsyncClient,
    ingredient: domain.Ingredient,
) -> None:
    data = ingredient.model_dump()
    resp = await in_memory_db_app_cannot_commit_client.post(
        "/v1/ingredients/", json=data
    )
    assert resp.status_code > 400, resp.json()


@pytest.mark.asyncio
async def test_problem_listing(
    in_memory_db_app_cannot_list_client: AsyncClient,
) -> None:
    resp = await in_memory_db_app_cannot_list_client.get("/v1/ingredients/")
    assert resp.status_code > 400, resp.json()


@pytest.mark.asyncio
async def test_problem_getting(
    in_memory_db_app_cannot_get_client: AsyncClient,
    ingredient: domain.Ingredient,
) -> None:
    data = ingredient.model_dump()
    resp = await in_memory_db_app_cannot_get_client.post("/v1/ingredients/", json=data)
    got = domain.IngredientInDB.model_validate(resp.json())
    resp = await in_memory_db_app_cannot_get_client.get(f"/v1/ingredients/{got.id}")
    assert resp.status_code > 400, resp.json()
