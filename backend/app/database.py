from .config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Generator

# Tworzenie silnika bazy danych z URL z konfiguracji
engine = create_engine(settings.DATABASE_URL)

# Fabryka sesji bazy danych
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Klasa bazowa dla modeli ORM
Base = declarative_base()
Base.metadata.create_all(bind=engine)

def get_db() -> Generator[Session, None, None]:
    """Generator sesji bazy danych dla dependency injection FastAPI.
    Yields:
        Session: Sesja bazy danych SQLAlchemy.
    Note:
        Sesja jest automatycznie zamykana po zakończeniu requestu.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()