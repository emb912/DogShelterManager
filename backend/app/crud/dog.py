from typing import Optional, List, Dict
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models
from ..schemas.dog import DogCreate, DogUpdate
from ..models.dog import Dog, DogStatus

def get_dogs(
    db: Session,
) -> List[Dog]:
    """Pobiera listę psów z bazy danych.
    
    Args:
        db: Sesja bazy danych.
        
    Returns:
        Lista obiektów Dog.
    """
    query = db.query(Dog)

    return query.all()


def get_dog(db: Session, dog_id: int) -> Optional[Dog]:
    """Pobiera pojedynczego psa po ID.
    
    Args:
        db: Sesja bazy danych.
        dog_id: Identyfikator psa.
        
    Returns:
        Obiekt Dog jeśli znaleziony, None w przeciwnym razie.
    """
    return db.query(models.dog.Dog).filter(models.dog.Dog.id == dog_id).first()

def create_dog(db: Session, dog: DogCreate) -> Dog:
    """Tworzy nowego psa w bazie danych.
    
    Args:
        db: Sesja bazy danych.
        dog: Dane nowego psa zgodne ze schematem DogCreate.
        
    Returns:
        Utworzony obiekt Dog z przypisanym ID.
        
    Note:
        Automatycznie commituje zmiany do bazy danych.
    """
    db_dog = models.dog.Dog(**dog.model_dump())
    db.add(db_dog)
    db.commit()
    db.refresh(db_dog)

    return db_dog

def update_dog(db: Session, dog_id: int, dog: DogUpdate) -> Optional[Dog]:
    """Aktualizuje dane istniejącego psa.
    
    Args:
        db: Sesja bazy danych.
        dog_id: Identyfikator psa do aktualizacji.
        dog: Dane do aktualizacji (tylko wypełnione pola zostaną zmienione).
        
    Returns:
        Zaktualizowany obiekt Dog jeśli znaleziony, None w przeciwnym razie.
        
    Note:
        Automatycznie commituje zmiany do bazy danych.
        Wykorzystuje partial update - aktualizuje tylko podane pola.
    """
    db_dog = get_dog(db, dog_id)
    if not db_dog:
        return None
        
    update_data = dog.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_dog, key, value)

    db.commit()
    db.refresh(db_dog)

    return db_dog

def delete_dog(db: Session, dog_id: int) -> bool:
    """Usuwa psa z bazy danych.
    
    Args:
        db: Sesja bazy danych.
        dog_id: Identyfikator psa do usunięcia.
        
    Returns:
        True jeśli pies został usunięty, False jeśli nie znaleziono.
        
    Note:
        Automatycznie commituje zmiany do bazy danych.
    """
    db_dog = get_dog(db, dog_id)
    if db_dog:
        db.delete(db_dog)
        db.commit()
        return True
    return False

def get_dog_stats(db: Session) -> Dict[str, int]:
    """Generuje statystyki wszystkich psów w systemie.
    
    Args:
        db: Sesja bazy danych.
        
    Returns:
        Słownik zawierający:
            - current_in_shelter: Liczba psów aktualnie w schronisku (status: arrived).
            - adopted_total: Całkowita liczba adoptowanych psów.
            - returned_total: Całkowita liczba zwróconych psów.
            - all_dogs_total: Całkowita liczba psów w bazie danych.
            
    Note:
        Statystyki są wykorzystywane do aktualizacji real-time przez WebSocket.
    """
    current = db.query(func.count(Dog.id)).filter(Dog.status == DogStatus.arrived).scalar()
    adopted = db.query(func.count(Dog.id)).filter(Dog.status == DogStatus.adopted).scalar()
    returned = db.query(func.count(Dog.id)).filter(Dog.status == DogStatus.returned).scalar()
    total = db.query(func.count(Dog.id)).scalar()

    return {
        "current_in_shelter": current,
        "adopted_total": adopted,
        "returned_total": returned,
        "all_dogs_total": total
    }

