from pydantic import BaseModel, ConfigDict, field_validator
from datetime import date
from typing import Optional
from ..models.cat import CatSize, CatStatus


class CatBase(BaseModel):
    """Bazowy schemat Pydantic dla kota.
    
    Zawiera wszystkie wspólne pola używane w różnych operacjach.
    
    Attributes:
        name: Imię kota.
        size: Rozmiar kota (small, medium, large).
        birth_date: Data urodzenia kota (opcjonalne).
        sex: Płeć kota (opcjonalne).
        neutered: Czy kot jest wysterylizowany/wykastrowany.
        admitted_date: Data przyjęcia do schroniska.
        released_date: Data wypuszczenia ze schroniska (opcjonalne).
        status: Status kota (arrived, adopted, returned).
        indoor_only: Czy kot jest przeznaczony tylko do życia w domu.
    """
    name: str
    size: CatSize
    birth_date: Optional[date]
    sex: Optional[str]
    neutered: bool
    admitted_date: date
    released_date: Optional[date]
    status: CatStatus
    indoor_only: bool = False

    @field_validator('birth_date', 'admitted_date', 'released_date')
    @classmethod
    def date_not_in_future(cls, v: Optional[date], info) -> Optional[date]:
        """Waliduje, że data nie jest z przyszłości."""
        if v is not None and v > date.today():
            field_name = info.field_name if hasattr(info, 'field_name') else str(info)
            raise ValueError(f"{field_name.replace('_', ' ').capitalize()} nie może być z przyszłości.")
        return v


class CatCreate(CatBase):
    """Schemat Pydantic dla tworzenia nowego kota.
    
    Dziedziczy wszystkie pola z CatBase.
    Używany przy operacji POST /cats/.
    """
    pass


class CatUpdate(BaseModel):
    """Schemat Pydantic dla aktualizacji istniejącego kota.
    
    Wszystkie pola są opcjonalne, umożliwiając częściową aktualizację.
    Używany przy operacji PUT /cats/{cat_id}.
    
    Attributes:
        name: Nowe imię kota (opcjonalne).
        size: Nowy rozmiar kota (opcjonalne).
        birth_date: Nowa data urodzenia (opcjonalne).
        sex: Nowa płeć (opcjonalne).
        neutered: Nowy status sterylizacji (opcjonalne).
        admitted_date: Nowa data przyjęcia (opcjonalne).
        released_date: Nowa data wypuszczenia (opcjonalne).
        status: Nowy status (opcjonalne).
        indoor_only: Nowy status indoor_only (opcjonalne).
    """
    name: Optional[str] = None
    size: Optional[CatSize] = None
    birth_date: Optional[date] = None
    sex: Optional[str] = None
    neutered: Optional[bool] = None
    admitted_date: Optional[date] = None
    released_date: Optional[date] = None
    status: Optional[CatStatus] = None
    indoor_only: Optional[bool] = None

    @field_validator('birth_date', 'admitted_date', 'released_date')
    @classmethod
    def date_not_in_future(cls, v: Optional[date], info) -> Optional[date]:
        """Waliduje, że data nie jest z przyszłości."""
        if v is not None and v > date.today():
            field_name = info.field_name if hasattr(info, 'field_name') else str(info)
            raise ValueError(f"{field_name.replace('_', ' ').capitalize()} nie może być z przyszłości.")
        return v


class Cat(CatBase):
    """Schemat Pydantic dla pełnej reprezentacji kota.
    
    Rozszerza CatBase o pole ID.
    Używany jako response model w endpointach API.
    
    Attributes:
        id: Unikalny identyfikator kota.
        
    Config:
        from_attributes: Pozwala na tworzenie obiektu z modelu ORM.
    """
    id: int

    model_config = ConfigDict(from_attributes=True)
