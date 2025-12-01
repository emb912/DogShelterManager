from sqlalchemy import Column, Integer, String, Date, Enum, Boolean
from ..database import Base
import enum

class DogSize(str, enum.Enum):
    """Enum określający możliwe rozmiary psów.
    
    Attributes:
        small: Mały pies.
        medium: Średni pies.
        large: Duży pies.
    """
    small = "small"
    medium = "medium"
    large = "large"

class DogStatus(str, enum.Enum):
    """Enum określający możliwe statusy psów w schronisku.
    
    Attributes:
        arrived: Pies aktualnie w schronisku.
        adopted: Pies adoptowany.
        returned: Pies zwrócony po adopcji.
    """
    arrived = "arrived"
    adopted = "adopted"
    returned = "returned"

class Dog(Base):
    """Model ORM reprezentujący psa w bazie danych.
    
    Attributes:
        id: Unikalny identyfikator psa (klucz główny).
        name: Imię psa (wymagane).
        size: Rozmiar psa (wymagane, wartość z DogSize).
        birth_date: Data urodzenia psa (opcjonalne).
        sex: Płeć psa (opcjonalne, max 10 znaków).
        neutered: Czy pies jest wysterylizowany/wykastrowany (wymagane, domyślnie False).
        admitted_date: Data przyjęcia do schroniska (wymagane).
        released_date: Data wypuszczenia ze schroniska (opcjonalne).
        status: Aktualny status psa (wymagane, domyślnie 'arrived').
    """
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

