from __future__ import annotations
from typing import Sequence
import uuid

from pydantic import BaseModel, ConfigDict, NonNegativeFloat


class Requirement(BaseModel):
    """Requirement in a [`Recipe`][recipes.domain.Recipe].

    Examples:
        >>> Requirement(
        ...     ingredient="carrot",
        ...     measurement="units",
        ...     quantity=2,
        ... )
        Requirement(ingredient='carrot', measurement='units', quantity=2.0)

    """

    ingredient: str
    measurement: str
    quantity: NonNegativeFloat


class RequirementInDB(Requirement):
    recipe_id: str

    model_config = ConfigDict(
        from_attributes=True,
    )


class Recipe(BaseModel):
    name: str
    requirements: Sequence[Requirement]

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "Rustica",
                    "requirements": [
                        {
                            "ingredient": "Spinach",
                            "measurement": "grams",
                            "quantity": 500,
                        }
                    ],
                }
            ]
        },
    )


class RecipeInDB(Recipe):
    id: str
    requirements: Sequence[RequirementInDB]

    model_config = ConfigDict(
        from_attributes=True,
    )

    @classmethod
    def from_recipe(cls, recipe: Recipe) -> RecipeInDB:
        recipe_id = str(uuid.uuid4().hex)
        return RecipeInDB.model_validate(
            recipe.model_dump()
            | {
                "id": recipe_id,
                "requirements": [
                    RequirementInDB.model_validate(
                        requirement.model_dump()
                        | {"id": str(uuid.uuid4().hex), "recipe_id": recipe_id}
                    )
                    for requirement in recipe.requirements
                ],
            }
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        sdict = self.model_dump()
        odict = other.model_dump()
        sdict["requirements"] = sorted(sorted(r.items()) for r in sdict["requirements"])
        odict["requirements"] = sorted(sorted(r.items()) for r in odict["requirements"])
        return sdict == odict
