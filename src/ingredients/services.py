import logging

from ingredients import domain
from ingredients.uow import UnitOfWork


logger = logging.getLogger(__name__)


class Services:
    unit_of_work_cls: type[UnitOfWork] | None = None

    @classmethod
    def initialise(cls, unit_of_work_cls: type[UnitOfWork]) -> None:
        cls.unit_of_work_cls = unit_of_work_cls

    def unit_of_work(self) -> UnitOfWork:
        if self.unit_of_work_cls is None:
            raise RuntimeError(f"{self.__class__.__name__} not initialised.")
        return self.unit_of_work_cls()

    async def get_ingredients(self) -> list[domain.IngredientInDB]:
        async with self.unit_of_work() as uow:
            ingredients = await uow.ingredients.list()
        logger.info("Got %r ingredients", len(ingredients))
        return ingredients

    async def create_ingredient(
        self, ingredient: domain.Ingredient
    ) -> domain.IngredientInDB:
        async with self.unit_of_work() as uow:
            ingredient_in_db = await uow.ingredients.add(ingredient)
            await uow.commit()
        logger.info("Created %r", ingredient_in_db)
        return ingredient_in_db

    async def get_ingredient(self, ingredient_id: str) -> domain.IngredientInDB:
        async with self.unit_of_work() as uow:
            ingredient = await uow.ingredients.get(ingredient_id=ingredient_id)
        logger.info("Got %r", ingredient)
        return ingredient
