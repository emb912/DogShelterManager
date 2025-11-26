from sqlalchemy import Column, Integer, String, Date, Enum, Boolean
from ..database import Base
import enum

class DogSize(str, enum.Enum):
    small = "small"
    medium = "medium"
    large = "large"

class DogStatus(str, enum.Enum):
    arrived = "arrived"
    adopted = "adopted"
    returned = "returned"

class Dog(Base):
    __tablename__ = "dogs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    size = Column(Enum(DogSize), nullable=False)
    birth_date = Column(Date)
    sex = Column(String(10))
    neutered = Column(Boolean, nullable=False, default=False)
    admitted_date = Column(Date, nullable=False)
    released_date = Column(Date)
    status = Column(Enum(DogStatus), nullable=False, default=DogStatus.arrived)

