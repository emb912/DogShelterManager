from sqlalchemy.orm import Session
from ..models.dog_history import DogHistory
from ..schemas.dog_history import DogHistoryCreate


def create_history_record(db: Session, record: DogHistoryCreate):
    db_record = DogHistory(**record.model_dump())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def get_history_for_dog(db: Session, dog_id: int):
    return db.query(DogHistory).filter(DogHistory.dog_id == dog_id).all()
