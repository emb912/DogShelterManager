from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.database import Base
from app.config import settings

engine = create_engine(settings.TEST_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(bind=engine)

def override_get_db() -> Generator[Session, None, None]:
    """Tworzy sesję bazy danych dla testów.
    Yields:
        Session: Sesja bazy danych SQLAlchemy.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def setup_test_db() -> None:
    """Przygotowuje bazę danych do testów (drop & create)."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
