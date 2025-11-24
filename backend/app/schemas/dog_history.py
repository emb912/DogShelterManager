from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class DogHistoryBase(BaseModel):
    field_name: str
    old_value: Optional[str]
    new_value: Optional[str]


class DogHistoryCreate(DogHistoryBase):
    dog_id: int


class DogHistory(DogHistoryBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

