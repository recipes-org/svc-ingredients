import logging

from fastapi import FastAPI

from recipes import config
from recipes import repository
from recipes import router
from recipes import services
from recipes import uow

logger = logging.getLogger(__name__)


def create_app(
    cfg: config.Config | None = None,
    repository_cls: type[repository.Repository] | None = None,
    unit_of_work_cls: type[uow.UnitOfWork] | None = None,
) -> FastAPI:
    """App factory.

    Initialise repository, unit-of-work, and services according to the config.

    Arguments:
        cfg: Configuration for the app.
        repository_cls: Repository class to use for the app. For testing.
        unit_of_work_cls: Unit of work class to use for the app. For testing.

    Examples:
        >>> app = create_app()

    """
    # Idea here is we want the config to be loaded up once, at the same time.
    # I.e., import config only appears in this file.
    cfg = config.Config() if cfg is None else cfg

    app = FastAPI(debug=cfg.recipes_debug)
    app.include_router(router.router)

    logger.info("Config: %s", cfg.log_safe_model_dump())

    repository_cls = (
        repository.create_repository(cfg.recipes_repository_name)
        if repository_cls is None
        else repository_cls
    )
    unit_of_work_cls = (
        uow.create_unit_of_work(cfg.recipes_unit_of_work_name)
        if unit_of_work_cls is None
        else unit_of_work_cls
    )

    async def initialise() -> None:
        await repository_cls.initialise(cfg)
        unit_of_work_cls.initialise(repository_cls)
        services.Services.initialise(unit_of_work_cls)

    app.add_event_handler("startup", initialise)

    return app
