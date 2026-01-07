from typing import List, Dict
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import cat as crud
from ..schemas.cat import CatCreate, CatUpdate, Cat
from ..websocket_manager import manager

router = APIRouter(prefix="/cats", tags=["cats"])


async def broadcast_cat_stats(db: Session) -> None:
    """Pobiera i rozsyła statystyki kotów przez WebSocket.
    
    Funkcja pomocnicza wykonywana w tle po operacjach CRUD.
    
    Args:
        db: Sesja bazy danych.
    """
    stats = crud.get_cat_stats(db)
    await manager.broadcast({"type": "cat_stats", **stats})


@router.get("/", response_model=List[Cat])
def list_cats(db: Session = Depends(get_db)) -> List[Cat]:
    """Pobiera listę kotów.
    
    Args:
        db: Sesja bazy danych (dependency injection).
        
    Returns:
        Lista kotów ze schroniska.
    """
    return crud.get_cats(db)


@router.get("/{cat_id}", response_model=Cat)
def get_one_cat(cat_id: int, db: Session = Depends(get_db)) -> Cat:
    """Pobiera pojedynczego kota po ID.
    
    Args:
        cat_id: Identyfikator kota.
        db: Sesja bazy danych (dependency injection).
        
    Returns:
        Dane kota.
        
    Raises:
        HTTPException: 404 jeśli kot nie został znaleziony.
    """
    cat = crud.get_cat(db, cat_id)
    if cat is None:
        raise HTTPException(status_code=404, detail="Cat not found")
    return cat


@router.post("/", response_model=Cat)
def create_one_cat(cat: CatCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)) -> Cat:
    """Tworzy nowego kota w systemie.
    
    Args:
        cat: Dane nowego kota.
        background_tasks: Zadania w tle FastAPI.
        db: Sesja bazy danych (dependency injection).
        
    Returns:
        Utworzony kot z przypisanym ID.
        
    Note:
        Po utworzeniu wysyła zaktualizowane statystyki przez WebSocket.
    """
    new_cat = crud.create_cat(db, cat)
    background_tasks.add_task(broadcast_cat_stats, db)
    return new_cat


@router.put("/{cat_id}", response_model=Cat)
def update_cat(cat_id: int, cat: CatUpdate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)) -> Cat:
    """Aktualizuje dane istniejącego kota.
    
    Args:
        cat_id: Identyfikator kota do aktualizacji.
        cat: Dane do aktualizacji (tylko wypełnione pola zostaną zmienione).
        background_tasks: Zadania w tle FastAPI.
        db: Sesja bazy danych (dependency injection).
        
    Returns:
        Zaktualizowany kot.
        
    Raises:
        HTTPException: 404 jeśli kot nie został znaleziony.
        
    Note:
        Po aktualizacji wysyła zaktualizowane statystyki przez WebSocket.
    """
    updated_cat = crud.update_cat(db, cat_id, cat)
    if not updated_cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    background_tasks.add_task(broadcast_cat_stats, db)
    return updated_cat


@router.delete("/{cat_id}")
def delete_one_cat(cat_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)) -> Dict[str, str]:
    """Usuwa kota z systemu.
    
    Args:
        cat_id: Identyfikator kota do usunięcia.
        background_tasks: Zadania w tle FastAPI.
        db: Sesja bazy danych (dependency injection).
        
    Returns:
        Słownik z potwierdzeniem usunięcia.
        
    Raises:
        HTTPException: 404 jeśli kot nie został znaleziony.
        
    Note:
        Po usunięciu wysyła zaktualizowane statystyki przez WebSocket.
    """
    success = crud.delete_cat(db, cat_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cat not found")
    background_tasks.add_task(broadcast_cat_stats, db)
    return {"status": "deleted"}
