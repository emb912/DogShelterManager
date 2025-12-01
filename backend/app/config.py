from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Klasa ustawień aplikacji.
       Przechowuje adresy URL do baz danych produkcyjnej i testowej.
    """
    DATABASE_URL: str
    TEST_DATABASE_URL: str | None = None

settings = Settings()
