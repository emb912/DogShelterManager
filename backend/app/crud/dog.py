from .. import models
from ..schemas.dog import DogCreate, DogUpdate
from sqlalchemy import func
from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from ..models.dog import Dog, DogSize, DogStatus
from typing import Optional

def get_dogs(
    db: Session,
    size: Optional[DogSize] = None,
    sex: Optional[str] = None,
    status: Optional[DogStatus] = None,
    min_age: Optional[int] = None,
    max_age: Optional[int] = None,
    admitted_from: Optional[date] = None,
    admitted_to: Optional[date] = None,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = "asc",
):
    query = db.query(Dog)

    # filters
    if size:
        query = query.filter(Dog.size == size)

    if sex:
        query = query.filter(Dog.sex == sex)

    if status:
        query = query.filter(Dog.status == status)

    if min_age is not None:
        max_birth_date = date.today() - timedelta(days=min_age * 365)
        query = query.filter(Dog.birth_date <= max_birth_date)

    if max_age is not None:
        min_birth_date = date.today() - timedelta(days=max_age * 365)
        query = query.filter(Dog.birth_date >= min_birth_date)

    if admitted_from:
        query = query.filter(Dog.admitted_date >= admitted_from)

    if admitted_to:
        query = query.filter(Dog.admitted_date <= admitted_to)

    # sort
    sortable_fields = {
        "name": Dog.name,
        "admitted_date": Dog.admitted_date,
        "birth_date": Dog.birth_date,
        "status": Dog.status
    }

    if sort_by in sortable_fields:
        sort_column = sortable_fields[sort_by]
        query = query.order_by(asc(sort_column) if sort_order == "asc" else desc(sort_column))

    return query.all()


def get_dog(db: Session, dog_id: int):
    return db.query(models.dog.Dog).filter(models.dog.Dog.id == dog_id).first()

def create_dog(db: Session, dog: DogCreate):
    db_dog = models.dog.Dog(**dog.model_dump())
    db.add(db_dog)
    db.commit()
    db.refresh(db_dog)

    return db_dog

def update_dog(db: Session, dog_id: int, dog: DogUpdate):
    db_dog = get_dog(db, dog_id)
    if not db_dog:
        return None
        
    update_data = dog.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_dog, key, value)

    db.commit()
    db.refresh(db_dog)

    return db_dog

def delete_dog(db: Session, dog_id: int):
    db_dog = get_dog(db, dog_id)
    if db_dog:
        db.delete(db_dog)
        db.commit()
        return True
    return False

def get_dog_stats(db: Session) -> dict:
    """
    Returns statistics about all dogs:
    - current in shelter
    - adopted total
    - returned total
    - all dogs total
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

