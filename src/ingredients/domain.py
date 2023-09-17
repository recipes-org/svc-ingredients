from __future__ import annotations
import uuid

from pydantic import BaseModel, ConfigDict


class Ingredient(BaseModel):
    name: str


class IngredientInDB(Ingredient):
    id: str

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_ingredient(cls, ingredient: Ingredient) -> IngredientInDB:
        return cls.model_validate(ingredient.model_dump() | {"id": uuid.uuid4().hex})
