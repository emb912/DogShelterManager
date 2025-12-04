from pydantic import BaseModel, ConfigDict, field_validator
from datetime import date
from typing import Optional
from ..models.dog import DogSize, DogStatus

class DogBase(BaseModel):
    """Bazowy schemat Pydantic dla psa.
    
    Zawiera wszystkie wspólne pola używane w różnych operacjach.
    
    Attributes:
        name: Imię psa.
        size: Rozmiar psa (small, medium, large).
        birth_date: Data urodzenia psa (opcjonalne).
        sex: Płeć psa (opcjonalne).
        neutered: Czy pies jest wysterylizowany/wykastrowany.
        admitted_date: Data przyjęcia do schroniska.
        released_date: Data wypuszczenia ze schroniska (opcjonalne).
        status: Status psa (arrived, adopted, returned).
    """
    name: str
    size: DogSize
    birth_date: Optional[date]
    sex: Optional[str]
    neutered: bool
    admitted_date: date
    released_date: Optional[date]
    status: DogStatus

    @field_validator('birth_date', 'admitted_date', 'released_date')
    @classmethod
    def date_not_in_future(cls, v: Optional[date], info) -> Optional[date]:
        """Waliduje, że data nie jest z przyszłości."""
        if v is not None and v > date.today():
            field_name = info.field_name if hasattr(info, 'field_name') else str(info)
            raise ValueError(f"{field_name.replace('_', ' ').capitalize()} nie może być z przyszłości.")
        return v

class DogCreate(DogBase):
    """Schemat Pydantic dla tworzenia nowego psa.
    
    Dziedziczy wszystkie pola z DogBase.
    Używany przy operacji POST /dogs/.
    """
    pass

class DogUpdate(BaseModel):
    """Schemat Pydantic dla aktualizacji istniejącego psa.
    
    Wszystkie pola są opcjonalne, umożliwiając częściową aktualizację.
    Używany przy operacji PUT /dogs/{dog_id}.
    
    Attributes:
        name: Nowe imię psa (opcjonalne).
        size: Nowy rozmiar psa (opcjonalne).
        birth_date: Nowa data urodzenia (opcjonalne).
        sex: Nowa płeć (opcjonalne).
        neutered: Nowy status sterylizacji (opcjonalne).
        admitted_date: Nowa data przyjęcia (opcjonalne).
        released_date: Nowa data wypuszczenia (opcjonalne).
        status: Nowy status (opcjonalne).
    """
    name: Optional[str] = None
    size: Optional[DogSize] = None
    birth_date: Optional[date] = None
    sex: Optional[str] = None
    neutered: Optional[bool] = None
    admitted_date: Optional[date] = None
    released_date: Optional[date] = None
    status: Optional[DogStatus] = None

    @field_validator('birth_date', 'admitted_date', 'released_date')
    @classmethod
    def date_not_in_future(cls, v: Optional[date], info) -> Optional[date]:
        """Waliduje, że data nie jest z przyszłości."""
        if v is not None and v > date.today():
            field_name = info.field_name if hasattr(info, 'field_name') else str(info)
            raise ValueError(f"{field_name.replace('_', ' ').capitalize()} nie może być z przyszłości.")
        return v

class Dog(DogBase):
    """Schemat Pydantic dla pełnej reprezentacji psa.
    
    Rozszerza DogBase o pole ID.
    Używany jako response model w endpointach API.
    
    Attributes:
        id: Unikalny identyfikator psa.
        
    Config:
        from_attributes: Pozwala na tworzenie obiektu z modelu ORM.
    """
    id: int

    model_config = ConfigDict(from_attributes=True)
