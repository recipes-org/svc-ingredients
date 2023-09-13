from httpx import AsyncClient
import pytest


from recipes import domain


@pytest.mark.asyncio
async def test_sanity(in_memory_db_app_client: AsyncClient) -> None:
    resp = await in_memory_db_app_client.get("/recipes/")
    assert resp.status_code == 200, resp
    assert resp.json() == [], resp.json()


@pytest.mark.asyncio
async def test_recipe_round_trip(
    in_memory_db_app_client: AsyncClient,
    recipe_with_requirements: domain.Recipe,
) -> None:
    data = recipe_with_requirements.model_dump()

    resp = await in_memory_db_app_client.post("/recipes/", json=data)
    assert resp.status_code == 201, resp.json()

    created_recipe = domain.RecipeInDB.model_validate(resp.json())
    assert created_recipe.id
    assert created_recipe.name == recipe_with_requirements.name
    assert all(
        og.ingredient == db.ingredient and db.recipe_id
        for og, db in zip(
            recipe_with_requirements.requirements, created_recipe.requirements
        )
    )

    resp = await in_memory_db_app_client.get(f"/recipes/{created_recipe.id}")
    assert resp.status_code == 200, resp.json()

    got = domain.RecipeInDB.model_validate(resp.json())

    assert got == created_recipe


@pytest.mark.asyncio
async def test_invalid_recipe(in_memory_db_app_client: AsyncClient) -> None:
    data = {"name": "no"}
    resp = await in_memory_db_app_client.post("/recipes/", json=data)
    assert resp.status_code == 422, resp.json()


@pytest.mark.asyncio
async def test_problem_committing(
    in_memory_db_app_cannot_commit_client: AsyncClient,
    recipe_with_requirements: domain.Recipe,
) -> None:
    data = recipe_with_requirements.model_dump()
    resp = await in_memory_db_app_cannot_commit_client.post("/recipes/", json=data)
    assert resp.status_code > 400, resp.json()


@pytest.mark.asyncio
async def test_problem_listing(
    in_memory_db_app_cannot_list_client: AsyncClient,
) -> None:
    resp = await in_memory_db_app_cannot_list_client.get("/recipes/")
    assert resp.status_code > 400, resp.json()


@pytest.mark.asyncio
async def test_problem_getting(
    in_memory_db_app_cannot_get_client: AsyncClient,
    recipe_with_requirements: domain.Recipe,
) -> None:
    data = recipe_with_requirements.model_dump()
    resp = await in_memory_db_app_cannot_get_client.post("/recipes/", json=data)
    got = domain.RecipeInDB.model_validate(resp.json())
    resp = await in_memory_db_app_cannot_get_client.get(f"/recipes/{got.id}")
    assert resp.status_code > 400, resp.json()
