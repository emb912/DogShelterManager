from typing import List, Dict
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import dog as crud
from ..schemas.dog import DogCreate, DogUpdate, Dog
from ..websocket_manager import manager

router = APIRouter(prefix="/dogs", tags=["dogs"])

async def broadcast_stats(db: Session) -> None:
    """Pobiera i rosyła statystyki psów przez WebSocket.
    
    Funkcja pomocnicza wykonywana w tle po operacjach CRUD.
    
    Args:
        db: Sesja bazy danych.
    """
    stats = crud.get_dog_stats(db)
    await manager.broadcast(stats)

@router.get("/", response_model=List[Dog])
def list_dogs(
    db: Session = Depends(get_db)
) -> List[Dog]:
    """Pobiera listę psów.
    
    Args:
        db: Sesja bazy danych (dependency injection).
        
    Returns:
        Lista psów spełniających ze schroniska.
    """
    return crud.get_dogs(db)

@router.get("/{dog_id}", response_model=Dog)
def get_one_dog(dog_id: int, db: Session = Depends(get_db)) -> Dog:
    """Pobiera pojedynczego psa po ID.
    
    Args:
        dog_id: Identyfikator psa.
        db: Sesja bazy danych (dependency injection).
        
    Returns:
        Dane psa.
        
    Raises:
        HTTPException: 404 jeśli pies nie został znaleziony.
    """
    dog = crud.get_dog(db, dog_id)
    if dog is None:
        raise HTTPException(status_code=404, detail="Dog not found")
    return dog

@router.post("/", response_model=Dog)
def create_one_dog(dog: DogCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)) -> Dog:
    """Tworzy nowego psa w systemie.
    
    Args:
        dog: Dane nowego psa.
        background_tasks: Zadania w tle FastAPI.
        db: Sesja bazy danych (dependency injection).
        
    Returns:
        Utworzony pies z przypisanym ID.
        
    Note:
        Po utworzeniu wysyła zaktualizowane statystyki przez WebSocket.
    """
    new_dog = crud.create_dog(db, dog)
    background_tasks.add_task(broadcast_stats, db)
    return new_dog

@router.put("/{dog_id}", response_model=Dog)
def update_dog(dog_id: int, dog: DogUpdate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)) -> Dog:
    """Aktualizuje dane istniejącego psa.
    
    Args:
        dog_id: Identyfikator psa do aktualizacji.
        dog: Dane do aktualizacji (tylko wypełnione pola zostaną zmienione).
        background_tasks: Zadania w tle FastAPI.
        db: Sesja bazy danych (dependency injection).
        
    Returns:
        Zaktualizowany pies.
        
    Raises:
        HTTPException: 404 jeśli pies nie został znaleziony.
        
    Note:
        Po aktualizacji wysyła zaktualizowane statystyki przez WebSocket.
    """
    updated_dog = crud.update_dog(db, dog_id, dog)
    if not updated_dog:
        raise HTTPException(status_code=404, detail="Dog not found")
    background_tasks.add_task(broadcast_stats, db)
    return updated_dog

@router.delete("/{dog_id}")
def delete_one_dog(dog_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)) -> Dict[str, str]:
    """Usuwa psa z systemu.
    
    Args:
        dog_id: Identyfikator psa do usunięcia.
        background_tasks: Zadania w tle FastAPI.
        db: Sesja bazy danych (dependency injection).
        
    Returns:
        Słownik z potwierdzeniem usunięcia.
        
    Raises:
        HTTPException: 404 jeśli pies nie został znaleziony.
        
    Note:
        Po usunięciu wysyła zaktualizowane statystyki przez WebSocket.
    """
    success = crud.delete_dog(db, dog_id)
    if not success:
        raise HTTPException(status_code=404, detail="Dog not found")
    background_tasks.add_task(broadcast_stats, db)
    return {"status": "deleted"}


