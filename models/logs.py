import uuid
from typing import Optional
from pydantic import BaseModel, Field
import datetime


class Log(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    machine_id: int = Field()
    data: str = Field()
    date_time: datetime = Field()

