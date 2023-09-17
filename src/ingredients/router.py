import logging

from fastapi import APIRouter, HTTPException

from ingredients.config import Config
from ingredients import domain
from ingredients.services import Services

logger = logging.getLogger(__name__)


CFG = Config()

router = APIRouter(prefix=CFG.ingredients_router_prefix)


@router.get("/ingredients/")
async def get_ingredients() -> list[domain.IngredientInDB]:
    try:
        return await Services().get_ingredients()
    except Exception as e:
        logger.error("%r", e)
        msg = "Could not get ingredients."
        raise HTTPException(500, f"{msg} {e}" if CFG.debug else msg) from e


@router.post("/ingredients/", status_code=201)
async def create_ingredient(ingredient: domain.Ingredient) -> domain.IngredientInDB:
    logger.info("ingredient=%r", ingredient)
    try:
        return await Services().create_ingredient(ingredient=ingredient)
    except Exception as e:
        logger.error("%r", e)
        msg = "Could not create ingredient."
        raise HTTPException(500, f"{msg} {e}" if CFG.debug else msg) from e


@router.get("/ingredients/{ingredient_id}")
async def get_ingredient(ingredient_id: str) -> domain.IngredientInDB:
    logger.info("ingredient_id=%s", ingredient_id)
    try:
        return await Services().get_ingredient(ingredient_id=ingredient_id)
    except Exception as e:
        logger.error("%r", e)
        msg = "Could not get ingredient."
        raise HTTPException(500, f"{msg} {e}" if CFG.debug else msg) from e
