from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud.dog_history import get_history_for_dog
from ..schemas.dog_history import DogHistory
from typing import List

router = APIRouter(prefix="/dog-history", tags=["dog-history"])

@router.get("/{dog_id}", response_model=List[DogHistory])
def history(dog_id: int, db: Session = Depends(get_db)):
    print("DOG HISTORY USING:", get_db)

    return get_history_for_dog(db, dog_id)
