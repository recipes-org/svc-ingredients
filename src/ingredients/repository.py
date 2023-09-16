from typing import Any, Protocol

from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from ingredients import config, domain, orm


class Repository(Protocol):
    """Ingredient repository protocol."""

    session_factory: async_sessionmaker[AsyncSession] | None
    session: AsyncSession

    @classmethod
    async def initialise(cls, cfg: config.Config) -> None: ...

    async def add(self, ingredient: domain.Ingredient) -> domain.IngredientInDB: ...

    async def get(self, ingredient_id: str) -> domain.IngredientInDB: ...

    async def list(self) -> list[domain.IngredientInDB]: ...


class SQLAlchemyRepository:
    """SQLAlchemy implementation of the ingredient repository protocol."""

    engine: AsyncEngine | None = None
    session_factory: async_sessionmaker[AsyncSession] | None = None

    @classmethod
    async def initialise(cls, cfg: config.Config) -> None:
        kwargs: dict[str, Any] = {}
        if "sqlite" in cfg.database_url.lower():  # pragma: no cover
            kwargs = kwargs | {"check_same_thread": False}
        engine = create_async_engine(
            cfg.database_url,
            connect_args=kwargs,
            echo=cfg.debug,
        )

        cls.engine = engine
        cls.session_factory = async_sessionmaker(
            autocommit=False, autoflush=False, bind=engine
        )
        if cfg.ingredients_sql_alchemy_database_create:
            async with cls.engine.begin() as conn:
                await conn.run_sync(orm.Base.metadata.create_all)

    def __init__(self) -> None:
        if self.session_factory is None:
            raise RuntimeError(f"{self.__class__.__name__} not initialised.")
        self.session = self.session_factory()

    async def add(self, ingredient: domain.Ingredient) -> domain.IngredientInDB:
        ingredient_in_db = domain.IngredientInDB.from_ingredient(ingredient)
        orm_ingredient = orm.Ingredient.from_domain(ingredient_in_db)
        self.session.add(orm_ingredient)
        return ingredient_in_db

    async def get(self, ingredient_id: str) -> domain.IngredientInDB:
        stmt = select(orm.Ingredient).where(orm.Ingredient.id == ingredient_id)
        orm_ingredient = await self.session.execute(stmt)
        return domain.IngredientInDB.model_validate(orm_ingredient.scalar_one())

    async def list(self) -> list[domain.IngredientInDB]:
        stmt = select(orm.Ingredient)
        orm_ingredients = (await self.session.execute(stmt)).scalars().all()
        return [domain.IngredientInDB.model_validate(o) for o in orm_ingredients]


REPOSITORIES = {
    "sqlalchemyrepository": SQLAlchemyRepository,
}


def create_repository(name: str) -> type[Repository]:
    name = name.lower()
    if name not in REPOSITORIES:
        raise ValueError(f"Unknown repository '{name}'")
    return REPOSITORIES[name]
