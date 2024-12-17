"""SQL operation"""

from typing import List, Literal, Optional, Tuple

from loguru import logger
from sqlalchemy import and_
from starlette import status

from app.database.base import BaseDao, get_db_dsn

class SQLDAO(BaseDao):
    """SQL DAO"""

    def __init__(self):
        """init"""
        super().__init__(db_dsn=get_db_dsn())

    def create_user(
        self,
        username: str,
        password: str,
    ) -> UserModel:
        """
        add new user
        """

        db_user = UserModel(username, password)

        with self.get_session() as session:
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
        return db_user