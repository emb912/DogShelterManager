from typing import Optional, List, Dict
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models
from ..schemas.cat import CatCreate, CatUpdate
from ..models.cat import Cat, CatStatus


def get_cats(db: Session) -> List[Cat]:
    """Pobiera listę kotów z bazy danych.
    
    Args:
        db: Sesja bazy danych.
        
    Returns:
        Lista obiektów Cat.
    """
    query = db.query(Cat)
    return query.all()


def get_cat(db: Session, cat_id: int) -> Optional[Cat]:
    """Pobiera pojedynczego kota po ID.
    
    Args:
        db: Sesja bazy danych.
        cat_id: Identyfikator kota.
        
    Returns:
        Obiekt Cat jeśli znaleziony, None w przeciwnym razie.
    """
    return db.query(models.cat.Cat).filter(models.cat.Cat.id == cat_id).first()


def create_cat(db: Session, cat: CatCreate) -> Cat:
    """Tworzy nowego kota w bazie danych.
    
    Args:
        db: Sesja bazy danych.
        cat: Dane nowego kota zgodne ze schematem CatCreate.
        
    Returns:
        Utworzony obiekt Cat z przypisanym ID.
        
    Note:
        Automatycznie commituje zmiany do bazy danych.
    """
    db_cat = models.cat.Cat(**cat.model_dump())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat


def update_cat(db: Session, cat_id: int, cat: CatUpdate) -> Optional[Cat]:
    """Aktualizuje dane istniejącego kota.
    
    Args:
        db: Sesja bazy danych.
        cat_id: Identyfikator kota do aktualizacji.
        cat: Dane do aktualizacji (tylko wypełnione pola zostaną zmienione).
        
    Returns:
        Zaktualizowany obiekt Cat jeśli znaleziony, None w przeciwnym razie.
        
    Note:
        Automatycznie commituje zmiany do bazy danych.
        Wykorzystuje partial update - aktualizuje tylko podane pola.
    """
    db_cat = get_cat(db, cat_id)
    if not db_cat:
        return None
        
    update_data = cat.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_cat, key, value)

    db.commit()
    db.refresh(db_cat)
    return db_cat


def delete_cat(db: Session, cat_id: int) -> bool:
    """Usuwa kota z bazy danych.
    
    Args:
        db: Sesja bazy danych.
        cat_id: Identyfikator kota do usunięcia.
        
    Returns:
        True jeśli kot został usunięty, False jeśli nie znaleziono.
        
    Note:
        Automatycznie commituje zmiany do bazy danych.
    """
    db_cat = get_cat(db, cat_id)
    if db_cat:
        db.delete(db_cat)
        db.commit()
        return True
    return False


def get_cat_stats(db: Session) -> Dict[str, int]:
    """Generuje statystyki wszystkich kotów w systemie.
    
    Args:
        db: Sesja bazy danych.
        
    Returns:
        Słownik zawierający:
            - current_in_shelter: Liczba kotów aktualnie w schronisku (status: arrived).
            - adopted_total: Całkowita liczba adoptowanych kotów.
            - returned_total: Całkowita liczba zwróconych kotów.
            - all_cats_total: Całkowita liczba kotów w bazie danych.
            
    Note:
        Statystyki są wykorzystywane do aktualizacji real-time przez WebSocket.
    """
    current = db.query(func.count(Cat.id)).filter(Cat.status == CatStatus.arrived).scalar()
    adopted = db.query(func.count(Cat.id)).filter(Cat.status == CatStatus.adopted).scalar()
    returned = db.query(func.count(Cat.id)).filter(Cat.status == CatStatus.returned).scalar()
    total = db.query(func.count(Cat.id)).scalar()

    return {
        "current_in_shelter": current,
        "adopted_total": adopted,
        "returned_total": returned,
        "all_cats_total": total
    }
