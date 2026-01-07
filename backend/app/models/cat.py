from sqlalchemy import Column, Integer, String, Date, Enum, Boolean
from ..database import Base
import enum


class CatSize(str, enum.Enum):
    """Enum określający możliwe rozmiary kotów.
    
    Attributes:
        small: Mały kot.
        medium: Średni kot.
        large: Duży kot.
    """
    small = "small"
    medium = "medium"
    large = "large"


class CatStatus(str, enum.Enum):
    """Enum określający możliwe statusy kotów w schronisku.
    
    Attributes:
        arrived: Kot aktualnie w schronisku.
        adopted: Kot adoptowany.
        returned: Kot zwrócony po adopcji.
    """
    arrived = "arrived"
    adopted = "adopted"
    returned = "returned"


class Cat(Base):
    """Model ORM reprezentujący kota w bazie danych.
    
    Attributes:
        id: Unikalny identyfikator kota (klucz główny).
        name: Imię kota (wymagane).
        size: Rozmiar kota (wymagane, wartość z CatSize).
        birth_date: Data urodzenia kota (opcjonalne).
        sex: Płeć kota (opcjonalne, max 10 znaków).
        neutered: Czy kot jest wysterylizowany/wykastrowany (wymagane, domyślnie False).
        admitted_date: Data przyjęcia do schroniska (wymagane).
        released_date: Data wypuszczenia ze schroniska (opcjonalne).
        status: Aktualny status kota (wymagane, domyślnie 'arrived').
        indoor_only: Czy kot jest przeznaczony tylko do życia w domu (wymagane, domyślnie False).
    """
    __tablename__ = "cats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    size = Column(Enum(CatSize), nullable=False)
    birth_date = Column(Date)
    sex = Column(String(10))
    neutered = Column(Boolean, nullable=False, default=False)
    admitted_date = Column(Date, nullable=False)
    released_date = Column(Date)
    status = Column(Enum(CatStatus), nullable=False, default=CatStatus.arrived)
    indoor_only = Column(Boolean, nullable=False, default=False)
