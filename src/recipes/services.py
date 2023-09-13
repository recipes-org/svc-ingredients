import logging

from recipes import domain
from recipes.uow import UnitOfWork


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

    async def get_recipes(self) -> list[domain.RecipeInDB]:
        async with self.unit_of_work() as uow:
            recipes = await uow.recipes.list()
        logger.info("Got %r recipes", len(recipes))
        return recipes

    async def create_recipe(self, recipe: domain.Recipe) -> domain.RecipeInDB:
        async with self.unit_of_work() as uow:
            recipe_in_db = await uow.recipes.add(recipe)
            await uow.commit()
        logger.info("Created %r", recipe_in_db)
        return recipe_in_db

    async def get_recipe(self, recipe_id: str) -> domain.RecipeInDB:
        async with self.unit_of_work() as uow:
            recipe = await uow.recipes.get(recipe_id=recipe_id)
        logger.info("Got %r", recipe)
        return recipe
