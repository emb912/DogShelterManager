from datetime import date
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import dog as crud
from ..models import DogSize, DogStatus
from ..schemas.dog import DogCreate, DogUpdate, Dog
from typing import List
from ..models.dog import Dog as DogModel
from ..websocket_manager import manager

router = APIRouter(prefix="/dogs", tags=["dogs"])

async def broadcast_stats(db: Session):
    stats = crud.get_dog_stats(db)
    await manager.broadcast(stats)

@router.get("/", response_model=List[Dog])
def list_dogs(
    size: DogSize | None = None,
    sex: str | None = None,
    status: DogStatus | None = None,

    min_age: int | None = None,
    max_age: int | None = None,

    admitted_from: date | None = None,
    admitted_to: date | None = None,

    sort_by: str | None = None,
    sort_order: str | None = "asc",

    db: Session = Depends(get_db)
):
    return crud.get_dogs(
        db,
        size=size,
        sex=sex,
        status=status,
        min_age=min_age,
        max_age=max_age,
        admitted_from=admitted_from,
        admitted_to=admitted_to,
        sort_by=sort_by,
        sort_order=sort_order
    )

@router.get("/{dog_id}", response_model=Dog)
def get_one_dog(dog_id: int, db: Session = Depends(get_db)):
    return crud.get_dog(db, dog_id)

@router.post("/", response_model=Dog)
def create_one_dog(dog: DogCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    new_dog = crud.create_dog(db, dog)
    background_tasks.add_task(broadcast_stats, db)
    return new_dog

@router.put("/{dog_id}", response_model=Dog)
def update_dog(dog_id: int, dog: DogUpdate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    updated_dog = crud.update_dog(db, dog_id, dog)
    if not updated_dog:
        raise HTTPException(status_code=404, detail="Dog not found")
    background_tasks.add_task(broadcast_stats, db)
    return updated_dog

@router.delete("/{dog_id}")
def delete_one_dog(dog_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    success = crud.delete_dog(db, dog_id)
    if not success:
        raise HTTPException(status_code=404, detail="Dog not found")
    background_tasks.add_task(broadcast_stats, db)
    return {"status": "deleted"}


