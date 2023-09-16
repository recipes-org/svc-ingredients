from __future__ import annotations
import os

from sqlalchemy import MetaData, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column

from ingredients import domain


metadata_obj = MetaData(schema=os.environ.get("INGREDIENTS_SCHEMA_NAME"))


class Base(AsyncAttrs, DeclarativeBase):
    metadata = metadata_obj


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = mapped_column(String(255), primary_key=True)
    name = mapped_column(String(255), nullable=False)

    @classmethod
    def from_domain(cls, ingredient: domain.IngredientInDB) -> Ingredient:
        return cls(**(ingredient.model_dump()))
