import logging

from fastapi import APIRouter, HTTPException

from recipes import domain
from recipes.services import Services

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/recipes/")
async def get_recipes() -> list[domain.RecipeInDB]:
    try:
        return await Services().get_recipes()
    except Exception as e:
        logger.error("%r", e)
        raise HTTPException(500, "Could not get recipes") from e


@router.post("/recipes/", status_code=201)
async def create_recipe(recipe: domain.Recipe) -> domain.RecipeInDB:
    logger.info("recipe=%r", recipe)
    try:
        return await Services().create_recipe(recipe=recipe)
    except Exception as e:
        logger.error("%r", e)
        raise HTTPException(500, "Could not create recipe") from e


@router.get("/recipes/{recipe_id}")
async def get_recipe(recipe_id: str) -> domain.RecipeInDB:
    logger.info("recipe_id=%s", recipe_id)
    try:
        return await Services().get_recipe(recipe_id=recipe_id)
    except Exception as e:
        logger.error("%r", e)
        raise HTTPException(500, "Could not get recipe") from e
