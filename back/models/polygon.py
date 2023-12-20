import datetime

from pydantic import BaseModel

from sqlalchemy import Boolean, Column, Integer, String, DateTime, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PolygonScheme(BaseModel):
    id: int = None
    name: str = None
    status: bool = None



