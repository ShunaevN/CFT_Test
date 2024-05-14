from datetime import datetime, timedelta

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import (Table, Column, Integer, String,
                        TIMESTAMP, ForeignKey, Boolean)

from database import Base, metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.now()),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
    Column("surname", String, nullable=False),
    Column("name", String, nullable=False),
)

tokens = Table(
    "tokens",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("access_token", String, unique=True, nullable=False),
    Column("user_id", ForeignKey(users.c.id), unique=True,)
)

employees = Table(
    "employees",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("id_user", Integer,  ForeignKey(users.c.id), primary_key=True),
    Column("salary", Integer, nullable=False),
    Column("next_grade_in", TIMESTAMP,
           default=datetime.now() + timedelta(weeks=8), nullable=False)
)


class Users(SQLAlchemyBaseUserTable[int], Base):
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow())
    name: str = Column(String(length=1024), nullable=False)
    surname: str = Column(String(length=1024), nullable=False)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
