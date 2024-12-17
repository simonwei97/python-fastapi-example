"""
Base DAOs
"""

import os
from abc import ABC
from typing import Any
from urllib.parse import quote_plus

from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, sessionmaker


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
        self.engine = create_db_engine(db_dsn, enable_repeatable_read)
        self.local_session = sessionmaker(
            bind=self.engine,
            autoflush=False,
        )
        self.db_session: Session

    def get_session(self) -> Session:
        """get session"""
        return self.local_session()

    def __enter__(self) -> Session:
        """enter"""
        self.db_session = self.get_session()
        return self.db_session

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """close"""
        self.db_session.close()


def get_db_dsn() -> str:
    """"""
    user = os.environ.get("MYSQL_USERNAME", "root")
    passwd = os.environ.get("MYSQL_PASSWORD", "root")
    database_name = os.environ.get("MYSQL_DATABASE", "app_db_name")
    address = os.environ.get("MYSQL_ADDRESS", "localhost:3306")
    return get_db_dsn_str(user, passwd, address, database_name)

def get_db_dsn_str(
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
    return f"mysql+pymysql://{user}:{passwd}@{address}/{database_name}?charset=utf8mb4"


def create_db_engine(
    db_url: str,
    enable_repeatable_read: bool = True,
) -> Engine:
    """create db engine"""
    logger.debug("connect to {}", db_url)
    if enable_repeatable_read:
        engine = create_engine(
            url=db_url,
            isolation_level="REPEATABLE READ",  # set isolation as RR
            echo=True,
            future=True,
            pool_size=5,
            pool_recycle=3600,
        )
    else:
        engine = create_engine(
            url=db_url,
            echo=True,
            future=True,
            pool_size=5,
            pool_recycle=3600,
        )

    # test connection
    try:
        with engine.connect() as _:
            logger.debug("database connection is valid.")
            return engine
    except OperationalError as op_rr:
        logger.error("database connection failed:", op_rr)
        raise op_rr
