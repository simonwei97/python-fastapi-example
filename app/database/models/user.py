"""
User Model
"""

from sqlalchemy import VARCHAR, Column, DateTime, Index, Integer, func

from app.database.models.base import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(
        "id",
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True,
        comment="auto increment pk",
    )

    username = Column(
        "username",
        VARCHAR(length=255),
        nullable=False,
        unique=True,
        comment="user name",
    )

    password = Column(
        "password",
        VARCHAR(length=255),
        nullable=False,
        comment="user password",
    )

    created_at = Column(
        "created_at",
        DateTime,
        default=func.now(),
        nullable=True,
        comment="create time",
    )
    updated_at = Column(
        "updated_at",
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=True,
        comment="update time",
    )

    __table_args__ = (
        Index("idx_created_at", "created_at"),
    )