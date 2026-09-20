from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

from app.core.app_config import AppConfig


def create_mysql_engine(
    config: AppConfig
) -> Engine:
    mysql = config.mysql

    url = (
        f"mysql+pymysql://"
        f"{mysql.username}:{mysql.password}"
        f"@{mysql.host}:{mysql.port}"
        f"/{mysql.database}"
        f"?charset={mysql.charset}"
    )

    return create_engine(
        url,
        pool_pre_ping=True,
        pool_recycle=3600,
        pool_size=10,
        max_overflow=20,
    )


def create_session_factory(
    engine: Engine
):
    return sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )