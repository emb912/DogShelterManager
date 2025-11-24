from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional, List
from ..models.dog import DogSize, DogStatus
from .dog_history import DogHistory

class DogBase(BaseModel):
    name: str
    size: DogSize
    birth_date: Optional[date]
    sex: Optional[str]
    neutered: bool
    admitted_date: date
    released_date: Optional[date]
    status: DogStatus

class DogCreate(DogBase):
    pass

class DogUpdate(BaseModel):
    name: Optional[str] = None
    size: Optional[DogSize] = None
    birth_date: Optional[date] = None
    sex: Optional[str] = None
    neutered: Optional[bool] = None
    admitted_date: Optional[date] = None
    released_date: Optional[date] = None
    status: Optional[DogStatus] = None

class Dog(DogBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class DogWithHistory(Dog):
    history: List[DogHistory]