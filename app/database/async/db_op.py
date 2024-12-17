from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError

from app.database.base import BaseDao, get_db_dsn
from app.database.models.users import UserModel


class SQLDAO(BaseDao):
    def __init__(self):
        """init"""
        super().__init__(db_dsn=get_db_dsn())

    async def add_user(
        self,
        username: str,
        password: str,
    ) -> None:
        """
        add new user
        """
        db_user = UserModel(username, password)
        async with self.get_async_session() as session:
            async with session.begin():
                try:
                    session.add(db_user)
                    await session.flush()  # refresh own primary key
                    session.expunge(db_user)  # release data
                    # begin() context will auto commit trancastion
                except SQLAlchemyError as sql_ex:
                    raise sql_ex
        return db_user
