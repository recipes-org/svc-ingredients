from recipes.config import Config


def test_config_database_url_async_driver() -> None:
    cfg = Config(database_url="postgresql://...:...")
    assert cfg.database_url == "postgresql+asyncpg://...:..."


def test_config_database_url_sslmode() -> None:
    cfg = Config(database_url="postgresql+asyncpg://...?...?sslmode=require")
    assert cfg.database_url == "postgresql+asyncpg://...?...?ssl=require"
