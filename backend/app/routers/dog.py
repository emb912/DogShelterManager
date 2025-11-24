from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import dog as crud
from ..models import DogSize, DogStatus
from ..schemas.dog import DogCreate, DogUpdate, Dog, DogWithHistory
from typing import List

router = APIRouter(prefix="/dogs", tags=["dogs"])


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
def create_one_dog(dog: DogCreate, db: Session = Depends(get_db)):
    return crud.create_dog(db, dog)

@router.put("/{dog_id}", response_model=Dog)
def update_dog(dog_id: int, dog: DogUpdate, db: Session = Depends(get_db)):
    return crud.update_dog(db, dog_id, dog)

@router.delete("/{dog_id}")
def delete_one_dog(dog_id: int, db: Session = Depends(get_db)):
    crud.delete_dog(db, dog_id)
    return {"status": "deleted"}

@router.get("/{dog_id}/details", response_model=DogWithHistory)
def get_dog_details(dog_id: int, db: Session = Depends(get_db)):
    dog = crud.get_dog_with_history(db, dog_id)
    if not dog:
        raise HTTPException(status_code=404, detail="Dog not found")
    return dog
