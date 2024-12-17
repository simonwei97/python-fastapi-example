"""
Base DAOs
"""

import os
from abc import ABC
from typing import Any
from urllib.parse import quote_plus

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


class BaseDao(ABC):
    """Interface for base db DAOs table"""

    def __init__(
        self,
        db_dsn: str,
        enable_repeatable_read: bool = True, 
    ) -> None:
        """
        Init DAOs
        """
        self.async_engine = create_async_db_engine(db_dsn, enable_repeatable_read)
        self.async_session = sessionmaker(
            bind=self.async_engine,
            autoflush=False,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        self.db_session: AsyncSession

    def get_async_session(self) -> AsyncSession:
        """get session"""
        return self.async_session()

    def __enter__(self) -> AsyncSession:
        """enter"""
        self.db_session = self.get_async_session()
        return self.db_session

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """close"""
        self.db_session.close()


def get_db_dsn() -> str:
    """get"""
    user = os.environ.get("MYSQL_USERNAME", "root")
    passwd = os.environ.get("MYSQL_PASSWORD", "root")
    database_name = os.environ.get("MYSQL_DATABASE", "app_db_name")
    address = os.environ.get("MYSQL_ADDRESS", "localhost:3306")
    return _get_db_dsn_str(user, passwd, address, database_name)


def _get_db_dsn_str(
    user: str,
    passwd: str,
    address: str,
    database_name: str,
    passwd_url_encod: bool = True,
) -> str:
    """
    get db dsn
    """
    if passwd_url_encod:
        passwd = quote_plus(passwd)
    # url: dialect[+driver]://user:password@host/dbname[?key=value..]
    return f"mysql+aiomysql://{user}:{passwd}@{address}/{database_name}?charset=utf8mb4"


def create_async_db_engine(
    db_url: str,
    enable_repeatable_read: bool = True,
) -> AsyncEngine:
    """create async db engine"""
    logger.debug("connect to {}", db_url)
    if enable_repeatable_read:
        async_engine = create_async_engine(
            url=db_url,
            isolation_level="REPEATABLE READ",  # set isolation as RR
            echo=True,
            future=True,
            pool_size=5,
            pool_recycle=3600,
        )
    else:
        async_engine = create_async_engine(
            url=db_url,
            echo=True,
            future=True,
            pool_size=5,
            pool_recycle=3600,
        )
    return async_engine
