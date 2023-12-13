import datetime

from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserDB(Base):
    __tablename__ = "app_users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    description = Column(String, index=True)
    hashed_password = Column(String, nullable=False)


class TokenHistory(Base):
    __tablename__ = "token_history"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    token = Column(String, unique=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
